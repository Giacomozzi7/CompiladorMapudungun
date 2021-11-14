import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

class ventanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana.ui",self)

        self.tableLexico.setColumnWidth(0,54)
        self.tableLexico.setColumnWidth(1,130)
        self.tableLexico.setColumnWidth(2,130)
        self.tableLexico.setColumnWidth(3,130)

        self.btnLimpiar_cod.clicked.connect(self.borrarTxtCod)
        self.btnLimpiar_lex.clicked.connect(self.borrarTabla)
        self.btnLimpiar_sin.clicked.connect(self.borrarTxtSin)

        self.borrarTabla()
        
    #Borra la tabla y setea celdas vacias
    def borrarTabla(self):
        while (self.tableLexico.rowCount() > 0):
            {
                self.tableLexico.removeRow(0)
            }
        
        self.tableLexico.setRowCount(11)
    
    def borrarTxtCod(self): self.txtCodigo.setPlainText('')
    def borrarTxtSin(self): self.txtSintactico.setPlainText('')
        
        

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ventanaPrincipal()
    ventana.show()
    app.exec_()