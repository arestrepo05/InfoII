class Servicio(object):
    def __init__(self):
        self.__usuarios = {}
        self.__usuarios['bio12345'] = 'medicoAnalitico'  
    def verificarUsuario(self, u, c):
        try:
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except: 
            return False