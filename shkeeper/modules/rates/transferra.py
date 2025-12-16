import os
from shkeeper import requests
from shkeeper.modules.classes.rate_source import RateSource
import json
from decimal import Decimal


class TransferraRateSource(RateSource):
    name = "transferra"


    def __init__(self):
        self.token = os.environ.get("TRANSFERRA_API_TOKEN")
        self.url = os.environ.get("TRANSFERRA_API_URL")

        if self.token is None:
            raise ValueError("TRANSFERRA_API_TOKEN environment variable not set")

        if self.url is None:
            raise ValueError("TRANSFERRA_API_URL environment variable not set")

    def get_rate(self, fiat, crypto):
        if fiat == "USD" and crypto in self.USDT_CRYPTOS:
            return Decimal(1.0)

        if crypto in self.USDC_CRYPTOS:
            crypto = "USDC"

        if crypto in self.BTC_CRYPTOS:
            crypto = "BTC"

        rate_url = f"{self.url}?from={fiat}&to={crypto}"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.get(rate_url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            if "rate" in data:
                return Decimal(data["rate"])
            else:
                raise Exception(f"Invalid response format: {data}")
        else:
            error_msg = f"Can't get rate for {crypto} / {fiat}. Status code: {response.status_code}"
            if response.text:
                error_msg += f". Response: {response.text}"
            raise Exception(error_msg)
