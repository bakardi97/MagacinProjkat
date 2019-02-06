from PySide2 import QtCore
import csv

class HalaModel(QtCore.QAbstractTableModel):
    """
    Klasa koja predstavlja specijalizaciju QAbstractTableModel-a.
    Koristimo tabelarni model jer cemo podatke posmatrati kao tabelu, i u tabeli ih prikazivati.
    Svaki tabelarni model ima redove i kolone. Red je jedan proizvod u hali, a kolone predstavalju
    pojedinacne podatke o svakom proizvodu (naziv, kolicina i datum isteka roka).
    Datoteka na osnovu koje se populise model je CSV datoteka, gdje su redovi modela zapravo redovi
    iz datoteke, a kolone modela su podaci koji su u redu u datoteci odvojeni separatorom (zarezom).
    """
    def __init__(self, path=""):
        """
        Inicijalizator modela za halu.
        Pri inicijalizaciji se na osnovu datoteke sa putanje path ucitavaju i populise se model.
        :param path: putanja do datoteke u kojoj su smjesteni podaci.
        :type path: str
        """
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o proizvodima iz hala
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
        Vraca broj kolona u modelu. Posto znamo da je nas proizvod iz hale opisan sa tri
        podatka, vracamo fiksni broj kolona na osnovu datoteke.
        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: int -- broj kolona modela.
        """
        return 3

    def data(self, index, role):
        """
        Vraca podatak smjesten na datom indeksu sa datom ulogom.
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
                return "Kolicina"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Datum isteka roka"

    def setData(self, index, value, role):
        """
        Postavlja vrijednost na zadatom indeksu.
        Ova metoda je vazna ako zelimo da nas model moze da se mijenja.
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

        #if(index.column() == 0):
            #return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
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

    def remove(self, index, quantity, name):
        """
        Uklanja element iz modela na zadatom indeksu.
        Pomocna metoda nase klase.
        :param index: indeks elementa modela.
        :param quantity: kolicina proizvoda koja se uklanja.
        :type index: list -- lista QModelIndex-a.
        """
        # na osnovu indeksa dobijamo njihove redove, posto su za jedan red vezana tri indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova

        index = sorted(set(map(lambda x: x.row(), index)))

        if(quantity>((int)(self._data[index[0]][1]))):
            return self._data[index[0]][1]
        self._data[index[0]][1] = (int)(self._data[index[0]][1])-quantity
        self.save_data("plugins/aleksandar_babic_magacin/"+name+".csv")
        self.load_data("plugins/aleksandar_babic_magacin/"+name+".csv")
        return -1

    def add(self, data):
        """
        Dodaje novi proizvod.
        Pomocna metoda nase klase.
        :param data: slozeni element.
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
        if(hala.get_data()==self.get_data()):
            hala = self
        postoji = False
        for p in hala.get_data():
            if(p[0]==data["proizvod"][0] and p[2]==data["datum"]):
                p[1]=(int)(p[1])+(int)(data["kolicina"])
                postoji = True
                break
        if(postoji is False):
            hala.add_proizvod(data)
        hala.save_data("plugins/aleksandar_babic_magacin/"+data["hala"][0]+".csv")
        hala.load_data("plugins/aleksandar_babic_magacin/"+data["hala"][0]+".csv")
        return 0, None

    def change(self, index, date, name):
        """
        Menja proizvod.
        Pomocna metoda nase klase.
        :param index: indeks elementa modela.
        :param date: datum isteka roka proizvoda.
        :type index: list -- lista QModelIndex-a.
        """
        # na osnovu indeksa dobijamo njihove redove, posto su za jedan red vezana tri indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova

        index = sorted(set(map(lambda x: x.row(), index)))

        postoji = False
        for p in self._data:
            if(p[2]==date):
                p[1]=(int)(p[1])+(int)(self._data[index[0]][1])
                self._data[index[0]][1] = 0
                postoji = True
                break
        if(postoji is False):
            self._data[index[0]][2] = date
        self.save_data("plugins/aleksandar_babic_magacin/"+name+".csv")
        self.load_data("plugins/aleksandar_babic_magacin/"+name+".csv")

    def add_proizvod(self, data : dict):
        """
        Dodaje novi proizvod (red matrice) u model.
        Pomocna metoda nase klase.
        :param data: indeks elementa modela.
        :type data: dict -- podaci o novom proizvodu.
        """
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data["proizvod"][0], data["kolicina"], data["datum"]])
        self.endInsertRows()

    def load_data(self, path=""):
        """
        Ucitava podatke iz CSV datoteke na zadatoj path putanji uz pomoc CSV reader-a.
        Pomocna metoda nase klase.
        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "r", encoding="utf-8") as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def save_data(self, path=""):
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

    def get_data(self):
        return self._data

    def get_stanje(self, name):
        """
        Metoda koja vraca kao rezultat zauzetost hale u procentima.
        """
        hale = []
        with open("plugins/aleksandar_babic_magacin/magacin.csv", "r", encoding="utf-8") as fp:
            hale = list(csv.reader(fp, dialect=csv.unix_dialect))
        for h in hale:
            if(h[0]==name):
                capacity = (int)(h[2])
        zauzeto = 0
        for p in self._data:
            zauzeto += (int)(p[1])
        return zauzeto/capacity*100