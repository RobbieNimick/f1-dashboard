import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from api.f1api import get_driver_standings, get_last_race_results
from PyQt5.QtGui import QColor, QBrush

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("F1 Dashboard")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.load_data)
        layout.addWidget(self.refresh_button)

        self.driver_table = QTableWidget()
        self.race_table = QTableWidget()

        self.tabs.addTab(self.driver_table, "Drivers")
        self.tabs.addTab(self.race_table, "Last Race")

        self.load_data()

    def load_data(self):
        self.refresh_button.setText("Loading...")
        self.refresh_button.setEnabled(False)

        drivers = get_driver_standings()
        self.populate_driver_table(drivers)

        results = get_last_race_results()
        self.populate_race_table(results)

        self.refresh_button.setText("Refresh Data")
        self.refresh_button.setEnabled(True)

    def populate_driver_table(self, drivers):
        self.driver_table.setColumnCount(3)
        self.driver_table.setHorizontalHeaderLabels(["Number", "Name", "Team"])
        self.driver_table.setRowCount(len(drivers))

        for row, driver in enumerate(drivers):
            self.driver_table.setItem(row, 0, QTableWidgetItem(str(driver.get("driver_number", ""))))
            self.driver_table.setItem(row, 1, QTableWidgetItem(driver.get("full_name", "")))
            self.driver_table.setItem(row, 2, QTableWidgetItem(driver.get("team_name", "")))
        
            colour = driver.get("team_colour", "FFFFFF")
            for col in range(3):
                item = self.driver_table.item(row, col)
                if item:
                    item.setBackground(QBrush(QColor(f"#{colour}")))

        self.driver_table.horizontalHeader().setStretchLastSection(True)
        self.driver_table.setEditTriggers(QTableWidget.NoEditTriggers)

    def populate_race_table(self, results):
        self.race_table.setColumnCount(3)
        self.race_table.setHorizontalHeaderLabels(
        ["Position", "Driver", "Team"])
        self.race_table.setRowCount(len(results))

        for row, result in enumerate(results):
            self.race_table.setItem(row, 0, QTableWidgetItem(str(result.get("position", ""))))
            self.race_table.setItem(row, 1, QTableWidgetItem(result.get("full_name", "")))
            self.race_table.setItem(row, 2, QTableWidgetItem(result.get("team_name", "")))

        self.race_table.horizontalHeader().setStretchLastSection(True)
        self.race_table.setEditTriggers(QTableWidget.NoEditTriggers)