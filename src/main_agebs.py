# python main_agebs.py /home/alfonso/devel/ageb_ints/09a_cg.int  /DISCO1/MAPAS/cdmx/puntos.csv  /DISCO1/MAPAS/cdmx/puntos_agebs.csv

import sys
import csv
from shapely import Point, Polygon, contains
from multiprocessing import Pool
import LectorAgeb as lec

NUM_PROC = 12

puntos = []
poligonos = []

aPols = []
aPuntos = []


def lee_recursos(archivo):
    with open(archivo) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            if i > 0:
                puntos.append(row)
            i += 1


def lee_ints(archivo):
    global poligonos
    lectorpol = lec.LectorAgeb(archivo)
    lectorpol.lector()
    poligonos = lectorpol.obtenpoligonos()


def procesapoligono(poligono):
    aux_pol = [(c[0], c[1]) for c in poligono['coords']]
    aux = dict(cve_mnz=poligono['cve_mnz'], poligono=Polygon(aux_pol))
    return aux


def procesapunto(p):
    punto = Point(float(p[1]), float(p[2]))
    return dict(id=p[0], punto=punto)


def buscacontenido(punto):
    for pol in aPols:
        if contains(pol['poligono'], punto['punto']):
            return dict(cve_mnz=pol['cve_mnz'], id=punto['id'])


if __name__ == '__main__':
    ARCHIVO_POL1 = sys.argv[1]
    ARCHIVO_REC = sys.argv[2]
    ARCHIVO_SAL = sys.argv[3]

    lee_recursos(ARCHIVO_REC)
    lee_ints(ARCHIVO_POL1)

    # print(puntos)
    # print(poligonos)

    for pol in poligonos:
        aPols.append(procesapoligono(pol))

    for pun in puntos:
        aPuntos.append(procesapunto(pun))

    p = Pool(NUM_PROC)
    res = p.map(buscacontenido, aPuntos)

    #print(res)

    with open(ARCHIVO_SAL, "w") as fs:
        for r in res:
            if r is not None:
                fs.write(f"{r['id']},{r['cve_mnz']}\n")
