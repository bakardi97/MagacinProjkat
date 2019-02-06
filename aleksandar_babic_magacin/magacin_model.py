from PySide2 import QtCore
from .hala_model import HalaModel
import csv
import os

class MagacinModel(QtCore.QAbstractTableModel):
    """
    Klasa koja predstavlja specijalizaciju QAbstractTableModel-a.
    Koristimo tabelarni model jer cemo podatke posmatrati kao tabelu, i u tabeli ih prikazivati.
    Svaki tabelarni model ima redove i kolone. Red je jedna hala u magacinu, a kolone predstavalju
    pojedinacne podatke o svakoj hali (naziv, tip i kapacitet).
    Datoteka na osnovu koje se populise model je CSV datoteka, gde su redovi modela zapravo redovi
    iz datoteke, a kolone modela su podaci koji su u redu u datoteci odvojeni separatorom (zarezom).
    """
    def __init__(self, path=""):
        """
        Inicijalizator modela za magacin.
        Pri inicijalizaciji se na osnovu datoteke sa putanje path ucitavaju i populise se model.
        :param path: putanja do datoteke u kojoj su smjesteni podaci.
        :type path: str
        """
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o hali iz magacina
        self._data = []
        self.load_data(path)

    def rowCount(self, index):
        """
        Vraca broj redova u modelu.
        :param index: putanja do datoteke u kojoj su smjesteni podaci.
        :type index: QModelIndex
        :returns: int -- broj redova modela.
        """
        return len(self._data)

    def columnCount(self, index):
        """
        Vraca broj kolona u modelu. Posto znamo da je nasa hala iz magacina opisana sa tri
        podatka, vracamo fiksni broj kolona na osnovu datoteke.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: int -- broj kolona modela.
        """
        return 3

    def data(self, index, role):
        """
        Vraca podatak smesten na datom indeksu sa datom ulogom.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :param role: putanja do datoteke u kojoj su smjesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: object -- podatak koji se nalazi na zadatom indeksu sa zadatom ulogom.
        """
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element
    
    def headerData(self, section, orientation, role):
        """
        Vraca podatak koji ce popuniti sekciju zaglavlja tabele.
        :param section: sekcija koja u zavisnosti od orijentacije predstavlja redni broj kolone ili reda.
        :type section: int
        :param orientation: odredjuje polozaj zaglavlja.
        :type orientation: QtCore.Qt.Vertical ili QtCore.Qt.Horizontal
        :param role: putanja do datoteke u kojoj su smjesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: str -- naziv sekcije zaglavlja.
        """
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "Naziv"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Tip"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Kapacitet"

    def setData(self, index, value, role):
        """
        Postavlja vrednost na zadatom indeksu.
        Ova metoda je vazna ako zelimo da nas model moze da se menja.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :param value: nova vrijednost koju zelimo da postavimo.
        :type value: str -- vrijednost koja ce biti dodijeljena, za sada radimo samo sa stringovima
        :param role: putanja do datoteke u kojoj su smjesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: bool -- podatak o uspjesnosti izmjene.
        """
        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def flags(self, index):
        """
        Vraca flagove koji su aktivni za dati indeks modela.
        Ova metoda je vazna ako zelimo da nas model moze da se mijenja.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- flagovi koji treba da budu aktivirani.
        """
        # onemogućavamo rucno mijenjanje podataka o halama
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def get_element(self, index : QtCore.QModelIndex):
        """
        Dobavlja podatak smjesten na zadatom indeksu, ako je indeks validan.
        Pomocna metoda nase klase.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- vrijednost na indeksu.
        """
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def remove(self, indices):
        """
        Uklanja elemente iz modela na zadatim indeksima. Mozemo uklanjati vise redova (hala) iz magacina
        u jednom pozivu metode.
        Pomocna metoda nase klase.
        :param indices: indeks elementa modela.
        :type indices: list -- lista QModelIndex-a.
        """
        # na osnovu indeksa dobijamo njihove redove, posto su za jedan red vezana tri indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo s kraja, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        if(len(indices)==0):
            return -1
        for i in indices:
            if os.path.exists("plugins/aleksandar_babic_magacin/"+self._data[i][0]+".csv"):
                os.remove("plugins/aleksandar_babic_magacin/"+self._data[i][0]+".csv")

            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()
            
        self.save_data()

        return 0

    def add(self, data : dict):
        """
        Dodaje novu halu (red matrice) u model.
        Pomocna metoda nase klase.
        :param data: indeks elementa modela.
        :type data: dict -- podaci o novoj hali.
        """
        for h in self._data:
            if(h[0]==data["name"]):
                return -1
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data["name"], data["type"], data["capacity"]])
        self.endInsertRows()
        self.save_data()
        open("plugins/aleksandar_babic_magacin/"+data["name"]+".csv", "w")
        return 0

    def add_new_proizvod(self, data : dict):
        """
        Dodaje novi proizvod.
        Pomocna metoda nase klase.
        :param data: indeks elementa modela.
        :type data: dict -- podaci o novoj hali.
        """
        proizvodi = []
        with open("plugins/aleksandar_babic_magacin/proizvodi.csv", "r", encoding="utf-8") as fp:
            proizvodi = list(csv.reader(fp, dialect=csv.unix_dialect))
        for p in proizvodi:
            if(p[0]==data["name"]):
                return -1
        proizvodi.append([data["name"], data["temperature"]])
        with open("plugins/aleksandar_babic_magacin/proizvodi.csv", "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for row in proizvodi:
                writer.writerow(row)
        return 0

    def load_data(self, path=""):
        """
        Ucitava podatke iz CSV datoteke na zadatoj path putanji uz pomoc CSV reader-a.
        Pomocna metoda nase klase.
        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "r", encoding="utf-8") as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def save_data(self, path="plugins/aleksandar_babic_magacin/magacin.csv"):
        """
        Zapisuje podatke iz modela u datoteku na zadatoj path putanji uz pomoc CSV writer-a.
        Pomocna metoda nase klase.
        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for row in self._data:
                writer.writerow(row)

    def open_hala(self, indices):
        """
        Otvara halu na zadatom indeksu.
        Pomocna metoda nase klase.
        :param indices: indeks elementa modela.
        :type indices: list -- lista QModelIndex-a.
        """
        
        indices = sorted(set(map(lambda x: x.row(), indices)))
        if(len(indices)==0):
            return -1
        elif(len(indices)>1):
            return 1
        name = self._data[indices[0]][0]
        return name

    def add_proizvod(self, data):
        """
        Dodaje novi proizvod.
        Pomocna metoda nase klase.
        :param data: indeks elementa modela.
        :type data: dict -- podaci o novom proizvodu.
        """
        tip = ""
        zauzeto = 0
        proizvodi = []
        with open("plugins/aleksandar_babic_magacin/"+data["hala"][0]+".csv", "r", encoding="utf-8") as fp:
            proizvodi = list(csv.reader(fp, dialect=csv.unix_dialect))
        for p in proizvodi:
            zauzeto += (int)(p[1])
        if((int)(data["kolicina"])>(((int)(data["hala"][2]))-zauzeto)):
            return -1, ((int)(data["hala"][2]))-zauzeto
        if((int)(data["proizvod"][1])>=-10 and (int)(data["proizvod"][1])<=0):
            tip = "Zamrzavanje"
        elif((int)(data["proizvod"][1])>=1 and (int)(data["proizvod"][1])<=18):
            tip = "Rashladna"
        else:
            tip = "Sobna temperatura"
        if(tip != data["hala"][1]):
            return 1, None
        hala = HalaModel("plugins/aleksandar_babic_magacin/"+data["hala"][0]+".csv")
        postoji = False
        for p in hala.get_data():
            if(p[0]==data["proizvod"][0] and p[2]==data["datum"]):
                p[1]=(int)(p[1])+(int)(data["kolicina"])
                postoji = True
                break
        if(postoji is False):
            hala.add_proizvod(data)
        hala.save_data("plugins/aleksandar_babic_magacin/"+data["hala"][0]+".csv")
        return 0, None