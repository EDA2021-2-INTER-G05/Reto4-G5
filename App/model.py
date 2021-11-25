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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import graph as gr

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = mp.newMap(loadfactor=4)
    mp.put(catalog,"Ciudades",mp.newMap())
    mp.put(catalog,"Grafo",gr.newGraph())
    mp.put(catalog,"Aereopuertos",mp.newMap())
    return catalog

def subirciudad(catalog,city):
    ciudad = mp.newMap()
    mp.put(ciudad,"Nombre",city["city"])
    mp.put(ciudad,"aereopuertos",lt.newList())

    mp.put(mp.get(catalog,"Ciudades")["value"],mp.get(ciudad,"Nombre")["value"],ciudad)

def subir_aereopuerto(catalog,airport):
    aereopuerto = mp.newMap()
    mp.put(aereopuerto,"Nombre",airport["Name"])
    mp.put(aereopuerto,"Codigo",airport["IATA"])
    mp.put(mp.get(catalog,"Aereopuertos")["value"],mp.get(aereopuerto,"Codigo")["value"],aereopuerto)


    contains = mp.contains(mp.get(catalog,"Ciudades")["value"],airport["City"])
    if not contains:
        mp.put(mp.get(catalog,"Ciudades")["value"],airport["City"],mp.newMap())
        ciudad = mp.get(mp.get(catalog,"Ciudades")["value"],airport["City"])["value"]
        mp.put(ciudad,"Nombre",airport["City"])
        mp.put(ciudad,"aereopuertos",lt.newList())

    ciudad = mp.get(mp.get(catalog,"Ciudades")["value"],airport["City"])["value"]
    mp.put(aereopuerto,"Ciudad",ciudad)
    nombre_ciudad = mp.get(mp.get(aereopuerto,"Ciudad")["value"],"Nombre")["value"]

    lista = mp.get(mp.get(mp.get(catalog,"Ciudades")["value"],nombre_ciudad)["value"],"aereopuertos")["value"]
    lt.addLast(lista,aereopuerto)

def subir_rutas(catalog,route):
    origen = route["Departure"]
    destino = route["Destination"]
    distancia = route["distance_km"]

    grafo = mp.get(catalog,"Grafo")["value"]

    if not gr.containsVertex(grafo,origen):
        gr.insertVertex(grafo,origen)
    
    if not gr.containsVertex(grafo,destino):
        gr.insertVertex(grafo,destino)

    adjacentes = gr.adjacentEdges(grafo,origen)

    contains = False
    for vertice in adjacentes:
        if vertice == destino:
            contains = True
            break

    if not contains:
        gr.addEdge(grafo,origen,destino,distancia)


    

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
