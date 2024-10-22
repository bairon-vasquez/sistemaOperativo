from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGridLayout, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QTimeZone
import sys
import psutil  # Biblioteca para obtener información de batería
from  models.apps.calculadora import Calculadora
from  models.apps.musica import MusicPlayer


class DesktopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Escritorio Principal')
        self.setGeometry(0, 0, 1024, 768)

        self.active_apps = {}  # Diccionario para almacenar aplicaciones activas

        # Crear QLabel para la imagen de fondo
        self.fondo = QLabel(self)
        pixmap = QPixmap('imagenes\\fondo.jpg')

        if pixmap.isNull():
            print("Error: No se pudo cargar la imagen.")
        else:
            self.fondo.setPixmap(pixmap)
            self.fondo.setScaledContents(True)
            self.fondo.setGeometry(self.rect())

        # Crear el widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Crear layout para la parte superior
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Crear barra de tareas en la parte superior izquierda
        self.create_taskbar(top_layout)

        # Crear reloj y batería en la parte superior derecha
        self.create_top_right_controls(top_layout)

        main_layout.addLayout(top_layout)  # Añadir la parte superior (barra y reloj)

        # Crear layout de grilla para los iconos de aplicaciones
        icons_layout = QGridLayout()
        icons_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        icons_layout.setSpacing(20)
        main_layout.addLayout(icons_layout, stretch=1)

        app_icons = [
            ('imagenes\\iconos\\aplicaciones\\papelera.png', 'Papelera'),
            ('imagenes\\iconos\\aplicaciones\\internet.png', 'Navegador'),
            ('imagenes\\iconos\\aplicaciones\\musica.jpg', 'Musica'),
            ('imagenes\\iconos\\aplicaciones\\gestor.jpg', 'Gestor'),
            ('imagenes\\iconos\\aplicaciones\\rendimiento.png', 'Rendimiento'),
            ('imagenes\\iconos\\aplicaciones\\calculadora.jpg', 'Calculadora')
        ]

        # Añadir iconos a la grilla
        row = 0
        col = 0
        for icon_path, name in app_icons:
            icon_frame = QFrame()
            icon_frame.setFixedSize(100, 150)
            icon_layout = QVBoxLayout(icon_frame)
            icon_layout.setAlignment(Qt.AlignCenter)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            button = QPushButton()
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                button.setIcon(QIcon(pixmap))
                button.setIconSize(QSize(80, 80))
            button.setFixedSize(80, 80)
            button.setStyleSheet("border: none;")

            app_label = QLabel(name)
            app_label.setAlignment(Qt.AlignCenter)
            app_label.setStyleSheet("color: white;")

            icon_layout.addWidget(button)
            icon_layout.addWidget(app_label)

            if name == 'Calculadora':
                button.clicked.connect(self.abrir_calculadora)
            elif name == 'Musica':
                button.clicked.connect(self.abrir_reproductor_musica)

            icons_layout.addWidget(icon_frame, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1

        self.showFullScreen()

    def create_taskbar(self, top_layout):
        # Crear frame para la barra de tareas
        self.taskbar_frame = QFrame()
        self.taskbar_frame.setFixedWidth(200)
        self.taskbar_frame.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        self.taskbar_layout = QVBoxLayout(self.taskbar_frame)
        self.taskbar_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.taskbar_layout.setContentsMargins(10, 10, 10, 10)

        top_layout.addWidget(self.taskbar_frame, alignment=Qt.AlignLeft)  # Barra de tareas a la izquierda

    def create_top_right_controls(self, top_layout):
        # Crear frame para reloj, batería y botón de apagado
        top_right_frame = QFrame()
        top_right_frame.setFixedHeight(100)
        top_right_layout = QHBoxLayout(top_right_frame)
        top_right_layout.setContentsMargins(0, 0, 10, 0)
        top_right_layout.setAlignment(Qt.AlignRight)  # Alinear el layout a la derecha

        # Agregar reloj
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("color: white; font-size: 18px;")
        top_right_layout.addWidget(self.clock_label, alignment=Qt.AlignRight)  # Alinear el reloj a la derecha

        # Agregar porcentaje de batería
        self.battery_label = QLabel()
        self.battery_label.setStyleSheet("color: white; font-size: 14px;")
        top_right_layout.addWidget(self.battery_label, alignment=Qt.AlignRight)  # Alinear la batería a la derecha

        # Agregar botón de apagado
        shutdown_button = QPushButton()
        shutdown_button.setIcon(QIcon('imagenes\\iconos\\aplicaciones\\apagado.png'))
        shutdown_button.setIconSize(QSize(32, 32))
        shutdown_button.clicked.connect(self.shutdown_system)
        shutdown_button.setStyleSheet("border: none;")
        top_right_layout.addWidget(shutdown_button, alignment=Qt.AlignRight)  # Alinear el botón de apagado a la derecha

        # Añadir los controles del reloj y batería al layout superior
        top_layout.addWidget(top_right_frame, alignment=Qt.AlignRight)

        # Temporizador para actualizar reloj y batería
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_top_right_info)
        self.timer.start(1000)
        self.update_top_right_info()

    def abrir_calculadora(self):
        # Mostrar calculadora
        if 'Calculadora' not in self.active_apps:
            self.calculadora = Calculadora()
            self.calculadora.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            self.calculadora.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\calculadora.jpg'))
            self.calculadora.show()
            self.add_to_taskbar('Calculadora', 'imagenes\\iconos\\aplicaciones\\calculadora.jpg', self.calculadora)
        else:
            self.calculadora.showNormal()
            self.calculadora.activateWindow()

    def abrir_reproductor_musica(self):
        # Mostrar reproductor de música
        if 'Musica' not in self.active_apps:
            self.reproductor = MusicPlayer()
            self.reproductor.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            self.reproductor.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\musica.jpg'))
            self.reproductor.show()
            self.add_to_taskbar('Musica', 'imagenes\\iconos\\aplicaciones\\musica.jpg', self.reproductor)
        else:
            self.reproductor.showNormal()
            self.reproductor.activateWindow()

    def add_to_taskbar(self, app_name, icon_path, app_window):
        if app_name not in self.active_apps:
            button = QPushButton()
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(40, 40))
            button.setStyleSheet("border: none;")
            button.clicked.connect(app_window.showNormal)  # Mostrar la aplicación al hacer clic
            button.clicked.connect(app_window.activateWindow)  # Activar la ventana
            self.taskbar_layout.addWidget(button)
            self.active_apps[app_name] = app_window  # Añadir la aplicación a las activas


    def update_top_right_info(self):
        # Actualizar reloj
        col_time_zone = QTimeZone(-18000)
        current_time = QDateTime.currentDateTime().toTimeZone(col_time_zone)
        self.clock_label.setText(current_time.toString('HH:mm:ss'))

        # Actualizar porcentaje de batería
        battery = psutil.sensors_battery()
        if battery:
            self.battery_label.setText(f"Batería: {battery.percent}%")

    def shutdown_system(self):
        # Apagar el sistema
        sys.exit(0)

    def resizeEvent(self, event):
        self.fondo.setGeometry(self.rect())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()


def main():
    app = QApplication(sys.argv)
    desktop = DesktopWindow()
    desktop.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
