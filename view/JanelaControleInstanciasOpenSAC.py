import os
import sys
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                             QRadioButton, QCheckBox,  QMessageBox, QScrollArea, QTextEdit)
from PyQt5.QtGui import QIcon


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