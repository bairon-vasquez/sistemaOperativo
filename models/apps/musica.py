from PyQt5.QtWidgets import ( # type: ignore
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt, QUrl, QTimer # type: ignore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent # type: ignore
from PyQt5.QtGui import QIcon # type: ignore
import sys


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Reproductor de Música')
        self.setGeometry(300, 300, 600, 400)  # Ventana más grande para un diseño moderno

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Reproductor de medios
        self.player = QMediaPlayer()

        # Etiqueta para mostrar la canción
        self.song_label = QLabel('Ninguna canción seleccionada')
        self.song_label.setAlignment(Qt.AlignCenter)
        self.song_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.song_label)

        # Control de volumen
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Volumen inicial en 50%
        self.volume_slider.valueChanged.connect(self.change_volume)
        layout.addWidget(self.volume_slider)

        # Controles de reproducción con iconos
        controls_layout = QHBoxLayout()
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("archivos\\imagenes\\iconos\\aplicaciones\\musica\\play.png"))  # Agregar íconos de play/pause/stop
        self.play_button.clicked.connect(self.play_music)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon("archivos\\imagenes\\iconos\\aplicaciones\\musica\\pausa.png"))
        self.pause_button.clicked.connect(self.pause_music)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("archivos\\imagenes\\iconos\\aplicaciones\\musica\\stop.png"))
        self.stop_button.clicked.connect(self.stop_music)

        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)
        layout.addLayout(controls_layout)

        # Barra de progreso de la canción
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)  # Permitir que el usuario avance en la canción
        layout.addWidget(self.slider)

        # Tiempo transcurrido y duración
        self.time_label = QLabel('00:00 / 00:00')
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        # Conectar el slider con el progreso de la música
        self.player.positionChanged.connect(self.update_slider)
        self.player.durationChanged.connect(self.update_slider_duration)

        # Botón para abrir archivos de música
        self.open_button = QPushButton('Abrir Archivo de Música')
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        # Temporizador para actualizar el tiempo transcurrido
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo de Música", "", "Archivos de Audio (*.mp3 *.wav *.ogg)")
        if file_name != '':
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.song_label.setText(file_name.split('/')[-1])
            self.play_music()

    def play_music(self):
        self.player.play()
        self.timer.start(1000)  # Actualizar cada segundo

    def pause_music(self):
        self.player.pause()
        self.timer.stop()

    def stop_music(self):
        self.player.stop()
        self.timer.stop()
        self.slider.setValue(0)
        self.time_label.setText('00:00 / 00:00')

    def update_slider(self, position):
        self.slider.setValue(position)

    def update_slider_duration(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

    def update_time(self):
        elapsed_time = self.player.position() // 1000
        duration = self.player.duration() // 1000
        elapsed_str = f'{elapsed_time // 60:02}:{elapsed_time % 60:02}'
        duration_str = f'{duration // 60:02}:{duration % 60:02}'
        self.time_label.setText(f'{elapsed_str} / {duration_str}')

    def change_volume(self, value):
        self.player.setVolume(value)


def main():
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
