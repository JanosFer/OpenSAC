import os
import subprocess
import threading
import psutil
from tkinter import Tk, Label, Button, messagebox
import time

# Configurações
usuario = {"usuario": "seu_usuario", "senha": "sua_senha"}
base_private = {"Private037": "\\PRIVATE D4010S037", "Private038": "\\PRIVATE D4010S038",
                "Private039": "\\PRIVATE D4010S039", "Private040": "\\PRIVATE D4010S040",
                "Private041": "\\PRIVATE D4010S041"}
base_prime = {"Prime037": "\\PRIME D4010S037", "Prime038": "\\PRIME D4010S038", "Prime039": "\\PRIME D4010S039",
              "Prime040": "\\PRIME D4010S040", "Prime041": "\\PRIME D4010S041"}
max_instancias = {"Private": 20, "Prime": 40}
servidores = {"Private": 4, "Prime": 8}
instancias = []


# Funções para exibir programas selecionados
def exibir_programas_selecionados():
    """Exibe os programas selecionados pelo usuário."""
    programas_selecionados = [programa for programa, var in programas.items() if var.get()]
    if not programas_selecionados:
        messagebox.showerror("Erro", "Selecione pelo menos um programa.")
        return
    messagebox.showinfo("Programas Selecionados", "\n".join(programas_selecionados))  # Exibe os programas selecionados


# Função para ler diretórios
def carregar_dados():
    """Carrega as opções de bases, servidores e programas de acordo com a estrutura de diretórios."""
    global bases, servidores, programas

    # Limpar listas e variáveis para recarregar os dados
    bases = []
    servidores = {}
    programas = {}

    # Caminho base onde os diretórios estão armazenados
    caminho_base = "\\Atalhos_Produção\\TOTVS"

    # Verifica os diretórios de bancos (bd01, bd02, etc.)
    for base in os.listdir(caminho_base):
        base_path = os.path.join(caminho_base, base)
        if os.path.isdir(base_path) and base.startswith("bd"):
            bases.append(base)  # Adiciona o nome do banco à lista

    base_var.set(bases[0] if bases else "")  # Se existirem bancos, preenche com o primeiro banco


def selecionar_base():
    base = base_var.get()
    if base == "":
        messagebox.showerror("Erro", "Selecione uma base.")
        return

    # Carregar servidores dentro da base selecionada
    caminho_banco = os.path.join("C:/caminho/dos/bancos", base)  # Caminho completo do banco
    servidores.clear()  # Limpa servidores anteriores
    for diretorio in os.listdir(caminho_banco):
        serv_path = os.path.join(caminho_banco, diretorio)
        if os.path.isdir(serv_path) and diretorio.startswith("serv"):
            servidores[diretorio] = tk.BooleanVar()  # Adiciona servidor com checkbox

    atualizar_servidores()


def atualizar_servidores():
    """Atualiza os checkboxes de servidores com base no banco selecionado."""
    for widget in frame_servidores.winfo_children():
        widget.destroy()  # Limpa os widgets existentes

    # Cria um checkbox para cada servidor encontrado
    for idx, (servidor, var) in enumerate(servidores.items()):
        tk.Checkbutton(frame_servidores, text=servidor, variable=var).grid(row=idx, column=0, sticky='w')

    # Atualiza os programas ao selecionar um servidor
    selecionar_servidores()


def selecionar_servidores():
    """Exibe os programas de cada servidor selecionado."""
    programas.clear()  # Limpa os programas anteriores
    servidores_selecionados = [servidor for servidor, var in servidores.items() if var.get()]

    if not servidores_selecionados:
        messagebox.showerror("Erro", "Selecione pelo menos um servidor.")
        return

    # Caminho base para servidores
    for servidor in servidores_selecionados:
        caminho_servidor = os.path.join("C:/caminho/dos/bancos", base_var.get(), servidor)
        for programa in os.listdir(caminho_servidor):
            if programa.startswith("sac"):
                programas[programa] = tk.BooleanVar()  # Adiciona o programa à lista

    atualizar_programas()


def atualizar_programas():
    """Atualiza os checkboxes dos programas para os servidores selecionados."""
    for widget in frame_programas.winfo_children():
        widget.destroy()  # Limpa os widgets de programas anteriores

    # Cria um checkbox para cada programa encontrado
    for idx, (programa, var) in enumerate(programas.items()):
        tk.Checkbutton(frame_programas, text=programa, variable=var).grid(row=idx, column=0, sticky='w')


# Função para validar as escolhas do usuário
def validar_entrada():
    """Valida as escolhas do usuário em cada etapa do processo."""
    banco = base_var.get()
    if banco == "":
        messagebox.showerror("Erro", "Por favor, selecione um banco de dados.")
        return
    selecionar_servidores()


def encontrar_executaveis(base):
    executaveis = []
    for servidor, str in base.itens():
        caminho = os.path.join("\\Atalhos_Produção\\TOTVS", servidor)
        for raiz, diretorios, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                if arquivo.startswith("SAC"):
                    executaveis.append(os.path.join(raiz, arquivo))
    return executaveis


def iniciar_instancias(base, num_instancias):
    if (base == "private"):
        executaveis_private = encontrar_executaveis(base_private)
        for sac in executaveis_private:
            for _ in range(num_instancias):
                processo = subprocess.Popen()
                instancias.append(processo)
    elif (base == "prime"):
        executaveis_prime = encontrar_executaveis(base_prime)
        for sac in executaveis_prime:
            for _ in range(num_instancias):
                processo = subprocess.Popen()
                instancias.append(processo)



def monitorar_instancias():
    while True:
        for proc in instances:
            if proc.poll() is not None:  # Processo finalizou
                erro = proc.returncode
                log_erro(f"Instância no PID {proc.pid} fechou com erro {erro}")
                ask_restart(proc)
        time.sleep(5)  # Evitar sobrecarregar o sistema com verificações constantes


def ask_restart(proc):
    def restart():
        new_proc = subprocess.Popen(proc.args)
        instances.append(new_proc)
        log_erro(f"Reiniciando instância com PID {proc.pid}")

    if messagebox.askyesno("Instância Fechada", f"Instância no PID {proc.pid} fechou. Deseja reiniciá-la?"):
        restart()


def log_erro(msg):
    with open("log_erros.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: {msg}\n")


def run_monitoring_thread():
    monitor_thread = threading.Thread(target=monitor_instances, daemon=True)
    monitor_thread.start()


# Interface Gráfica
def create_gui():
    root = Tk()
    root.title("Gerenciador de Instâncias")

    Label(root, text="Gerenciamento de Instâncias").pack(pady=10)
    Button(root, text="Iniciar Instâncias", command=start_instances).pack(pady=5)
    Button(root, text="Sair", command=root.quit).pack(pady=5)

    run_monitoring_thread()
    root.mainloop()


# Fluxo Principal
if name == "main":
    create_gui()