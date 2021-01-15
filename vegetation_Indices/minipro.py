from PyQt5 import QtCore, QtGui
import os,sys,struct
import numpy as np
from osgeo import gdal, gdalconst
import math

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MainWindow(QtGui.QMainWindow):    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(_translate("Form", "Vegetation Index", None))
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\mrg14-9395\Desktop\icon.png'))
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        global login_widget
        login_widget = LoginWidget(self)        
        login_widget.setupUi(login_widget)        
        login_widget.show()
        login_widget.pushButton.clicked.connect(self.login)
        self.central_widget.addWidget(login_widget)        

    def login(self):
        self.boolVal = login_widget.login_validate()
        if self.boolVal==1:
            global logged_in_widget
            logged_in_widget = LoggedWidget(self)
            logged_in_widget.setupUi(logged_in_widget)
            logged_in_widget.show()
            self.central_widget.addWidget(logged_in_widget)
            self.central_widget.setCurrentWidget(logged_in_widget)                          
   
class LoginWidget(QtGui.QWidget):
     def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setFixedSize(400, 350)
        Form.setWindowIcon(QtGui.QIcon(r'C:\Users\mrg14-9395\Desktop\icon.png'))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(90, 90, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 50, 111, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 130, 113, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(230, 90, 113, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(230, 130, 81, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 180, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

     def login_validate(self):
         self.username = str(self.lineEdit.text())
         self.password = str(self.lineEdit_2.text())         
         if self.username=='admin' and self.password=='password':
             return 1
         else:
             return 0      

     def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Vegetation Index", None))
        self.label.setText(_translate("Form", "Login Page", None))
        self.label_2.setText(_translate("Form", "Username", None))
        self.label_3.setText(_translate("Form", "Password", None))
        self.pushButton.setText(_translate("Form", "Login", None))
        
class LoggedWidget(QtGui.QWidget):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        #Form.resize(400, 300)
        Form.setWindowIcon(QtGui.QIcon(r'C:\Users\mrg14-9395\Desktop\icon.png'))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 30, 231, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 80, 141, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.selectInputFile)
        self.comboBox = QtGui.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(60, 180, 141, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))

        self.comboBox.activated.connect(self.select_index)        

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 270, 313, 13))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(60, 290, 313, 13))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.comboBox_2 = QtGui.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 180, 141, 22))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))

        self.comboBox_2.activated.connect(self.select_sensor)       
        
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 130, 141, 21))
        self.pushButton_2.clicked.connect(self.selectOutputDirectory)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(230, 80, 313, 20))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(230, 130, 313, 20))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 230, 141, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_3.clicked.connect(self.calculate_index)

        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(230, 230, 141, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.display_metadata)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def display_metadata(self):
        self.m_details(self.m_ds)

    def m_details(self,m_ds):
        xsize = str(m_ds.RasterXSize)
        ysize = str(m_ds.RasterYSize)
        cbands = str(m_ds.RasterCount)
        geotransform = str(m_ds.GetGeoTransform())
        lab2 = 'Size is '+ xsize+ 'x'+ ysize+ 'x'+ cbands        
        lab6 = str(geotransform[0])+ ','+str(geotransform[3])+')'
        lab5 = str(m_ds.GetDriver().ShortName)+ '/'+str(m_ds.GetDriver().LongName)
        self.label_5.setText('Driver: '+lab5 + ' Origin = ('+lab6)        
                             
    def selectInputFile(self):
        #self.lineEdit.setText(QtGui.QFileDialog.getOpenFileName())
        self.label_3.setText(QtGui.QFileDialog.getOpenFileName())
        self.m_file_path = str(self.label_3.text())
        
    def selectOutputDirectory(self):
        #self.lineEdit.setText(QtGui.QFileDialog.getOpenFileName())
        self.label_4.setText(QtGui.QFileDialog.getExistingDirectory())
        self.m_out_path = str(self.label_4.text())
        
    def select_index(self):
        self.choice = str(self.comboBox.currentText())
        #self.label_2.setText("The selected index is "+self.choice)

    def select_sensor(self):
        self.sensor = str(self.comboBox_2.currentText())
        #self.label_2.setText("The selected sensor is "+self.sensor)

    def calculate_index(self):
        self.m_ds = gdal.Open( self.m_file_path, gdal.GA_ReadOnly )
        if self.m_ds == None:
            self.label_2.setText('Could not Open file')
            sys.exit(1)
        if self.sensor == "Landsat":
            self.bands = [3,4,2]
        elif self.sensor =="LISS-IV":
            self.bands = [2,3,1]
        else:
            self.label_2.setText('Select a proper sensor!!') 
            
        if self.choice == "Index":
            self.label_2.setText('Select a proper index!!')  
        elif self.choice == "DVI":
            self.calc_DVI(self.m_file_path,self.m_out_path,self.bands,self.m_ds)
        elif self.choice == "NDVI":
            self.calc_NDVI(self.m_file_path,self.m_out_path,self.bands,self.m_ds)
        elif self.choice == "TVI":
            self.calc_TVI(self.m_file_path,self.m_out_path,self.bands,self.m_ds)
        elif self.choice == "SAVI":
            self.calc_SAVI(self.m_file_path,self.m_out_path,self.bands,self.m_ds)
        elif self.choice == 'NDGI':
            self.calc_NDGI(self.m_file_path,self.m_out_path,self.bands,self.m_ds)           

    def create_blank(self, m_ds,m_out_path):
        driver = gdal.GetDriverByName( m_ds.GetDriver().ShortName )
        dst_ds=driver.Create(m_out_path, m_ds.RasterXSize,m_ds.RasterYSize, 1, gdal.GDT_Float32)
        dst_ds.SetGeoTransform(m_ds.GetGeoTransform())
        dst_ds.SetProjection(m_ds.GetProjection())
        return dst_ds

    def raster_tuple(self, band,xsize,ysize,line):
        m_scanline = band.ReadRaster(0,line,xsize,1,xsize,1,gdal.GDT_Float32)
        m_tuple = struct.unpack('f' * xsize, m_scanline)
        return m_tuple

    def calc_DVI(self, m_input,m_output,bands,m_ds):
        m_out_path = m_output + "\\1.DVI.tiff"
        dst_ds = self.create_blank(m_ds,m_out_path)
        red_band = m_ds.GetRasterBand(bands[0]) # RED BAND
        nir_band = m_ds.GetRasterBand(bands[1]) # NIR BAND

        for line in range(m_ds.RasterYSize):
            outputLine = ''
            red_tuple = self.raster_tuple(red_band, m_ds.RasterXSize,m_ds.RasterYSize,line)
            nir_tuple = self.raster_tuple(nir_band, m_ds.RasterXSize,m_ds.RasterYSize,line)

            for i in range(len(red_tuple)):
                dvi = (nir_tuple[i] - red_tuple[i])
                outputLine = outputLine + struct.pack('f', dvi)
            dst_ds.GetRasterBand(1).WriteRaster(0,line,m_ds.RasterXSize,1,outputLine,m_ds.RasterXSize,1,gdal.GDT_Float32)
            del outputLine
        self.label_2.setText('DVI Calculated and Outputted to File 1.DVI.tiff')

    def calc_NDVI(self, m_input,m_output,bands, m_ds):
        m_out_path = m_output + "\\2.NDVI.tiff"
        dst_ds = self.create_blank(m_ds,m_out_path)
        red_band = m_ds.GetRasterBand(bands[0]) # RED BAND
        nir_band = m_ds.GetRasterBand(bands[1]) # NIR BAND

        for line in range(m_ds.RasterYSize):
            outputLine = ''
            red_tuple = self.raster_tuple(red_band, m_ds.RasterXSize,m_ds.RasterYSize,line)
            nir_tuple = self.raster_tuple(nir_band, m_ds.RasterXSize,m_ds.RasterYSize,line)

            for i in range(len(red_tuple)):
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi = 0
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    ndvi = ndvi_upper/ndvi_lower
                outputLine = outputLine + struct.pack('f', ndvi)
            dst_ds.GetRasterBand(1).WriteRaster(0,line,m_ds.RasterXSize,1,outputLine,m_ds.RasterXSize,1,gdal.GDT_Float32)
            del outputLine
        self.label_2.setText('NDVI Calculated and Outputted to File 2.NDVI.tiff')

    def calc_TVI(self, m_input,m_output,bands,m_ds):
        m_out_path = m_output + "\\3.TVI.tiff"
        dst_ds = self.create_blank(m_ds,m_out_path)
        red_band = m_ds.GetRasterBand(bands[0]) # RED BAND
        nir_band = m_ds.GetRasterBand(bands[1]) # NIR BAND

        for line in range(m_ds.RasterYSize):
            outputLine = ''
            red_tuple = self.raster_tuple(red_band, m_ds.RasterXSize,m_ds.RasterYSize,line)
            nir_tuple = self.raster_tuple(nir_band, m_ds.RasterXSize,m_ds.RasterYSize,line)

            for i in range(len(red_tuple)):
                ndvi_upper = (nir_tuple[i] - red_tuple[i])
                ndvi_lower = (nir_tuple[i] + red_tuple[i])
                ndvi = 0
                if ndvi_lower == 0:
                    ndvi = 0
                else:
                    try:
                        ndvi = (ndvi_upper/ndvi_lower)**.5
                    except ValueError as e :
                        ndvi = (((ndvi_upper/ndvi_lower)*-1)**.5)*-1
                outputLine = outputLine + struct.pack('f', ndvi)
            dst_ds.GetRasterBand(1).WriteRaster(0,line,m_ds.RasterXSize,1,outputLine,m_ds.RasterXSize,1,gdal.GDT_Float32)
            del outputLine
        self.label_2.setText('TVI Calculated and Outputted to File 3.TVI.tiff')

    def calc_SAVI(self, m_input,m_output,bands,m_ds):
        m_out_path = m_output + "\\4.SAVI.tiff"
        dst_ds = self.create_blank(m_ds,m_out_path)
        red_band = m_ds.GetRasterBand(bands[0]) # RED BAND
        nir_band = m_ds.GetRasterBand(bands[1]) # NIR BAND

        for line in range(m_ds.RasterYSize):
            outputLine = ''
            red_tuple = self.raster_tuple(red_band, m_ds.RasterXSize,m_ds.RasterYSize,line)
            nir_tuple = self.raster_tuple(nir_band, m_ds.RasterXSize,m_ds.RasterYSize,line)

            for i in range(len(red_tuple)):
                savi_upper = (nir_tuple[i] - red_tuple[i])
                savi_lower = (nir_tuple[i] + red_tuple[i] + 0.5)
                ndvi = 0
                if savi_lower == 0:
                    savi = 0
                else:
                    savi = (savi_upper/savi_lower)*1.5
                outputLine = outputLine + struct.pack('f', savi)
            dst_ds.GetRasterBand(1).WriteRaster(0,line,m_ds.RasterXSize,1,outputLine,m_ds.RasterXSize,1,gdal.GDT_Float32)
            del outputLine
        self.label_2.setText('SAVI Calculated and Outputted to File 4.SAVI.tiff')

    def calc_NDGI(self, m_input,m_output,bands, m_ds):
        m_out_path = m_output + "\\5.NDGI.tiff"
        dst_ds = self.create_blank(m_ds,m_out_path)
        red_band = m_ds.GetRasterBand(bands[0]) # RED BAND
        green_band = m_ds.GetRasterBand(bands[2]) # GREEN BAND

        for line in range(m_ds.RasterYSize):
            outputLine = ''
            red_tuple = self.raster_tuple(red_band, m_ds.RasterXSize,m_ds.RasterYSize,line)
            green_tuple = self.raster_tuple(green_band, m_ds.RasterXSize,m_ds.RasterYSize,line)

            for i in range(len(red_tuple)):
                ndgi_upper = (green_tuple[i] - red_tuple[i])
                ndgi_lower = (green_tuple[i] + red_tuple[i])
                ndgi = 0
                if ndgi_lower == 0:
                    ndgi = 0
                else:
                    ndgi = ndgi_upper/ndgi_lower
                outputLine = outputLine + struct.pack('f', ndgi)
            dst_ds.GetRasterBand(1).WriteRaster(0,line,m_ds.RasterXSize,1,outputLine,m_ds.RasterXSize,1,gdal.GDT_Float32)
            del outputLine
        self.label_2.setText('NDGI Calculated and Outputted to File 5.NDGI.tiff')

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Vegetation Index", None))
        self.label.setText(_translate("Form", "Vegetation Index Tool", None))
        self.pushButton.setText(_translate("Form", "Browse Input", None))
        self.pushButton_2.setText(_translate("Form", "Output Directory", None))
        self.comboBox.setItemText(0, _translate("Form", "Index", None))
        self.comboBox.setItemText(1, _translate("Form", "DVI", None))
        self.comboBox.setItemText(2, _translate("Form", "NDVI", None))
        self.comboBox.setItemText(3, _translate("Form", "TVI", None))        
        self.comboBox.setItemText(4, _translate("Form", "NDGI", None))
        self.comboBox.setItemText(5, _translate("Form", "SAVI", None))
        self.comboBox_2.setItemText(0, _translate("Form", "Sensor", None))
        self.comboBox_2.setItemText(1, _translate("Form", "Landsat", None))
        self.comboBox_2.setItemText(2, _translate("Form", "LISS-IV", None))
        self.pushButton_3.setText(_translate("Form", "Calculate", None))
        self.pushButton_4.setText(_translate("Form", "Metadata", None)) 

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()    
    app.exec_()
