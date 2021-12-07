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


from typing import Dict
from DISClib.DataStructures.adjlist import degree, outdegree
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort 
assert cf
from DISClib.ADT import graph as gr
from math import radians, cos, sin, asin, sqrt
import math
from DISClib.ADT import minpq 
from DISClib.Algorithms.Graphs import dijsktra as djk

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initCatalog():
    catalog = mp.newMap(loadfactor=4)
    mp.put(catalog,"Ciudades",mp.newMap())
    mp.put(catalog,"DiGrafo",gr.newGraph(directed=True))
    mp.put(catalog,"Aereopuertos",mp.newMap())
    mp.put(catalog,"Grafo",gr.newGraph())
    mp.put(catalog,"Arbol_aereo",om.newMap())
    #El árbol está organizado por longitud
    return catalog

def subirciudad(catalog,city):
    ciudad = mp.newMap()
    mp.put(ciudad,"Nombre",city["city"])
    mp.put(ciudad,"Pais",city["country"])
    mp.put(ciudad,"Longitud",round(float(city["lng"]),2))
    mp.put(ciudad,"Latitud",round(float(city["lat"]),2))
    
    mapa = mp.get(catalog,"Ciudades")["value"]
    nombre = mp.get(ciudad,"Nombre")["value"]

    if mp.contains(mapa,nombre):
        lista = mp.get(mapa,nombre)["value"]
        lt.addLast(lista,ciudad)
    else:
        mp.put(mapa,nombre,lt.newList())
        lista = mp.get(mapa,nombre)["value"]
        lt.addLast(lista,ciudad)

def subir_aereopuerto(catalog,airport):
    #Crear aereopuerto
    aereopuerto = mp.newMap()
    mp.put(aereopuerto,"Nombre",airport["Name"])
    mp.put(aereopuerto,"Codigo",airport["IATA"])
    mp.put(mp.get(catalog,"Aereopuertos")["value"],mp.get(aereopuerto,"Codigo")["value"],aereopuerto)
    mp.put(aereopuerto,"Ciudad",airport["City"])
    mp.put(aereopuerto,"Pais",airport["Country"])
    mp.put(aereopuerto,"Latitud",round(float(airport["Latitude"]),2))
    mp.put(aereopuerto,"Longitud",round(float(airport["Longitude"]),2))

    #Subir a los grafos
    digrafo = mp.get(catalog,"DiGrafo")["value"]
    grafo = mp.get(catalog,"Grafo")["value"]
    iata = mp.get(aereopuerto,"Codigo")["value"]

    if not gr.containsVertex(digrafo,iata):
        gr.insertVertex(digrafo,iata)

    if not gr.containsVertex(grafo,iata):
        gr.insertVertex(grafo,iata)
    
    #Subir al árbol
    arbol = mp.get(catalog,"Arbol_aereo")["value"]
    add_or_create_om_in_om(arbol,mp.get(aereopuerto,"Longitud")["value"],mp.get(aereopuerto,"Latitud")["value"],aereopuerto)
    
    return aereopuerto


def subir_rutas(catalog,route):
    origen = route["Departure"]
    destino = route["Destination"]
    distancia = float(route["distance_km"])

#Carga digrafo
    digrafo = mp.get(catalog,"DiGrafo")["value"]
    if not gr.containsVertex(digrafo,origen):
        gr.insertVertex(digrafo,origen)
    if not gr.containsVertex(digrafo,destino):
        gr.insertVertex(digrafo,destino)

    adjacentes = gr.adjacents(digrafo,origen)
    contains = False
    for vertice in lt.iterator(adjacentes):
        if vertice == destino:
            contains = True
            break
    if not contains:
        gr.addEdge(digrafo,origen,destino,distancia)
#Carga grafo
    grafo = mp.get(catalog,"Grafo")["value"]
    if not gr.containsVertex(grafo,origen):
        gr.insertVertex(grafo,origen)
    if not gr.containsVertex(grafo,destino):
        gr.insertVertex(grafo,destino)
    if gr.getEdge(grafo,origen,destino) == None and gr.getEdge(digrafo,destino,origen):
        gr.addEdge(grafo,destino,origen,distancia)
    

# Funciones para agregar informacion al catalogo

def add_or_create_om_in_om(arbol,llave_arbol1,llave_arbol2,valor):
    if om.contains(arbol,llave_arbol1):
        arbol2 = om.get(arbol,llave_arbol1)["value"]
        if om.contains(arbol2,llave_arbol2):
            lista = om.get(arbol2,llave_arbol2)["value"]
            lt.addLast(lista,valor)
        else:
            om.put(arbol2,llave_arbol2,lt.newList("ARRAY_LIST"))
            lista = om.get(arbol2,llave_arbol2)["value"]
            lt.addLast(lista,valor)
    
    else:
        om.put(arbol,llave_arbol1,om.newMap())
        arbol2=om.get(arbol,llave_arbol1)["value"]
        om.put(arbol2,llave_arbol2,lt.newList("ARRAY_LIST"))
        lista = om.get(arbol2,llave_arbol2)["value"]
        lt.addLast(lista,valor)

# Funciones para creacion de datos

# Funciones de consulta

def mayor_grado(catalog):
    #digrafo
    grafo = mp.get(catalog,"Grafo")["value"]
    lista_vertices = gr.vertices(grafo)

    val_min = 10000000000
    lista_min = lt.newList("ARRAY_LIST")

    for vertice in lt.iterator(lista_vertices):
        diccionario = mp.newMap()
        mp.put(diccionario,"vertice",vertice)
        mp.put(diccionario,"grado",gr.degree(grafo,vertice))

        grado = gr.degree(grafo,vertice)
        if lt.size(lista_min)<6:
            lt.addLast(lista_min,diccionario)
            if grado < val_min:
                val_min = grado
        else:
            if grado > val_min:
                pos = 0
                for candidato_min in lt.iterator(lista_min):
                    pos += 1
                    if mp.get(candidato_min,"grado")["value"] == val_min:
                        lt.deleteElement(lista_min,pos)
                        lt.addLast(lista_min,diccionario)
                        break
                pos2 = 0
                val_min_nuevo = 10000000000
                for nuevo_cand_min in lt.iterator(lista_min):
                    pos2 += 1
                    if mp.get(nuevo_cand_min,"grado")["value"] < val_min_nuevo:
                        val_min_nuevo = mp.get(nuevo_cand_min,"grado")["value"]
                
                val_min = val_min_nuevo
                

    insertionsort.sort(lista_min,compare_degree)

    digrafo = mp.get(catalog,"DiGrafo")["value"]
    lista_vertices = gr.vertices(digrafo)

    val_min = 10000000000
    lista_min_digra = lt.newList("ARRAY_LIST")

    for vertice in lt.iterator(lista_vertices):
        diccionario = mp.newMap()
        mp.put(diccionario,"vertice",vertice)
        mp.put(diccionario,"grado",gr.outdegree(digrafo,vertice)+gr.indegree(digrafo,vertice))
        mp.put(diccionario,"entrada",gr.indegree(digrafo,vertice))
        mp.put(diccionario,"salida",gr.outdegree(digrafo,vertice))

        grado = gr.outdegree(grafo,vertice) + gr.indegree(digrafo,vertice)
        if lt.size(lista_min_digra)<6:
            lt.addLast(lista_min_digra,diccionario)
            if grado < val_min:
                val_min = grado
        else:
            if grado > val_min:
                pos = 0
                for candidato_min in lt.iterator(lista_min_digra):
                    pos += 1
                    if mp.get(candidato_min,"grado")["value"] == val_min:
                        lt.deleteElement(lista_min_digra,pos)
                        lt.addLast(lista_min_digra,diccionario)
                        break
                pos2 = 0
                val_min_nuevo = 10000000000
                for nuevo_cand_min in lt.iterator(lista_min_digra):
                    pos2 += 1
                    if mp.get(nuevo_cand_min,"grado")["value"] < val_min_nuevo:
                        val_min_nuevo = mp.get(nuevo_cand_min,"grado")["value"]
                
                val_min = val_min_nuevo
                

    insertionsort.sort(lista_min_digra,compare_degree)
    return lista_min,lista_min_digra

def aereopuerto_cercano(ciudad,catalog):
    lat = float(mp.get(ciudad,"Latitud")["value"])
    lon = float(mp.get(ciudad,"Longitud")["value"])
    rango = 10
    encontrado = False

    while not encontrado:
        (latMax,latMin,lonMax,lonMin) = coordenadasMaximas(lon,lat,rango)
        lista = busqueda_aerea(catalog,lonMin,lonMax,latMin,latMax)
        if lt.size(lista) != 0:
            encontrado = True
        else:
            rango += 10
    
    aereopuerto = mas_cercano(lista,lat,lon)
    return mp.get(aereopuerto,"aereopuerto")["value"]
        
    
def compare_degree(dict1,dict2):
    if mp.get(dict1,"grado")["value"]>mp.get(dict2,"grado")["value"]:
        return True
    else:
        return False

def mas_cercano(lista,lat,lon):
    lista_dict = minpq.newMinPQ(compare_distance)
    for aereopuerto in lt.iterator(lista):
        diccionario = mp.newMap()
        mp.put(diccionario,"aereopuerto",aereopuerto)
        mp.put(diccionario,"distancia",haversine(lon,lat,mp.get(aereopuerto,"Longitud")["value"],mp.get(aereopuerto,"Latitud")["value"]))
        minpq.insert(lista_dict,diccionario)
    return minpq.min(lista_dict)

def ruta_corta(catalog,inicio,fin):
    grafo = mp.get(catalog,"Grafo")["value"]
    inicio = mp.get(inicio,"Codigo")["value"]
    caminos_grafo = djk.Dijkstra(grafo,inicio)
    fin = mp.get(fin,"Codigo")["value"]
    camino_grafo =djk.pathTo(caminos_grafo,fin)

    digrafo = mp.get(catalog,"DiGrafo")["value"]
    caminos_di = djk.Dijkstra(digrafo,inicio)
    camino_digrafo =djk.pathTo(caminos_di,fin)

    return camino_grafo,camino_digrafo

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)

    Codigo obtenido de: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def coordenadasMaximas(longitude,latitude,km):

    dlat = (1/110)*km 
    
    latMax=latitude + dlat
    latMin=latitude  -  dlat

    dlon = (1/(111*cos(latitude*(math.pi/180))))*km

    lonMax= longitude + dlon
    lonMin=longitude - dlon

    return (latMax,latMin,lonMax,lonMin)

def busqueda_aerea(catalog,lon_min,lon_max,lat_min,lat_max):
    arbol_Lon = mp.get(catalog,"Arbol_aereo")["value"]
    lista_retorno = lt.newList("ARRAY_LIST")
    
    lon_min = om.ceiling(arbol_Lon,lon_min)
    lon_max = om.floor(arbol_Lon,lon_max)

    if lon_min != None and lon_max != None:
        rango_lon = om.values(arbol_Lon,lon_min,lon_max)

        for arbol_Lat in lt.iterator(rango_lon):
            lat_min_in = om.ceiling(arbol_Lat,lat_min)
            lat_max_in = om.floor(arbol_Lat,lat_max)
            if lat_min_in !=None and lat_max_in != None:
                rango_lat = om.values(arbol_Lat,lat_min_in,lat_max_in)
                for latitud in lt.iterator(rango_lat):
                    for avistamiento in lt.iterator(latitud):
                        lt.addLast(lista_retorno,avistamiento)
    
    return lista_retorno

def compare_distance(dict1,dict2):
    if mp.get(dict1,"distancia")["value"] > mp.get(dict2,"distancia")["value"]:
        return True
    else:
        return False
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
