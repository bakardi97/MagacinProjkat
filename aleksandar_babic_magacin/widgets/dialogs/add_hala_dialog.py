from PySide2 import QtWidgets, QtGui

class AddHalaDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje nove hale u magacin.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za dodavanje nove hale u magacin.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj halu")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit(self)
        self.type_input = QtWidgets.QComboBox(self)
        self.type_input.addItem(QtGui.QIcon("resources/icons/weather.png"), "Sobna temperatura")
        self.type_input.addItem(QtGui.QIcon("resources/icons/weather-moon.png"), "Rashladna")
        self.type_input.addItem(QtGui.QIcon("resources/icons/weather-snowflake.png"), "Zamrzavanje")
        self.capacity_input = QtWidgets.QSpinBox(self)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.capacity_input.setMinimum(1)
        self.capacity_input.setMaximum(999999)
        self.capacity_input.setSingleStep(1)

        self.form_layout.addRow("Naziv:", self.name_input)
        self.form_layout.addRow("Tip:", self.type_input)
        self.form_layout.addRow("Kapacitet:", self.capacity_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. Ukoliko neko polje nije popunjeno korisniku se 
        prikazuje upozorenje.
        """
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provera naziva", "Naziv mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return
        self.accept()

    def get_data(self):
        """
        Dobavlja podatke iz forme.

        :returns: dict -- rjecnik s podacima iz forme.
        """
        return {
            "name": self.name_input.text(),
            "type": self.type_input.currentText(),
            "capacity": self.capacity_input.value(),
        }
    



