import telegram
import asyncio
import locale
from datetime import datetime
import requests as requests


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Define variáveis e constantes utilizadas no programa
telegram_data = {}
URL_BASE = 'https://api.coingecko.com/api/v3'
ENDPOINT_PING = f'{URL_BASE}/ping'
ENDPOINT_PRECOS = f'{URL_BASE}/simple/price'

# Recupera os dados de acesso ao Telegram do arquivo telegram_data.txt no diretório corrente
with open("telegram_data.txt", 'r') as fd:
    for linha in fd:
        telegram_data.setdefault(linha.split('=')[0], linha.split('=')[1].removesuffix('\n'))

# Testa a integridade do arquivo, se está formatado corretamente
if 'token' not in telegram_data:
    raise ValueError('Não foi encontrada a informação de token no arquivo telegram_data.txt')
elif 'chat_id' not in telegram_data:
    raise ValueError('Não foi encontrada a informação de chat ID no arquivo telegram_data.txt')

bot = telegram.Bot(token=telegram_data["token"])

if requests.get(url=ENDPOINT_PING).status_code == 200:
    url = f'{ENDPOINT_PRECOS}?ids=ethereum&vs_currencies=BRL&include_last_updated_at=true&precision=2'

    resposta = requests.get(url=url).json()
    dados_moeda = resposta.get('ethereum', None)
    preco = dados_moeda.get('brl', None)
    atualizado_em = dados_moeda.get('last_updated_at', None)

    timestamp = datetime.fromtimestamp(atualizado_em).strftime('%x %X')

    minha_mensagem = f'Cotação do Ethereum: R$ {preco} em {timestamp}'
    asyncio.run(bot.send_message(text=minha_mensagem, chat_id=telegram_data["chat_id"]))

else:
    print("API indisponível no momento. Tente mais tarde.")
