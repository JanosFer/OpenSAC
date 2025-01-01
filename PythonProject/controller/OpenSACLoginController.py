import os
import subprocess
from tkinter import messagebox

import win32security
from pywinauto import Application

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
        else:
            return False
    except Exception as e:
        return False


def abrir_instancias(base, servidores_selecionados, instancias):
    # Caminho base para os servidores
    caminho_base = r"/Atalhos_Produção/TOTVS"

    instancias_por_servidor = 0

    if base == "private":
        instancias_por_servidor = 4
    elif base == "prime":
        instancias_por_servidor = 8


    # Abre as instâncias para cada servidor selecionado
    for servidor in servidores_selecionados:
        caminho_servidor = os.path.join(caminho_base, servidor)
        if os.path.exists(caminho_servidor):
            for i in range(instancias_por_servidor):
                for sac in os.listdir(caminho_servidor):
                    if sac.startswith("SAC"):
                        processo = subprocess.Popen(os.path.join(caminho_servidor, sac))
                        print(f"Instância aberta: {servidor} - PID: {processo.pid}")
        else:
            messagebox.showerror("Aviso", f"Servidor {servidor} não encontrado.")


def logar_sac(pid, usuario, senha):
    try:
        sac = Application(backend="uia").connect(process=pid)

        janela = sac.top_window()
        janela.wait('visible')

        janela.child_window(title="Usuário:", control_type="Edit").type_keys(usuario)

        campo_senha = janela.child_window(title="Senha:", control_type="Edit").type_keys(senha)

        campo_senha.type_keys("{ENTER}")


    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível preencher o login : {e}")