import sys
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtGui import QImage,QPixmap
from PyQt6.QtWidgets import QFileDialog,QLabel
from PyQt6.QtCore import QFile, QTextStream, QIODevice
from ui import Ui_MainWindow
import fitz


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super(Main_Window,self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.initUI()
            self.show()
            self.f1 =''
            self.added = []
            self.countall = 0
        except Exception as e:
            print(e)
    


    def initUI(self):
        try:
            self.ui.LoadButton.clicked.connect(self.load_file)
            self.ui.plusbutton.clicked.connect(self.plus)
            self.ui.minusbutton.clicked.connect(self.minus)
            self.ui.lineEdit.textChanged.connect(self.work)
            self.ui.ClearButton.clicked.connect(self.clear)
            self.ui.textEdit.textChanged.connect(self.textchange)
            self.ui.SaveButton.clicked.connect(self.SaveFile)
            self.ui.AddButton.clicked.connect(self.AddText)
        except Exception as e:
            print(e)
            
    def load_file(self):
        try:
            file = QFileDialog.getOpenFileName(self, 'Open File', '','PDF(*.pdf)')
            f = str(file).partition(',')[0]
            self.f1 = f.replace('(','')
            self.f1 = self.f1.replace('\'','')
            doc = fitz.open(self.f1)
            self.pagecount = doc.page_count
            x = 0
            self.pages = []
            while x < self.pagecount:
                
                page = doc.load_page(x)
                text = page.get_text('Text')
                self.pages.append(text)
                x+=1
            
            
            self.ui.textEdit.setText(self.pages[0])
            self.ui.lineEdit.setText('1')
            

            pix = doc.load_page(0).get_pixmap(alpha=False)
            qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            self.ui.label.setScaledContents(True)
            self.ui.label.setPixmap(QPixmap.fromImage(qimg))
            
        except Exception as e:
            print(e)

        
    def work(self):
            
        try:
            doc = fitz.open(self.f1)
            self.number = int(self.ui.lineEdit.text())-1
            if self.number >= self.pagecount-1:
                self.number = self.pagecount-1
            page = doc.load_page(self.number)
            self.ui.lineEdit.setText(str(self.number+1))
            
            self.ui.textEdit.setText(self.pages[self.number])

            pix = page.get_pixmap(alpha=False)
            qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            self.ui.label.setScaledContents(True)
            self.ui.label.setPixmap(QPixmap.fromImage(qimg))
            
        except Exception as e:
            print(e)
            
            
    def plus(self):
        try:
            self.number = int(self.ui.lineEdit.text())-1
            if self.number >= self.pagecount-1:
                self.number = self.pagecount-1
            else:
                self.number += 1
            self.ui.lineEdit.setText(str(self.number+1))
            
        except Exception as e:
            print(e)

        
    def minus(self):
        try:
            self.number = int(self.ui.lineEdit.text())-1
            if self.number >0:
                self.number -= 1
                self.ui.lineEdit.setText(str(self.number+1))
        except Exception as e:
            print(e)


    def clear(self):
        try:
            self.pages.clear()
            self.f1=''
            self.ui.lineEdit.setText('1')
            self.ui.label.clear()
            self.ui.textEdit.clear()
            self.added.clear()
            self.ui.CountLines.setText("Количество строк: 0")
            self.ui.AddCountLines.setText("Количество добавленных строк: 0")
            self.ui.AddCountLines.setStyleSheet('color: black')
        except Exception as e:
            print(e)

    
    def textchange(self):
        try:
            self.number = int(self.ui.lineEdit.text())-1
            self.pages[self.number] = self.ui.textEdit.toPlainText()
            self.lines_count = self.ui.textEdit.toPlainText().splitlines()
            self.lines_count = len(self.lines_count)
            self.ui.CountLines.setText('Количество строк: '+str(self.lines_count))
            pass
        except Exception as e:
            print(e)
        pass


    def SaveFile(self):
        try:
            self.add = ''
            x = 0
            while x< len(self.added): 
                self.add += self.added[x]
                x+=1

            filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
 
            if filename:
                with open(filename, 'w') as file:
                    file.write(self.add)
        except Exception as e:
            print(e)
        pass

    def AddText(self):
        try:
            self.added.append(self.ui.textEdit.toPlainText())
            self.countall +=int(self.lines_count)
            
            self.ui.AddCountLines.setText('Количество добавленных строк: '+ str(self.countall))

            if self.countall >500:
                self.ui.AddCountLines.setStyleSheet('color: red;')
            else:
                self.ui.AddCountLines.setStyleSheet('color: black')
                
            
        except Exception as e:
            print(e)


app = QtWidgets.QApplication(sys.argv)
application = target= Main_Window()
sys.exit(app.exec())
    


