﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from prettytable import PrettyTable


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def initCatalog():
    return controller.initCatalog()
def loadData(catalog):
    return controller.loadData(catalog)

def print_mayor_grado(lista_gra,lista_digra,catalog):
    print("Para el grafo:")
    tabla = PrettyTable()
    tabla.field_names =["Nombre","Ciudad","País","IATA","Conecciones"]
    for diccionario in lt.iterator(lista_gra):
        aereopuerto = mp.get(mp.get(catalog,"Aereopuertos")["value"],mp.get(diccionario,"vertice")["value"])["value"]
        tabla.add_row([mp.get(aereopuerto,"Nombre")["value"],mp.get(aereopuerto,"Ciudad")["value"],mp.get(aereopuerto,"Pais")["value"],mp.get(aereopuerto,"Codigo")["value"],mp.get(diccionario,"grado")["value"]])
    print(tabla)

    print("Para el digrafo:")
    tabla = PrettyTable()
    tabla.field_names =["Nombre","Ciudad","País","IATA","Conecciones totales","Conecciones llegada","Conecciones salida"]
    for diccionario in lt.iterator(lista_digra):
        aereopuerto = mp.get(mp.get(catalog,"Aereopuertos")["value"],mp.get(diccionario,"vertice")["value"])["value"]
        tabla.add_row([mp.get(aereopuerto,"Nombre")["value"],mp.get(aereopuerto,"Ciudad")["value"],mp.get(aereopuerto,"Pais")["value"],mp.get(aereopuerto,"Codigo")["value"],mp.get(diccionario,"grado")["value"],mp.get(diccionario,"entrada")["value"],mp.get(diccionario,"salida")["value"]])
    print(tabla)

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea")
    print("2- Encontrar clústeres de tráfico aéreo")
    print("3- Encontrar la ruta más corta entre ciudades")
    print("4- Utilizar las millas de viajero")
    print("5- Cuantificar el efecto de un aeropuerto cerrado")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        datos = loadData(catalog)
        digrafo = mp.get(catalog,"DiGrafo")["value"]
        grafo = mp.get(catalog,"Grafo")["value"]
        print("Digrafo:")
        print(gr.numVertices(digrafo))
        print(gr.numEdges(digrafo))
        print("Grafo:")
        print(gr.numVertices(grafo))
        print(gr.numEdges(grafo))

    elif int(inputs[0]) == 1:
        resultado = controller.mayor_grado(catalog)
        print_mayor_grado(resultado[0],resultado[1],catalog)

    else:
        sys.exit(0)
sys.exit(0)
