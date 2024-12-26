import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from main import config
from main.services.data_base_object import Data_Base
from main.models import Currency, Request, Conversion
from django.http import JsonResponse
from django.db.models import Q
from main.serializers import ConversionReportSerializer



def gather_data(request):
    print('[TRACE]: gather data called.')
    #   check if database once initiate
    #   get last convertion time and id
    #   check if timedelta less than 5 hours
    #   renew rate db if needed
    #   collect data and make dataset for frondend
    db = Data_Base()
    if not Request.objects.exists(): 
        print('[TRACE]: existing request not found.')
        db.initiate_db()
    
    latest_rates = Request.objects.last()
    
    if latest_rates: print(latest_rates.datetime)
    rates_are_valid = (
        datetime.now() - latest_rates.datetime.replace(tzinfo=None)
        ) <= config.MAX_RATES_AGE
    if not rates_are_valid: 
        print('[TRACE]: last request is not valid.')
        latest_rates = db.renew_rates()
        pass
    
    currencies_dict = db.build_currencies_dictionary()
    response = JsonResponse(currencies_dict, safe=False)    
    
    return response
    
    pass

def save_conversion(request):
    print('save convertion called.')
    data = json.loads(request.body)
    db = Data_Base()
    res = db.dump_convertion(data)
    print('response: ', res)
    data['savingStatus'] = res
    response = JsonResponse(data)
    # response['ok'] = True if res == 'OK' else res
    response["Access-Control-Allow-Origin"] = "https://localhost:4200"
    response["Access-Control-Allow-Credentials"] = 'true'
    # res = db.dump_convertion(data)
    return response
    
    pass
def base_operations(request):
    return render(
        request=request,
        template_name="db_page.html/",
    )
    
def test(request):
    print('test handler called.')
    response = JsonResponse({'ok': True})
    response["Access-Control-Allow-Origin"] = "https://localhost:4200"
    response["Access-Control-Allow-Credentials"] = 'true'
    return response
    
    
def test_db(data):
    print('test db called')
    currency = Currency.objects.get(iso_code=data['fromCode'])
    
    print('found currency = ', currency)
    return 'OK'

def report(request):
    print('report function called.')
    request_parameters = json.loads(request.body)
    print('[REQUEST]: ', request_parameters)
    qs = queryset_constructor(request_parameters)
    serializer = ConversionReportSerializer(qs, many=True)
    report = serializer.data
    print('[RESPONSE]:', report)
    return JsonResponse(report, safe=False)
             
def queryset_constructor(params:dict):
    print('queryset_constructor called.')
    #convert data format:
    start_date = datetime.strptime(params['sinceDate'], "%Y-%m-%d") if params['sinceDate'] else ''
    end_date = datetime.strptime(params['untilDate'], "%Y-%m-%d") + timedelta(days=1) if params['untilDate'] else ''
    queryset = Conversion.objects.select_related('rate_source', 'rate_target', 'rate_source__request_id')
    filters = {}
    if params['sinceDate']: 
        filters['convert_date__gte']=start_date
    if params['untilDate']: 
        filters['convert_date__lte']=end_date
    if params['lowerLimit']: 
        filters['amount_source__gte']=params['lowerLimit']
    if params['upperLimit']: 
        filters['amount_source__lte']=params['upperLimit']
    if params['fromCurrency'] != 'SLCT': 
        filters['currency_source']=params['fromCurrency']
    if params['toCurrency'] != 'SLCT': 
        print('Target currency code: ', params['toCurrency'])
        filters['currency_target']=params['toCurrency']
    return queryset.filter(**filters)
