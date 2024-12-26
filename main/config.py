import datetime


COUNTRIES_DATA_URL = "main/data/currency_data/countries.json"
CURRENCIES_URL = "main/data/currency_data/currencies.json"
MAX_RATES_AGE = datetime.timedelta(hours=5)
# API_KEY = '936c37064e984e73a5ba59cfefebcc74'
# RATES_API_URL = f'https://openexchangerates.org/api/latest.json?app_id=${API_KEY}'
FLAGS_DIR = "main/data/currency_data/flags/"

# new api rates access:
# https://manage.exchangeratesapi.io/dashboard
# API_KEY = '104b3d976cf7d66b780026a914f3f1be'
API_KEY = "5687058810609fbe6dcae60ad84f31e3"  # gmail.com

RATES_API_URL = f"https://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}"
# API_KEY = 'fca_live_2Fi65jKC5CgGOHSsgl2ryLVMO6bmMjgYuml7RI91'
# RATES_API_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}'

INTERNATIONAL = [
    {
            "iso_code": "USD",
            "name": "US Dollar",
            "symbol_native": "$",
            "countryName": "United States",
            "countryCode": "US",
    },
    {
            "iso_code": "EUR",
            "name": "Euro",
            "symbol_native": "€",
            "countryName": "European Union",
            "countryCode": "EU",
    },
    {
            "iso_code": "SLCT",
            "name": "Select currency",
            "symbol_native": " ",
            "countryName": "Select Currensy",
            "countryCode": "slct",
    },
]
