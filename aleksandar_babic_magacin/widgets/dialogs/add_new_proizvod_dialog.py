from PySide2 import QtWidgets

class AddNewProizvodDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje novog proizvoda.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za dodavanje novog proizvoda.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj novi proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit(self)
        self.temp_input = QtWidgets.QSpinBox(self)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.temp_input.setMinimum(-10)
        self.temp_input.setMaximum(25)
        self.temp_input.setSingleStep(1)

        self.form_layout.addRow("Naziv:", self.name_input)
        self.form_layout.addRow("Temperatura na kojoj se cuva:", self.temp_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo provjerava popunjenost forme. Ukoliko neko polje nije popunjeno korisniku se 
        prikazuje upozorenje.
        """
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provjera naziva", "Naziv mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return
        self.accept()

    def get_data(self):
        """
        Dobavlja podatke iz forme.

        :returns: dict -- rjecnik s podacima iz forme.
        """
        return {
            "name": self.name_input.text(),
            "temperature": self.temp_input.value(),
        }
    



