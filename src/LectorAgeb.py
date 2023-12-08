from lectorint.Lector import Lector


class LectorAgeb(Lector):

    def procesalinea(self, linea):
        daux = linea.split('|')
        coords = self.procesacoordenadas(daux[2])
        dpol = dict(mid=daux[5], lid=daux[6].strip(), eid=daux[4], cve_mnz=daux[3], coords=coords[0], clon=coords[1],
                    clat=coords[2])
        self.apoligonos.append(dpol)
