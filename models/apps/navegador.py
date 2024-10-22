from PyQt5.QtWebEngineWidgets import QWebEngineView # type: ignore
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit # type: ignore
from PyQt5.QtCore import QUrl # type: ignore

class Navegador(QWidget):
    def __init__(self):
        super().__init__()

        # Crear el layout principal
        layout = QVBoxLayout(self)
        
        # Crear la barra de búsqueda
        self.barra_busqueda = QLineEdit()
        self.barra_busqueda.setPlaceholderText("Ingresa URL o búsqueda...")
        self.barra_busqueda.returnPressed.connect(self.navegar)
        
        layout.addWidget(self.barra_busqueda)

        # Crear los botones de navegación
        nav_layout = QHBoxLayout()
        
        btn_back = QPushButton('Atrás')
        btn_back.clicked.connect(self.volver_atras)
        nav_layout.addWidget(btn_back)
        
        btn_reload = QPushButton('Recargar')
        btn_reload.clicked.connect(self.recargar_pagina)
        nav_layout.addWidget(btn_reload)

        btn_home = QPushButton('Inicio')
        btn_home.clicked.connect(self.ir_inicio)
        nav_layout.addWidget(btn_home)

        # Agregar el layout de botones al layout principal
        layout.addLayout(nav_layout)
        
        # Crear la vista web
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        # Agregar el navegador al layout principal
        layout.addWidget(self.browser)
        
        self.setWindowTitle("Navegador Web")
        self.resize(1024, 768)

    def navegar(self):
        url = self.barra_busqueda.text()
        if url.startswith("http://") or url.startswith("https://"):
            self.browser.setUrl(QUrl(url))
        else:
            # Si no es una URL válida, buscar en Google
            self.browser.setUrl(QUrl(f"https://www.google.com/search?q={url}"))

    def volver_atras(self):
        if self.browser.history().canGoBack():
            self.browser.back()

    def recargar_pagina(self):
        self.browser.reload()

    def ir_inicio(self):
        self.browser.setUrl(QUrl("https://www.google.com"))
