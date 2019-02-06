from PySide2 import QtWidgets

class RemoveProizvodDialog(QtWidgets.QDialog):
    """
    Dijalog za uklanjanje proizvoda iz hale.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za uklanjanje proizvoda iz hale.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Ukloni proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.quantity_input = QtWidgets.QSpinBox(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setSingleStep(1)

        self.form_layout.addRow("Kolicina:", self.quantity_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def get_data(self):
        """
        Dobavlja podatke iz forme.
        """
        return (int)(self.quantity_input.text())
        
    



