import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                             QRadioButton, QCheckBox, QSpinBox, QMessageBox, QScrollArea, QTextEdit)
from PyQt5.QtGui import QIcon

from controller.OpenSACLoginController import OpenSacController


# noinspection PyUnresolvedReferences
class JanelaControleInstancias(QWidget):
    def __init__(self, controller, base):
        super().__init__()
        self.setWindowTitle("Controle de Instâncias")
        self.setStyleSheet("background-color: #F1F1F1;")
        self.setFixedSize(900, 500)
        icone_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'Icone_OpenSAC.png')
        self.setWindowIcon(QIcon(icone_path))
        self.controller = controller
        self.base = base
        self.lista_programas = []
        self.iniciar_ui()

        # Iniciar o monitoramento
        self.controller.iniciar_monitoramento()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_status_programas)  # Conecta o timeout do timer à função
        self.timer.start(1000)  # Inicia o timer com intervalo de 1 segundo

    def iniciar_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setAlignment(Qt.AlignTop)

        tela = QFrame(self)
        tela.setFixedSize(870, 470)
        tela.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_tela = QVBoxLayout(tela)
        layout_tela.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Topo da tela
        topo_frame = QFrame()
        topo_frame.setStyleSheet("border: none;")
        layout_topo = QHBoxLayout(topo_frame)
        layout_topo.setContentsMargins(10, 10, 10, 10)
        layout_topo.setSpacing(15)

        # Título fora da área rolável
        titulo_label = QLabel("Controle de Instâncias                        Opções de Rotinas")
        titulo_label.setStyleSheet("color: #CC092F; font-size: 24px; font-weight: bold;")
        layout_topo.addWidget(titulo_label)

        layout_tela.addWidget(topo_frame)

        # Corpo da tela
        container = QFrame()
        container.setStyleSheet("background-color: #FFFFFF; border: none;")
        layout_container = QHBoxLayout(container)
        layout_container.setSpacing(40)
        layout_container.setContentsMargins(15, 15, 15, 15)

        # Layout da esquerda
        layout_esquerda = QVBoxLayout()

        # Área de rolagem para a lista de programas
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area.setWidget(scroll_area_widget)

        layout_esquerda.addWidget(scroll_area)

        # Layout interno para a área de rolagem
        layout_scroll = QVBoxLayout(scroll_area_widget)

        # Lista de programas e seus controles
        if self.base == "PRIVATE":
            self.lista_programas = [
                {"nome": "PRIVATE SAC_37", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_37_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_37_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_37_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_38", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_38_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_38_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_38_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_39", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_39_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_39_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_39_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_40", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_40_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_40_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_40_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_41", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_41_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_41_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIVATE SAC_41_3", "botao_abrir": None, "botao_fechar": None}
            ]
        elif self.base == "PRIME":
            self.lista_programas = [
                {"nome": "PRIME SAC_37", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_4", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_5", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_6", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_37_7", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_4", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_5", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_6", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_38_7", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_4", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_5", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_6", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_39_7", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_4", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_5", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_6", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_40_7", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_1", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_2", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_3", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_4", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_5", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_6", "botao_abrir": None, "botao_fechar": None},
                {"nome": "PRIME SAC_41_7", "botao_abrir": None, "botao_fechar": None}
            ]

        # Criar os programas
        for programa in self.lista_programas:
            self.add_programa(layout_scroll, programa)


        # Botões para abrir/fechar todos os programas
        self.botao_abrir_todos = QPushButton("Abrir Todos")
        self.botao_abrir_todos.setStyleSheet(self.estilo_botao_ativo())
        self.botao_abrir_todos.clicked.connect(self.abrir_todos)

        self.botao_fechar_todos = QPushButton("Fechar Todos")
        self.botao_fechar_todos.setStyleSheet(self.estilo_botao_ativo())
        self.botao_fechar_todos.clicked.connect(self.fechar_todos)

        # Layout para os botões de abrir/fechar
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_abrir_todos)
        layout_botoes.addWidget(self.botao_fechar_todos)
        layout_esquerda.addLayout(layout_botoes)

        # Atualizar o estado dos botões
        self.atualizar_botao_geral()

        layout_container.addLayout(layout_esquerda)

        # Layout da direita
        layout_direita = QVBoxLayout()

        rotinas_frame = QFrame()
        rotinas_frame.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_rotinas_frame = QVBoxLayout(rotinas_frame)
        layout_rotinas_frame.setContentsMargins(15, 15, 15, 15)

        # RadioButtons para selecionar a rotina
        self.radio_netreport = QRadioButton("NetReport")
        self.radio_netreport.setStyleSheet("color: #333333; font-size: 13px; border: none;")
        layout_rotinas_frame.addWidget(self.radio_netreport)

        self.radio_processamento = QRadioButton("Processamento Geral")
        self.radio_processamento.setStyleSheet("color: #333333; font-size: 13px; border: none;")
        self.radio_processamento.toggled.connect(self.carregar_checkboxes)
        layout_rotinas_frame.addWidget(self.radio_processamento)

        self.checkbox_automatiza = QCheckBox("Rodar Scripts")
        self.checkbox_automatiza.setStyleSheet("color: #333333; font-size: 13px; border: none;")
        self.checkbox_automatiza.stateChanged.connect(self.adicionar_scripts)
        layout_rotinas_frame.addWidget(self.checkbox_automatiza)

        layout_rotinas_frame.addSpacing(5)

        layout_data = QHBoxLayout()

        # Campo de entrada para data
        self.label_data = QLabel("Informe a Data do Processamento")
        self.label_data.setStyleSheet("color: #333333; font-size: 13px; border: none;")
        layout_data.addWidget(self.label_data)

        layout_data.addSpacing(5)

        self.data_input = QLineEdit(self)
        self.data_input.setInputMask(" 00/00/0000")
        self.data_input.setPlaceholderText("DD/MM/AAAA")
        self.data_input.setStyleSheet("padding: 3px; font-size: 11px;")

        layout_data.addWidget(self.data_input)

        layout_rotinas_frame.addLayout(layout_data)

        layout_rotinas_frame.addSpacing(5)

        # Inicialização do layout de scripts
        layout_scripts = QVBoxLayout()
        self.layout_scripts = layout_scripts  # Salvando o layout na variável da classe

        layout_rotinas_frame.addLayout(layout_scripts)

        self.layout_modulos = QVBoxLayout()
        self.layout_modulos.setSpacing(5)
        layout_rotinas_frame.addLayout(self.layout_modulos)

        self.label_modulos = QLabel("Selecione os módulos a serem processados:")
        self.label_modulos.setStyleSheet("color: #333333; font-size: 13px; border: none;")
        self.label_modulos.setVisible(False)
        self.layout_modulos.addWidget(self.label_modulos)
        self.radio_processamento.toggled.connect(lambda checked: self.label_modulos.setVisible(checked))

        layout_rotinas_frame.addStretch()

        # Botão de rodar automação
        self.botao_rodar = QPushButton("Rodar Automação")
        self.botao_rodar.setStyleSheet(self.estilo_botao_ativo())
        self.botao_rodar.toggled.connect(self.confirmar)
        layout_rotinas_frame.addWidget(self.botao_rodar)

        layout_direita.addWidget(rotinas_frame)
        layout_container.addLayout(layout_direita)

        layout_tela.addWidget(container)
        layout_principal.addWidget(tela)

    def adicionar_scripts(self, state):
        if state == 2:  # Checkbox marcada (checked)
            if not hasattr(self, 'input_widget') or self.input_widget is None:
                # Criar o widget de input (QTextEdit)
                self.input_widget = QTextEdit(self)
                self.input_widget.setPlaceholderText("Cole os Scripts a serem processados aqui:")
                self.input_widget.setFixedHeight(80)
                self.layout_scripts.addWidget(self.input_widget)  # Adicionar ao layout de scripts
        else:  # Checkbox desmarcada (unchecked)
            if hasattr(self, 'input_widget') and self.input_widget:
                self.input_widget.deleteLater()  # Destruir o widget de input
                self.input_widget = None  # Resetar o widget de input

    def carregar_checkboxes(self):
        # Limpa as checkboxes existentes
        for i in reversed(range(self.layout_modulos.count())):
            widget = self.layout_modulos.itemAt(i).widget()
            if widget and isinstance(widget, QCheckBox):
                widget.deleteLater()

        opcoes = []

        if self.radio_processamento.isChecked():
            opcoes = ["Renda Variável", "Futuros", "Swap", "Outros", "Clientes"]

        self.checkboxes_marcadas = []

        for opcao in opcoes:
            checkbox = QCheckBox(opcao)
            checkbox.setStyleSheet("color: #333333; font-size: 13px; border: none;")
            self.layout_modulos.addWidget(checkbox)
            self.checkboxes_marcadas.append(checkbox)

    def atualizar_botao_geral(self):
        aberto = all(programa["status_label"].text() == "Aberto" for programa in self.lista_programas)
        fechado = all(programa["status_label"].text() == "Fechado" for programa in self.lista_programas)

        self.botao_abrir_todos.setEnabled(not aberto)
        self.botao_fechar_todos.setEnabled(not fechado)

    def add_programa(self, layout, programa):
        frame_programa = QFrame()
        frame_programa.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_programa = QHBoxLayout(frame_programa)

        # Nome do programa
        nome_label = QLabel(programa["nome"])
        nome_label.setStyleSheet("font-size: 14px; color: #333333;")
        layout_programa.addWidget(nome_label)

        # Status do programa
        status_label = QLabel("Fechado")
        status_label.setStyleSheet("font-size: 12px; color: #FF0000;")
        layout_programa.addWidget(status_label)

        # Botões de abrir e fechar
        botao_abrir = QPushButton("Abrir")
        botao_abrir.setStyleSheet(self.estilo_botao_ativo())
        botao_abrir.setEnabled(True)
        botao_abrir.clicked.connect(
            lambda: self.abrir_programa(programa, status_label, botao_abrir, botao_fechar)
        )

        botao_fechar = QPushButton("Fechar")
        botao_fechar.setStyleSheet(self.estilo_botao_inativo())
        botao_fechar.setEnabled(False)
        botao_fechar.clicked.connect(
            lambda: self.fechar_programa(programa, status_label, botao_abrir, botao_fechar)
        )

        # Armazenando os botões no dicionário do programa
        programa["botao_abrir"] = botao_abrir
        programa["botao_fechar"] = botao_fechar
        programa["status_label"] = status_label

        layout_programa.addWidget(botao_abrir)
        layout_programa.addWidget(botao_fechar)

        layout.addWidget(frame_programa)

    def abrir_programa(self, programa, status_label, botao_abrir, botao_fechar):
        try:
            self.controller.reabrir_instancia(programa["nome"], self.base)
            status_label.setText("Aberto")
            status_label.setStyleSheet("font-size: 12px; color: #008000;")
            botao_abrir.setEnabled(False)
            botao_abrir.setStyleSheet(self.estilo_botao_inativo())
            botao_fechar.setEnabled(True)
            botao_fechar.setStyleSheet(self.estilo_botao_ativo())
            self.atualizar_botao_geral()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o programa: {e}")

    def fechar_programa(self, programa, status_label, botao_abrir, botao_fechar):
        try:
            pid = next(
                (pid for pid, nome in self.controller.SACs_abertos.items() if nome == programa["nome"]),
                None
            )
            self.controller.fechar_instancia(pid)
            status_label.setText("Fechado")
            status_label.setStyleSheet("font-size: 12px; color: #FF0000;")
            botao_fechar.setEnabled(False)
            botao_fechar.setStyleSheet(self.estilo_botao_inativo())
            botao_abrir.setEnabled(True)
            botao_abrir.setStyleSheet(self.estilo_botao_ativo())
            self.atualizar_botao_geral()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao fechar o programa: {e}")

    def abrir_todos(self):
        try:
            for programa in self.lista_programas:
                self.abrir_programa(
                    programa,
                    programa["status_label"],
                    programa["botao_abrir"],
                    programa["botao_fechar"]
                )
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir todos os programas: {e}")

    def fechar_todos(self):
        try:
            self.controller.fechar_todas_instancias()
            for programa in self.lista_programas:
                self.fechar_programa(
                    programa,
                    programa["status_label"],
                    programa["botao_abrir"],
                    programa["botao_fechar"]
                )
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao fechar todos os programas: {e}")

    def atualizar_status_programas(self):
        for programa in self.lista_programas:
            nome_programa = programa["nome"]
            status_label = programa["status_label"]

            if nome_programa in self.controller.SACs_abertos:
                status_label.setText("Aberto")
                status_label.setStyleSheet("font-size: 12px; color: #008000;")
            elif nome_programa in self.controller.SACs_fechados:
                status_label.setText("Fechado")
                status_label.setStyleSheet("font-size: 12px; color: #FF0000;")
            elif nome_programa in self.controller.SACs_processando:
                status_label.setText("Processando")
                status_label.setStyleSheet("font-size: 12px; color: #569CD6;")
            elif nome_programa in self.controller.SACs_erros:
                status_label.setText("Erro")
                status_label.setStyleSheet("font-size: 12px; color: #FFA500;")

    def confirmar(self):
        text = self.text_edit.toPlainText()
        lista_scripts = [linha for linha in text.splitlines() if linha.strip()]

        automatizado = False
        data = self.data_input.text()

        if self.checkbox_automatiza.isChecked():
            automatizado = True

        if self.radio_netreport.isChecked() and self.controller.SACs_abertos:
            try:
                self.controller.roda_automacao(data, "NetReport", automatizado, None, lista_scripts)
            except Exception as e:
                print(f"Erro na automação: {e}")
                sys.exit(1)


        elif self.radio_processamento.isChecked() and self.controller.SACs_abertos and self.checkboxes_marcadas:
            try:
                self.controller.roda_automacao(data, "Processamento Geral", automatizado, self.checkboxes_marcadas, lista_scripts)
            except Exception as e:
                QMessageBox.critical(None, "Erro", f"Erro na automação: {e}")


        elif self.radio_processamento.isChecked() and not self.checkboxes_marcadas:
            QMessageBox.critical(None, "Aviso", "É necessário marcar ao menos um Módulo, para dar inicio ao processamento")

        if not self.controller.SACs_abertos:
            QMessageBox.critical(None, "Aviso", "Nenhuma instancia de SAC aberta, por favor, abra alguma antes de rodar a automação.")


    @staticmethod
    def estilo_botao_ativo():
        return """
                    QPushButton {
                        background-color: #CC092F;
                        color: #FFFFFF;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #B80A2C;
                        cursor: pointer;
                    }
                    QPushButton:pressed {
                        background-color: #9B0726;
                    }
                """

    @staticmethod
    def estilo_botao_inativo():
        return """
                    QPushButton {
                        background-color: #D3D3D3;
                        color: #B0B0B0;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        cursor: not-allowed;
                    }
                """

# noinspection PyUnresolvedReferences
class JanelaEscolhaInstancias(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.janela_controle_instancias = None
        self.setWindowTitle("Escolha a base e a quantidade de SACs")
        self.setStyleSheet("background-color: #F1F1F1;")
        self.setFixedSize(600, 500)
        icone_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'Icone_OpenSAC.png')
        self.setWindowIcon(QIcon(icone_path))
        self.controller = controller
        self.iniciar_ui()

    def iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tela = QFrame(self)
        tela.setFixedSize(570, 470)
        tela.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_tela = QVBoxLayout(tela)
        layout_tela.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Topo da tela
        topo_frame = QFrame()
        topo_frame.setStyleSheet("border: none;")
        layout_topo = QHBoxLayout(topo_frame)
        layout_topo.setContentsMargins(10, 10, 10, 10)
        layout_topo.setSpacing(15)

        titulo_label = QLabel("Escolha de Instâncias")
        titulo_label.setStyleSheet("color: #CC092F; font-size: 25px; font-weight: bold; border: none;")
        layout_topo.addWidget(titulo_label)

        layout_tela.addWidget(topo_frame)

        # Corpo da tela
        container = QFrame()
        container.setStyleSheet("background-color: #FFFFFF; border: none;")
        layout_container = QVBoxLayout(container)
        layout_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout para dividir os blocos
        layout_dividido = QVBoxLayout()

        # Bloco para escolher a base
        base_frame = QFrame()
        base_frame.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_base_frame = QVBoxLayout(base_frame)
        layout_base_frame.setContentsMargins(15, 15, 15, 15)

        label_base = QLabel("Escolha a base:")
        label_base.setStyleSheet("color: #333333; font-size: 12px; border: none;")
        layout_base_frame.addWidget(label_base)

        self.radio_private = QRadioButton("Private")
        self.radio_private.setStyleSheet("color: #333333; font-size: 11px; border: none;")
        self.radio_private.toggled.connect(self.atualizar_checkboxes)

        self.radio_prime = QRadioButton("Prime")
        self.radio_prime.setStyleSheet("color: #333333; font-size: 11px; border: none;")
        self.radio_prime.toggled.connect(self.atualizar_checkboxes)

        layout_base_frame.addWidget(self.radio_private)
        layout_base_frame.addWidget(self.radio_prime)

        layout_dividido.addWidget(base_frame)

        # Bloco para escolher os servidores
        servidor_frame = QFrame()
        servidor_frame.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_servidor_frame = QVBoxLayout(servidor_frame)
        layout_servidor_frame.setContentsMargins(15, 15, 15, 15)

        self.label_servidores = QLabel("Escolha quais servidores deseja usar:")
        self.label_servidores.setStyleSheet("color: #333333; font-size: 12px; border: none;")
        layout_servidor_frame.addWidget(self.label_servidores)

        self.checkbox_marcar_todos = QCheckBox("Marcar todos")
        self.checkbox_marcar_todos.setStyleSheet("color: #333333; font-size: 11px; border: none;")

        # Layout dos servidores (inicialmente oculto)
        self.layout_servidores = QVBoxLayout()
        self.layout_servidores.setSpacing(10)
        layout_servidor_frame.addLayout(self.layout_servidores)

        layout_dividido.addWidget(servidor_frame)

        # Adiciona o layout de divisão no layout principal
        layout_container.addLayout(layout_dividido)

        # Layout para o campo de quantidade de instâncias
        layout_instancias = QHBoxLayout()

        self.label_instancias = QLabel("Digite a quantidade de instâncias que deseja abrir:")
        self.label_instancias.setStyleSheet("color: #333333; font-size: 12px;")
        layout_instancias.addWidget(self.label_instancias)

        self.spinner_instancias = QSpinBox()
        self.spinner_instancias.setRange(0, 40)
        self.spinner_instancias.setStyleSheet("color: #333333; font-size: 12px;")
        layout_instancias.addWidget(self.spinner_instancias)

        layout_container.addLayout(layout_instancias)

        # Exibir a quantidade máxima permitida
        self.label_maxima = QLabel("Quantidade máxima: 0")
        self.label_maxima.setStyleSheet("color: #333333; font-size: 12px;")
        layout_container.addWidget(self.label_maxima)

        layout_container.setSpacing(10)

        # Botão de confirmar
        self.botao_confirmar = QPushButton("Confirmar")
        self.botao_confirmar.setStyleSheet("""
            QPushButton {
                background-color: #CC092F;
                color: #FFFFFF;
                font-size: 12px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 0px;
            }
            QPushButton:hover {
                background-color: #B80A2C;
                cursor: pointer;
            }
            QPushButton:pressed {
                background-color: #9B0726;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        self.botao_confirmar.clicked.connect(self.confirmar)
        layout_container.addWidget(self.botao_confirmar)

        layout_tela.addWidget(container)
        layout_principal.addWidget(tela)

    def confirmar(self):
        instancias_solicitadas = self.spinner_instancias.value()

        if not self.radio_private.isChecked() and not self.radio_prime.isChecked():
            QMessageBox.critical(self, "Erro", "Por favor selecione uma base.")
        elif instancias_solicitadas > self.max_instancias:
            QMessageBox.critical(self, "Erro", "A quantidade de instâncias solicitadas é maior que a máxima permitida.")
        elif instancias_solicitadas <= 0:
            QMessageBox.critical(self, "Erro", "A quantidade de instâncias solicitadas é inválida.")


        instancias_por_servidor = 0
        total_instancias = instancias_solicitadas

        if self.radio_private.isChecked():
            instancias_por_servidor = 4
        elif self.radio_prime.isChecked():
            instancias_por_servidor = 8

        for servidor in self.checkboxes_marcadas:
            if instancias_por_servidor > total_instancias:
                self.controller.abrir_instancias(servidor.text(), total_instancias)
                break

            total_instancias -= instancias_por_servidor
        self.controller.iniciar_monitoramento()
        self.abrir_janela_controle_instancias()

    def abrir_janela_controle_instancias(self):
        self.janela_controle_instancias = JanelaControleInstancias(self.controller, self.base)
        self.janela_controle_instancias.show()
        self.close()

    def atualizar_max_instancias(self):
        # Conta o número de checkboxes marcadas
        servidores_selecionados = sum(1 for checkbox in self.checkboxes_marcadas if checkbox.isChecked())

        # Ajusta o máximo de instâncias com base na seleção
        if self.radio_private.isChecked():
            self.base = "PRIVATE"
            self.max_instancias = servidores_selecionados * 4
        elif self.radio_prime.isChecked():
            self.base = "PRIME"
            self.max_instancias = servidores_selecionados * 8

        # Atualiza o label com a quantidade máxima
        self.label_maxima.setText(f"Quantidade máxima: {self.max_instancias}")
        self.spinner_instancias.setValue(self.max_instancias)

    def atualizar_checkboxes(self):
        # Limpa as checkboxes existentes (removendo todas, exceto o checkbox "marcar todos")
        for i in reversed(range(self.layout_servidores.count())):
            widget = self.layout_servidores.itemAt(i).widget()
            if widget and isinstance(widget, QCheckBox) and widget != self.checkbox_marcar_todos:
                widget.deleteLater()

        # Define as opções baseadas na base escolhida
        opcoes = []
        if self.radio_private.isChecked():
            opcoes = ["PRIVATE D4010S037", "PRIVATE D4010S038", "PRIVATE D4010S039", "PRIVATE D4010S040", "PRIVATE D4010S041"]
        elif self.radio_prime.isChecked():
            opcoes = ["PRIME D4010S037", "PRIME D4010S038", "PRIME D4010S039", "PRIME D4010S040", "PRIME D4010S041"]

        # Adiciona a checkbox "marcar todos" (se já não estiver no layout)
        if self.checkbox_marcar_todos not in self.layout_servidores.children():
            self.layout_servidores.addWidget(self.checkbox_marcar_todos)

        # Cria e adiciona as novas checkboxes com base nas opções
        self.checkboxes_marcadas = []  # Lista para armazenar as checkboxes marcadas

        for opcao in opcoes:
            checkbox = QCheckBox(opcao)
            checkbox.setStyleSheet("color: #333333; font-size: 9px; border: none;")
            self.layout_servidores.addWidget(checkbox)
            self.checkboxes_marcadas.append(checkbox)

            # Conectar o sinal de mudança de estado para chamar a função atualizar_max_instancias
            checkbox.stateChanged.connect(self.atualizar_max_instancias)

        # Conectar o sinal do "marcar todos" para desabilitar ou habilitar as checkboxes
        self.checkbox_marcar_todos.stateChanged.connect(self.atualizar_estado_checkboxes)

        # Limpar o estado de "marcar todos" quando trocar de botão
        self.checkbox_marcar_todos.setChecked(False)
        self.atualizar_estado_checkboxes()

        # Atualiza as instâncias na tela
        self.atualizar_max_instancias()

    def atualizar_estado_checkboxes(self):
        # Se o "marcar todos" estiver marcado
        if self.checkbox_marcar_todos.isChecked():
            # Marcar todas as checkboxes e desabilitar elas
            for checkbox in self.checkboxes_marcadas:
                checkbox.setChecked(True)  # Marca a checkbox
                checkbox.setEnabled(False)  # Desabilita a checkbox
                checkbox.setStyleSheet("color: #888888; font-size: 11px; border: none;")  # Cor cinza
        else:
            # Desmarcar todas as checkboxes e habilitar elas
            for checkbox in self.checkboxes_marcadas:
                checkbox.setChecked(False)  # Desmarca a checkbox
                checkbox.setEnabled(True)  # Habilita a checkbox
                checkbox.setStyleSheet("color: #333333; font-size: 11px; border: none;")


# noinspection PyUnresolvedReferences
class JanelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Open SAC")
        self.setStyleSheet("background-color: #F1F1F1;")
        self.setFixedSize(600, 500)
        icone_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'Icone_OpenSAC.png')
        self.setWindowIcon(QIcon(icone_path))
        self.iniciar_ui()

    def iniciar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tela = QFrame(self)
        tela.setFixedSize(570, 470)
        tela.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: 2px solid #B9B9B9;")
        layout_tela = QVBoxLayout(tela)
        layout_tela.setAlignment(Qt.AlignmentFlag.AlignTop)

        topo_frame = QFrame()
        topo_frame.setStyleSheet("border: none;")
        layout_topo = QHBoxLayout(topo_frame)
        layout_topo.setContentsMargins(10, 10, 10, 10)
        layout_topo.setSpacing(15)

        logo_label = QLabel()
        caminho_imagem = os.path.join(os.path.dirname(__file__), '..', 'lib/Banco_Bradesco_logo_(minimalista).png')
        pixmap = QPixmap(caminho_imagem)
        pixmap = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setStyleSheet("border: none;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        titulo_label = QLabel("Open SAC")
        titulo_label.setStyleSheet("color: #CC092F; font-size: 38px; font-weight: bold; border: none;")
        titulo_label.setContentsMargins(90, 0, 0, 0)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout_topo.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignTop)
        layout_topo.addWidget(titulo_label, alignment=Qt.AlignmentFlag.AlignTop)
        layout_topo.addStretch()

        layout_tela.addWidget(topo_frame)

        container = QFrame()
        container.setFixedSize(500, 320)
        container.setStyleSheet("background-color: #FFFFFF; border: none;")
        container.setContentsMargins(120, 0, 80, 0)
        layout_container = QVBoxLayout(container)
        layout_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_frame = QFrame()
        login_frame.setStyleSheet("""
            QFrame {
                background-color: #CC092F;
                border: 2px solid #B9B9B9;
                border-radius: 10px;
            }
        """)
        layout_login_frame = QVBoxLayout(login_frame)
        layout_login_frame.setContentsMargins(0, 0, 0, 0)

        login_label = QLabel("Login")
        login_label.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;")
        login_label.setContentsMargins(0, 3, 0, 0)
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_login_frame.addWidget(login_label)

        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #FFFFFF; border-radius: 10px; border: none")
        layout_input_frame = QVBoxLayout(input_frame)
        layout_input_frame.setContentsMargins(15, 15, 15, 15)

        user_label = QLabel("Usuário")
        user_label.setStyleSheet("color: #333333; font-size: 14px;")
        self.input_usuario = QLineEdit()
        self.input_usuario.setStyleSheet("""
            background-color: #FFFFFF;
            color: #000000;
            border: 1px solid #D3D3D3;
            border-radius: 10px;
            padding: 5px;
        """)
        layout_input_frame.addWidget(user_label)
        layout_input_frame.addWidget(self.input_usuario)

        senha_label = QLabel("Senha")
        senha_label.setStyleSheet("color: #333333; font-size: 14px;")
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_senha.setStyleSheet("""
            background-color: #FFFFFF;
            color: #000000;  
            border: 1px solid #D3D3D3;
            border-radius: 10px;
            padding: 5px;
        """)
        layout_input_frame.addWidget(senha_label)
        layout_input_frame.addWidget(self.input_senha)

        layout_login_frame.addWidget(input_frame)
        layout_container.addWidget(login_frame)
        layout_container.setSpacing(30)

        login_button = QPushButton("Confirmar Login")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #CC092F;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 0px;
            }

            QPushButton:hover {
                background-color: #B80A2C;
                cursor: pointer;
            }

            QPushButton:pressed {
                background-color: #9B0726;
            }

            QPushButton:focus {
                outline: none;
            }
        """)

        login_button.clicked.connect(self.verificar_login)
        self.input_usuario.returnPressed.connect(self.verificar_login)
        self.input_senha.returnPressed.connect(self.verificar_login)

        login_button.setFixedHeight(40)
        layout_container.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_tela.addWidget(container)
        layout_principal.addWidget(tela)

    def verificar_login(self):
        usuario = self.input_usuario.text()
        senha = self.input_senha.text()

        validar = OpenSacController()

        if not usuario or not senha:
            QMessageBox.critical(self, "Erro", "Usuário e Senha devem ser preenchidos!")
        else:
            if validar.validar_login(usuario, senha):
                self.input_usuario.clear()
                self.input_senha.clear()
                usuario = None
                senha = None
                self.abrir_janela_escolha_instancias(validar)
    def abrir_janela_escolha_instancias(self, controller):
        self.janela_escolha_instancias = JanelaEscolhaInstancias(controller)
        self.janela_escolha_instancias.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaLogin()
    janela.show()
    sys.exit(app.exec())