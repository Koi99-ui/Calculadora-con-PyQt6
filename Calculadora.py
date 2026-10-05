# -*- coding: utf-8 -*-
"""
Calculadora simple (PyQt6)
--------------------------
Permite sumar, restar, multiplicar y dividir.
Controla la división entre cero y muestra el historial
de las últimas cinco operaciones.
Creado por Jhudith Romero - 2026
"""

import sys
from collections import deque

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt

# ---------------------------------------------------------------------------
# Paleta de color rosado suave
# ---------------------------------------------------------------------------
COLOR_FONDO = "#FBEEEF"
COLOR_PANEL = "#F6DEE3"
COLOR_ACENTO = "#D9A5B3"
COLOR_BOTON = "#E4B7C2"
COLOR_BOTON_HOVER = "#D9A0B0"
COLOR_TEXTO = "#6B4B57"
COLOR_BLANCO = "#FFF9FA"

ESTILO = f"""
QWidget {{
    background-color: {COLOR_FONDO};
    color: {COLOR_TEXTO};
    font-size: 13px;
}}
QLabel#titulo {{
    font-size: 18px;
    font-weight: bold;
    background-color: {COLOR_PANEL};
    padding: 10px;
    border-radius: 8px;
}}
QLineEdit {{
    background-color: {COLOR_BLANCO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 8px;
    font-size: 22px;
}}
QPushButton {{
    background-color: {COLOR_BOTON};
    color: {COLOR_TEXTO};
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
    font-size: 15px;
    min-width: 56px;
    min-height: 40px;
}}
QPushButton:hover {{
    background-color: {COLOR_BOTON_HOVER};
}}
QListWidget {{
    background-color: {COLOR_BLANCO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 4px;
}}
"""


class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.resize(420, 620)

        self.historial = deque(maxlen=5)  # últimas cinco operaciones
        self.operando = None              # primer número guardado
        self.operacion = None             # operación pendiente
        self.nuevo_numero = True          # indica si el próximo dígito inicia número

        titulo = QLabel("Calculadora Simple")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Pantalla única (como calculadora real)
        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.pantalla.setText("0")

        # Teclado numérico y de operaciones
        teclas = QGridLayout()
        botones = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "⌫", "%", "±"],
        ]
        for fila_idx, fila in enumerate(botones):
            for col_idx, texto in enumerate(fila):
                boton = QPushButton(texto)
                boton.clicked.connect(lambda checked=False, t=texto: self.pulsar(t))
                teclas.addWidget(boton, fila_idx, col_idx)

        # Historial
        etiqueta_hist = QLabel("Historial (últimas 5 operaciones):")
        self.lista_historial = QListWidget()

        # Pie de página
        pie = QLabel("Creado por Jhudith Romero - 2026")
        pie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie.setStyleSheet(
            f"background-color: {COLOR_PANEL}; border-radius: 8px; "
            "padding: 6px; font-style: italic;"
        )

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.pantalla)
        layout.addLayout(teclas)
        layout.addWidget(etiqueta_hist)
        layout.addWidget(self.lista_historial)
        layout.addWidget(pie)
        self.setLayout(layout)

    # --------------------------- Lógica ---------------------------
    def pulsar(self, texto):
        if texto.isdigit():
            self.escribir_digito(texto)
        elif texto == ".":
            self.escribir_punto()
        elif texto == "C":
            self.limpiar()
        elif texto == "⌫":
            actual = self.pantalla.text()
            self.pantalla.setText(actual[:-1] if len(actual) > 1 else "0")
        elif texto == "%":
            self.pantalla.setText(self.formatear(float(self.pantalla.text()) / 100))
        elif texto == "±":
            valor = float(self.pantalla.text())
            self.pantalla.setText(self.formatear(-valor))
        elif texto == "=":
            self.calcular()
        else:  # operadores
            self.guardar_operando(texto)

    def escribir_digito(self, digito):
        if self.nuevo_numero:
            self.pantalla.setText(digito)
            self.nuevo_numero = False
        else:
            actual = self.pantalla.text()
            self.pantalla.setText(digito if actual == "0" else actual + digito)

    def escribir_punto(self):
        if self.nuevo_numero:
            self.pantalla.setText("0.")
            self.nuevo_numero = False
        elif "." not in self.pantalla.text():
            self.pantalla.setText(self.pantalla.text() + ".")

    def guardar_operando(self, simbolo):
        # Si ya hay operación pendiente, calcula primero (encadenar)
        if self.operacion is not None and not self.nuevo_numero:
            self.calcular()
        self.operando = float(self.pantalla.text())
        self.operacion = simbolo
        self.nuevo_numero = True

    def calcular(self):
        if self.operacion is None or self.operando is None:
            return
        try:
            b = float(self.pantalla.text())
        except ValueError:
            return

        a = self.operando
        if self.operacion == "+":
            resultado = a + b
        elif self.operacion == "-":
            resultado = a - b
        elif self.operacion == "×":
            resultado = a * b
        else:  # ÷
            if b == 0:
                QMessageBox.critical(self, "Error", "No se puede dividir entre cero.")
                self.limpiar()
                return
            resultado = a / b

        self.pantalla.setText(self.formatear(resultado))
        self.historial.appendleft(f"{self.formatear(a)} {self.operacion} {self.formatear(b)} = {self.formatear(resultado)}")
        self.lista_historial.clear()
        self.lista_historial.addItems(self.historial)

        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    def limpiar(self):
        self.pantalla.setText("0")
        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    @staticmethod
    def formatear(valor):
        return str(int(valor)) if isinstance(valor, float) and valor == int(valor) else str(valor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ESTILO)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec())
