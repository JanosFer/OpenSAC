import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                             QRadioButton, QCheckBox, QSpinBox, QMessageBox)

from controller.OpenSACLoginController import OpenSacController

# noinspection PyUnresolvedReferences
class JanelaEscolhaInstancias(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha a base e a quantidade de SACs")
        self.setStyleSheet("background-color: #F1F1F1;")
        self.setFixedSize(600, 500)
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
        else:
            QMessageBox.information(self, "Sucesso", "Instâncias confirmadas.")

            instancias_por_servidor = 0
            total_instancias = instancias_solicitadas

            if self.radio_private.isChecked():
                instancias_por_servidor = 4
            elif self.radio_prime.isChecked():
                instancias_por_servidor = 8

            for servidor in self.checkboxes_marcadas:
                if instancias_por_servidor > total_instancias:
                    abrir_instancias(servidor.text(), total_instancias)
                    break

                total_instancias -= instancias_por_servidor
                abrir_instancias(servidor.text(), instancias_por_servidor)




    def atualizar_max_instancias(self):
        # Conta o número de checkboxes marcadas
        servidores_selecionados = sum(1 for checkbox in self.checkboxes_marcadas if checkbox.isChecked())

        # Ajusta o máximo de instâncias com base na seleção
        if self.radio_private.isChecked():
            self.base = "private"
            self.max_instancias = servidores_selecionados * 4
        elif self.radio_prime.isChecked():
            self.base = "prime"
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
        self.iniciar_ui()

    def iniciar_ui(self):
        caminho_imagem = "C:/Users/Jonas/PycharmProjects/PythonProject/lib/Banco_Bradesco_logo_(minimalista).png"

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
        if os.path.exists(caminho_imagem):  # Verifica se a imagem existe
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
                self.abrir_janela_principal()
    def abrir_janela_principal(self):
        self.janela_principal = JanelaEscolhaInstancias()
        self.janela_principal.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaLogin()
    janela.show()
    sys.exit(app.exec())