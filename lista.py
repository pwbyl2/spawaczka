from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLineEdit
import os
import subprocess

class MultiSelectComboBox(QListWidget):
    def __init__(self):
        super().__init__()

        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

    def sizeHint(self):
        width = self.sizeHintForColumn(0) + self.verticalScrollBar().sizeHint().width() + 10
        height = self.sizeHintForRow(0) * self.count() + self.frameWidth() * 2
        return QSize(width, height)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista Kontrahentów")

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create the search box
        search_box = QLineEdit()
        self.search_box = search_box  # Store a reference to the search box
        search_box.textChanged.connect(self.search_items)
        layout.addWidget(search_box)

        # Create the checkmark list
        checkmark_list = MultiSelectComboBox()
        self.checkmark_list = checkmark_list  # Store a reference to the checkmark list
        layout.addWidget(checkmark_list)

        # Parse the settings file and populate the checkmark list with names
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, 'settings.txt')
        with open(settings_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('name'):
                    name = line.split('=')[1]
                    item = QListWidgetItem(name, checkmark_list)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Unchecked)

        # Connect the itemClicked signal to handle_item_clicked slot
        checkmark_list.itemClicked.connect(self.handle_item_clicked)



        def get_selected_options():
            selected_options = []
            for index in range(checkmark_list.count()):
                item = checkmark_list.item(index)
                if item.checkState() == Qt.CheckState.Checked:
                    selected_options.append(item.text())

            # Read the IP and port values for the selected options
            ip = {}
            port = {}
            baza = {}
            with open(settings_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i in range(0, len(lines), 4):
                    name_line = lines[i].strip()
                    ip_line = lines[i + 1].strip()
                    port_line = lines[i + 2].strip()
                    baza_line = lines[i + 3].strip()
                    name = name_line.split('=')[1]
                    ip_value = ip_line.split('=')[1]
                    port_value = port_line.split('=')[1]
                    baza_value = baza_line.split('=')[1]
                    if name in selected_options:
                        ip[name] = ip_value
                        port[name] = port_value
                        baza[name] = baza_value

            # Prepare the data to be saved in the desired format
            data = ""
            for i, option in enumerate(selected_options, start=1):
                name_key = f"name{i}"
                ip_key = f"ip{i}"
                port_key = f"port{i}"
                baza_key = f"baza{i}"
                data += f"{name_key}={option}\n"
                data += f"{ip_key}={ip.get(option, '')}\n"
                data += f"{port_key}={port.get(option, '')}\n"
                data += f"{baza_key}={baza.get(option, '')}\n"

            # Save the data to the file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            inne_file = os.path.join(script_dir, 'inne.txt')
            with open(inne_file, 'w', encoding='utf-8') as file:
                file.write(data)

            # Print the selected options
            for option in selected_options:
                print(option)
            
            self.close()

        # Create a button to get selected options
        wybierz_btn = QPushButton("Wybierz")
        wybierz_btn.clicked.connect(get_selected_options)
        layout.addWidget(wybierz_btn)

        layout_buttons = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_items)
        layout_buttons.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_items)
        layout_buttons.addWidget(deselect_all_btn)

        layout.addLayout(layout_buttons)

    def handle_item_clicked(self, item):
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    def select_all_items(self):
        for index in range(self.checkmark_list.count()):
            item = self.checkmark_list.item(index)
            item.setCheckState(Qt.CheckState.Checked)

    def deselect_all_items(self):
        for index in range(self.checkmark_list.count()):
            item = self.checkmark_list.item(index)
            item.setCheckState(Qt.CheckState.Unchecked)

    def search_items(self, search_query):
        search_text = search_query.lower()
        for index in range(self.checkmark_list.count()):
            item = self.checkmark_list.item(index)
            item_text = item.text().lower()
            item.setHidden(not search_text in item_text)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
