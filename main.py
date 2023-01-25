import telegram
import asyncio
import locale
from datetime import datetime
import requests as requests
from time import sleep

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Define variáveis e constantes utilizadas no programa
##### Conjunto de moedas de interesse
moedas = {'ethereum', 'bitcoin'}

# URL e ENDPOINTs da API da coingecko
URL_BASE = 'https://api.coingecko.com/api/v3'
ENDPOINT_PING = f'{URL_BASE}/ping'
ENDPOINT_PRECOS = f'{URL_BASE}/simple/price'

# Dados extraídos das respostas para cada uma das moedas
respostas = []
dados_moedas = []
precos = []
atualizados_em = []
timestamps = []

# Dados para a conexão com o Bot do Telegram que virão do arquivo
telegram_data = {}

# Recupera os dados de acesso ao Telegram do arquivo telegram_data.txt no diretório corrente
with open("telegram_data.txt", 'r') as fd:
    for linha in fd:
        telegram_data.setdefault(linha.split('=')[0], linha.split('=')[1].removesuffix('\n'))

# Testa se o arquivo está formatado corretamente e contém as informações necessárias
if 'token' not in telegram_data:
    raise ValueError('Não foi encontrada a informação de token no arquivo telegram_data.txt')
elif 'chat_id' not in telegram_data:
    raise ValueError('Não foi encontrada a informação de chat ID no arquivo telegram_data.txt')

# Cria um Objeto Bot do pacote telegram
bot = telegram.Bot(token=telegram_data["token"])

while True:
    if requests.get(url=ENDPOINT_PING).status_code == 200:
        # Monta o Conjunto (set) com todos os endpoints + query strings de cada uma das moedas de interesse
        urls_moedas = set()
        for moeda in moedas:
            urls_moedas.add(f'{ENDPOINT_PRECOS}?ids={moeda}&vs_currencies=BRL&include_last_updated_at=true&precision=2')

        # Monta uma lista com todas as respostas de cada um dos GETs na lista de urls_moedas
        for url in urls_moedas:
            respostas.append(requests.get(url=url).json())

        # Monta uma lista com os dados das respostas para cada uma das moedas de interesse
        for resposta, moeda in zip(respostas, moedas):
            dados_moedas.append(resposta.get(f'{moeda}', None))

        # Monta as listas de precos e atualizados em para cada um dos dados de moeda presentes em dados_moedas
        for dado in dados_moedas:
            precos.append(dado.get('brl', None))
            atualizados_em.append((dado.get('last_updated_at', None)))

        # Monta uma lista com os timestamps das respostas após a conversão de cada um dos atualizados_em
        for atualizacao in atualizados_em:
            timestamps.append(datetime.fromtimestamp(atualizacao).strftime("%x %X"))

        # Para cada preco e timestamp presente nas respectivas listas, elabora uma mensagem e envia no Telegram
        for preco, timestamp in zip(precos, timestamps):
            asyncio.run(bot.send_message(text=f'Cotação do Ethereum: R$ {preco} em {timestamp}',
                                         chat_id=telegram_data["chat_id"])
                        )

    else:
        print("API indisponível no momento. Tente mais tarde.")

    sleep(300)
