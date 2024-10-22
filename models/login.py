from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon, QRegion
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTimeZone, QSize, QRect
import sys
import os
from models.escritorio import DesktopWindow  # Importar DesktopWindow desde escritorio.py

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        # Crear QLabel para la imagen de fondo
        self.fondo = QLabel(self)
        pixmap = QPixmap('imagenes\\bloqueo.jpg')

        if pixmap.isNull():
            print("Error: No se pudo cargar la imagen.")
        else:
            self.fondo.setPixmap(pixmap)
            self.fondo.setScaledContents(True)
            self.fondo.setGeometry(self.rect())

        # Enviar el fondo al nivel más bajo
        self.fondo.lower()

        # Asegúrate de que la imagen de fondo sea siempre redimensionada con la ventana
        self.setFixedSize(1024, 768)  # Establece el tamaño fijo para evitar distorsión
        self.setStyleSheet("background-color: #f0f0f0;")  # Color de fondo de la ventana, para contraste

        self.perfiles = {
            'Bonee': {'icon': 'imagenes\\iconos\\usuarios\\bone.jpg', 'password': '1234'},
            'Jineth': {'icon': 'imagenes\\iconos\\usuarios\\jineth.jpg', 'password': 'abcd'},
            'Luk': {'icon': 'imagenes\\iconos\\usuarios\\luk.jpg', 'password': '0000'},
            'Rafa': {'icon': 'imagenes\\iconos\\usuarios\\rafa.jpg', 'password': '4444'}
        }

        self.showFullScreen()



        self.selected_profile = None

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # Reloj grande centrado en la parte superior
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("font-size: 50px; padding: 10px; color: white; background-color: rgba(255, 255, 255, 0);")
        #self.clock_label.setStyleSheet("font-size: 48px; color: white;")
        self.clock_label.setAlignment(Qt.AlignCenter)  # Centra el reloj en la pantalla
        main_layout.addWidget(self.clock_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        # Contenedor para la parte central del login
        central_frame = QFrame()
        central_frame.setFrameShape(QFrame.StyledPanel)
        central_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 20px;
                padding: 20px;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.8);
            }
        """)  # Caja redondeada y semitransparente
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignCenter)
        central_frame.setLayout(central_layout)
        main_layout.addWidget(central_frame)

        # Añadir el icono del perfil seleccionado
        self.profile_icon = QLabel(self)
        pixmap_icon = QPixmap('imagenes\\iconos\\usuarios\\usuario_default.png')  # Icono de perfil genérico
        self.profile_icon.setPixmap(pixmap_icon)
        self.profile_icon.setAlignment(Qt.AlignCenter)
        self.profile_icon.setFixedSize(100, 100)
        central_layout.addWidget(self.profile_icon)

        # Nombre de usuario (se actualizará al seleccionar)
        self.username_label = QLabel("Nombre de Usuario")
        self.username_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.username_label.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(self.username_label)

        # Campo de contraseña
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Ingrese su contraseña")
        self.pass_input.setFixedSize(300, 40)
        self.pass_input.setEnabled(False)
        self.pass_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 18px;
                border: 2px solid white;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        central_layout.addWidget(self.pass_input, alignment=Qt.AlignCenter)

        # Botón de login
        self.login_button = QPushButton('Iniciar Sesión')
        self.login_button.setEnabled(False)
        self.login_button.setFixedSize(300, 40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 122, 204, 0.8);
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 90, 158, 0.8);
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        central_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.pass_input.returnPressed.connect(self.check_login)

        # Crear botones de perfiles
        self.create_profile_buttons(central_layout)

        # Botones de "Sleep", "Restart", "Shutdown"
        self.create_system_buttons(main_layout)

        # Temporizador para actualizar el reloj
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.update_clock()
        self.showFullScreen()

    def create_profile_buttons(self, parent_layout):
        profiles_layout = QHBoxLayout()
        profiles_layout.setAlignment(Qt.AlignCenter)
        parent_layout.addLayout(profiles_layout)

        self.profile_buttons = {}

        for perfil, datos in self.perfiles.items():
            profile_widget = QVBoxLayout()

            button = QPushButton()
            pixmap = QPixmap(datos['icon']).scaled(100, 100, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            # Crear una máscara circular
            mask = QRegion(QRect(0, 0, 100, 100), QRegion.Ellipse)
            button.setMask(mask)

            # Aplicar la imagen
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(100, 100)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, p=perfil: self.select_profile(p))

            label = QLabel(perfil)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white;")

            profile_widget.addWidget(button)
            profile_widget.addWidget(label)
            profiles_layout.addLayout(profile_widget)

            self.profile_buttons[perfil] = button

    def create_system_buttons(self, main_layout):
        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """

        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(bottom_buttons_layout)

        # Botón de Sleep
        self.sleep_button = QPushButton('Sleep')
        self.sleep_button.setFixedSize(100, 40)
        self.sleep_button.setStyleSheet(button_style)
        self.sleep_button.clicked.connect(self.sleep_system)
        bottom_buttons_layout.addWidget(self.sleep_button)

        # Botón de Restart
        self.restart_button = QPushButton('Restart')
        self.restart_button.setFixedSize(100, 40)
        self.restart_button.setStyleSheet(button_style)
        self.restart_button.clicked.connect(self.restart_system)
        bottom_buttons_layout.addWidget(self.restart_button)

        # Botón de Shutdown
        self.shutdown_button = QPushButton('Shutdown')
        self.shutdown_button.setFixedSize(100, 40)
        self.shutdown_button.setStyleSheet(button_style)
        self.shutdown_button.clicked.connect(self.shutdown_system)
        bottom_buttons_layout.addWidget(self.shutdown_button)

    def select_profile(self, perfil):
        self.selected_profile = perfil

        for p, btn in self.profile_buttons.items():
            if p == perfil:
                btn.setStyleSheet("border: 2px solid blue;")
                btn.setChecked(True)
            else:
                btn.setStyleSheet("")
                btn.setChecked(False)

        perfil_datos = self.perfiles[perfil]
        self.username_label.setText(perfil)  # Actualizar el nombre de usuario
        pixmap_icon = QPixmap(perfil_datos['icon']).scaled(100, 100, Qt.KeepAspectRatioByExpanding,
                                                           Qt.SmoothTransformation)
        self.profile_icon.setPixmap(pixmap_icon)

        self.pass_input.setEnabled(True)
        self.login_button.setEnabled(True)
        self.pass_input.setFocus()

    def check_login(self):
        if not self.selected_profile:
            QMessageBox.warning(self, 'Error', 'Por favor, selecciona un perfil.')
            return

        contrasena = self.pass_input.text().strip()

        if not contrasena:
            QMessageBox.warning(self, 'Error', 'Por favor, completa el campo de contraseña.')
            return

        perfil_datos = self.perfiles[self.selected_profile]
        if perfil_datos['password'] == contrasena:
            self.open_desktop()
        else:
            QMessageBox.warning(self, 'Login Fallido', 'Contraseña incorrecta.')

    def open_desktop(self):
        self.close()
        self.desktop_window = DesktopWindow()
        self.desktop_window.showFullScreen()

    def update_clock(self):
        col_time_zone = QTimeZone(b"America/Bogota")
        current_time = QDateTime.currentDateTime()  # Obtener la hora actual sin zona horaria
        current_time = current_time.toTimeZone(col_time_zone)  # Convertirla a la zona horaria deseada
        self.clock_label.setText(current_time.toString("hh:mm:ss"))

    def sleep_system(self):
        if sys.platform == 'win32':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif sys.platform == 'linux':
            os.system("systemctl suspend")
        elif sys.platform == 'darwin':
            os.system("osascript -e 'tell application \"System Events\" to sleep'")

    def restart_system(self):
        if sys.platform == 'win32':
            os.system("shutdown /r /t 0")
        elif sys.platform == 'linux':
            os.system("reboot")
        elif sys.platform == 'darwin':
            os.system("osascript -e 'tell app \"System Events\" to restart'")

    def shutdown_system(self):
        if sys.platform == 'win32':
            os.system("shutdown /s /t 0")
        elif sys.platform == 'linux':
            os.system("poweroff")
        elif sys.platform == 'darwin':
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
    def resizeEvent(self, event):
        # Redimensionar la imagen de fondo cuando cambie el tamaño de la ventana
        self.fondo.setGeometry(self.rect())
        self.fondo.lower()  # Asegurar que el fondo siempre esté detrás

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
