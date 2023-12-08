class Lector:

    def __init__(self, archivo):
        self.archivo = archivo
        self.apoligonos = []

    def lector(self):
        with open(self.archivo, "r") as fr:
            lineas = fr.readlines()
            for linea in lineas:
                self.procesalinea(linea)

    def procesalinea(self, linea):
        pass

    def procesacoordenadas(self, coords):
        caux = coords.split(',')
        apuntos = []

        lat = 0.0
        lon = 0.0

        for i in range(0, len(caux), 2):
            apuntos.append([float(caux[i]), float(caux[i + 1])])
            lat += float(caux[i + 1])
            lon += float(caux[i])

        tam = len(apuntos)
        lat /= tam
        lon /= tam
        return apuntos, lon, lat

    def obtenpoligonos(self):
        return self.apoligonos
