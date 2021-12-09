"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT import queue as que


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    return model.initCatalog()

def loadData(catalog):
    cargar_ciudades(catalog)
    datos = cargar_aereopuertos(catalog)
    cargar_rutas(catalog)
    return datos

def cargar_ciudades(catalog):
    file = cf.data_dir + "worldcities-utf8.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for ciudad in input_file:
        model.subirciudad(catalog,ciudad)

def cargar_aereopuertos(catalog):
    file = cf.data_dir + "airports-utf8-large.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    contador = 1
    fila = que.newQueue()

    for aereopuerto in input_file:
        actual = model.subir_aereopuerto(catalog,aereopuerto)
        if contador == 1:
            primero = actual
            que.enqueue(fila,actual)
        else:
            que.dequeue(fila)
            que.enqueue(fila,actual)
        contador +=1
        
    return primero,fila

def cargar_rutas(catalog):
    file = cf.data_dir + "routes-utf8-large.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for ruta in input_file:
        model.subir_rutas(catalog,ruta)

def mayor_grado(catalog):
    return model.mayor_grado(catalog)

def ruta_corta(catalog,inicio,fin):
    inicio = model.aereopuerto_cercano(inicio,catalog)
    fin = model.aereopuerto_cercano(fin,catalog)
    resultado = model.ruta_corta(catalog,inicio,fin)
    return resultado

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

def loadAirportsRutes(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    airportsfile = cf.data_dir + 'airports-utf8-small.csv'
    rutasfile = cf.data_dir + 'routes-utf8-small.csv'
    ciudaesfile = cf.data_dir + 'worldcities-utf8.csv'

    input_file_aeropuertos = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")

    input_file_rutas = csv.DictReader(open(rutasfile, encoding="utf-8"),
                                delimiter=",")

    input_file_ciudades = csv.DictReader(open(ciudaesfile, encoding="utf-8"),
                                delimiter=",")

    for aeropuerto in input_file_aeropuertos:
        model.addVerticeGrafo(analyzer,aeropuerto)

    for ruta in input_file_rutas:
        model.addRuta(analyzer,ruta)

    for ciudad in input_file_ciudades:
        model.addCiudad(analyzer,ciudad)

    model.addRutaidayvuleta(analyzer)

def infoaeropuerto(analyzer,codigoAita):
    informacion = model.infoaeropuerto(analyzer,codigoAita)
    return informacion



def Encontrar_clusters(analyzer,codigo1,codigo2):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    conectados = model.Encontrar_clusters(analyzer,codigo1,codigo2)
    return conectados

def millas_viajero(analyzer,codigo,millas):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    caminos = model.millas_viajero(analyzer,codigo,millas)
    return caminos

def quinto_req(analyzer,codigo):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    afectados = model.quinto_req(analyzer,codigo)
    return afectados

def opciones_ciudades(analyzer,ciudad):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    ciudades = model.opciones_ciudades(analyzer,ciudad)
    return ciudades

def aeropuertoopciones(analyzer,ciudad):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    aeropuertos = model.aeropuertoopciones(analyzer,ciudad)
    return aeropuertos