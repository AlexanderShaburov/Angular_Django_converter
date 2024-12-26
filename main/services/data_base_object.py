from main.models import Conversion, Country, Currency, Rate, Request
import main.config as config
import requests, datetime, json
from pathlib import Path
from django.conf import settings
from django.templatetags.static import static


API_KEY = config.API_KEY
RATES_API_URL = config.RATES_API_URL
CURRENCIES_URL = Path(
            settings.BASE_DIR /
            "main" /
            static(config.CURRENCIES_URL).lstrip("/")
            )
COUNTRIES_URL = Path(
            settings.BASE_DIR /
            "main" /
            static(config.COUNTRIES_DATA_URL).lstrip("/")
        )
FLAG_URL_PATTERN = Path(settings.BASE_DIR  / "main"  / static(config.FLAGS_DIR).lstrip("/"))

class Data_Base():
    
    def initiate_db(self) -> None:
        print('[TRACE]: initiate_db called.')
        
    #   1. collsect data from all sources:
    #   I. CURRENCIES:
        #   read currencies info file:
        with open(CURRENCIES_URL, "r") as f:
            self.currencies_raw_data = json.load(f)
        
        #   II. COUNTRIES:
        #   read countries info file:
        with open(COUNTRIES_URL, "r") as f:
            self.countries_raw_data = json.load(f)
        
        #   III. CURRENCIES RATES:
        #   request rates data to have valueted currencies list:
        self.fresh_rates = self.rates_request()
        
        
        #   2. Build intersection:
        '''
        Every currency has to meet next conditions:
            1. attends in currencies_raw_data
            2. attends in countries_raw_data
            3. attends in rates
            
        Take rates and check presence in currencies and countries, keeping in mind
        USD and EUR as internationl currencies:
        '''
        for next_curr in self.fresh_rates['rates'].keys():
    #   avoid international currencies:
            if next_curr != "USD" and next_curr != "EUR":
        #   check presence in currencies:
                for next_entry in self.currencies_raw_data:
                    if (next_entry['code'] == next_curr):
                        
                        for next_country in self.countries_raw_data['countries']['country']:
                            if next_country['currencyCode'] == next_curr:
                                self._create_currency_country(next_entry, next_country)
                                break
                                
                        break
        else: self._set_international_currensies()
        print('[TRACE]: __init__ complited.')
        #   get first rate request and save it to db:
        self.renew_rates()
        pass
    
    def rates_request(self):
        print('[TRACE]: rates request called.')
        rates_raw_data = requests.get(RATES_API_URL).content.decode("utf-8")
        return json.loads(rates_raw_data)

    def renew_rates(self):
        print('[TRACE]: renew rates called.')
        fresh_rates = self.rates_request()
        #   save new request date
        new_request = Request(datetime=datetime.datetime.now(tz=None))
        new_request.save()
        #   save all currencies rates
        for next_curr in Currency.objects.all():
            if next_curr.iso_code == "SLCT":
                Rate.objects.create(
                    currency=next_curr,
                    request_id=new_request,
                    rate=1,
                    )
            else:
                Rate.objects.create(
                    currency=next_curr,
                    request_id=new_request,
                    rate=fresh_rates["rates"][next_curr.iso_code],
                    )
            pass
        

        print(f'[TRACE]: rates data saved with requwst stamp: {new_request.datetime} \n and \
            with rates quantity: {Rate.objects.filter(request_id=new_request)} ')
        pass
    
    def _create_currency_country(self, crrncy:dict, country:dict):
        new_currency_obj = Currency(
            iso_code = crrncy['code'],
            name = crrncy['name'],
            symbol = crrncy['symbol_native'],
        )
        new_currency_obj.save()
        
        flag_url = Path(FLAG_URL_PATTERN / f'{country['countryCode']}.svg'.lower())
        with open(flag_url, "r") as f:
            xml_flag = f.read()
        new_country_obj = Country(
            currency = new_currency_obj,
            name = country['countryName'],
            flag = xml_flag
        )
        new_country_obj.save()
        
        pass
    
    def _set_international_currensies(self):
        print('[TRACE]: set internationl currencies called.')
        # for all intnl currencies in list:
        for next_currency in config.INTERNATIONAL:
            # print('config.INTERNATIONAL[next_currency]: ', config.INTERNATIONAL[next_currency])
            # create Currency object:
            new_currency_obj = Currency(
                iso_code = next_currency['iso_code'],
                name = next_currency['name'],
                symbol = next_currency['symbol_native'],
            )
            new_currency_obj.save()
            # create Country object:
            flag_url = Path(FLAG_URL_PATTERN / f'{next_currency['countryCode']}.svg'.lower())
            with open(flag_url, "r") as f:
                xml_flag = f.read()
            new_country_obj = Country(
                currency = new_currency_obj,
                name = next_currency['countryName'],
                flag = xml_flag
            )
            new_country_obj.save()
            print(f"international currensy {next_currency} created.")
            pass
        pass
    
    
    def build_currencies_dictionary(self):
        print('[TRACE]: build data object for frontend.')
        currencies_dict = {}
        last_rating = Request.objects.last()
        currencies_set = Currency.objects.all()
        for next_currency in currencies_set:
            next_country = Country.objects.get(currency=next_currency)
            next_rate = Rate.objects.get(
                currency=next_currency,
                request_id=last_rating,
            )

            currencies_dict.update({
                next_currency.iso_code: {
                    'symbol': next_currency.symbol,
                    'flag': next_country.flag,
                    'name': next_currency.name,
                    'rate': next_rate.rate,
                }
            })
        
        return currencies_dict
    
    def dump_convertion(self, data:dict)->str:
        print('dump conversion called.')
        print('data object: ', data)
        try:
            last_rates_request = Request.objects.last()
            print('[DB INFO]last_rates_request:', last_rates_request)
            print("[DB INFO]data['fromCode']: ", data['fromCode'])
            from_currency = Currency.objects.get(iso_code=data['fromCode'])
            print('[DB INFO]from_currency: ', from_currency)
            to_currency = Currency.objects.get(iso_code=data['toCode'])
            print('[DB INFO]to_currency: ', to_currency)
            new_convertion = Conversion(
                currency_source = from_currency,
                currency_target = to_currency,
                amount_source = data['fromAmount'],
                amount_target = data['toAmount'],
                rate_source = Rate.objects.get(currency=from_currency, request_id=last_rates_request),
                rate_target = Rate.objects.get(currency=to_currency, request_id=last_rates_request),
                convert_date = datetime.datetime.now()
            )
            new_convertion.save()
            status = 'OK'
        except Exception as e:
            status = str(e)
            print(str(e))
        return status
    pass


