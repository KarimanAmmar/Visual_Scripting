import os, sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from examples.DataScience.datascience_window import DataScienceWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("icons/gold_logo.png"))

    wnd = DataScienceWindow()
    wnd.show()

    sys.exit(app.exec_())
