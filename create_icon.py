"""
Script para criar um ícone simples para a aplicação.
"""
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt
import sys

def create_icon():
    """Cria um ícone simples com a letra 'D' para Determinante."""
    # Criar pixmap de 64x64
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 120, 212))  # Azul elétrico
    
    # Criar painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Desenhar fundo circular
    painter.setBrush(QColor(0, 120, 212))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    
    # Desenhar letra D
    painter.setPen(QColor(255, 255, 255))  # Branco
    painter.setFont(QFont("Arial", 32, QFont.Bold))
    painter.drawText(0, 0, 64, 64, Qt.AlignCenter, "D")
    
    painter.end()
    
    # Salvar como ICO
    pixmap.save("icon.ico", "ICO")
    print("Ícone criado: icon.ico")

if __name__ == "__main__":
    create_icon()
