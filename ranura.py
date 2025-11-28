

from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana")
        self.boton1 = QPushButton("Haz clic!")
        self.setCentralWidget(self.boton1)

        self.boton1.clicked.connect(self.clic_de_boton)

    def clic_de_boton(self):
        print("Señal de clic recibida -> Ejecución de la ranura")


if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()