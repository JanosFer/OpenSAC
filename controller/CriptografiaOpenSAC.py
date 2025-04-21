from cryptography.fernet import Fernet

class _Criptografia:
    def __init__(self):
        if not hasattr(_Criptografia, "_chave"):
            _Criptografia._chave = Fernet.generate_key()
        self.__fernet = Fernet(_Criptografia._chave)
        self.__dados_criptografados = None

    def criptografar_credenciais(self, usuario, senha):
        credenciais = f"{usuario}:{senha}".encode()
        self.__dados_criptografados = self.__fernet.encrypt(credenciais)

    def descriptografar_credenciais(self):
        if not self.__dados_criptografados:
            raise ValueError("Credenciais não armazenadas.")
        dados = self.__fernet.decrypt(self.__dados_criptografados).decode()
        usuario, senha = dados.split(":")
        return usuario, senha