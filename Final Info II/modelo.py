class Servicio(object):
    def __init__(self):
        self.__usuarios = {}
        self.__usuarios['0505'] = 'Alejandro'
        self.__usuarios['1234'] = 'Sebastian'  

    def verificarUsuario(self, u, c):
        try:
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except KeyError:
            return False
