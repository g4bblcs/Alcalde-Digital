class NodoDecision:
    def __init__(self, texto, consecuencia=None, etiqueta=None):
        self.texto = texto
        self.consecuencia = consecuencia
        self.etiqueta = etiqueta
        self.izquierda = None
        self.derecha = None        

    def es_hoja(self):
        return self.izquierda is None and self.derecha is None