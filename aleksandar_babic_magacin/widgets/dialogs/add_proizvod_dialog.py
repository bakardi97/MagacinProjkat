from PySide2 import QtWidgets, QtCore, QtGui
import csv

class AddProizvodDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje proizvoda u halu.
    """
    def __init__(self,name, parent=None):
        """
        Inicijalizator dijaloga za dodavanje proizvoda u halu.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self._hale = []
        self._proizvodi = []
        self.setWindowTitle("Dodaj proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.proizvod_input = QtWidgets.QComboBox(self)
        self.get_all_proizvodi()
        for p in self._proizvodi:
            self.proizvod_input.addItem(p[0])
        self.quantity_input = QtWidgets.QSpinBox(self)
        self.hala = name
        self.hala_input = QtWidgets.QLabel(self)
        self.get_all_hale()
        self.hala_input.setText(name)
        self.date_input = QtWidgets.QDateEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setSingleStep(1)

        self.date_input.setDate(QtCore.QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.form_layout.addRow("Proizvod:", self.proizvod_input)
        self.form_layout.addRow("Kolicina:", self.quantity_input)
        self.form_layout.addRow("Hala:", self.hala_input)
        self.form_layout.addRow("Datum isteka roka:", self.date_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def get_data(self):
        """
        Dobavlja podatke iz forme.

        :returns: dict -- rjecnik s podacima iz forme.
        """
        proizvod = None
        hala = None
        for p in self._proizvodi:
            if(p[0] == self.proizvod_input.currentText()):
                proizvod = p
        for h in self._hale:
            if(h[0] == self.hala):
                hala = h
        return {
            "proizvod": proizvod,
            "kolicina": self.quantity_input.text(),
            "hala": hala,
            "datum": self.date_input.text(),
        }

    def get_all_hale(self):
        """
        Ucitava sve hale iz CSV datoteke uz pomoc CSV reader-a.
        Pomocna metoda nase klase.
        """
        with open("plugins/aleksandar_babic_magacin/magacin.csv", "r", encoding="utf-8") as fp:
            self._hale = list(csv.reader(fp, dialect=csv.unix_dialect))

    def get_all_proizvodi(self):
        """
        Ucitava sve proizvode iz CSV datoteke uz pomoc CSV reader-a.
        Pomocna metoda nase klase.
        """
        with open("plugins/aleksandar_babic_magacin/proizvodi.csv", "r", encoding="utf-8") as fp:
            self._proizvodi = list(csv.reader(fp, dialect=csv.unix_dialect))