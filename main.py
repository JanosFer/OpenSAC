import sys
from PyQt5.QtWidgets import QApplication
from view.JanelaLoginOpenSAC import JanelaLogin

def main():
    app = QApplication(sys.argv)
    janela = JanelaLogin()
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()