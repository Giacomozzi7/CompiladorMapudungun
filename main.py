import sys
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
import analizadorlexico as al
import analizadorsintactico as ast

class ventanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ventana.ui',self)
        self.setWindowTitle('Compilador Mapudungun')

        #Definicion para ancho de cada columna de la tabla
        self.tableLexico.setColumnWidth(0,80)
        self.tableLexico.setColumnWidth(1,80)
        self.tableLexico.setColumnWidth(2,144)
        self.tableLexico.setColumnWidth(3,140)

        #Definicion de evento click para botones
        self.btnAnalizar_cod.clicked.connect(self.analizaLexico)
        self.btnLimpiar_cod.clicked.connect(self.borrarData)
        self.btnSubir_cod.clicked.connect(self.cargaFile)
        self.btnExportar.clicked.connect(self.exportaFile)

        self.borrarData()
        self.btnExportar.setEnabled(False)
        self.tableLexico.setStyleSheet("QTableWidget::item {background-color:rgb(62,62,62);border-bottom: 1px solid #cccccc;color:rgb(255,255,255)}")

    #Ejecuta el analizador lexico y asigna los resultados a las celdas de la tabla
    def analizaLexico(self):
        sData = self.txtCodigo.toPlainText().strip()
        self.aResultado = al.analizadorLexico(sData)

        nRow = 11
        if len(self.aResultado)>nRow:
            self.tableLexico.setRowCount(len(self.aResultado))

        #Llenar tabla
        nFila = 0
        for registro in self.aResultado:
            nColumna = 0
            for elemento in registro:
                el = QTableWidgetItem(str(elemento))
                self.tableLexico.setItem(nFila,nColumna,el)
                nColumna+=1
            nFila+=1
        
        self.analizaSintax()
    
    #Ejecuta el analizador sintactico y asigna los resultados a su cuadro respectivo
    def analizaSintax(self):
        #self.borrarData()
        sData = self.txtCodigo.toPlainText().strip()
        self.aResultadoS = ast.prueba_sintactica(sData)
        sCad = ''
        for fila in self.aResultadoS:
            sCad += fila + '\n'
        self.txtSintactico.setPlainText(sCad)
        self.btnAnalizar_cod.setEnabled(False)
        self.btnExportar.setEnabled(True)
        
        
    #Borra la tabla y setea celdas vacias
    def borrarData(self):
        self.txtSintactico.setPlainText('')
        while (self.tableLexico.rowCount() > 0):
            {
                self.tableLexico.removeRow(0)
            }
        self.tableLexico.setRowCount(11)

        al.aResultado = []
        ast.aResultado = []
        self.btnAnalizar_cod.setEnabled(True)
        self.btnExportar.setEnabled(False)
    
    #Carga el archivo en el cuadro de texto del codigo y especifica el nombre
    def cargaFile(self):
        selectArchivo = QFileDialog()
        if selectArchivo.exec_():
            aFiles = selectArchivo.selectedFiles()
            with open(aFiles[0], 'r') as File:
                sDirectorio = aFiles[0]
                sData = File.read()
                if sData: 
                    aDirectorio = sDirectorio.split('/')
                    sDirectorio = aDirectorio[-1]
                    sDirectorio = f'!archivo importado: {sDirectorio}' + '\n'
                    self.txtCodigo.setPlainText(sDirectorio+sData+'\n')
    
    #Exporta los resultados de los analizadores 
    def exportaFile(self):
        with open('exportacion.txt', 'w') as f:
            sRes = ''
            for i in range(len(self.aResultado)):
                sRes += f'{i+1}. Linea: {self.aResultado[i][0]} Posicion: {self.aResultado[i][1]} Tipo Variable: {self.aResultado[i][2]} Valor: {self.aResultado[i][3]}' + '\n'

            sRes2 = ''
            for i in range(len(self.aResultadoS)):
                sRes2+=f'{self.aResultadoS[i]}' + '\n'
    
            sLine = '#---------------------------------------------------------------------------#'
            sCodigo = f'Codigo del programa \n{sLine}\n{self.txtCodigo.toPlainText().strip()}'+'\n\n'
            sFinal = f'''Exportacion resultados Compilador Mapudungun \n\n{sCodigo}Analizador Lexico\n{sLine}\n{sRes} \nAnalizador Sintactico\n{sLine}\n{sRes2}'''
            f.write(sFinal)
            msgBox = QMessageBox.about(self, "Exportacion", "Exportación realizada")

          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ventanaPrincipal()
    ventana.show()
    app.exec_()