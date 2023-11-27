from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QMainWindow, QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QRegExpValidator, QPixmap
from PyQt5.QtCore import QRegExp
from nilearn import plotting
from nilearn.plotting import plot_anat

class VentanaPrincipal(QMainWindow):
    def __init__(self, ppal=None):
        super(VentanaPrincipal, self).__init__(ppal)
        loadUi('VentanaLogin .ui', self)
        self.setup()

    def setup(self):
        self.boton_ingresar.clicked.connect(self.abrir_escoger)
        letter_validator = QRegExpValidator(QRegExp("[a-zA-Z]+"))
        self.campo_usuario.setValidator(letter_validator)
        number_validator = QRegExpValidator(QRegExp("[0-9]+"))
        self.campo_password.setValidator(number_validator)

    def abrir_escoger(self):
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        resultado = self.__controlador.validar_usuario(usuario, password)

        if resultado:
            escoger = Opciones()
            escoger.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Usuario Inválido', 'Usuario o contraseña incorrectos')

    def asignarControlador(self, control):
        self.__controlador = control

class Opciones(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('Opciones.ui', self)
        self.__ventanaPadre = ppal
        self.setup()
   
    def setup(self):
        self.boton_cerebro.clicked.connect(self.abrir_cerebro)
        self.boton_torax.clicked.connect(self.abrir_torax)
        self.boton_salir2.clicked.connect(lambda: self.close())


    def abrir_cerebro(self):
        self.__vista_cerebro = VistaCerebro(self)
        self.__vista_cerebro.show()
        self.hide()
       
    def abrir_torax(self): 
        self.vista_torax = VistaTorax(self)
        self.vista_torax.show()
        self.hide()

class VistaCerebro(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('Cerebro.ui', self)
        self.__ventanaPadre = ppal
        self.setup()

    def setup(self):
        self.boton_regresar1.clicked.connect(self.volver)
        self.boton_salir3.clicked.connect(self.cerrar)

        self.mostrar_imagen()

    def mostrar_imagen(self):
        img_path = "Cerebro.nii"
        pixmap = self.cargar_imagen_en_qpixmap(img_path)
        self.imagen.setPixmap(pixmap)

    def cargar_imagen_en_qpixmap(self, img_path):
        plotting.plot_anat(img_path, display_mode='ortho', output_file='temp.png')
        pixmap = QPixmap('temp.png')
        return pixmap
    
           
    def cerrar(self):
        QApplication.quit()

    def volver(self):
        self.__ventanaPadre.show()
        self.close()

        
class VistaTorax(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('Torax.ui', self)
        self.__ventanaPadre = ppal
        self.setup()

        self.mostrar_imagen()

    def mostrar_imagen(self):
        img_path = "CTLiver.nii"
        pixmap = self.cargar_imagen_en_qpixmap(img_path)
        self.imagen2.setPixmap(pixmap) 

    def cargar_imagen_en_qpixmap(self, img_path):
        plotting.plot_anat(img_path, display_mode='ortho', output_file='temp_torax.png')
        pixmap = QPixmap('temp_torax.png')
        return pixmap
    

    def setup(self):
        self.boton_regresar2.clicked.connect(self.volver)
        self.boton_salir4.clicked.connect(self.cerrar)

    def cerrar(Self):
        QApplication.quit()

    def volver(self):
        self.__ventanaPadre.show()
        self.close()


