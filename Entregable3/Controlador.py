from Vista import VentanaPrincipal
import sys
from PyQt5.QtWidgets import QApplication
from Modelo import Servicio

class Coordinador(object):
    def __init__(self, vista, sistema):
        self.__mi_vista = vista
        self.__mi_sistema = sistema
    def validar_usuario(self, u, p):
        return self.__mi_sistema.verificarUsuario(u,p)
    
class Principal(object):
    def __init__(self):
        self.__app = QApplication(sys.argv)
        self.__mi_vista = VentanaPrincipal()
        self.__mi_sistema = Servicio()
        self.__mi_coordinador = Coordinador(self.__mi_vista, self.__mi_sistema)
        self.__mi_vista.asignarControlador(self.__mi_coordinador)
        
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())   
  
p = Principal()
p.main()   