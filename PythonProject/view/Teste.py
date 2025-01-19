import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QApplication, \
    QMessageBox, QCheckBox, QLineEdit, QRadioButton, QGroupBox
from PyQt5.QtCore import Qt

from controller.OpenSACLoginController import OpenSacController

controller = OpenSacController()
base = "PRIVATE"


class JanelaControleInstancias(QWidget):
    def __init__(self, controller, base):
        super().__init__()
        self.setWindowTitle("Controle de Instâncias")
        self.setStyleSheet("background-color: #F1F1F1;")
        self.setFixedSize(900, 500)
        self.controller = controller
        self.base = base
        self.lista_programas = []
        self.iniciar_ui()

        # Iniciar o monitoramento
        self.controller.iniciar_monitoramento()

    def iniciar_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setAlignment(Qt.AlignTop)

        # Layout principal da janela (lado esquerdo)
        layout_esquerda = QVBoxLayout()
        layout_principal.addLayout(layout_esquerda)

        # Título fora da área rolável
        titulo_label = QLabel("Controle de Instâncias")
        titulo_label.setStyleSheet("color: #CC092F; font-size: 24px; font-weight: bold;")
        layout_esquerda.addWidget(titulo_label)

        # Criação da área de rolagem
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area.setWidget(scroll_area_widget)

        layout_esquerda.addWidget(scroll_area)

        # Layout da tela para os programas
        layout_tela = QVBoxLayout(scroll_area_widget)

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
            self.add_programa(layout_tela, programa)

        # Botões para abrir e fechar todos os programas
        self.botao_abrir_todos = QPushButton("Abrir Todos")
        self.botao_abrir_todos.setStyleSheet(self.estilo_botao_ativo())
        self.botao_abrir_todos.clicked.connect(self.abrir_todos)

        self.botao_fechar_todos = QPushButton("Fechar Todos")
        self.botao_fechar_todos.setStyleSheet(self.estilo_botao_ativo())
        self.botao_fechar_todos.clicked.connect(self.fechar_todos)

        # Layout para os botões de abrir/fechar todos
        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_abrir_todos)
        layout_botoes.addWidget(self.botao_fechar_todos)

        layout_esquerda.addLayout(layout_botoes)
        # Atualizar o estado dos botões ao iniciar
        self.atualizar_botao_geral()

        # Layout da direita (Quadro de Opções)
        layout_direita = QVBoxLayout()
        layout_principal.addLayout(layout_direita)

        # Quadro de Opções de Rotinas
        grupo_rotinas = QGroupBox("Opções de Rotinas")
        layout_direita.addWidget(grupo_rotinas)

        layout_rotinas = QVBoxLayout(grupo_rotinas)

        # RadioButtons para escolher a rotina
        self.radio_netreport = QRadioButton("NetReport")
        self.radio_processamento = QRadioButton("Processamento Geral")
        layout_rotinas.addWidget(self.radio_netreport)
        layout_rotinas.addWidget(self.radio_processamento)

        # Campo de data
        self.data_input = QLineEdit(self)
        self.data_input.setPlaceholderText("DD/MM/AAAA")
        layout_rotinas.addWidget(self.data_input)

        # Checkboxes adicionais para "Processamento Geral"
        self.checkbox_rv = QCheckBox("RV")
        self.checkbox_futuros = QCheckBox("Futuros")
        self.checkbox_rf = QCheckBox("RF")
        self.checkbox_swap = QCheckBox("SWAP")
        self.checkbox_outros = QCheckBox("Outros")
        self.checkbox_clientes = QCheckBox("Clientes")



        # Botão de rodar automação
        self.botao_rodar = QPushButton("Rodar Automação")
        self.botao_rodar.setStyleSheet(self.estilo_botao_ativo())
        self.botao_rodar.setEnabled(False)  # Inicialmente desabilitado
        layout_rotinas.addWidget(self.botao_rodar)

        # Conectar eventos dos radio buttons
        self.radio_netreport.toggled.connect(self.atualizar_botao_rodar)
        self.radio_processamento.toggled.connect(self.atualizar_botao_rodar)

        # Conectar eventos dos checkboxes (para Processamento Geral)
        self.checkbox_rv.toggled.connect(self.atualizar_checkbox_check)
        self.checkbox_futuros.toggled.connect(self.atualizar_checkbox_check)
        self.checkbox_rf.toggled.connect(self.atualizar_checkbox_check)
        self.checkbox_swap.toggled.connect(self.atualizar_checkbox_check)
        self.checkbox_outros.toggled.connect(self.atualizar_checkbox_check)
        self.checkbox_clientes.toggled.connect(self.atualizar_checkbox_check)

        # Lista de programas e seus controles

    def atualizar_botao_rodar(self):
        """Habilita o botão de rodar automação apenas quando um radio button for selecionado."""

        if not self.radio_processamento.isChecked() and not self.radio_netreport.isChecked():
            self.botao_rodar.setEnabled(False)
        elif self.radio_processamento.isChecked():
            self.layout_rotinas.addWidget(self.checkbox_rv)
            self.layout_rotinas.addWidget(self.checkbox_futuros)
            self.layout_rotinas.addWidget(self.checkbox_rf)
            self.layout_rotinas.addWidget(self.checkbox_swap)
            self.layout_rotinas.addWidget(self.checkbox_outros)
            self.layout_rotinas.addWidget(self.checkbox_clientes)
            self.botao_rodar.setEnabled(True)
        elif self.radio_netreport.isChecked():
            self.botao_rodar.setEnabled(True)

    def atualizar_checkbox_check(self):
        """Verifica se pelo menos um checkbox foi marcado em 'Processamento Geral'."""
        if self.radio_processamento.isChecked():
            if (self.checkbox_rv.isChecked() or self.checkbox_futuros.isChecked() or
                    self.checkbox_rf.isChecked() or self.checkbox_swap.isChecked() or
                    self.checkbox_outros.isChecked() or self.checkbox_clientes.isChecked()):
                self.botao_rodar.setEnabled(True)
            else:
                self.botao_rodar.setEnabled(False)


    def atualizar_botao_geral(self):
        aberto = all(programa["status_label"].text() == "Aberto" for programa in self.lista_programas)
        fechado = all(programa["status_label"].text() == "Fechado" for programa in self.lista_programas)

        self.botao_abrir_todos.setEnabled(not aberto)
        self.botao_fechar_todos.setEnabled(not fechado)

    def add_programa(self, layout, programa):
        """Adiciona um programa com seu botão e status na tela."""
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
        """Abre uma instância do programa através do controlador."""
        try:
            self.controller.reabrir_instancias(programa["nome"], self.base)  # Ajuste conforme o controlador
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
        """Fecha uma instância do programa através do controlador."""
        try:
            pid = self.controller.SACs_abertos.get(programa["nome"])  # Obter PID associado
            if pid:
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
        """Abre todas as instâncias através do controlador."""
        try:
            self.controller.reabrir_instancias("servidor", len(self.lista_programas), self.base)
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
        """Fecha todas as instâncias através do controlador."""
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
        """Atualiza os status dos programas em tempo real."""
        for programa in self.lista_programas:
            nome_programa = programa["nome"]
            status_label = programa["status_label"]

            if nome_programa in self.controller.SACs_abertos:
                status_label.setText("Aberto")
                status_label.setStyleSheet("font-size: 12px; color: #008000;")
            elif nome_programa in self.controller.SACs_fechados:
                status_label.setText("Fechado")
                status_label.setStyleSheet("font-size: 12px; color: #FF0000;")

    @staticmethod
    def estilo_botao_ativo():
        return """
                    QPushButton {
                        background-color: #CC092F;
                        color: #FFFFFF;
                        font-size: 14px;
                        font-weight: bold;
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
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        cursor: not-allowed;
                    }
                """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaControleInstancias(controller, base)
    janela.show()
    sys.exit(app.exec())