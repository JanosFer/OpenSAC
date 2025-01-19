# import os
# import subprocess
# import OpenSACController
# import tkinter as tk
# from tkinter import messagebox
#
#
# class OpenSacApp:
#     def __init__(self):
#         self.servidores_selecionados = None
#         self.janela_login = tk.Tk()
#         self.janela_login.title("Login OpenSAC")
#         self.janela_login.geometry("400x300")
#         self.janela_login.resizable(False, False)
#
#         # Tela de login
#         self.texto_login = tk.Label(self.janela_login, text="Login OpenSAC", font=("Arial", 16))
#         self.texto_login.grid(row=0, column=1, columnspan=2, padx=10, pady=30)
#
#         self.texto_usuario = tk.Label(self.janela_login, text="Usuário:")
#         self.texto_usuario.grid(row=1, column=1, padx=10, pady=10)
#         self.entry_usuario = tk.Entry(self.janela_login)
#         self.entry_usuario.grid(row=1, column=2, padx=10, pady=10)
#
#         self.texto_senha = tk.Label(self.janela_login, text="Senha:")
#         self.texto_senha.grid(row=2, column=1, padx=10, pady=10)
#         self.entry_senha = tk.Entry(self.janela_login, show="*")
#         self.entry_senha.grid(row=2, column=2, padx=10, pady=10)
#
#         self.botao_login = tk.Button(self.janela_login, text="Confirmar Login", command=self.validar_login)
#         self.botao_login.grid(row=3, column=1, columnspan=2, padx=10, pady=20)
#
#         self.margem = tk.Button(self.janela_login, text="                       ", relief="flat")
#         self.margem.grid(row=4, column=0)
#
#         self.janela_login.mainloop()
#
#
#     def validar_login(self):
#         usuario = self.entry_usuario.get()
#         senha = self.entry_senha.get()
#
#         if usuario == "i" and senha == "i":
#             self.janela_login.destroy()
#             self.janela_config_sac()
#         else:
#             messagebox.showerror("Erro", "Usuário ou Senha inválidos")
#
#
#     def janela_config_sac(self):
#         self.janela_config = tk.Tk()
#         self.janela_config.title("Escolha de Servidores e SACs")
#         self.janela_config.geometry("600x500")
#         self. janela_config.resizable(False, False)
#
#
#
#         # Texto inicial de escolha de base
#         texto_base = tk.Label(self.janela_config, text="Escolha a base:", font=("Arial", 12))
#         texto_base.grid(row=0, column=0, padx=10, pady=10)
#
#         # Inicializa a variável da base
#         self.base_var = tk.StringVar()
#
#         # Base Private e Prime
#         base_private = tk.Button(self.janela_config, text="Private",
#                                  command=lambda: [self.base_var.set("PRIVATE"), self.campos_janela_config_sac(), self.selecionar_base(),
#                                                   texto_servidores.config(text="Escolha os servidores:"),
#                                                   texto_instancias.config(text="Escolha a quantidade de instâncias:")],
#                                  bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
#         base_private.grid(row=0, column=1, padx=5, pady=10)
#         base_private.bind("<Enter>", lambda event: base_private.config(bg="#D3D3D3"))
#         base_private.bind("<Leave>", lambda event: base_private.config(bg="#f0f0f0"))
#
#
#         base_prime = tk.Button(self.janela_config, text="Prime",
#                                command=lambda: [self.base_var.set("PRIME"), self.campos_janela_config_sac(), self.selecionar_base(),
#                                                 texto_servidores.config(text="Escolha os servidores:"),
#                                                 texto_instancias.config(text="Escolha a quantidade de instâncias:")],
#                                bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
#         base_prime.grid(row=0, column=2, padx=5, pady=10)
#         base_prime.bind("<Enter>", lambda event: base_prime.config(bg="#D3D3D3"))
#         base_prime.bind("<Leave>", lambda event: base_prime.config(bg="#f0f0f0"))
#
#
#         # Texto para escolher os servidores
#         texto_servidores = tk.Label(self.janela_config, text="", font=("Arial", 12))
#         texto_servidores.grid(row=2, column=0, padx=5, pady=10, columnspan=1)
#
#
#         # Texto para escolher a quantidade de instâncias
#         texto_instancias = tk.Label(self.janela_config, text="",
#                                          font=("Arial", 12))
#         texto_instancias.grid(row=5, column=0, padx=10, pady=10)
#
#
#         self.janela_config.mainloop()
#
#
#     def campos_janela_config_sac(self):
#         # Frame para os checkbuttons dos servidores
#         self.frame_servidores = tk.Frame(self.janela_config)
#         self.frame_servidores.grid(row=4, column=0, columnspan=2)
#
#         # Checkbox para marcar todos os servidores
#         self.check_all_var = tk.BooleanVar()
#         check_all = tk.Checkbutton(self.janela_config, text="Marcar todos", variable=self.check_all_var,
#                                         command=self.marcar_todos)
#         check_all.grid(row=3, column=0, padx=10, pady=10)
#
#         self.entry_instancias = tk.Entry(self.janela_config)
#         self.entry_instancias.grid(row=5, column=1, padx=10, pady=50)
#
#         # Label para mostrar a quantidade máxima de instâncias
#         self.texto_max_instancias = tk.Label(self.janela_config, text="Max: 0", font=("Arial", 10))
#         self.texto_max_instancias.grid(row=5, column=2, padx=10, pady=10)
#
#         # Botão de Confirmar
#         botao_confirmar = tk.Button(self.janela_config, text="Confirmar", command=self.confirmar_escolhas)
#         botao_confirmar.grid(row=6, column=0, columnspan=4, padx=10, pady=20)
#
#
#     def selecionar_base(self):
#         # Atualiza as opções de servidores com base na base escolhida
#         for widget in self.frame_servidores.winfo_children():
#             widget.destroy()
#
#         base = self.base_var.get()
#
#         if base == "PRIVATE":
#             opcoes = ["PRIVATE D4010S037", "PRIVATE D4010S038", "PRIVATE D4010S039", "PRIVATE D4010S040",
#                       "PRIVATE D4010S041"]
#         elif base == "PRIME":
#             opcoes = ["PRIME D4010S037", "PRIME D4010S038", "PRIME D4010S039", "PRIME D4010S040", "PRIME D4010S041"]
#         else:
#             opcoes = []
#
#         # Criação de checkboxes para servidores
#         self.servidores_selecionados = []
#         for opcao in opcoes:
#             var = tk.BooleanVar()
#             servidor = tk.Checkbutton(self.frame_servidores, text=opcao, variable=var, command=self.atualizar_instancias)
#             servidor.grid(sticky='w', padx=10)
#             self.servidores_selecionados.append((servidor, var))
#
#
#     def marcar_todos(self):
#         # Marca ou desmarca todas as opções de servidores e desabilita se marcado
#         selecionar_todos = self.check_all_var.get()
#
#         for marcado, var in self.servidores_selecionados:
#             var.set(selecionar_todos)  # Marca ou desmarca todos como selecionados
#             marcado.config(state="disabled" if selecionar_todos else "normal")  # Desabilita ou habilita os checkbuttons
#
#         # Atualiza o número de instâncias
#         self.atualizar_instancias()
#
#
#     def atualizar_instancias(self):
#         base = self.base_var.get()
#         self.max_instancias = 0
#
#         if base == "PRIVATE":
#             self.max_instancias = sum(4 for _, var in self.servidores_selecionados if var.get())
#         elif base == "PRIME":
#             self.max_instancias = sum(8 for _, var in self.servidores_selecionados if var.get())
#
#         self.entry_instancias.delete(0, tk.END)
#         self.entry_instancias.insert(0, str(self.max_instancias))
#
#         # Atualiza o texto que mostra a quantidade máxima de instâncias
#         self.texto_max_instancias.config(text=f"Max: {self.max_instancias}")
#
#     def abrir_instancias(self):
#         servidores_marcados = self.servidores_selecionados
#         self.instancias = []
#
#         if not servidores_marcados:
#             messagebox.showerror("Erro", "Nenhum servidor selecionado.")
#             return
#
#         caminho_base = r"\\Atalhos_Produção\\TOTVS"
#
#         for servidor in servidores_marcados:
#             caminho_servidor = os.path.join(caminho_base, servidor)
#             if os.path.exists(caminho_servidor):
#                 i = 0
#                 for sac in os.listdir(caminho_servidor):
#                     if sac.startswith("SAC"):
#                         processo = subprocess.Popen(os.path.join(caminho_servidor, sac))
#                         instancia = Instancia(nome= servidor + "_SAC32.exe_" + str(i), pid=processo.pid)
#                         self.instancias.append(instancia)
#                         i += 1
#             else:
#                 messagebox.showwarning("Aviso", f"Servidor {servidor} não encontrado.")
#
#         for instancia in self.instancias:
#             usuario = self.entry_usuario.get()
#             senha = self.entry_senha.get()
#
#             OpenSACController.logar_sac(instancia.pid, usuario, senha)
#

#     def confirmar_escolhas(self):
#         # Confirma as escolhas feitas
#         base = self.base_var.get()
#         servidores_selecionados = [servidor.cget("text") for servidor, var in self.servidores_selecionados if var.get()]
#         instancias = self.entry_instancias.get()
#         max_instancias = self.max_instancias
#
#         if not base or not servidores_selecionados:
#             messagebox.showwarning("Aviso", "Você precisa escolher ao menos um servidor.")
#         elif int(instancias) > max_instancias or int(instancias) < 1:
#             messagebox.showwarning("Aviso", "Não é possível abrir a quantidade de SACs solicitada.")
#         else:
#             self.abrir_instancias()
#             messagebox.showinfo("Confirmação",
#                                 f"Base: {base}\nServidores: {', '.join(servidores_selecionados)}\nInstâncias: {instancias}")
#
#
# class Instancia:
#     def __init__(self, nome, pid):
#         self.nome = nome
#         self.pid = pid
#
#     def __str__(self):
#         return f"Instância: {self.nome}; PID: {self.pid}"
#
# if __name__ == "__main__":
#     OpenSacApp()