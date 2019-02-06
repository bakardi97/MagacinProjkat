from PySide2 import QtWidgets
from PySide2 import QtGui
from ..hala_model import HalaModel
from .dialogs.dialog import Dialog

class HalaWidget(QtWidgets.QWidget):
    """
    Klasa koja predstavlja widget za vodjenje hale.
    """
    def __init__(self, name, parent=None):
        """
        Inicijalizator widgeta za vodjenje hale.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self._name = name
        self._parent = parent
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.back = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/arrow-curve-180-left.png"), "&Nazad")        
        self.add_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "&Dodaj proizvod", self)
        self.change_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/pencil.png"), "&Izmijeni proizvod", self)
        self.remove_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "&Ukloni proizvod", self)
        self.stanje_hale = QtWidgets.QProgressBar(self)
        self.hbox_layout.addWidget(self.back)
        self.hbox_layout.addWidget(self.add_button)
        self.hbox_layout.addWidget(self.change_button)
        self.hbox_layout.addWidget(self.remove_button)
        self.hbox_layout.addWidget(self.stanje_hale)
        self.stanje_hale.setStyleSheet("::chunk {"
                    "background-color: green;"
                    "width: 10px;"
                    "margin: 0.5px;}")
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.back.clicked.connect(self._on_back)
        self.add_button.clicked.connect(self._on_add)
        self.change_button.clicked.connect(self._on_change)
        self.remove_button.clicked.connect(self._on_remove)

        parent.vbox_layout.addLayout(self.hbox_layout)
        parent.vbox_layout.addWidget(self.table_view)

        parent.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):
        """
        Postavlja novi model na tabelarni prikaz.

        :param model: model koji se prikazuje u tabeli.
        :type model: HalaModel
        """
        self.table_view.setModel(model)

    def _open(self):
        """
        Metoda koja se poziva prilikom pokretanja aplikacije.
        """
        if(self._name is not None):
            self.set_model(HalaModel("plugins/aleksandar_babic_magacin/"+self._name+".csv"))
        self._set_stanje()


    def _on_add(self):
        """
        Metoda koja se poziva na klik dugmeta add.
        Otvara dijalog sa formom za dodavanje proizvoda u halu.
        """
        dialog = Dialog().getAddProizvodDialog(self._name, self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ind = self.table_view.model().add(dialog.get_data())
            data = dialog.get_data()
            if(ind[0] == -1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Nedovoljno mesta u hali!")
                message.setInformativeText("Maksimalna kolicina koju je moguce dodati je: "+str(ind[1]))
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add()
            elif(ind[0] == 1):
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Neodgovarajuci tip proizvoda!")
                tip = ""
                if((int)(data["proizvod"][1])>=-10 and (int)(data["proizvod"][1])<=0):
                    tip = "Zamrzavanje"
                elif((int)(data["proizvod"][1])>=1 and (int)(data["proizvod"][1])<=18):
                    tip = "Rashladna"
                else:
                    tip = "Sobna temperatura"
                message.setInformativeText("Izabrani tip proizvoda: "+tip)
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_add()
            elif(ind[0] == 0):
                self._set_stanje()
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspesno dodavanje proizvoda!")
                message.setWindowTitle("Obavestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def _on_change(self):
        """
        Metoda koja se poziva na klik dugmeta change.
        Otvara dijalog sa formom za izmjenu proizvoda u hali.
        """
        index = sorted(set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index)==0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedan proizvod nije izabran!")
            message.setInformativeText("Izaberite jedan proizvod koji zelite da izmenite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        dialog = Dialog().getChangeProizvodDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_view.model().change(self.table_view.selectedIndexes(), dialog.get_data(), self._name)
            self._set_stanje()
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Uspesna izmena proizvoda!")
            message.setWindowTitle("Obavjestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

    def _on_remove(self):
        """
        Metoda koja se poziva na klik dugmeta remove.
        Otvara dijalog sa formom za uklanjanje proizvoda iz hale.
        """
        index = sorted(set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index)==0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedan proizvod nije izabran!")
            message.setInformativeText("Izaberite jedan proizvod koji zelite da ukonite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        elif(len(index)>1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Izabrano je vise od jednog proizvoda!")
            message.setInformativeText("Izaberite samo jedan proizvod koji zelite da ukonite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        dialog = Dialog().getRemoveProizvodDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            ind = self.table_view.model().remove(self.table_view.selectedIndexes(), dialog.get_data(), self._name)
            if(ind == -1):
                self._set_stanje()
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspijesno uklanjanje proizvoda!")
                message.setWindowTitle("Obavjestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
            else:
                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Critical)
                message.setText("Nedovoljno proizvoda u hali!")
                message.setInformativeText("Maksimalna kolicina koju je moguce ukloniti je: "+ind)
                message.setWindowTitle("Greska")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()
                self._on_remove()

    def _on_back(self):
        """
        Metoda koja se poziva na klik dugmeta back.
        Vraca nas u magacin.
        """
        self._parent.unfill(self._parent.vbox_layout)
        self._parent.set_layout()

    def _set_stanje(self):
        """
        Metoda koja postavlja stanje hale (zauzetost).
        """
        stanje = self.table_view.model().get_stanje(self._name)
        self.stanje_hale.setValue(stanje)