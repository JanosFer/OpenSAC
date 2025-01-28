import os
import subprocess
import sys
import threading
import time

import psutil
import win32security
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
from pywinauto import Application, Desktop


class OpenSacController:
    class _Criptografia:
        def __init__(self):
            if not hasattr(OpenSacController._Criptografia, "_chave"):
                OpenSacController._Criptografia._chave = Fernet.generate_key()
            self.__fernet = Fernet(OpenSacController._Criptografia._chave)
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

    def __init__(self):
        self.base = None
        self.monitorando = False
        self.SACs_abertos = {}
        self.SACs_fechados = {}
        self.gerenciador_criptografia = OpenSacController._Criptografia()

    def validar_login(self, usuario, senha):
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
                self.gerenciador_criptografia.criptografar_credenciais(usuario, senha)
                return True
        except Exception as e:
            e = "Usuário ou Senha estão incorretos!"
            QMessageBox.critical(None, "Erro", f"{e}")
        finally:
            del usuario
            del senha

    def abrir_instancias(self, servidor, instancias, base):
        caminho_base = r"/Atalhos_Produção/TOTVS"
        caminho_servidor = os.path.join(caminho_base, servidor)

        if os.path.exists(caminho_servidor):
            sacs = [sac for sac in os.listdir(caminho_servidor) if sac.startswith("SAC")]
            for i in range(instancias):
                sac = sacs[i]
                processo = subprocess.Popen(os.path.join(caminho_servidor, sac))

                instancia_SAC = self.diferencia_SACs(servidor)

                self.SACs_abertos[processo.pid] = instancia_SAC

                self.logar_sac(processo.pid)
        else:
            QMessageBox.critical(None, "Aviso", f"Servidor {servidor} não encontrado.")

    def reabrir_instancia(self, nome_instancia, base):
        partes = nome_instancia.split('_')
        servidor = f"{base} D4010S0{partes[1]}"
        sac = None

        caminho_base = r"/Atalhos_Produção/TOTVS"

        if len(partes) >= 3:
            sac = f"{servidor}/{partes[0]}_{partes[2]}"
        else:
            sac = f"{partes[0]}"

        if os.path.exists(servidor):
            processo = subprocess.Popen(os.path.join(caminho_base, sac))
            instancia_SAC = self.diferencia_SACs(servidor)

            self.SACs_abertos[processo.pid] = instancia_SAC

            self.logar_sac(processo.pid)

    def fechar_instancia(self, pid):
        try:
            # Executa o comando taskkill para encerrar o SAC pelo PID
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)

            # Remove o PID de SACs_abertos, caso exista
            if pid in self.SACs_abertos:
                instancia_SAC = self.SACs_abertos.pop(pid)
                self.SACs_fechados[pid] = instancia_SAC
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(None, "Aviso", f"Ocorreu um erro ao tentar fechar o SAC com PID {pid}: {e}")
        except Exception as e:
            QMessageBox.critical(None, "Aviso",f"Ocorreu erro inesperado: {e}")

    def fechar_todas_instancias(self):
        for pid in list(self.SACs_abertos.keys()):
            self.fechar_instancia(pid)

    def diferencia_SACs(self, servidor):
        i = 1
        num_servidor = servidor[-2:]

        instancia_SAC = f"SAC_{num_servidor}"

        while instancia_SAC in self.SACs_abertos.values():
            instancia_SAC = f"SAC_{num_servidor}_{i}"
            i += 1

        return instancia_SAC

    def logar_sac(self, pid):
        try:
            usuario, senha = self.gerenciador_criptografia.descriptografar_credenciais()
            sac = Application(backend="uia").connect(process=pid)

            janela = sac.top_window()
            janela.wait('visible')

            janela.child_window(title="Usuário:", control_type="Edit").type_keys(usuario)
            janela.child_window(title="Senha:", control_type="Edit").type_keys(senha + "{ENTER}")

        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Não foi possível preencher o login: {e}")
        finally:
            del usuario
            del senha

    def iniciar_monitoramento(self):
        self.monitorando = True
        thread = threading.Thread(target=self._monitorar_sacs, daemon=True)
        thread.start()

    def parar_monitoramento(self):
        self.monitorando = False

    def _monitorar_sacs(self):
        while self.monitorando:
            time.sleep(5)  # Define um intervalo de 5 segundos entre verificações
            pids_abertos = list(self.SACs_abertos.keys())

            for pid in pids_abertos:
                if not psutil.pid_exists(pid):  # Verifica se o processo ainda existe
                    instancia_SAC = self.SACs_abertos.pop(pid)
                    self.SACs_fechados[pid] = instancia_SAC

    def automacao_netreport(self, pid, data, automatizado):
        app = Application(backend="win32").connect(process=pid)

        # Conectar à janela principal da aplicação
        janela = app.top_window()

        janela.menu_select("Tabelas->NetReport->Exportação")

        radio_cliente = janela.child_window(title="Cliente", control_type="RadioButton")
        radio_cliente.select()

        # Alterar os campos de data
        campos = janela.descendants(control_type="Edit")  # Pega todos os campos de texto "Edit"

        # Alterar as datas (primeiro e segundo campo de texto)
        campos[0].set_text(f"{data}")  # Primeiro campo de data
        campos[1].set_text(f"{data}")  # Segundo campo de data

        # Clicar no botão "Desmarcar Todas"
        botao_desmarcar = janela.child_window(title="Nenhum", control_type="Button")
        botao_desmarcar.click()

        # Listar todas as checkboxes
        checkboxes = janela.descendants(control_type="CheckBox")

        # Marcar somente as checkboxes da rotina de NetReport
        for checkbox in checkboxes:
            if checkbox.window_text() in ["CD", "CD-CPR_A", "DDC", "MEC", "OFI", "ORF", "ORV", "PPG", "MFU", "MSW"]:
                    checkbox.check()

    def automacao_processamento_geral(self, pid, automatizado, modulos):

        while True:
            try:
                # Captura todas as janelas abertas no desktop
                janela = Desktop(backend="win32").windows()

                for win in janela:
                    title = win.window_text()

                    # Verifica janelas com título "Sistema de Administração de Carteiras"
                    if "Sistema de Administração de Carteiras" in title:
                        # Tenta capturar o texto interno da mensagem
                        try:
                            message = win.child_window(control_type="Text").window_text()

                            if "falha na conexão" in message:
                                win.Button.click()
                                break

                            elif "Processamento concluído" in message:
                                print("Mensagem de sucesso detectada.")
                                win.Button.click()
                                break

                        except Exception as e:
                            print("Erro ao capturar mensagem:", e)

                    # Verifica janelas com título "System Error"
                    elif "System Error" in title:
                        print("Erro crítico detectado.")
                        win.Button.click()
                        break

                time.sleep(1)  # Intervalo para evitar alto uso de CPU

            except Exception as e:
                print("Erro ao monitorar janelas:", e)

    def monitorar_erros(pid):
        from pywinauto import Desktop

        while True:
            try:
                # Acessa janelas pelo PID do programa
                windows = Desktop(backend="uia").windows(process=pid)
                for win in windows:
                    # Verifica mensagens de erro e interage apenas com elas
                    if "System Error" in win.window_text() or "Sistema de Administração de Carteiras" in win.window_text():
                        botao_ok = win.child_window(title="OK", control_type="Button")
                        botao_ok.invoke()
            except Exception:
                pass
            time.sleep(1)

    def executar_automacao(self, pid, data):
        app = Application(backend="uia").connect(process=pid)
        janela = app.top_window()

        janela.menu_select("Tabelas->NetReport->Exportação")

        # Seleciona o radio button "Cliente"
        radio_cliente = janela.child_window(title="Cliente", control_type="RadioButton")
        radio_cliente.invoke()  # Interage sem usar o mouse

        # Altera os campos de data
        campos = janela.descendants(control_type="Edit")
        campos[0].set_text(data)  # Primeiro campo de data
        campos[1].set_text(data)  # Segundo campo de data

        # Clica no botão "Nenhum"
        botao_desmarcar = janela.child_window(title="Nenhum", control_type="Button")
        botao_desmarcar.invoke()  # Clica sem mexer no mouse

        # Marca as checkboxes da rotina de NetReport
        checkboxes = janela.descendants(control_type="CheckBox")
        for checkbox in checkboxes:
            if checkbox.window_text() in ["CD", "CD-CPR_A", "DDC", "MEC", "OFI", "ORF", "ORV", "PPG", "MFU", "MSW"]:
                checkbox.check()