import requests
from decouple import config

from academics.models import Currency
from academics.serializers import ListCurrencyShortCodesSerializer

class CurrencyUpdater:

    def __init__(self):
        self.API_URL = "http://api.currencylayer.com/live"

    def update(self):
        self.__update_exchange_rates()

    def __get_short_codes(self):
        serializer = ListCurrencyShortCodesSerializer(Currency.objects.all(), many=True)
        self.currencies = serializer.data
        self.short_codes = [(lambda currency: currency['short_code'])(currency) for currency in self.currencies]

    def __fetch_exchange_rates(self):
        short_codes_stringed = ",".join(self.short_codes)
        payload = {
            "access_key": config("CURRENCY_LAYER_API_KEY"),
            "currencies": short_codes_stringed
        }
        r = requests.get(self.API_URL, params=payload)
        if r.status_code == requests.codes.ok:
            r = r.json()
            if r["success"]:
                return r["quotes"]
            else:
                raise Exception(f"{r['error']}")
        else:
            r.raise_for_status()

    def __update_exchange_rates(self):
        self.__get_short_codes()
        try:
            rates = self.__fetch_exchange_rates()
            print(rates)
        except requests.exceptions.ConnectionError as e:
            print(e)
        except requests.exceptions.HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

"""
    1. Use a serializer to retrieve short_codes
    2. Use a serializer to update the currencies
    3. Define a utilities folder in helpers and add this class to a new module
    4. Don't forget async if necessary
    5. Commit filters refactoring
"""
    