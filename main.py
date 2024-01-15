from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QCheckBox, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QFileDialog, QMessageBox
import csv
import subprocess
import sys
import os
import threading
import paramiko
import csv
import shutil
import tempfile
import re
import glob
#import qdarkstyle
from PyQt6.QtGui import QPalette, QColor, QStandardItemModel, QIcon, QBrush
from lista2 import MultiSelectComboBox, MainWindow
from datetime import datetime
current_date = datetime.now().strftime('%Y-%m-%d')


#123

# Run the update script and pass the path to spawaczka.exe as an argument
#subprocess.Popen([sys.executable, 'update.py'])


script_directory = os.path.dirname(os.path.abspath(__file__))
temp_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))






class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Nazwa", "PB_SERWIS", "WEW", "ZEW", "POB", "BAZA", "TERM"])
        self.setSortingEnabled(True)

    def add_row(self, nazwa, serwis, wew, zew, pob, baza, term):
        row_count = self.rowCount()
        self.setRowCount(row_count + 1)

        # Create QTableWidgetItem objects for each cell
        item_nazwa = QTableWidgetItem(nazwa)
        item_serwis = QTableWidgetItem(serwis)
        item_wew = QTableWidgetItem(wew)
        item_zew = QTableWidgetItem(zew)
        item_pob = QTableWidgetItem(pob)
        item_baza = QTableWidgetItem(baza)
        item_term = QTableWidgetItem(term)

        # Set the background color for cells with "BLAD" value
        if nazwa == "BLAD":
            item_nazwa.setBackground(QColor("yellow"))
        if serwis == "BLAD":
            item_serwis.setBackground(QColor("yellow"))
        if wew == "BLAD":
            item_wew.setBackground(QColor("yellow"))
        if zew == "BLAD":
            item_zew.setBackground(QColor("yellow"))
        if pob == "BLAD":
            item_pob.setBackground(QColor("yellow"))
        if baza == "BLAD":
            item_baza.setBackground(QColor("yellow"))
        if term == "BLAD":
            item_term.setBackground(QColor("yellow"))
        # Add the QTableWidgetItem objects to the table widget
        self.setItem(row_count, 0, item_nazwa)
        self.setItem(row_count, 1, item_serwis)
        self.setItem(row_count, 2, item_wew)
        self.setItem(row_count, 3, item_zew)
        self.setItem(row_count, 4, item_pob)
        self.setItem(row_count, 5, item_baza)
        self.setItem(row_count, 6, item_term)









class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        Dialog.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)  # Add minimize button
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QRadioButton(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(80, 10, 100, 17)) #wszystkie
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setChecked(True)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(80, 200, 200, 40)) #lista programow
        self.comboBox.setObjectName("comboBox")
        self.passwordLineEdit = QtWidgets.QLineEdit(Dialog)
        self.passwordLineEdit.setGeometry(QtCore.QRect(80, 250, 200, 25)) #password
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.commandTextEdit = QtWidgets.QTextEdit(Dialog)
        self.commandTextEdit.setGeometry(QtCore.QRect(400, 400, 750, 200))  #commands
        self.commandTextEdit.setObjectName("commandTextEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(280, 250, 100, 25)) #send
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushit)
        self.checkBox_2 = QtWidgets.QRadioButton(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(80, 40, 100, 17)) #komis
        self.checkBox_2.setObjectName("checkBox_2")
        self.consoleTextEdit = QtWidgets.QTextEdit(Dialog)
        self.consoleTextEdit.setGeometry(QtCore.QRect(400, 600, 750, 150)) #consle
        self.consoleTextEdit.setObjectName("consoleTextEdit")
        self.clearConsoleButton = QtWidgets.QPushButton(parent=Dialog)
        self.clearConsoleButton.setGeometry(QtCore.QRect(280, 475, 100, 25)) #clear console
        self.clearConsoleButton.setObjectName("clearConsoleButton")
        self.clearConsoleButton.setText("Clear Console")
        
        self.clearCommand = QtWidgets.QPushButton(parent=Dialog)
        self.clearCommand.setGeometry(QtCore.QRect(280, 450, 100, 25)) #clear commands
        self.clearCommand.setObjectName("clearCommand")
        self.clearCommand.setText("Clear Commands")
        
        
        

        self.checkBox_3 = QtWidgets.QRadioButton(Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(80, 70, 100, 17)) #inne
        self.checkBox_3.setObjectName("checkBox_3")        
        self.checkBox_3.clicked.connect(self.toggle_lista2)
        
        self.ListaPole = QtWidgets.QTextEdit(Dialog)
        self.ListaPole.setGeometry(QtCore.QRect(80, 300, 200, 200))  # lista wybranych firm
        self.ListaPole.setObjectName("ListaPole")
        self.ListaPole.setReadOnly(True)

        self.tableWidget = TableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(400, 30, 750, 350))  # Adjust the geometry as needed
        self.tableWidget.setObjectName("tableWidget")

        self.QLabel = QtWidgets.QLabel(Dialog)
        self.QLabel.setGeometry(QtCore.QRect(80, 170, 100, 20))  #lista programow nazwa
        self.QLabel.setObjectName("Opis1")
        
        
        
        self.ncom = QtWidgets.QLabel(Dialog)
        self.ncom.setGeometry(QtCore.QRect(400, 380, 100, 20))  #nazwa commands
        self.ncom.setObjectName("comm")

        self.clearConsoleButton.clicked.connect(self.clear_console)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.clearCommand.clicked.connect(self.clear_command)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.comboBox.addItem("check version")
        self.comboBox.addItem("check_size")
        self.comboBox.addItem("aktualizator")
        self.comboBox.addItem("aktualizator bez dmp")
        self.comboBox.addItem("insert csv")
        self.comboBox.addItem("update csv")
        self.comboBox.addItem("update in csv")
        self.comboBox.addItem("rob")


        self.browseButton = QtWidgets.QPushButton(Dialog)
        self.browseButton.setGeometry(QtCore.QRect(280, 300, 100, 25))
        self.browseButton.setObjectName("browseButton")
        self.browseButton.setText("Browse CSV")
        self.browseButton.clicked.connect(self.browse_csv)


        self.sql = QtWidgets.QPushButton(Dialog)
        self.sql.setGeometry(QtCore.QRect(280, 325, 100, 25))
        self.sql.setObjectName("sql")
        self.sql.setText("SQL")
        self.sql.clicked.connect(self.open_name_input_dialog)



        self.prefiks = QtWidgets.QPushButton(Dialog)
        self.prefiks.setGeometry(QtCore.QRect(280, 350, 100, 25))
        self.prefiks.setObjectName("prefiks")
        self.prefiks.setText("Prefiksy")
        self.prefiks.clicked.connect(self.runprefiksy)



    def open_name_input_dialog(self):
        entered_name, ok = QtWidgets.QInputDialog.getText(
            None, "Enter Name", "Enter the name:"
        )

        if ok:
            self.runsql(entered_name)




    def browse_csv(self):
        self.input_file = ""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_name, _ = file_dialog.getOpenFileName(self.browseButton, "Open CSV or TXT File", "", "CSV Files (*.csv);;TXT Files (*.txt)")

        if file_name:
            self.input_file = file_name


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Spawaczka 0.7b"))
        self.checkBox.setText(_translate("Dialog", "wszystkie"))
        self.pushButton.setText(_translate("Dialog", "SEND"))
        self.checkBox_2.setText(_translate("Dialog", "komis"))
        self.QLabel.setText(_translate("Dialog", "Lista programów:"))  # Corrected object name to self.QLabel
        self.checkBox_3.setText(_translate("Dialog", "inne"))
        self.ncom.setText(_translate("Dialog", "Commands to run:"))       


    def execute_selected_program(self):
        selected_item = self.comboBox.currentText()
        password = self.passwordLineEdit.text()
        commands_text = self.commandTextEdit.toPlainText()
        commands = commands_text.split('\n')
        commands = [command.strip() for command in commands if command.strip()]
        


        if self.checkBox.isChecked():  # wszystkie
            settings_file = "settings.txt"
        elif self.checkBox_2.isChecked():  # komis
            settings_file = "settings_komis.txt"
        elif self.checkBox_3.isChecked():  # inne
            settings_file = "inne.txt"
        else:
            return  # No option selected







        if selected_item == "insert csv":
            self.insert_csv()
        elif selected_item == "update csv":
            if self.input_file:
                self.update_csv(self.input_file)
            else:
                self.consoleTextEdit.append("Error: Please select a CSV file.")
        elif selected_item == "update in csv":
            if self.input_file:
                self.update_in_csv(self.input_file)
            else:
                self.consoleTextEdit.append("Error: Please select a CSV file.")
        else:
            #self.consoleTextEdit.append("No option selected.")  # Handle the case when no option is selected

            if not password:
                self.consoleTextEdit.append("Please enter a password before executing the program.")
                return


            # Verify if the password is correct by attempting to connect to the first server
            if self.verify_password(password, settings_file):
                try:
                    if selected_item == "check_size":
                        self.run_check_size(password)
                    elif selected_item == "aktualizator":
                        self.aktualizator(password, settings_file)
                    elif selected_item == "aktualizator bez dmp":
                        self.aktualizator2(password, settings_file)
                    elif selected_item == "check version":
                        self.check_version(password, settings_file)
                    elif selected_item == "rob":
                        self.run_rob_command(password, commands, settings_file)
                except Exception as e:
                    self.consoleTextEdit.append(f"Error occurred: {str(e)}")
            else:
                self.consoleTextEdit.append("Invalid password. Please enter a correct password.")


    def verify_password(self, password, settings_file):
        try:
            # Read the server information from the settings file and attempt to connect to the first server
            settings_file_path = os.path.join(script_directory, settings_file)
            with open(settings_file_path, 'r', encoding='utf-8') as settings:
                lines = settings.readlines()
                if lines:
                    server = {}
                    for line in lines:
                        line = line.strip()
                        if line.startswith("name"):
                            server['name'] = line.split('=')[1]
                        elif line.startswith("ip"):
                            server['ip'] = line.split('=')[1]
                        elif line.startswith("port"):
                            server['port'] = int(line.split('=')[1])
                            break

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(server['ip'], port=server['port'], username='root', password=password)
                    ssh.close()

                    return True  # Connection successful, password is correct
        except paramiko.AuthenticationException:
            pass  # Authentication failed, continue to return False
        except Exception:
            pass  # Other exceptions, continue to return False

        return False  # Password is incorrect or connection failed


    def pushit(self):
        selected_item = self.comboBox.currentText()
        self.consoleTextEdit.append(f"Script starting for {selected_item}...")

        # Perform the selected program execution in a separate thread
        script_thread = threading.Thread(target=self.execute_selected_program)
        script_thread.start()


    def runsql(self, entered_name):
        if not entered_name:
            self.consoleTextEdit.append("Please enter a name.")
            return

        self.commandTextEdit.append(f"rm {entered_name}.sql")
        self.commandTextEdit.append(f"wget http://repo.moto-profil.pl/{entered_name}.sql")
        self.commandTextEdit.append(f"psql -U postgres -d pgpb -q -f {entered_name}.sql")



    def runprefiksy(self):
        self.commandTextEdit.append(f"cp /home/samba/Pobieraczka/Pobieraczka.sh /home/samba/Pobieraczka/prefiks.sh")
        self.commandTextEdit.append(f"chmod 777 /home/samba/Pobieraczka/prefiks.sh")
        self.commandTextEdit.append(f"cp /home/samba/Pobieraczka/konfiguracja.xml /home/samba/Pobieraczka/prefiks.xml")
        self.commandTextEdit.append(f"sed -i 's/konfiguracja/prefiks/g' /home/samba/Pobieraczka/prefiks.sh")
        self.commandTextEdit.append(f"sed -i 's#.*<Prefiksy>.*#  <Prefiksy>tutaj|wpisz|prefiks</Prefiksy>#' /home/samba/Pobieraczka/prefiks.xml")
        self.commandTextEdit.append(f"sed -i 's|.*<WszystkiePrefiksy>.*|  <WszystkiePrefiksy>false</WszystkiePrefiksy>|' /home/samba/Pobieraczka/prefiks.xml")
        self.commandTextEdit.append(f"echo -e '00 11 * * * root nice -n 19 /home/samba/Pobieraczka/prefiks.sh' >> /etc/crontab")

        self.commandTextEdit.append(f"===================================================")
        self.commandTextEdit.append(f"ZMIEŃ GODZINIĘ W POWYŻSZYM WPISIE DO CRONA")
        self.commandTextEdit.append(f"===================================================")
        

        self.commandTextEdit.append(f"PO WYKONANIU POBIERACZKI USUŃ WPIS Z CRONA. NIE PUSZCZAĆ TEGO NA RAZ!")
        self.commandTextEdit.append(f"sed -i '/prefiks.sh/d' /etc/crontab")        
        self.commandTextEdit.append(f"===================================================")        
        

    def toggle_lista2(self):
        if self.checkBox_3.isChecked():
            self.run_lista2()
        else:
            self.ListaPole.clear()

    def run_lista2(self):
        try:
            
            lista2_path = os.path.join(temp_dir, 'lista2.py')
            process = subprocess.Popen(["python", lista2_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            output, errors = process.communicate()

            if process.returncode == 0:
                self.ListaPole.setPlainText(output)
            else:
                self.ListaPole.setPlainText(f"Error: {errors}")
        except Exception as e:
            self.ListaPole.setPlainText(str(e))


    def run_check_size(self, password):
        run_check_size_path = os.path.join(temp_dir, 'check_size.py')
        result = subprocess.run(["python", run_check_size_path, "--password", password], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.populate_table_from_size()
        self.consoleTextEdit.append(output_text)  # Append all outputs to consoleTextEdit        

    def aktualizator(self, password, settings_file):
        aktualizator_path = os.path.join(temp_dir, 'aktualizator.py')
        command_args = ["python", aktualizator_path, "--password", password]
        if settings_file:
            command_args += ["--settings", settings_file]

       # subprocess.run(command_args, shell=True)
        result = subprocess.run(command_args, capture_output=True, text=True, shell=True)
        output_text = result.stdout.strip()

        # Append the captured output to consoleTextEdit
        self.consoleTextEdit.append(output_text)


    def aktualizator2(self, password, settings_file):
        aktualizator_path2 = os.path.join(temp_dir, 'aktualizator_bez_dmp.py')
        command_args = ["python", aktualizator_path2, "--password", password]
        if settings_file:
            command_args += ["--settings", settings_file]

       # subprocess.run(command_args, shell=True)
        result = subprocess.run(command_args, capture_output=True, text=True, shell=True)
        output_text = result.stdout.strip()

        # Append the captured output to consoleTextEdit
        self.consoleTextEdit.append(output_text)


            
    def check_version(self, password, settings_file):
    
        check_version_path = os.path.join(temp_dir, 'check_version.py')   
        command_args = ["python", check_version_path, "--password", password]
        if settings_file:
            command_args += ["--settings", settings_file]
        result = subprocess.run(command_args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.consoleTextEdit.append(output_text)  # Append all outputs to consoleTextEdit
        if result.returncode == 0:  # Successful execution
            self.populate_table_from_file()  # Call the method to populate the table

    def run_rob_command(self, password, commands, settings_file):
        rob_path = os.path.join(temp_dir, 'rob.py')  
        command_args = ["python", rob_path, "--password", password]
        if settings_file:
            command_args += ["--settings", settings_file]
        command_args += ["--commands"] + commands
        result = subprocess.run(command_args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.consoleTextEdit.append(output_text)  # Append all outputs to consoleTextEdit

    def insert_csv(self):
        # Get the table name from the commandTextEdit
        command_text = self.commandTextEdit.toPlainText().strip()
        commands = command_text.split("\n")

        if len(commands) > 1:
            self.consoleTextEdit.append("Error: Only one command can be sent to insert_csv.")
            return

        table_name = commands[0].strip()

        if not table_name:
            table_name = "popraw.to"  # Set default table name as "asd.asd" if the command is empty

        if not self.input_file:
            self.consoleTextEdit.append("Error: Please select a CSV file.")
            return

        # Prepare the command arguments to call insert_csv.py
        insert_csv_path = os.path.join(temp_dir, 'insert_csv.py')
        command_args = ["python", insert_csv_path, table_name, self.input_file]
        result = subprocess.run(command_args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.consoleTextEdit.append(output_text)





    def update_csv(self, file_name):
        command_text = self.commandTextEdit.toPlainText().strip()  # Get the command text from the commandTextEdit
        if not command_text:
            self.consoleTextEdit.append("Please enter the table name and primary keys in the command field.")
            return

        # Split the command text into table name and primary keys
        command_parts = command_text.splitlines()
        table_name = command_parts[0]
        primary_keys = "\n".join(command_parts[1:]) if len(command_parts) > 1 else ""

        # Verify if the provided primary keys are headers of the CSV file
        if primary_keys:
            with open(file_name, "r", newline="",  encoding="utf-8") as csv_input:
                csv_reader = csv.DictReader(csv_input, delimiter=";")
                csv_headers = set(csv_reader.fieldnames)
                provided_keys = set(primary_keys.split("\n"))
                if not provided_keys.issubset(csv_headers):
                    self.consoleTextEdit.append("Error: The provided primary keys do not match the headers of the CSV file.")
                    return

        # Prepare the command arguments to call update_csv.py
        update_csv_path = os.path.join(temp_dir, 'update_csv.py')
        command_args = ["python", update_csv_path, table_name, primary_keys, file_name]
        result = subprocess.run(command_args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.consoleTextEdit.append(output_text)



    def update_in_csv(self, file_name):
        command_text = self.commandTextEdit.toPlainText().strip()  # Get the command text from the commandTextEdit
        if not command_text:
            self.consoleTextEdit.append("Please enter the table name and primary keys in the command field.")
            return

        # Split the command text into table name and primary keys
        command_parts = command_text.splitlines()
        table_name = command_parts[0]
        primary_keys = "\n".join(command_parts[1:]) if len(command_parts) > 1 else ""

        # Verify if the provided primary keys are headers of the CSV file
        if primary_keys:
            with open(file_name, "r", newline="",  encoding="utf-8") as csv_input:
                csv_reader = csv.DictReader(csv_input, delimiter=";")
                csv_headers = set(csv_reader.fieldnames)
                provided_keys = set(primary_keys.split("\n"))
                if not provided_keys.issubset(csv_headers):
                    self.consoleTextEdit.append("Error: The provided primary keys do not match the headers of the CSV file.")
                    return

        # Prepare the command arguments to call update_csv.py
        update_in_csv_path = os.path.join(temp_dir, 'update_in_csv.py')
        command_args = ["python", update_in_csv_path , table_name, primary_keys, file_name]
        result = subprocess.run(command_args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        output_text = result.stdout.strip()
        self.consoleTextEdit.append(output_text)











 

    def clear_console(self):
        self.consoleTextEdit.clear()
        
        
    def clear_command(self):
        self.commandTextEdit.clear()


    def populate_table_from_file(self, filename=f"versions/{current_date}_all_output_version.txt"):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        records = []
        record = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Non-empty line
                record.append(stripped_line)
            elif record:  # Empty line indicating the end of a record
                records.append(record)
                record = []
        
        
        # Clear the existing table and disable sorting temporarily
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        
        # Add the last record if it exists
        if record:
            records.append(record)

        record_count = len(records)
        self.tableWidget.setRowCount(record_count)  # Set the row count based on the number of records

        for row_index, record in enumerate(records):
            if len(record) == 7:  # Check if the record has all 6 lines
                nazwa = record[0]
                serwis = record[1]
                wew = record[2]
                zew = record[3]
                pob = record[4]
                baza = record[5]
                term = record[6]
            else:  # Handle incomplete records
                nazwa = record[0] if len(record) > 0 else "BLAD"
                serwis = record[1] if len(record) > 1 else "BLAD"
                wew = record[2] if len(record) > 2 else "BLAD"
                zew = record[3] if len(record) > 3 else "BLAD"
                pob = record[4] if len(record) > 4 else "BLAD"
                baza = record[5] if len(record) > 5 else "BLAD"
                term = record[6] if len(record) > 6 else "BLAD"

            self.tableWidget.add_row(nazwa, serwis, wew, zew, pob, baza, term)





        # Remove any empty rows at the start of the table
        while self.tableWidget.rowCount() > record_count:
            self.tableWidget.removeRow(0)
        # Re-enable sorting for the table after populating
        self.tableWidget.setSortingEnabled(True)


    def populate_table_from_size(self, directory="raport"):
        # Clear the existing table and disable sorting temporarily
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # Get a list of all files in the directory
        files = glob.glob(os.path.join(directory, '*.txt'))

        # Sort the files by modification time to get the most recent one
        files.sort(key=os.path.getmtime, reverse=True)

        # Check if there are any files in the directory
        if not files:
            return

        # Get the most recent file
        filename = files[0]

        # Read the file and extract the values
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        records = []
        record = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Non-empty line
                record.append(stripped_line)
            elif record:  # Empty line indicating the end of a record
                records.append(record)
                record = []

        # Add the last record if it exists
        if record:
            records.append(record)

        # Set the number of rows in the table
        self.tableWidget.setRowCount(len(records))

        # Populate the table with the records
        for row_index, record in enumerate(records):
            if len(record) >= 2:  # Check if the record has at least 2 lines
                nazwa = record[0]
                serwis = re.search(r'\d+%', record[1]).group() if re.search(r'\d+%', record[1]) else "BLAD"
                # Set the values in the table
                self.tableWidget.setItem(row_index, 0, QTableWidgetItem(nazwa))
                self.tableWidget.setItem(row_index, 1, QTableWidgetItem(serwis))
            else:
                # Handle incomplete records by filling with "BLAD"
                self.tableWidget.setItem(row_index, 0, QTableWidgetItem("BLAD"))
                self.tableWidget.setItem(row_index, 1, QTableWidgetItem("BLAD"))

        # Re-enable sorting for the table after populating
        self.tableWidget.setSortingEnabled(True)




if __name__ == "__main__":
    app = QApplication([])
    palette = app.palette()
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(0, 0, 75))
    palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(128, 255, 255))
    app.setPalette(palette)

    icon_file_path = os.path.join(script_directory, "welder.ico")
    app_icon = QIcon(icon_file_path)
    app.setWindowIcon(app_icon)

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)




   # ui.populate_table_from_file()  # Call the method to populate the table
    Dialog.show()

    app.exec()
    
    
