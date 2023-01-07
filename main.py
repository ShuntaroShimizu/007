from PyQt5.QtWidgets import *
import sys
import mainwindow as mw

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = mw.Window()
    ex.showMaximized()
    sys.exit(app.exec_())