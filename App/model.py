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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort 
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
    mp.put(catalog,"DiGrafo",gr.newGraph(directed=True))
    mp.put(catalog,"Aereopuertos",mp.newMap())
    mp.put(catalog,"Grafo",gr.newGraph())
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
    mp.put(aereopuerto,"Ciudad",airport["City"])
    mp.put(aereopuerto,"Pais",airport["Country"])


    digrafo = mp.get(catalog,"DiGrafo")["value"]
    grafo = mp.get(catalog,"Grafo")["value"]
    iata = mp.get(aereopuerto,"Codigo")["value"]

    if not gr.containsVertex(digrafo,iata):
        gr.insertVertex(digrafo,iata)

    if not gr.containsVertex(grafo,iata):
        gr.insertVertex(grafo,iata)

def subir_rutas(catalog,route):
    origen = route["Departure"]
    destino = route["Destination"]
    distancia = route["distance_km"]


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
        gr.addEdge(grafo,destino,origen)
    


# Funciones para agregar informacion al catalogo

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
    

    
def compare_degree(dict1,dict2):
    if mp.get(dict1,"grado")["value"]>mp.get(dict2,"grado")["value"]:
        return True
    else:
        return False


        




# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
