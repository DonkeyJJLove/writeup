# File: main.py
# Author: cha0s
# Date: 2024-04-26

"""
============================================================
File: main.py
Author: cha0s
Date: 2024-04-26
Description:
    Główny plik aplikacji, który uruchamia GUI.

    Funkcjonalności:
        - Inicjalizacja logowania.
        - Uruchamianie interfejsu użytkownika.

Future Enhancements:
    - Dodanie opcji konfiguracji z poziomu GUI.
    - Integracja z systemem monitorowania wydajności.
============================================================
"""

import logging
import sys
from PyQt5.QtWidgets import QApplication
from modules.gui import SynapticApp


def main():
    # Konfiguracja logowania
    logging.basicConfig(
        filename='logs/app.log',
        filemode='a',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG  # Ustawienie na DEBUG dla szczegółowego logowania
    )

    logging.info("Uruchamianie aplikacji...")

    try:
        # Inicjalizacja aplikacji PyQt5
        app = QApplication(sys.argv)
        logging.info("QApplication zainicjalizowane.")

        synaptic_app = SynapticApp()
        synaptic_app.show()  # Wywołanie show() bezpośrednio
        logging.info("SynapticApp wyświetlone.")

        sys.exit(app.exec_())
    except Exception as e:
        logging.exception("Wystąpił nieoczekiwany błąd podczas uruchamiania aplikacji.")
        sys.exit(1)


if __name__ == '__main__':
    main()
