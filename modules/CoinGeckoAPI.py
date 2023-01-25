import requests
import datetime


class CoinGeckoAPI:
    URL_BASE = 'https://api.coingecko.com/api/v3'
    URL_PING = 'https://api.coingecko.com/api/v3/ping'

    @classmethod
    def ping(cls) -> bool:
        return requests.get(url=CoinGeckoAPI.URL_PING).status_code == requests.codes.ok

    @classmethod
    def get_precos(cls, id_moeda: str) -> tuple:
        ENDPOINT_PRECOS = f'{CoinGeckoAPI.URL_BASE}/simple/price?ids={id_moeda}&vs_currencies=BRL&include_last_updated_at=true&precision=2'

        if CoinGeckoAPI.ping():
            dados = requests.get(url=ENDPOINT_PRECOS).json()

            preco = dados[id_moeda]['brl']

            atualizado_em = dados[id_moeda]['last_updated_at']
            timestamp = datetime.datetime.fromtimestamp(atualizado_em).strftime("%x %X")

            return preco, timestamp
        else:
            return None, None
