from PySide2 import QtWidgets, QtCore

class ChangeProizvodDialog(QtWidgets.QDialog):
    """
    Dijalog za izmjenu proizvoda.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za izmjenu proizvoda.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Izmijeni proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        
        self.date_input = QtWidgets.QDateEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.date_input.setDate(QtCore.QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.form_layout.addRow("Datum isteka roka:", self.date_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def get_data(self):
        """
        Dobavlja podatke iz forme.
        """
        return self.date_input.text()