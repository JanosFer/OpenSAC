import os
import subprocess

import win32security
from PyQt5.QtWidgets import QMessageBox
from pywinauto import Application

SACs_abertos = {}

def validar_login(usuario, senha):
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
            return True
    except Exception as e:
        e = "Usuário ou Senha estão incorretos!"
        QMessageBox.critical(None, "Erro", f"{e}")


def abrir_instancias(servidor, instancias):
    caminho_base = r"/Atalhos_Produção/TOTVS"

    caminho_servidor = os.path.join(caminho_base, servidor)
    if os.path.exists(caminho_servidor):
        for i in range(instancias):
            for sac in os.listdir(caminho_servidor):
                if sac.startswith("SAC"):
                    processo = subprocess.Popen(os.path.join(caminho_servidor, sac))

                    instancia_SAC = diferencia_SACs(servidor)

                    SACs_abertos[processo.pid] = instancia_SAC

                    print(f"Instância aberta: {instancia_SAC} - PID: {processo.pid}")
                    logar_sac(processo.pid)
    else:
        QMessageBox.critical(None, "Aviso", f"Servidor {servidor} não encontrado.")


def diferencia_SACs(servidor):
    i = 1
    instancia_SAC = servidor

    while instancia_SAC in SACs_abertos.values():
        instancia_SAC = f"{servidor}{i}"
        i += 1

    return instancia_SAC

def logar_sac(pid, usuario, senha):
    try:
        sac = Application(backend="uia").connect(process=pid)

        janela = sac.top_window()
        janela.wait('visible')

        janela.child_window(title="Usuário:", control_type="Edit").type_keys(usuario)

        campo_senha = janela.child_window(title="Senha:", control_type="Edit").type_keys(senha)

        campo_senha.type_keys("{ENTER}")


    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Não foi possível preencher o login : {e}")