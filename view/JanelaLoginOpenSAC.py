import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                             QMessageBox)
from PyQt5.QtGui import QIcon

from controller.ControllerOpenSAC import OpenSacController
from view.JanelaEscolhaInstanciasOpenSAC import JanelaEscolhaInstancias

# noinspection PyUnresolvedReferences
class JanelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.input_senha = None
        self.input_usuario = None
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

        if not usuario or not senha:
            QMessageBox.critical(self, "Erro", "Usuário e Senha devem ser preenchidos!")
            return

        try:
            controller = OpenSacController()
            if controller.validar_login(usuario, senha):
                self.abrir_janela_escolha_instancias(controller)
            else:
                QMessageBox.warning(self, "Erro", "Login inválido")
        except Exception as e:
            QMessageBox.critical(self, "Erro Interno", str(e))


    def abrir_janela_escolha_instancias(self, controller):
        escolha_instancias = JanelaEscolhaInstancias(controller)
        self.janela_escolha_instancias = escolha_instancias
        self.janela_escolha_instancias.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaLogin()
    janela.show()
    sys.exit(app.exec())