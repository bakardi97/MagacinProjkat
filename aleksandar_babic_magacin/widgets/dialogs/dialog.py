from .add_proizvod_dialog import AddProizvodDialog
from .remove_proizvod_dialog import RemoveProizvodDialog
from .change_proizvod_dialog import ChangeProizvodDialog
from .add_new_proizvod_dialog import AddNewProizvodDialog
from .add_hala_dialog import AddHalaDialog

class Dialog():
    """
    Klasa koja predstavlja fabriku dijaloga.
    """
    def __init__(self):
        """
        Inicijalizator fabrike.
        """

    def getAddHalaDialog(self, parent):
        """
        Dobavlja dijalog za dodavanje hale.
        """
        return AddHalaDialog(parent)

    def getAddProizvodDialog(self, name, parent):
        """
        Dobavlja dijalog za dodavanje proizvoda.
        """
        return AddProizvodDialog(name, parent)

    def getAddNewProizvodDialog(self, parent):
        """
        Dobavlja dijalog za dodavanje novog proizvoda.
        """
        return AddNewProizvodDialog(parent)

    def getRemoveProizvodDialog(self, parent):
        """
        Dobavlja dijalog za uklanjanje proizvoda.
        """
        return RemoveProizvodDialog(parent)

    def getChangeProizvodDialog(self, parent):
        """
        Dobavlja dijalog za izmjenu proizvoda.
        """
        return ChangeProizvodDialog(parent)