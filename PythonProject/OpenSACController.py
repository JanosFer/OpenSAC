from tkinter import messagebox
from pywinauto import Application

def logar_sac(pid, login, senha):
    try:
        sac = Application(backend="uia").connect(process=pid)

        janela = sac.top_window()
        janela.wait('visible')

        campo_login = janela.child_window(title="Usuário:", control_type="Edit").type_keys(login)
        #campo_login.click_input(double=True)

        #campo_login.set_text(login)

        campo_senha = janela.child_window(title="Senha:", control_type="Edit").type_keys(senha)
        #campo_senha.click_input(double=True)

        #campo_senha.set_text(senha)

        campo_senha.type_keys("{ENTER}")


    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível preencher o login : {e}")