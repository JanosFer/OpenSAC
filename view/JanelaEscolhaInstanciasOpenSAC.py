import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                             QRadioButton, QCheckBox, QSpinBox, QMessageBox)
from PyQt5.QtGui import QIcon

from view.JanelaControleInstanciasOpenSAC import JanelaControleInstancias

# noinspection PyUnresolvedReferences
class JanelaEscolhaInstancias(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.max_instancias = None
        self.checkboxes_marcadas = None
        self.base = ""
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
        self.spinner_instancias.setRange(0, 20)
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
            return
        elif instancias_solicitadas > self.max_instancias:
            QMessageBox.critical(self, "Erro", "A quantidade de instâncias solicitadas é maior que a máxima permitida.")
            return
        elif instancias_solicitadas <= 0:
            QMessageBox.critical(self, "Erro", "A quantidade de instâncias solicitadas é inválida.")
            return
        else:
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
            self.spinner_instancias.setRange(0, 20)
        elif self.radio_prime.isChecked():
            self.base = "PRIME"
            self.max_instancias = servidores_selecionados * 8
            self.spinner_instancias.setRange(0, 40)

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
