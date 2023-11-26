from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import qimage2ndarray
import os
import pydicom

class VentanaPrincipal(QMainWindow):
    def __init__(self, ppal=None):
        super(VentanaPrincipal, self).__init__(ppal)
        loadUi('VentanaLogin.ui', self)
        self.setup()

    def setup(self):
        self.boton_ingresar.clicked.connect(self.abrir_escoger)

    def abrir_escoger(self):
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        resultado = self.__controlador.validar_usuario(usuario, password)

        if resultado:
            self.__ventanaOpciones = Opciones(ppal=self)
            self.__ventanaOpciones.asignarVentanaPadre(self)
            self.close() 
            self.__ventanaOpciones.show()
        
        else:
            QMessageBox.warning(self, 'Usuario Inválido', 'Usuario no encontrado o contraseña incorrecta')

    def asignarControlador(self, control):
        self.__controlador = control

class Opciones(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('accion.ui', self)
        self.__ventanaPadre = None
        self.setup()

    def setup(self):
        self.datos_imagenes.clicked.connect(self.abrir_datos)
        self.visualizar_imagenes.clicked.connect(self.abrir_visualizacion)
        self.regresar.clicked.connect(self.volver)

    def asignarVentanaPadre(self, ventana_padre):
        self.__ventanaPadre = ventana_padre

    def abrir_datos(self):
        self.datos = datos(self)
        self.datos.show()

    def abrir_visualizacion(self):
       self.visualizar = visualizar(self)
       self.visualizar.show()

    def volver(self):
        self.__ventanaPadre.show()
        self.close()

class datos(QDialog):
    def __init__(self, ventana_padre, ppal=None):
        super().__init__(ppal)
        loadUi('informacion.ui', self)
        self.__ventanaPadre = ventana_padre
        self.setup()

    def setup(self):
        self.archivos_carpeta = self.listar_archivos()
        self.NombrePaciente.setText(self.extraer_paciente())
        self.FechaEstudio.setText(self.extraer_fecha())
        self.ModalidadEstudio.setText(self.extraer_modalidad())
        self.DescripcionEstudio.setText(self.extraer_descripcion())
        self.IDPaciente.setText(self.extraer_ID())
        self.archivo.addItems(self.archivos_carpeta)
        self.regresar2.clicked.connect(self.volver)

    def listar_archivos(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        archivos = [nombre for nombre in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, nombre))]
        return archivos

    def extraer_paciente(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        c = self.archivo.currentText()
        ruta = os.path.join(carpeta, c)
        lectura = pydicom.dcmread(ruta)
        nombre_paciente = lectura.PatientName
        return nombre_paciente

    def extraer_fecha(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        c = self.archivo.currentText()
        ruta = os.path.join(carpeta, c)
        lectura = pydicom.dcmread(ruta)
        fecha_estudio = lectura.StudyDate
        return fecha_estudio

    def extraer_modalidad(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        c = self.archivo.currentText()
        ruta = os.path.join(carpeta, c)
        lectura = pydicom.dcmread(ruta)
        modalidad_estudio = lectura.Modality
        return modalidad_estudio

    def extraer_descripcion(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        c = self.archivo.currentText()
        ruta = os.path.join(carpeta, c)
        lectura = pydicom.dcmread(ruta)
        descripcion_estudio = lectura.StudyDescription
        return descripcion_estudio

    def extraer_ID(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        c = self.archivo.currentText()
        ruta = os.path.join(carpeta, c)
        lectura = pydicom.dcmread(ruta)
        ID_paciente = lectura.PatientID
        return ID_paciente

    def volver(self):
        self.__ventanaPadre.show()
        self.close()
    
class visualizar(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('visualizacion.ui', self)
        self.__ventanaPadre = ppal
        self.setup()


    def obtener_numero_archivos(self):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        archivos = [nombre for nombre in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, nombre))]
        return len(archivos)


    def cargar_imagen(self, numero_archivo):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(directorio_actual, 'Imagenes_dicom')
        archivos = [nombre for nombre in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, nombre))]


        if 1 <= numero_archivo <= len(archivos):
            archivo_actual = archivos[numero_archivo - 1]
            ruta_archivo = os.path.join(carpeta, archivo_actual)


            ds = pydicom.dcmread(ruta_archivo)


            pixmap = QPixmap.fromImage(qimage2ndarray.array2qimage(ds.pixel_array))


            self.imagenes.setPixmap(pixmap)
        else:
            print("Número de archivo fuera de rango.")


    def setup(self):
        self.numero_archivos = self.obtener_numero_archivos()
        self.slider.setMinimum(1)
        self.slider.setMaximum(self.numero_archivos)
        self.slider.setValue(1)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.actualizar_imagen)
        self.regresar3.clicked.connect(self.volver)


    def actualizar_imagen(self):
        valor_slider = self.slider.value()
        self.cargar_imagen(valor_slider)


    def volver(self):
        self.__ventanaPadre.show()
        self.close()