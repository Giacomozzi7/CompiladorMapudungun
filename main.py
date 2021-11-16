import sys
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
import analizadorlexico as al
import analizadorsintactico as ast

class ventanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ventana.ui",self)

        #Definicion para ancho de cada columna de la tabla
        self.tableLexico.setColumnWidth(0,80)
        self.tableLexico.setColumnWidth(1,80)
        self.tableLexico.setColumnWidth(2,144)
        self.tableLexico.setColumnWidth(3,140)

        #Definicion de evento click para botones
        self.btnLimpiar_cod.clicked.connect(self.borrarTxtCod)
        self.btnLimpiar_lex.clicked.connect(self.borrarTabla)
        self.btnLimpiar_sin.clicked.connect(self.borrarTxtSin)
        self.btnAnalizar_lex.clicked.connect(self.analizaLexico)
        self.btnAnalizar_sin.clicked.connect(self.analizaSintax)

        self.borrarTabla()
        self.tableLexico.setStyleSheet("QTableWidget::item {background-color:rgb(62,62,62);border-bottom: 1px solid #cccccc;color:rgb(255,255,255)}")

    #Ejecuta el analizador lexico y asigna los resultados a las celdas de la tabla
    def analizaLexico(self):
        self.borrarTabla()
        sData = self.txtCodigo.toPlainText().strip()
        aResultado = al.analizadorLexico(sData)

        nRow = 11
        if len(aResultado)>nRow:
            self.tableLexico.setRowCount(len(aResultado))

        #Llenar tabla
        nFila = 0
        for registro in aResultado:
            nColumna = 0
            for elemento in registro:
                el = QTableWidgetItem(str(elemento))
                self.tableLexico.setItem(nFila,nColumna,el)
                nColumna+=1
            nFila+=1
    
    def analizaSintax(self):
        self.borrarTxtSin()
        sData = self.txtCodigo.toPlainText().strip()
        aResultadoS = ast.prueba_sintactica(sData)
        sCad = ''
        for fila in aResultadoS:
            sCad += fila + "\n"
        self.txtSintactico.setPlainText(sCad)
        
        
    #Borra la tabla y setea celdas vacias
    def borrarTabla(self):
        while (self.tableLexico.rowCount() > 0):
            {
                self.tableLexico.removeRow(0)
            }
        self.tableLexico.setRowCount(11)
    
    #Borra los textos de los EditText
    def borrarTxtCod(self): self.txtCodigo.setPlainText('')
    def borrarTxtSin(self): 
        self.txtSintactico.setPlainText('')
        al.resultado_gramatica = []
        al.resultado_lexema = []

          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ventanaPrincipal()
    ventana.show()
    app.exec_()