#import from restframework
from rest_framework import serializers
from downloadcsv.models import YearlyResult


class YearlyResultSerializer(serializers.ModelSerializer): #YearlyResult serialize
    class Meta:
        model = YearlyResult
        fields = '__all__'
        # fields = ('node_id', 'reading_date', 'reading_time', 'rating')


