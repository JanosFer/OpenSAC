import os
import subprocess
import threading
import time

import psutil
import win32con
import win32gui
from win32security import LOGON32_PROVIDER_DEFAULT, LOGON32_LOGON_NETWORK, LookupAccountName, LogonUser
from PyQt5.QtWidgets import QMessageBox

from pywinauto import Application, Desktop

from controller import CriptografiaOpenSAC

class OpenSacController:
    def __init__(self):
        self.base = None
        self.monitorando = False
        self.SACs_abertos = {}
        self.SACs_fechados = {}
        self.SACs_processando = {}
        self.SACs_erros = {}
        self.scripts_erros = []
        self.script_concluido = None
        self.gerenciador_criptografia = CriptografiaOpenSAC._Criptografia()

    def validar_login(self, usuario, senha):
        try:
            user, domain, sid = LookupAccountName('', usuario)
            status = LogonUser(
                usuario,
                domain,
                senha,
                LOGON32_LOGON_NETWORK,
                LOGON32_PROVIDER_DEFAULT
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

                instancia_SAC = self.diferencia_sacs(servidor)

                removido = None
                for pid, sac in self.SACs_fechados.items():
                    if sac == instancia_SAC:
                        removido = self.SACs_fechados.pop(pid)
                        break

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
            instancia_SAC = self.diferencia_sacs(servidor)

            removido = None
            for pid, sac in self.SACs_fechados.items():
                if sac == instancia_SAC:
                    removido = self.SACs_fechados.pop(pid)
                    break

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

    def diferencia_sacs(self, servidor):
        i = 1
        num_servidor = servidor[-2:]

        instancia_SAC = f"SAC_{num_servidor}"

        while instancia_SAC in self.SACs_abertos.values():
            instancia_SAC = f"SAC_{num_servidor}_{i}"
            i += 1

        return instancia_SAC

    def logar_sac(self, pid):
        try:
            # Descriptografa as credenciais
            usuario, senha = self.gerenciador_criptografia.descriptografar_credenciais()

            # Conecta à aplicação
            sac = Application(backend="uia").connect(process=pid)
            janela = sac.top_window()
            janela.wait('visible')

            # Preenche os campos de usuário e senha
            campo_usuario = janela.child_window(title="Usuário:", control_type="Edit")
            campo_usuario.set_text(usuario)

            campo_senha = janela.child_window(title="Senha:", control_type="Edit")
            campo_senha.set_text(senha)

            # Confirma o login e clica no botão "OK"
            botao_entrar = janela.child_window(title="OK", control_type="Button")
            botao_entrar.invoke()

        except Exception as e:
            print(f"Erro ao preencher o login: {e}")
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

    def _automacao_netreport(self, pid, data):
        app = Application(backend="uia").connect(process=pid)
        janela = app.top_window()

        janela.menu_select("Tabelas->NetReport->Exportação")

        if pid in self.SACs_erros:
            instancia_SAC = self.SACs_erros.pop(pid)
            self.SACs_abertos[pid] = instancia_SAC

            botao_fechar = janela.child_window(title="Fechar", control_type="Button")
            botao_fechar.invoke()
            janela.menu_select("Tabelas->NetReport->Exportação")

        # Seleciona o radio button "Cliente"
        radio_cliente = janela.child_window(title="Cliente", control_type="RadioButton")
        radio_cliente.invoke()

        # Altera os campos de data
        campos = janela.descendants(control_type="Edit")
        campos[0].set_text(data)  # Primeiro campo de data
        campos[1].set_text(data)  # Segundo campo de data

        # Clica no botão "Nenhum"
        botao_desmarcar = janela.child_window(title="Nenhum", control_type="Button", found_index=1)
        botao_desmarcar.invoke()

        # Marca as checkboxes da rotina de NetReport
        checkboxes = janela.descendants(control_type="CheckBox")
        for checkbox in checkboxes:
            if checkbox.window_text() in ["CD", "CD-CPR_A", "DDC", "MEC", "OFI", "ORF", "ORV", "PPG", "MFU", "MSW"]:
                checkbox.check()


    def _automacao_processamento_geral(self, pid, data, modulos):

        app = Application(backend="uia").connect(process=pid)
        janela = app.top_window()

        janela.menu_select("Processamento->Processamento Geral")

        if pid in self.SACs_erros:
            instancia_SAC = self.SACs_erros.pop(pid)
            self.SACs_abertos[pid] = instancia_SAC

            botao_fechar = janela.child_window(title="Fechar", control_type="Button")
            botao_fechar.invoke()
            janela.menu_select("Processamento->Processamento Geral")

        # Define o tipo de processamento como fechamento
        tipo_processamento = janela.child_window(control_type="ComboBox")
        tipo_processamento_hwnd = tipo_processamento.handle
        win32gui.SendMessage(tipo_processamento_hwnd, win32con.CB_SETCURSEL, 1, 0)

        # Altera o campo de data
        campos = janela.descendants(control_type="Edit")
        campos[0].set_text(data)

        checkboxes = janela.descendants(control_type="CheckBox")
        for checkbox in checkboxes:
            if checkbox.window_text() in modulos:
                checkbox.check()


    def roda_automacao(self, data, tipo_processamento, automatizado, modulos, lista_scripts):
        pids_abertos = list(self.SACs_abertos.keys())
        for pid in pids_abertos:

            if tipo_processamento == "NetReport":
                self._automacao_netreport(pid, data)

            elif tipo_processamento == "Processamento Geral":
                self._automacao_processamento_geral(pid, data, modulos)


        if automatizado:
            while lista_scripts:
                if self.SACs_abertos:
                    abertos = list(self.SACs_abertos.keys())
                    pid = abertos.pop(0)
                    if lista_scripts:
                        script = lista_scripts.pop(0)
                        self._selecionar_scripts(pid, script)

                        # Inicia o monitoramento de erros em uma thread separada
                        thread_monitoramento = threading.Thread(target=self._monitorar_erros, args=(pid, script,))
                        thread_monitoramento.daemon = True
                        thread_monitoramento.start()
                elif not self.SACs_abertos and not self.SACs_processando:
                    QMessageBox.critical(None, "ERRO", f"Não foi possível concluir o processamento pois todos os SACs caíram! Foi possível processar até o Script: {self.script_concluido}")
                    break


            if not self.scripts_erros:
                QMessageBox.information(None, "Sucesso", "Todos os Scripts foram processados com sucesso.")
            elif self.scripts_erros:
                total = len(self.scripts_erros)
                limite = 30
                restantes = total - limite
                qtdlimitada = self.scripts_erros[:limite]
                scripts = "; ".join(qtdlimitada) + f" (+{restantes})"
                QMessageBox.critical(None, "Aviso", f"{total} Scripts caíram: {scripts}")



    def _selecionar_scripts(self, pid, script):
        app = Application(backend="uia").connect(process=pid)
        janela = app.top_window()

        if pid in self.SACs_abertos:
            instancia_SAC = self.SACs_abertos.pop(pid)
            self.SACs_processando[pid] = instancia_SAC

        botao_scripts = janela.child_window(title="Scripts", control_type="Button")
        botao_scripts.invoke()

        janela_scripts = janela.child_window(title="Seleção de Scripts")
        lista = janela_scripts.child_window(control_type="ListBox")
        lista_hwnd = lista.handle

        items = lista.item_texts()

        if script in items:
            script_index = items.index(script)
            win32gui.SendMessage(lista_hwnd, win32con.LB_SETCURSEL, script_index, 0)

    def _monitorar_erros(self, pid, script):
        while True:
            try:
                # Acessa janelas pelo PID do programa
                janelas = Desktop(backend="uia").windows(process=pid)
                for janela in janelas:
                    # Verifica mensagens de erro
                    if "System Error" in janela.window_text() or "Sistema de Administração de Carteiras" in janela.window_text():
                        botao_ok = janela.child_window(title="OK", control_type="Button")
                        botao_ok.invoke()
                        self.scripts_erros.append(script)
                        instancia_SAC = self.SACs_abertos.pop(pid)
                        self.SACs_fechados[pid] = instancia_SAC

                    elif "Sistema de Administração de Carteiras" in janela.window_text():
                            mensagem = janela.child_window(control_type="Text").window_text()

                            if "erro" in mensagem:
                                botao_ok = janela.child_window(title="OK", control_type="Button")
                                botao_ok.invoke()
                                self.scripts_erros.append(script)
                                instancia_SAC = self.SACs_processando.pop(pid)
                                self.SACs_erros[pid] = instancia_SAC
                                break

                            if "falha na conexão" in mensagem:
                                botao_ok = janela.child_window(title="OK", control_type="Button")
                                botao_ok.invoke()
                                self.scripts_erros.append(script)
                                self.fechar_instancia(pid)
                                break

                            elif "Processamento concluído" in mensagem:
                                botao_ok = janela.child_window(title="OK", control_type="Button")
                                botao_ok.invoke()

                                self.script_concluido = script
                                instancia_SAC = self.SACs_processando.pop(pid)
                                self.SACs_abertos[pid] = instancia_SAC

                                break
            except Exception:
                pass
            time.sleep(1)
