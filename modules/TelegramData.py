class TelegramData:
    def __init__(self, arquivo: str):
        self.telegram_data = {}
        self.arquivo = arquivo

    def get_data(self) -> dict:
        with open(self.arquivo, 'r') as fd:
            for linha in fd:
                self.telegram_data.setdefault(linha.split('=')[0], linha.split('=')[1].removesuffix('\n'))

        # Testa se o arquivo está formatado corretamente e contém as informações necessárias
        if 'token' not in self.telegram_data:
            raise ValueError(f'Não foi encontrada a informação de token no arquivo {self.arquivo}')
        elif 'chat_id' not in self.telegram_data:
            raise ValueError(f'Não foi encontrada a informação de chat ID no arquivo {self.arquivo}')

        return self.telegram_data
