import os
import os.path
import pandas as pd
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from downloadcsv.models import YearlyResult
from downloadcsv.ae_api_client import ActiveEnergyAPIClient


def make_client():
    return ActiveEnergyAPIClient('https', 'cylonaem.com', 443, 'ucd-api', 'xolg-cpgo-ugzc-itve-zbdj-sjgp-tdtn-ydad')


def print_node_ids(client):
    tree_query = {
        'tree_id': 3,     # UCD
    }

    response = client.query_trees(tree_query)
    for node in response['results']:
        print('%i: %s' % (node['node_id'], node['name']))


def make_datalog_query(client, node):
    start_date, end_date = get_processing_dates()
    datalog_query = [{
        'request_id': 'Request ID',
        'node_id': node, # 87Engineering + Material Science Electricity
        'request_type': 'usage',
        'from_date': start_date.strftime("%Y-%m-%d"),
        'to_date': end_date.strftime("%Y-%m-%d"),
        'group': 'raw',
        'timezone': 'UTC',
        'date_format': 'iso',
        'ignore_today': False,
    }]

    response = client.query_datalogs(datalog_query)
    p = []
    for datapoint in response['results'][0]['datapoints']:
        c = datapoint['timestamp'], datapoint['value'] #datapoint['node_id']
        p.append(c)

    Data_DF = pd.DataFrame(p, columns=['date', 'value'])
    #,'node'])
    Data_DF.to_csv('data.csv',index = False)
    df = pd.read_csv('data.csv', parse_dates=['date'], index_col='date')
    df.reset_index(inplace=True)
    df['year'] = [d.year for d in df.date]
    df['month'] = [d.strftime('%b') for d in df.date]
    df['mon_no'] = [d.month for d in df.date]
    df['date_only'] = [d.strftime("%Y-%m-%d") for d in df.date]
    df['time_only'] = [d.strftime("%H:%M:%S") for d in df.date]

    day_data = []
    curr_date = start_date
    while  curr_date < end_date:
        daily = days_data(curr_date.strftime("%Y-%m-%d"), df)
        if daily:
            day_data += daily
        curr_date +=  datetime.timedelta(days=1)
    return day_data


def days_data(D, df):
    l = {}
    w = []
    sum1 = 0
    for index, row in df.iterrows():
        if (row["date_only"] == D):
            l = {}
            sum1 = sum1 + row["value"]
            l.update({'Time': str(row["time_only"])})
            l.update({'Date': str(row["date_only"])})
            #l.update({'Timestamp':p.time})
            l.update({'Rating': sum1})
            w.append(l)
    return w


def write_to_csv(filepointer, data, node, idx):
    if data:
        fields = list(data[0].keys()) + ["node-id"]
        csvwriter = csv.DictWriter(filepointer, fieldnames=fields)
        if idx == 0:
            csvwriter.writeheader()
        for info_dict in data:
            info_dict.update({"node-id": node})
            csvwriter.writerow(info_dict)


def clean_rows_for_date_range(node):
    start_date, end_date = get_processing_dates()
    print("Going to clean any duplicate entries for the node %d in date range %s to %s." % (node, start_date, end_date))
    existing_data = YearlyResult.objects.filter(
        reading_date__gte=start_date,
        reading_date__lt=end_date
    )
    if existing_data.count() > 0:
        print("Deleting %d rows of data found between %s and %s." % (existing_data.count(), start_date, end_date))
        existing_data.delete()


def _run_pre_checks(day_data, node):
    clean_rows_for_date_range(node)


def write_db(day_data, node):
    _run_pre_checks(day_data, node)
    results = []
    for data in day_data:
        results.append(YearlyResult(
            node_id=node,
            rating=data.get('Rating', 0.0),
            reading_date=data.get('Date'),
            reading_time=data.get('Time')))

    YearlyResult.objects.bulk_create(results)


def get_processing_dates():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=10)
    return start_date, end_date


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        current_date = datetime.datetime.now()
        n = 806, 39230  #65,66,72,78,79,82,84,86,87,88,89,90,91,92,93,96,101,103,104,105,106,107,108,109,110,115,116,117,118,119,120,121,122,124,128,146,148,155,157,158,160,164,165,167,168,169,789,790,793,795,796,798,802,804,806,809,812,813,814,815,818,820,821,823,824,825,827,828,829,831,834,837,838,839,840,841,842,845,846,847,849,850,851,852,853,854,856,857,858,881,882,883,884,888,889,890,892,893,895,896,897 #901,902,903,994,1104,2211,2217,2339,2340,2341,2342,2343,2344,2345,2346,2347,2348,2349,2350,2351,2352,2353,2355,2356,2359,2360,2361,2362,2364,2366,2373,2374,2376,2377,2382,2384,2385,2386,2389,2391,2392,2396,2401,2403,2471,2848,2850,3979,3980,3982,3983,3984,3986,3987,3989,3990,3992,3993,3994,3995,3996,3997,3998,3999,4000,4001,4002,4003,4007,4009,4010,4011,4013,4016,4017,4021,4921,4922,4926,4930,4931,4932,4933,4934,4935,4936,4937,4940,4942,4943,4944,4945,4946,4947,4948,4949,4950,4951,4952,4963,4965,4966,4970,4971,4976,4978,4979,4980,4983,5053,5283,6201,6204,6205,6208,6213,6215,6216,6219,6220,6292,6293,6294,6295,6296,6297,6298,6300,6302,6304,6305,6306,6307,6308,6309,6310,6311,6312,6313,6314,6315,6316,6318,6322,6343,6344,6345,6346,6347,6348,6349,6350,6351,6352,6354,6355,6360,6383,6385,6386,6387,6389,6390,6391,6399,6400,6417,6418,6419,6420,6421,6452,7369,7370,8715,8857,8858,8860,8862,8863,8864,8873,10085,10669,10889,11010,11026,11129,11130,11355,11443,11663,11916,11917,11918,12364,13598,13599,13600,13601,13603,13604,13606,13777,13778,14342,14345,14346,14348,14349,14350,14351,14352,14354,14355,14356,14357,14374,14634,14695,15949,15950,16037,16150,16151,16152,16153,16154,16155,16156,16157,16158,16159,16160,16161,16162,16163,16164,16166,16222,16240,16241,16242,16243,16244,16245,16246,16247,16249,16250,16251,16252,16253,16254,16255,16256,16257,16258,16259,16260,16261,16263,16264,16266,16267,16268,16269,16270,16271,16272,16273,16274,16275,16276,16681,16682,16746,17186,17247,17248,17249,17306,17307,17308,17451,17521,17674,17827,18151,18893,19011,19055,19056,19596,19597,19598,19599,19600,19601,19602,19603,19604,19606,19721,19723,19724,19852,19895,19896,19994,20002,20003,20004,20005,20006,20007,20008,20009,20808,21250,21456,22319,22497,22498,22499,22500,22501,22502,22503,22504,22643,22644,22988,23107,23120,24109,24110,24341,24929,25067,25068,25069,25083,25087,25088,25107,25153,25154,25155,25156,25157,25158,25159,25160,25161,25162,25163,25164,25180,25264,25265,25266,25402,25403,25458,25466,25468,25704,25706,25707,25708,26092,26208,26209,26210,26211,26212,26213,26228,26229,26231,26232,26236,26237,26238,26239,26241,26242,26244,26245,26246,26251,26252,26277,26678,26679,26680,26681,26682,26684,26685,26687,26688,26690,26691,26692,26693,26694,26695,26696,26697,26699,26700,26702,26703,26706,26707,26709,26710,26711,26712,26713,26714,26715,26716,26717,26718,26719,26720,26721,26996,27060,27080,27236,28258,28292,28293,28296,28304,28305,28306,28307,28503,28727,28728,28729,28740,28753,30436,30437,30439,30440,30447,30994,30995,30996,30997,30998,30999,31121,31122,31123,31124,31125,31126,31127,31128,31257,31258,31259,31260,31261,31262,31263,31264,31265,31266,31267,32204,32208,32209,32210,33248,34025,34026,34027,34045,34046,34047,34048,34049,34050,34051,34052,34053,34054,34055,34056,34057,34058,34059,34060,34061,34259,34260,34261,34513,34514,34515,34516,34517,34718,34719,34720,34721,34887,34888,34890,34891,34893,34894,34895,34896,34897,34898,34899,36465,37479,37482,37483,37484,37485,37500,37859,37860,37862,38369,38370,38371,38372,39090,39091,39092,39100,39101,39102,39103,39104,39105,39106,39107,39108,39109,39110,39111,39112,39113,39114,39115,39116,39117,39118,39119,39120,39121,39122,39123,39124,39125,39126,39127,39128,39129,39130,39131,39132,39133,39134,39135,39136,39137,39138,39139,39140,39141,39142,39143,39144,39145,39146,39147,39148,39230,39231

        client = make_client()
        filename = 'YearlyResult_%s.csv' % current_date.strftime('%Y')
        filepath = os.path.join(settings.BASE_DIR, filename)

        for idx, node in enumerate(n):
            try:
                day_data = make_datalog_query(client, node)
            except Exception as e:
                self.stdout.error("API error occurred for node %d." % node)
                self.stdout.error(str(e))
            else:
                filemode = 'w+'
                if os.path.exists(filepath):
                    filemode = 'a+'
                with open(filepath, filemode, newline='') as fp:
                    write_to_csv(fp, day_data, node, idx)
                write_db(day_data, node)
