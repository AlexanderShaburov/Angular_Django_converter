from rest_framework import serializers
from main.models import Conversion, Rate, Request



class ConversionReportSerializer(serializers.ModelSerializer):
    source_rate = serializers.FloatField(source='rate_source.rate')
    print('[TYPE]: ', type(source_rate))
    target_rate = serializers.FloatField(source='rate_target.rate')
    # target_rate / source_rate
    rates_request_time = serializers.DateTimeField(source='rate_source.request_id.datetime')
    
    class Meta:
        model = Conversion
        fields = ['currency_source',
                  'currency_target',
                  'amount_source',
                  'amount_target',
                  'convert_date',
                  'rates_request_time',
                  'source_rate',
                  'target_rate',
                  ]
