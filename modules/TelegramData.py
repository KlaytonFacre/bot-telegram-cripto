class TelegramData:
    def __init__(self, nome: str = None):
        self._telegram_data = {}
        self._nome_bot = nome

    def load_data_from(self, arquivo: str) -> dict:
        with open(arquivo, 'r') as fd:
            for linha in fd:
                self._telegram_data.setdefault(linha.split('=')[0], linha.split('=')[1].removesuffix('\n'))

        # Testa se o arquivo está formatado corretamente e contém as informações necessárias
        if 'token' not in self._telegram_data:
            raise Exception(f'Não foi encontrada a informação de token no arquivo {arquivo}')
        elif 'chat_id' not in self._telegram_data:
            raise Exception(f'Não foi encontrada a informação de chat ID no arquivo {arquivo}')

        return self._telegram_data

    def get_token(self) -> str:
        if 'token' in self._telegram_data:
            return self._telegram_data["token"]
        else:
            raise Exception('Nenhum token encontrado')

    def get_chat_id(self) -> str:
        if 'chat_id' in self._telegram_data:
            return self._telegram_data['chat_id']
        else:
            raise Exception('Nenhum chat ID encontrado')

    def get_nome_bot(self) -> str:
        return self._nome_bot

