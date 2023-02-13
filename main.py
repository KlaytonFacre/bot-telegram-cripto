import telegram
import locale
import os
from modules.CoinGeckoAPI import CoinGeckoAPI
from dotenv import load_dotenv


load_dotenv()

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Define variáveis e constantes utilizadas no programa
# Conjunto de moedas de interesse
moedas = {'bitcoin', 'ethereum'}

# Cria um Objeto Bot do pacote telegram
bot = telegram.Bot(token=str(os.getenv('TELEGRAM_TOKEN')))

for moeda in moedas:
    preco, timestamp = CoinGeckoAPI.get_precos(moeda)
    bot.send_message(text=f'Cotação de {moeda}: R$ {preco} em {timestamp}', chat_id=str(os.getenv('TELEGRAM_CHAT_ID')))
