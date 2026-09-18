class NodoDecision:
    def __init__(self, texto, consecuencia=None):
        self.texto = texto              
        self.consecuencia = consecuencia 
        self.izquierda = None           
        self.derecha = None             

    def es_hoja(self):
        return self.izquierda is None and self.derecha is None