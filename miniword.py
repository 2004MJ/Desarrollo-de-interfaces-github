import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QFileDialog, QToolBar, QStatusBar, QMessageBox, QLabel, QColorDialog, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QDockWidget)
from PySide6.QtGui import QKeySequence, QAction, QTextCursor, QTextCharFormat, QColor, QTextDocument
from PySide6.QtCore import Qt




class MiniWord(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")
        self.resize(900, 600)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.word_label = QLabel("Palabras: 0")
        self.text_edit.textChanged.connect(self.contar_palabras)

        self.archivo_actual = None
        self.guardado = True
        self.text_edit.textChanged.connect(lambda: setattr(self, "guardado", False))

        self.crear_acciones()
        self.crear_menu()
        self.crear_toolbar()
        self.crear_statusbar()
        self.crear_panel_busqueda()

    def crear_acciones(self):
        self.nuevo = QAction("🆕", self, triggered=self.nuevo_archivo)
        self.abrir = QAction("📂", self, triggered=self.abrir_archivo)
        self.guardar = QAction("💾", self, triggered=self.guardar_archivo)
        self.salir = QAction("❌", self, triggered=self.close)

        self.deshacer = QAction("↩️", self,triggered=self.text_edit.undo)
        self.rehacer = QAction("↪️", self, triggered=self.text_edit.redo)
        self.copiar = QAction("📋", self,triggered=self.text_edit.copy)
        self.cortar = QAction("✂️", self, triggered=self.text_edit.cut)
        self.pegar = QAction("📥", self, triggered=self.text_edit.paste)

        self.buscar = QAction("🔍", self, triggered=self.mostrar_panel_busqueda)
        self.color_fondo = QAction("🎨 Color fondo", self, triggered=self.cambiar_color)

    def crear_menu(self):
        menu = self.menuBar()
        m_archivo = menu.addMenu("Archivo")
        m_archivo.addActions([self.nuevo, self.abrir, self.guardar, self.salir])

        m_editar = menu.addMenu("Editar")
        m_editar.addActions([self.deshacer, self.rehacer, self.cortar, self.copiar, self.pegar, self.buscar])

        m_ver = menu.addMenu("Personalizar")
        m_ver.addAction(self.color_fondo)

    def crear_toolbar(self):
        barra = QToolBar()
        self.addToolBar(barra)
        for accion in [self.nuevo, self.abrir, self.guardar, self.deshacer, self.rehacer, self.cortar, self.copiar, self.pegar, self.buscar]:
            barra.addAction(accion)

    def crear_statusbar(self):
        barra_estado = QStatusBar()
        barra_estado.addPermanentWidget(self.word_label)
        self.setStatusBar(barra_estado)

    def nuevo_archivo(self):
        if not self.comprobar_guardado():
            return
        self.text_edit.clear()
        self.archivo_actual = None
        self.guardado = True

    def abrir_archivo(self):
        if not self.comprobar_guardado():
            return
        nombre, _ = QFileDialog.getOpenFileName(self, "Abrir", "", "Archivos de texto (*.txt)")
        if nombre:
            with open(nombre, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())
            self.archivo_actual = nombre
            self.guardado = True

    def guardar_archivo(self):
        if not self.archivo_actual:
            nombre, _ = QFileDialog.getSaveFileName(self, "Guardar", "", "Archivos de texto (*.txt)")
            if not nombre:
                return
            self.archivo_actual = nombre
        with open(self.archivo_actual, "w", encoding="utf-8") as f:
            f.write(self.text_edit.toPlainText())
        self.guardado = True

    def comprobar_guardado(self):
        if not self.guardado:
            r = QMessageBox.question(self, "Guardar cambios", "¿Guardar antes de continuar?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if r == QMessageBox.StandardButton.Yes:
                self.guardar_archivo()
            elif r == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def closeEvent(self, event):
        if self.comprobar_guardado():
            event.accept()
        else:
            event.ignore()

    def crear_panel_busqueda(self):
        self.panel = QWidget()
        layout = QVBoxLayout()
        self.txt_buscar = QLineEdit(placeholderText="Buscar...")
        self.txt_reemplazar = QLineEdit(placeholderText="Reemplazar con...")
        self.btn_sig = QPushButton(" Siguiente")
        self.btn_ant = QPushButton(" Anterior")
        self.btn_reem = QPushButton(" Reemplazar")
        self.btn_todos = QPushButton(" Reemplazar todos")

        fila1 = QHBoxLayout()
        fila1.addWidget(self.btn_ant)
        fila1.addWidget(self.btn_sig)

        fila2 = QHBoxLayout()
        fila2.addWidget(self.btn_reem)
        fila2.addWidget(self.btn_todos)

        layout.addWidget(self.txt_buscar)
        layout.addWidget(self.txt_reemplazar)
        layout.addLayout(fila1)
        layout.addLayout(fila2)
        self.panel.setLayout(layout)

        self.dock = QDockWidget("Buscar / Reemplazar", self)
        self.dock.setWidget(self.panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.hide()

        self.btn_sig.clicked.connect(self.buscar_siguiente)
        self.btn_ant.clicked.connect(self.buscar_anterior)
        self.btn_reem.clicked.connect(self.reemplazar_una)
        self.btn_todos.clicked.connect(self.reemplazar_todas)

    def mostrar_panel_busqueda(self):
        self.dock.setVisible(not self.dock.isVisible())

    def buscar_siguiente(self):
        texto = self.txt_buscar.text()
        if not texto:
            return
        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        encontrado = doc.find(texto, cursor)
        if encontrado.isNull():
            QMessageBox.information(self, "Buscar", "No hay más coincidencias.")
        else:
            self.text_edit.setTextCursor(encontrado)

    def buscar_anterior(self):
        texto = self.txt_buscar.text()
        if not texto:
            return
        cursor = self.text_edit.textCursor()
        try:
            encontrado = self.text_edit.document().find(texto, cursor, QTextDocument.FindFlag.FindBackward)
            if encontrado.isNull():
                QMessageBox.information(self, "Buscar", "No hay coincidencias anteriores.")
            else:
                self.text_edit.setTextCursor(encontrado)
        except Exception:
            QMessageBox.information(self, "Buscar", "Error al buscar anterior (límite alcanzado).")

    
    def reemplazar_una(self):
        buscar = self.txt_buscar.text()
        reemplazar = self.txt_reemplazar.text()
        if not buscar:
            return

        cursor = self.text_edit.textCursor()

        
        if cursor.selectedText() != buscar:
            self.buscar_siguiente()
            cursor = self.text_edit.textCursor()

        if cursor.selectedText() == buscar:
            cursor.insertText(reemplazar)
            self.text_edit.setTextCursor(cursor)
            self.buscar_siguiente()
        else:
            QMessageBox.information(self, "Reemplazar", "No se encontró coincidencia para reemplazar.")

    def reemplazar_todas(self):
        buscar = self.txt_buscar.text()
        reemplazar = self.txt_reemplazar.text()
        texto = self.text_edit.toPlainText()
        contador = texto.count(buscar)
        self.text_edit.setPlainText(texto.replace(buscar, reemplazar))
        QMessageBox.information(self, "Reemplazar todos", f"{contador} reemplazos realizados.")

    def cambiar_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setStyleSheet(f"background-color: {color.name()};")

    def contar_palabras(self):
        self.word_label.setText(f"Palabras: {len(self.text_edit.toPlainText().split())}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiniWord()
    ventana.show()
    sys.exit(app.exec())
