from PyQt5.QtWidgets import (  # type: ignore
    QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QTimer  # type: ignore

class ProcessControlTable(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tabla de Control de Procesos")
        self.setGeometry(150, 150, 600, 400)

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Crear la tabla
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre del Proceso", "Estado", "Acción"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        # Almacenar referencia a DesktopWindow para gestionar procesos
        self.desktop = parent

        # Configurar el temporizador para actualizar la tabla cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

        # Actualizar la tabla inicialmente
        self.update_table()

    def update_table(self):
        # Limpiar tabla existente
        current_processes = self.desktop.running_apps
        self.table.setRowCount(len(current_processes))  # Ajustar el tamaño de la tabla

        # Actualizar los procesos en la tabla
        for index, process in enumerate(current_processes):
            # Nombre del proceso
            name_item = QTableWidgetItem(process['name'])
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(index, 0, name_item)

            # Estado del proceso
            status_item = QTableWidgetItem("En ejecución" if not process['window'].isHidden() else "Detenido")
            status_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(index, 1, status_item)

            # Botón de acción (Alternar)
            btn_toggle = QPushButton("Alternar")
            btn_toggle.clicked.connect(lambda checked, p=process: self.toggle_process(p))
            self.table.setCellWidget(index, 2, btn_toggle)

    def toggle_process(self, process):
        """Alterna el estado de la aplicación entre visible y oculta."""
        if process['window'].isHidden():
            process['window'].show()  # Mostrar si está oculto
        else:
            process['window'].hide()  # Ocultar si está visible

        # Actualizar la tabla después de alternar el estado
        self.update_table()
