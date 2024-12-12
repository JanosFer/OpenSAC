import os
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Label
import subprocess


# Função para obter servidores selecionados
def servidores_var(opcoes, servidores_marcados):
    return [opcao for opcao, var in zip(opcoes, servidores_marcados) if var.get()]


# Função para selecionar a base e listar servidores
def selecionar_base():
    global servidores_marcados

    # Limpar a área de servidores
    for widget in frame_servidores.winfo_children():
        widget.destroy()

    base = base_var.get()
    if not base:
        messagebox.showerror("Erro", "Selecione uma base.")
        return

    opcoes = []

    if base == "PRIVATE":
        opcoes = ["PRIVATE D4010S037", "PRIVATE D4010S038", "PRIVATE D4010S039", "PRIVATE D4010S040", "PRIVATE D4010S041"]
    elif base == "PRIME":
        opcoes = ["PRIME D4010S037", "PRIME D4010S038", "PRIME D4010S039", "PRIME D4010S040", "PRIME D4010S041"]

    if not opcoes:
        messagebox.showwarning("Aviso", "Nenhum servidor encontrado para essa base.")
        return

    servidores_marcados = []
    for opcao in opcoes:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame_servidores, text=opcao, variable=var)
        chk.pack(anchor='w')
        servidores_marcados.append(var)

    return opcoes, servidores_marcados


# Função para abrir os diretórios dos servidores selecionados
def abrir_servidores():
    opcoes, servidores_marcados = selecionar_base()
    servidores_selecionados = servidores_var(opcoes, servidores_marcados)

    if not servidores_selecionados:
        messagebox.showerror("Erro", "Nenhum servidor selecionado.")
        return

    caminho_base = r"\\Atalhos_Produção\\TOTVS"
    for servidor in servidores_selecionados:
        caminho_servidor = os.path.join(caminho_base, servidor)
        if os.path.exists(caminho_servidor):
            for sac in os.listdir(caminho_servidor):
                if sac.startswith("SAC"):
                    subprocess.Popen(os.path.join(caminho_servidor, sac))
        else:
            messagebox.showwarning("Aviso", f"Servidor {servidor} não encontrado.")


# Criando a interface
janela = tk.Tk()
janela.title("Escolha de Servidores e SACS")
janela.geometry("800x600")


# Base
base_var = tk.StringVar()
texto_base = Label(janela, text="Escolha a Base:", font=("open sans", 12, "bold"))
texto_base.grid(row=0, column=0, sticky='w', padx=10,pady=10)

base_private = tk.Button(janela, text="Private", command=lambda: [base_var.set("PRIVATE"), selecionar_base(), texto_servidores.config(text="Escolha os servidores:"), texto_instancias.config(text="Escolha a quantidade de instâncias:")], bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
base_private.grid(row=0, column=1, padx=10, pady=10)
base_private.bind("<Enter>", lambda event: base_private.config(bg="#D3D3D3"))
base_private.bind("<Leave>", lambda event: base_private.config(bg="#f0f0f0"))

base_prime = tk.Button(janela, text="Prime", command=lambda: [base_var.set("PRIME"), selecionar_base(), texto_servidores.config(text="Escolha os servidores:"), texto_instancias.config(text="Escolha a quantidade de instâncias:")], bg="#f0f0f0", fg="#1c1c1c", font=("open sans", 12, "bold"), bd=2)
base_prime.grid(row=0, column=2, padx=10, pady=10)
base_prime.bind("<Enter>", lambda event: base_prime.config(bg="#D3D3D3"))
base_prime.bind("<Leave>", lambda event: base_prime.config(bg="#f0f0f0"))


# Servidores
texto_servidores = Label(janela, text="", font=("open sans", 12, "bold"))
texto_servidores.grid(row=1, column=0, sticky='w', padx=10, pady=10)

frame_servidores = tk.Frame(janela)
frame_servidores.grid(row=2, column=0, columnspan=1)


# Instancias
instancia_var = tk.IntVar()

texto_instancias = Label(janela, text="", font=("open sans", 12, "bold"))
texto_instancias.grid(row=3, column=0, padx=10, pady=50)

instancia_input = tk.Entry(janela)


# Confirmar seleção
def confirmar_selecao():
    opcoes, servidores_marcados = selecionar_base()
    servidores_selecionados = servidores_var(opcoes, servidores_marcados)
    if not servidores_selecionados:
        messagebox.showerror("Erro", "Nenhum servidor selecionado.")
        return
    messagebox.showinfo("Seleção", f"Servidores selecionados: {', '.join(servidores_selecionados)}")
    # Agora você pode chamar a função para abrir os diretórios
    abrir_servidores()


tk.Button(janela, text="Confirmar Seleção", command=confirmar_selecao).grid(row=10, column=0, columnspan=3, pady=10, sticky="s")

# Iniciar a interface
janela.mainloop()