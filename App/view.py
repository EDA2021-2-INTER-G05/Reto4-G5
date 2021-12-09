"""
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
from DISClib.DataStructures.adjlist import numEdges
from DISClib.DataStructures import mapentry as me
import time


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

def print_info(catalog,primero,fila):
    digrafo = mp.get(catalog,"DiGrafo")["value"]
    grafo = mp.get(catalog,"Grafo")["value"]
    tabla = PrettyTable()
    tabla.field_names = ["Tipo de Grafo","Número de aereopuertos","Número de rutas"]
    tabla.add_row(["Grafo no dirigido",gr.numVertices(grafo),numEdges(grafo)])
    tabla.add_row(["Grafo dirigido",gr.numVertices(digrafo),numEdges(digrafo)])
    print(tabla)
    print("El primer y último aereopuerto cargado fueron: ")
    tabla = PrettyTable()
    tabla.field_names = ["IATA","Nombre","Ciudad","País","Latitud","Longitud"]
    tabla.add_row([mp.get(primero,"Codigo")["value"],mp.get(primero,"Nombre")["value"],mp.get(primero,"Ciudad")["value"],mp.get(primero,"Pais")["value"],mp.get(primero,"Latitud")["value"],mp.get(primero,"Longitud")["value"]])
    ultimo = lt.getElement(fila,1)
    tabla.add_row([mp.get(ultimo,"Codigo")["value"],mp.get(ultimo,"Nombre")["value"],mp.get(ultimo,"Ciudad")["value"],mp.get(ultimo,"Pais")["value"],mp.get(ultimo,"Latitud")["value"],mp.get(ultimo,"Longitud")["value"]])
    print(tabla)
def print_aeropuerto(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre", "Ciudad", 'Pais','Latitud','Longitud'])
        x._max_width = {"Nombre" : 20, "Ciudad" : 20,"Pais" : 20, "Latitud" : 20,"Longitud" : 20}
        x.add_row([author['Name']+'\n', author['City'], author['Country'],author['Latitude'],author['Longitude']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_ciudades(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre", "Poblacion", 'Latitud','Longitud'])
        x._max_width = {"Nombre" : 20, "Poblacion" : 20,"Latitud" : 20, "Longitud" : 20}
        x.add_row([author['city']+'\n', author['population'], author['lat'],author['lng']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_opciones(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Opcion","Ciudad", "Pais",'Admin','Latitud','Longitud'])
        x._max_width = {"Opcion" : 20,"Ciudad" : 20, "Pais" : 20, "Admin" : 20,"Latitud" : 20,"Longitud" : 20}
        numero = 1
        for artistas in lt.iterator(me.getValue(author)['repetidas']):
            x.add_row([numero, artistas['city'],artistas['country'],artistas['admin_name'],artistas['lat'],artistas['lng']])
            numero += 1
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_ciudades_opciones(author):
    """
    Imprime la información del autor seleccionado
    """
    if author == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif author:
        print("\n")
        x = PrettyTable(["Nombre","Pais","Admin","Poblacion", 'Latitud','Longitud'])
        x._max_width = {"Nombre" : 20,"Pais" : 20,"Admin" : 20, "Poblacion" : 20,"Latitud" : 20, "Longitud" : 20}
        x.add_row([author['city']+'\n', author['country'],author['admin_name'],author['population'], author['lat'],author['lng']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_aaeropuertos_conectados(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["Nombre", "Ciudad", 'Pais','AITA','Total','Inbound','Outbound'])
        x._max_width = {"Nombre" : 20, "Ciudad" : 20,"Pais" : 20, "AITA" : 20,"Total" : 20,"Inbound" : 20,"Outbound" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            valor = me.getValue(mp.get(cont['infoaeropuertos'],aeropuerto['aeropuerto']))
            x.add_row([valor['Name']+'\n', valor['City'], valor['Country'],valor['IATA'],aeropuerto['cantidadtotal'],aeropuerto['cantidadentrada'],aeropuerto['cantidadsalida']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_aeropuerto_LISTA(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["IATA",'Nombre','Ciudad','Pais'])
        x._max_width = {"IATA" : 20, "Nombre" : 20,"Ciudad" : 20, "Pais" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            info_aeropuerto = me.getValue(mp.get(cont['aeropuertos'],aeropuerto))
            x.add_row([info_aeropuerto['IATA']+'\n', info_aeropuerto['Name'], info_aeropuerto['City'],info_aeropuerto['Country']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_camino(aeropuertos):
    """
    Imprime la información del autor seleccionado
    """
    if aeropuertos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif aeropuertos:
        print("\n")
        x = PrettyTable(["Salida",'Llegada','Distancia'])
        x._max_width = {"Salida" : 20, "Llegada" : 20,"Distancia" : 20}
        for aeropuerto in lt.iterator(aeropuertos):
            x.add_row([aeropuerto['vertexA']+'\n', aeropuerto['vertexB'], aeropuerto['weight']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')


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

def print_caminos(camino_gra,camino_di):
    print("Para el grafo no dirigido:")
    if camino_gra == None:
        print("No existe una ruta entre los dos aereopuertos más cercanos a las ciudades escogidas")
    else:
        tabla = PrettyTable()
        tabla.field_names = ["Inicio","Fin","Distancia"]
        distancia_acu = 0
        for parada in lt.iterator(camino_gra):
            tabla.add_row([parada["vertexA"],parada["vertexB"],parada["weight"]])
            distancia_acu += float(parada["weight"])
        print(tabla)
        print("Distancia total: " + str(round(distancia_acu,2))+" km")
    
    print("Para el grafo dirigido:")
    if camino_di == None:
        print("No existe una ruta entre los dos aereopuertos más cercanos a las ciudades escogidas")
    else:
        tabla = PrettyTable()
        tabla.field_names = ["Inicio","Fin","Distancia"]
        distancia_acu = 0
        for parada in lt.iterator(camino_di):
            tabla.add_row([parada["vertexA"],parada["vertexB"],parada["weight"]])
            distancia_acu += float(parada["weight"])
        print(tabla)
        print("Distancia total: " + str(round(distancia_acu,2))+" km")


def escoger_ciudad(ciudad,catalog):
    lista = mp.get(mp.get(catalog,"Ciudades")["value"],ciudad)["value"]
    if lt.size(lista) == 1:
        return lt.getElement(lista,1)
    else:
        print("Existe más de una ciudad con el nombre seleccionado. Por favor seleccione la que desea escoger")
        contador = 1
        for ciudad in lt.iterator(lista):
            print(contador)
            tabla = PrettyTable()
            tabla.field_names=["Nombre","País","Longitud","Latitud"]
            tabla.add_row([mp.get(ciudad,"Nombre")["value"],mp.get(ciudad,"Pais")["value"],mp.get(ciudad,"Longitud")["value"],mp.get(ciudad,"Latitud")["value"]])
            print(tabla)
            contador += 1
        
        pos = int(input("Ingrese el número de la ciudad que desea escoger: "))
        return lt.getElement(lista,pos)


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
        start_time = time.process_time()
        catalog = initCatalog()
        datos = loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_info(catalog,datos[0],datos[1])
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")
        cont = controller.init()
        controller.loadAirportsRutes(cont)
    elif int(inputs[0]) == 1:
        start_time = time.process_time()
        resultado = controller.mayor_grado(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_mayor_grado(resultado[0],resultado[1],catalog)
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 2:
        
        print('aqui se ve a presentar el cluster prsente en la red de aeropuertos y una comparacion')
        codigo1 = input('Escriba el codigo del primer aeropuerto: ')
        codigo2 = input('Escriba el codigo del segundo aeropuerto: ')
        start_time = time.process_time()
        respuesta = controller.Encontrar_clusters(cont,codigo1,codigo2)
        print('\n' + 'El numero de elementos fuertemente conectados es de:' + str(respuesta[0]))
        print('\n' + 'Los dos vertices pertenecen al mismo cluster:' + str(respuesta[1]))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 3:
        inicio = input("Ingrese el nombre de la ciudad de inicio: ")
        inicio = escoger_ciudad(inicio,catalog)
        fin = input("Ingrese el nombre de la ciudad final: ")
        fin = escoger_ciudad(fin,catalog)
        start_time = time.process_time()
        resultado = controller.ruta_corta(catalog,inicio,fin)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print_caminos(resultado[0],resultado[1])
        print("Tiempo requerido: "+ str(elapsed_time_mseg) + " mseg")

    elif int(inputs[0]) == 4:
        print('aqui se ve a presentar la red expansion minima')
        ciudad1 = input('Escriba el nombre de la ciudad de origen: ')
        opcion_origen = controller.opciones_ciudades(cont,ciudad1)
        print_opciones(opcion_origen)
        ciudad_origen = input('Escriba la opcion de la tabla de arriba que desea buscar: ')
        info_ciudad_origen = lt.getElement(me.getValue(opcion_origen)['repetidas'],int(ciudad_origen))
        print_ciudades_opciones(info_ciudad_origen)
        aeropuerto1 = controller.aeropuertoopciones(cont,info_ciudad_origen)
        millas = input('Escriba la cantidad de millas que tiene: ')
        start_time = time.process_time()
        respuesta = controller.millas_viajero(cont,aeropuerto1['aeropuerto'],millas)
        print('\n' + 'El numero de nodos conectados es:' + str(respuesta[0]))
        print('\n' + 'El costo total de la red de expansion es de:' + str(respuesta[1]))
        print_camino(respuesta[2])
        print('\n' + respuesta[3] + 'millas para la ruta mas larga')
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

    elif int(inputs[0]) == 5:
        
        codigo1 = input('Escriba el codigo del aeropuerto que sale de funcionamiento: ')
        start_time = time.process_time()
        respuesta = controller.quinto_req(cont,codigo1)
        print('\n' + 'El numero de rutas restantes es de (en el digrafo): ' + str(respuesta[0]))
        print('\n' + 'El numero de rutas restantes es de (en el grafo no dirigido): ' + str(respuesta[1]))

        print('\n' + 'El numero de aeropuertos afectados en totalidad:' + str(respuesta[8]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[9])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[10])

        print('\n' + 'El numero de aeropuertos afectados en el grafo no dirigido: ' + str(respuesta[2]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[3])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[4])

        print('\n' + 'El numero de aeropuertos afectados en el grafo dirigido: ' + str(respuesta[5]))
        print('\n' + 'La lista de los primeros 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[6])
        print('\n' + 'La lista de los ultimos 3 aeropuertos son los siguientes: ')
        print_aeropuerto_LISTA(respuesta[7])

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    else:
        sys.exit(0)
sys.exit(0)
