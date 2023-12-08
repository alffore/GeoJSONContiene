import sys
import json
import csv
import shapely
from shapely import Point, Polygon, contains
from multiprocessing import Pool

recs = []
recs_aprox = []

recs_clas = []
recs_clas_aprox = []

apoligonos = []


def lee_recursos(archivo):
    with open(archivo) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            recs.append(row)


def lee_poligonos(archivo):
    with open(archivo, "r") as read_file:
        data = json.load(read_file)

        for d in data['features']:
            if d['geometry']['type'] == 'Polygon':
                procesa_poligonos(d['properties']['cve_col'], d['geometry']['coordinates'][0])
            elif d['geometry']['type'] == 'MultiPolygon':
                for pols in d['geometry']['coordinates']:
                    procesa_poligonos(d['properties']['damage_gra'], pols[0])


def procesa_poligonos(grado, poligono):
    """
    Función que recupera los poligonos y el grado de daño
    :param grado:
    :param poligono:
    :return:
    """
    global apoligonos

    aux_pol = [(c[0], c[1]) for c in poligono]
    aux = dict(grado=grado, poligono=Polygon(aux_pol))
    apoligonos.append(aux)


def procesa(recurso):
    """
    Función que checa si el punto del recurso se encuentra contenido en un poligono
    :param recurso:
    :return:
    """
    global apoligonos

    p = Point(float(recurso[3]), float(recurso[4]))

    for d in apoligonos:
        if contains(d['poligono'], p):
            return [d['grado'], recurso, 'C']

    return [None, recurso]


def procesa_aprox(recurso):
    global apoligonos

    dmin = 1E10
    grado_min = ''
    p = Point(float(recurso[3]), float(recurso[4]))
    for d in apoligonos:
        daux = shapely.distance(d['poligono'], p)
        if daux < dmin:
            dmin = daux
            grado_min = d['grado']

    return [grado_min, recurso, 'E']


if __name__ == '__main__':
    ARCHIVO_POL1 = sys.argv[1]
    ARCHIVO_REC = sys.argv[2]

    lee_recursos(ARCHIVO_REC)
    print(recs)
    lee_poligonos(ARCHIVO_POL1)

    p = Pool(8)
    resultados = p.map(procesa, recs)

    # filtramos los que faltan por clasificar
    for res in resultados:
        if res[0] is None:
            recs_aprox.append(res[1])
        else:
            recs_clas.append(res)

    # paprox = Pool(8)
    # resultados_aprox = paprox.map(procesa_aprox, recs_aprox)
    #
    # recs_clas = recs_clas + resultados_aprox
    # print(recs_clas)

    with open(f'{ARCHIVO_REC}_salida.txt', 'w') as ft:
        for r in recs_clas:
            aux = [r[1][0], r[1][2], r[0], r[2]]
            ft.write("|".join(aux))
            ft.write("\n")
