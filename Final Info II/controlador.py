from PyQt5.QtWidgets import QApplication
from vista import VentanaPrincipal
from modelo import Servicio

class Coordinador(object):
    def __init__(self, vista, sistema):
        self.__vista = vista
        self.__sistema = sistema

    def validar_usuario(self, u, p):
        return self.__sistema.verificarUsuario(u, p)
        
class Principal(object):
    def __init__(self):
        self.__app = QApplication([])
        self.__vista = VentanaPrincipal()
        self.__sistema = Servicio()
        self.__mi_coordinador = Coordinador(self.__vista, self.__sistema)
        self.__vista.asignarControlador(self.__mi_coordinador)

    def main(self):
        self.__vista.show()
        self.__app.exec_()

p = Principal()
p.main()
