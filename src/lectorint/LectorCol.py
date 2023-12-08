import Lector


class LectorCol(Lector):

    def procesalinea(self, linea):
        daux = linea.split('|')
        coords = self.procesacoordenadas(daux[2])
        dpol = dict(nombre=daux[6].strip(), id=daux[5], cve_col=daux[4], coords=coords[0], clon=coords[1],
                    clat=coords[2])
        self.apoligonos.append(dpol)


