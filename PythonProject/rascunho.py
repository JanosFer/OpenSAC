import os
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label
import subprocess


class OpenSac:
    def __init__(self):
        self.janela_login = tk.Tk()
        self.janela_login.title("Login OpenSAC")
        self.janela_login.geometry("800x600")

        self.texto_login = tk.Label(self.janela_login, text="Abaixo, insira o mesmo Usuário e Senha utilizados no SAC")
        self.texto_login.grid(row=3, column=0, padx=10, pady=10)

        self.texto_usuario = tk.Label(self.janela_login, text="Usuário:")
        self.texto_usuario.grid(row=4, column=0, padx=10, pady=20)
        self.entry_usuario = tk.Entry(self.janela_login)
        self.entry_usuario.grid(row=4, column=1, padx=10, pady=20)

        self.texto_senha = tk.Label(self.janela_login, text="Senha:")
        self.texto_senha.grid(row=5, column=0, padx=10, pady=20)
        self.entry_senha = tk.Entry(self.janela_login, show="*")
        self.entry_senha.grid(row=5, column=1, padx=10, pady=20)

        self.botao_login = tk.Button(self.janela_login, text="Confirmar Login", command=self.validar_login)
        self.botao_login.grid(row=6, column=1, padx=10, pady=20)

        self.janela_login.mainloop()

    def servidores_var(self, opcoes, servidores_marcados):
        return [opcao for opcao, var in zip(opcoes, servidores_marcados) if var.get()]

    def selecionar_base(self):
        global servidores_marcados  # Certifique-se de declarar corretamente o escopo de servidores_marcados

        # Limpar a área de servidores
        for widget in self.frame_servidores.winfo_children():
            widget.destroy()

        base = self.base_var.get()
        if not base:
            messagebox.showerror("Erro", "Selecione uma base.")
            return

        opcoes = []

        if base == "PRIVATE":
            opcoes = ["PRIVATE D4010S037", "PRIVATE D4010S038", "PRIVATE D4010S039", "PRIVATE D4010S040",
                      "PRIVATE D4010S041"]
        elif base == "PRIME":
            opcoes = ["PRIME D4010S037", "PRIME D4010S038", "PRIME D4010S039", "PRIME D4010S040", "PRIME D4010S041"]

        if not opcoes:
            messagebox.showwarning("Aviso", "Nenhum servidor encontrado para essa base.")
            return

        servidores_marcados = []
        for opcao in opcoes:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.frame_servidores, text=opcao, variable=var)
            chk.pack(anchor='w')
            servidores_marcados.append(var)

    def validar_login(self):
        self.usuario = self.entry_usuario.get()
        self.senha = self.entry_senha.get()


        self.janela_login.destroy()
        self.janela_config_sac()

    def janela_config_sac(self):
        self.janela_config = tk.Tk()
        self.janela_config.title("Escolha de Servidores e SACS")
        self.janela_config.geometry("800x600")

        # Base
        self.base_var = tk.StringVar()
        self.texto_base = Label(self.janela_config, text="Escolha a Base:", font=("open sans", 12, "bold"))
        self.texto_base.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        base_private = tk.Button(self.janela_config, text="Private",
                                 command=lambda: [self.base_var.set("PRIVATE"), self.selecionar_base(),
                                                  self.texto_servidores.config(text="Escolha os servidores:"),
                                                  self.texto_instancias.config(text="Escolha a quantidade de instâncias:")],
                                 bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
        base_private.grid(row=0, column=1, padx=10, pady=10)
        base_private.bind("<Enter>", lambda event: base_private.config(bg="#D3D3D3"))
        base_private.bind("<Leave>", lambda event: base_private.config(bg="#f0f0f0"))

        base_prime = tk.Button(self.janela_config, text="Prime",
                               command=lambda: [self.base_var.set("PRIME"), self.selecionar_base(),
                                                self.texto_servidores.config(text="Escolha os servidores:"),
                                                self.texto_instancias.config(text="Escolha a quantidade de instâncias:")],
                               bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
        base_prime.grid(row=0, column=2, padx=10, pady=10)
        base_prime.bind("<Enter>", lambda event: base_prime.config(bg="#D3D3D3"))
        base_prime.bind("<Leave>", lambda event: base_prime.config(bg="#f0f0f0"))

        # Servidores
        self.texto_servidores = Label(self.janela_config, text="", font=("open sans", 12, "bold"))
        self.texto_servidores.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        self.frame_servidores = tk.Frame(self.janela_config)
        self.frame_servidores.grid(row=2, column=0, columnspan=1)

        # Instâncias
        self.texto_instancias = Label(self.janela_config, text="", font=("open sans", 12, "bold"))
        self.texto_instancias.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        self.janela_config.mainloop()


app = OpenSac()