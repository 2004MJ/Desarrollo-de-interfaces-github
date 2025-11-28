from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

class Ventana(QMainWindow):
    def __init__(self, nombre):
        super().__init__()
        self.setWindowTitle(f"Ventana {nombre}")
        self.boton = QPushButton(f"Haz clic en {nombre}",self)
        self.setCentralWidget(self.boton)
        self.boton.clicked.connect(self.on_click)

    def on_click(self):
        # Cada instancia usa su propio `self`
        self.boton.setText(f"Clic en {self.windowTitle()}")
        print(f"[{self.windowTitle()}] Señal recibida -> self={hex(id(self))}")

if __name__ == "__main__":
    app = QApplication([])
    a = Ventana("A")
    b = Ventana("B")
    a.move(200, 200)
    b.move(450, 200)
    a.show()
    b.show()
    app.exec()
