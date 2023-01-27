import telegram
import asyncio
import locale
from time import sleep
from modules.TelegramData import TelegramData
from modules.CoinGeckoAPI import CoinGeckoAPI

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

"""
proxies = {
  'http': 'http://192.168.132.202:8080',
  'https': 'http://192.168.132.202:8080',
}
"""


# Define variáveis e constantes utilizadas no programa
# Conjunto de moedas de interesse
moedas = {'bitcoin', 'ethereum'}

# Dados para a conexão com o Bot do Telegram que virão do arquivo
telegram_data = TelegramData(nome='cripto_jah')
telegram_data.carregar_dados_de('./telegram_data.txt')

# Cria um Objeto Bot do pacote telegram
bot = telegram.Bot(token=telegram_data.get_token())

for moeda in moedas:
    preco, timestamp = CoinGeckoAPI.get_precos(moeda)
    asyncio.run(bot.send_message(text=f'Cotação de {moeda}: R$ {preco} em {timestamp}', chat_id=telegram_data.get_chat_id()))
    sleep(10)
