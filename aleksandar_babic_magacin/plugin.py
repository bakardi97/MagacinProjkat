from plugin_framework.plugin import Plugin
from .widgets.magacin_widget import MagacinWidget

class Main(Plugin):
    """
    Klasa koja predstavlja konkretan plugin. Nasledjujemo "apstraktnu" klasu Plugin.
    Ova klasa predstavlja plugin za aplikaciju vodjenje magacina (magacin).
    """
    def __init__(self, spec):
        """
        Inicijalizator magacin plugina.

        :param spec: specifikacija metapodataka o pluginu.
        :type spec: dict
        """
        super().__init__(spec)

    def get_widget(self, parent=None):
        """
        Ova metoda vraca konkretan widget koji ce biti smjesten u centralni dio aplikacije i njenog 
        glavnog prozora. Moze da vrati toolbar, kao i meni, koji ce biti smjesten u samu aplikaciju.
        
        :param parent: bi trebao da bude widget u koji ce se smjestiti ovaj koji nas plugin omogucava.
        :returns: QWidget, QToolbar, QMenu
        """
        return MagacinWidget(parent), None, None