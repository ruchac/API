from django.shortcuts import render

# Create your views here.
class NodeConsumptionsAPI():
    """
    @url: /api/v1/consumptions/:node_id
    @return: {
        'node_id': 65,
        'department_name': 'ABC',
        'building_name': 'XYZ',
        'consumptions: [
            {
                'node_id': 65,
                'reading_date': '2020-01-02',
                'rating': 3.65
            },
            {
                'node_id': 65,
                'reading_date': '2020-01-03',
                'rating': 3
            }, ..
        ]
    }
    """
    def get(self, node_id):
        start = datetime.date(2020, 01, 01)
        end = datetime.date(2020, 01, 31)
        if request.GET.get('from'):
            start = datetime.datetime.strptime(request.GET.get('from'))
        if request.GET.get('to'):
            end = datetime.datetime.strptime(request.GET.get('to'))
        # TODO: validate the date range to be a period that we can query and return a response without timeout.
        node = NodeDetail.objects.get(node_id=node_id)
        consumptions = YearlyResult.objects.filter(
            node_id=node_id,
            reading_date__gte=start,  # reading_date >= start
            reading_date__lt=end  # reading_date < end
        )
        serialized_node = NodeDetailsSerializer.data(node)
        serialized_node['consumptions'] = YearlyResultSerializer.data(consumptions)
        return serialized_node
