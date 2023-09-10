import requests
import logging
from decouple import config

from academics.models import Currency
from academics.serializers import ListCurrencyShortCodesSerializer, UpdateCurrencyRateSerializer

class CurrencyRatesUpdater:

    API_URL = "http://api.currencylayer.com/live"
    BASE_CURRENCY = "USD"

    logger = logging.getLogger('django')

    def update(self):
        self.__update_exchange_rates()

    def __update_exchange_rates(self):
        self.__get_short_codes()
        try:
            rates = self.__fetch_exchange_rates()
            formatted_rates = self.__format_rates(rates)
            for currency in self.currencies:
                short_code = currency['short_code']
                if short_code in formatted_rates:
                    exchange_rate = round(formatted_rates[short_code], 10)
                    currency_instance = Currency.objects.get(short_code=short_code)
                    serializer = UpdateCurrencyRateSerializer(currency_instance, data={'usd_exchange_rate': exchange_rate}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        self.logger.error(f"Error updating exchange rate for {short_code}: {serializer.errors}")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection Error: {e}")
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP Error: {e}")
        except Exception as e:
            self.logger.error(f"Unknown Exception: {e}")

    def __get_short_codes(self):
        serializer = ListCurrencyShortCodesSerializer(Currency.objects.exclude(short_code=self.BASE_CURRENCY.lower()), many=True)
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

    def __format_rates(self, rates):
        formatted_rates = {}
        for rate in rates:
            formatted_rates[rate[3:].lower()] = rates[rate]
        return formatted_rates
    