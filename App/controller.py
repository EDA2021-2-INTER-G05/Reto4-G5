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
    file = cf.data_dir + "worldcities.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for ciudad in input_file:
        model.subirciudad(catalog,ciudad)

def cargar_aereopuertos(catalog):
    file = cf.data_dir + "airports_full.csv"
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
    file = cf.data_dir + "routes_full.csv"
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for ruta in input_file:
        model.subir_rutas(catalog,ruta)

def mayor_grado(catalog):
    return model.mayor_grado(catalog)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
