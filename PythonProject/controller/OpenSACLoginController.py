import os
import subprocess

import win32security
from PyQt5.QtWidgets import QMessageBox
from pywinauto import Application
from cryptography.fernet import Fernet


class OpenSacController:
    class _Criptografia:
        def __init__(self):
            self.__chave = Fernet.generate_key()
            self.__fernet = Fernet(self.__chave)
            self.__dados_criptografados = None

        def criptografar_credenciais(self, usuario, senha):
            """Criptografa as credenciais e armazena o resultado internamente"""
            credenciais = f"{usuario}:{senha}".encode()
            self.__dados_criptografados = self.__fernet.encrypt(credenciais)

        def descriptografar_credenciais(self):
            """Descriptografa as credenciais armazenadas internamente"""
            if not self.__dados_criptografados:
                raise ValueError("Credenciais não armazenadas.")
            dados = self.__fernet.decrypt(self.__dados_criptografados).decode()
            usuario, senha = dados.split(":")
            return usuario, senha


    def validar_login(self,usuario, senha):
        try:
            user, domain, sid = win32security.LookupAccountName('', usuario)
            status = win32security.LogonUser(
                usuario,
                domain,
                senha,
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT
            )
            if status:
                gerenciador = OpenSacController._Criptografia()
                gerenciador.criptografar_credenciais(usuario, senha)
                del usuario
                del senha
                return True
        except Exception as e:
            e = "Usuário ou Senha estão incorretos!"
            QMessageBox.critical(None, "Erro", f"{e}")


    def __init__(self):
        self.SACs_abertos = {}

    def abrir_instancias(self, servidor, instancias):
        caminho_base = r"/Atalhos_Produção/TOTVS"

        caminho_servidor = os.path.join(caminho_base, servidor)
        if os.path.exists(caminho_servidor):
            for i in range(instancias):
                for sac in os.listdir(caminho_servidor):
                    if sac.startswith("SAC"):
                        processo = subprocess.Popen(os.path.join(caminho_servidor, sac))

                        instancia_SAC = self.diferencia_SACs(servidor)

                        self.SACs_abertos[processo.pid] = instancia_SAC

                        print(f"Instância aberta: {instancia_SAC} - PID: {processo.pid}")
                        self.logar_sac(processo.pid)
        else:
            QMessageBox.critical(None, "Aviso", f"Servidor {servidor} não encontrado.")


    def diferencia_SACs(self, servidor):
        i = 1
        instancia_SAC = servidor

        while instancia_SAC in self.SACs_abertos.values():
            instancia_SAC = f"{servidor}{i}"
            i += 1

        return instancia_SAC

    def logar_sac(pid):
        try:
            sac = Application(backend="uia").connect(process=pid)

            janela = sac.top_window()
            janela.wait('visible')

            janela.child_window(title="Usuário:", control_type="Edit").type_keys(usuario)

            campo_senha = janela.child_window(title="Senha:", control_type="Edit").type_keys(senha)

            campo_senha.type_keys("{ENTER}")


        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Não foi possível preencher o login : {e}")