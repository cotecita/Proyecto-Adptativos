import os
import sys
import time
import random
import heapq
import math
from copy import deepcopy
import asyncio

def ChooseInstance(instance):
    dataset_path = "dataset_grafos_no_dirigidos"
    first_dataset_path = os.path.join(dataset_path, "new_1000_dataset")
    second_dataset_path = os.path.join(dataset_path, "new_2000_dataset")
    third_dataset_path = os.path.join(dataset_path, "new_3000_dataset")

    script_dir = os.path.dirname(__file__)

    first_dataset_path = os.path.join(script_dir, first_dataset_path)
    second_dataset_path = os.path.join(script_dir, second_dataset_path)
    third_dataset_path = os.path.join(script_dir, third_dataset_path)

    if "erdos_n1000" in instance:
        return first_dataset_path
    elif "erdos_n2000" in instance:
        return second_dataset_path
    elif "erdos_n3000" in instance:
        return third_dataset_path
    
def FillInitialAdjMatrix(init_mat, file, total_nodes):
    graph_matrix = [[0 for _ in range(total_nodes)] for _ in range(total_nodes)]
    for line in file:
        ab_nodes = line.split()
        a_node = int(ab_nodes[0])
        b_node = int(ab_nodes[1])

        graph_matrix[a_node][b_node] += 1
        graph_matrix[b_node][a_node] += 1
    
        
    init_mat[:] = deepcopy(graph_matrix)
        
#f es un directorio de os.listdir(directory)
def egreedy(nodes_selected, f, init_mat, determinismo, size_lista):
    
    #print("processing " + filename)
    inst_start = time.time()
    total_nodes = int(f.readline())

    nodes_in_mis = 0

    graph_matrix = []

    graph_matrix[:] = deepcopy(init_mat)
    
    total_neighbors = [0 for _ in range(total_nodes)]
    
    #print("counting neighbours...")
    #aquí se cuentan los vecinos de cada nodo
    for i in range(total_nodes):
        for j in range(total_nodes):
            if(graph_matrix[i][j] == 1):
                total_neighbors[i] += 1

    remaining_nodes = total_nodes

    while remaining_nodes > 0:
        #este loop es para ir borrando el nodo con menos vecinos
        #si el nodo es -1 entonces ya se agregó al MIS
        min_value = total_nodes
        min_index=-1

        #aquí se ve qué nodo tiene menos vecinos y su índice
        #print("selecting node with the least neighbours...")
        for j in range(len(total_neighbors)):
            if total_neighbors[j] < min_value and total_neighbors[j] > -1:
                min_value = total_neighbors[j]
                min_index = j

        if min_index == -1:
            break

        #Este paso es exlusivo del e-greedy: tiramos una moneda (de 0 a 100). Si la moneda es menor a determinismo
        #entonces hacemos lista de mejores candidatos y seleccionamos uno al azar.
        randvalue = random.randint(0, 100)
        if randvalue < determinismo:
            #print("random!")
            best_nodes = []
            best_nodes = total_neighbors[:]
            indexed_list = list(enumerate(best_nodes))
            sorted_indexed_list = sorted(indexed_list, key=lambda item: item[1])
            
            new_tuple = tuple(x for x in sorted_indexed_list if x[1] != -1)
            
            index_select = random.randint(0, min(size_lista, len(new_tuple)) - 1)
            min_value = new_tuple[index_select][1]
            min_index = new_tuple[index_select][0]

        #print("node selected: " + str(min_index))
        nodes_selected.append(min_index)
        total_neighbors[min_index] = -1
        nodes_in_mis += 1

        #aquí borramos el nodo elegido y sus vecinos de la matriz de adyacencia
        #print("cleaning selected node...")
        for i in range(len(total_neighbors)):

            #este loop es para borrar todo rastro del vecino
            if graph_matrix[min_index][i] == 1:
                total_neighbors[i] = -1
                for j in range(len(total_neighbors)):
                    graph_matrix[j][i] = 0
                    graph_matrix[i][j] = 0

            #y aquí borramos el nodo
            graph_matrix[i][min_index] = 0
            graph_matrix[min_index][i] = 0

        #se reinician los nodos de cada vecino menos de los elegidos (y debería borrar a sus vecinos igual)
        #print("resetting neighbours...")
        for i in range(len(total_neighbors)):
            if total_neighbors[i]>-1:
                total_neighbors[i] = 0
        
        remaining_nodes = 0
        #aquí se ve cuantos nodos quedan y se agregan al mis los que no tienen vecinos
        #print("counting remaining nodes and adding to MIS")
        for i in range(total_nodes):
            if total_neighbors[i] == -1:
                continue
            
            for j in range(total_nodes):
                if(graph_matrix[i][j] == 1):
                    total_neighbors[i] += 1

            if total_neighbors[i] > 0:
                remaining_nodes += 1
            elif total_neighbors[i] == 0:
                nodes_in_mis += 1
                total_neighbors[i] = -1
        #print("nodes in mis: " + str(nodes_in_mis))
        #print("remaining nodes: " + str(remaining_nodes))
        #print(nodes_selected)
        

    #print("repetidos? " + str(len(nodes_selected) != len(set(nodes_selected))))
    #print("Nodos en grafo: " + str(nodes_in_mis))
    #inst_end = time.time()
    #inst_total_time = inst_end - inst_start
    #print("Listo en " + str(inst_total_time) + " segundos")
    #total_density_time += inst_total_time
    #total_density_nodes += nodes_in_mis

import heapq

def egreedy2(nodes_selected, f, init_mat, determinismo, size_lista):
    total_nodes = int(f.readline())
    graph_matrix = [row[:] for row in init_mat]  # copia superficial suficiente
    total_neighbors = [sum(row) for row in graph_matrix]

    # Heap para seleccionar nodo con menos vecinos
    heap = [(total_neighbors[i], i) for i in range(total_nodes)]
    heapq.heapify(heap)

    in_mis = [False] * total_nodes
    removed = [False] * total_nodes

    while heap:
        _, min_index = heapq.heappop(heap)
        if removed[min_index]:
            continue

        # e-greedy: con probabilidad, seleccionamos aleatoriamente entre los k mejores
        if random.random() < determinismo:
            candidatos = [(total_neighbors[i], i) for i in range(total_nodes) if not removed[i]]
            candidatos.sort()
            k = min(size_lista, len(candidatos))
            min_index = random.choice([i for _, i in candidatos[:k]])

        nodes_selected.append(min_index)
        in_mis[min_index] = True
        removed[min_index] = True

        # Eliminar vecinos
        for neighbor in range(total_nodes):
            if graph_matrix[min_index][neighbor] == 1 and not removed[neighbor]:
                removed[neighbor] = True
                for j in range(total_nodes):
                    if graph_matrix[neighbor][j] == 1:
                        total_neighbors[j] -= 1
                        graph_matrix[neighbor][j] = 0
                        graph_matrix[j][neighbor] = 0

        # Eliminar conexiones del nodo actual
        for j in range(total_nodes):
            graph_matrix[min_index][j] = 0
            graph_matrix[j][min_index] = 0

    # Reinserción final: nodos sin vecinos
    for i in range(total_nodes):
        if not removed[i] and sum(graph_matrix[i]) == 0:
            nodes_selected.append(i)


def egreedy3_fast(total_nodes, init_mat, determinismo, size_lista):
    from heapq import heappush, heappop

    graph = [set() for _ in range(total_nodes)]
    for i in range(total_nodes):
        for j in range(total_nodes):
            if init_mat[i][j]:
                graph[i].add(j)

    degree = [len(graph[i]) for i in range(total_nodes)]
    removed = [False] * total_nodes
    heap = [(degree[i], i) for i in range(total_nodes)]
    heapq.heapify(heap)

    nodes_selected = []

    while heap:
        _, node = heappop(heap)
        if removed[node]:
            continue

        # e-greedy selection
        if random.random() < determinismo:
            candidates = [(degree[i], i) for i in range(total_nodes) if not removed[i]]
            candidates.sort()
            k = min(size_lista, len(candidates))
            node = random.choice([i for _, i in candidates[:k]])
            if removed[node]:
                continue

        # Check independence (optional if graph is well-behaved)
        nodes_selected.append(node)
        removed[node] = True

        for neighbor in graph[node]:
            if not removed[neighbor]:
                removed[neighbor] = True
                for nn in graph[neighbor]:
                    if not removed[nn]:
                        degree[nn] -= 1
                graph[neighbor].clear()

        graph[node].clear()

    # Reinsertion: add isolated nodes
    for i in range(total_nodes):
        if not removed[i] and not graph[i]:
            nodes_selected.append(i)

    return nodes_selected


def solution_encoding(sol, total_nodes):
    encoding = [0] * total_nodes
    for i in sol:
        encoding[i] = 1
    return encoding

def Selection(soluciones_iniciales, total_nodes, k=3):
    torneo = random.sample(soluciones_iniciales, k)
    torneo.sort(key=len, reverse=True)
    return solution_encoding(torneo[0], total_nodes), solution_encoding(torneo[1], total_nodes)

def Mutation(first, second, total_nodes):
    child1 = [0] * total_nodes
    child2 = [0] * total_nodes

    point1 = random.randint(10, int(total_nodes / 2))
    point2 = random.randint(int(total_nodes / 2) + 1, total_nodes - 10)

    for i in range(total_nodes):
        if i < point1:
            child1[i] = first[i]
            child2[i] = second[i]
        elif i < point2:
            child1[i] = second[i]
            child2[i] = first[i]
        else:
            child1[i] = first[i]
            child2[i] = second[i]

    # Mutación con validación básica
    if random.random() < mutation_prob:
        for _ in range(mutation_max):
            for child in [child1, child2]:
                change_index = random.randint(0, total_nodes - 1)
                child[change_index] = 1 - child[change_index]  # flip bit

    # Actualizar nodos seleccionados después de mutación
    nodos_seleccionados1 = [i for i in range(total_nodes) if child1[i] == 1]
    nodos_seleccionados2 = [i for i in range(total_nodes) if child2[i] == 1]

    return nodos_seleccionados1, nodos_seleccionados2

def Repare(nodos_seleccionados, init_matrix):
    total_nodes = len(init_matrix)

    while True:
        conflictos = set()
        grados = {}

        # Detectar conflictos y contar vecinos
        for i in range(len(nodos_seleccionados)):
            node_i = nodos_seleccionados[i]
            for j in range(i + 1, len(nodos_seleccionados)):
                node_j = nodos_seleccionados[j]
                if init_matrix[node_i][node_j] > 0:
                    conflictos.add(node_i)
                    conflictos.add(node_j)
                    grados[node_i] = grados.get(node_i, 0) + 1
                    grados[node_j] = grados.get(node_j, 0) + 1

        if not conflictos:
            break  # No hay conflictos, solución válida

        # Elegir el nodo con más conflictos
        nodo_a_remover = max(grados, key=grados.get)
        #print("reparación: conflicto en", nodo_a_remover)
        nodos_seleccionados.remove(nodo_a_remover)

def Reinsertar(nodos_seleccionados, init_matrix):
    total_nodes = len(init_matrix)
    actuales = set(nodos_seleccionados)
    candidatos = [i for i in range(total_nodes) if i not in actuales]

    for nodo in candidatos:
        if all(init_matrix[nodo][otro] == 0 for otro in actuales):
            nodos_seleccionados.append(nodo)
            actuales.add(nodo)

def Reemplazo(soluciones_iniciales, nodos_seleccionados1, nodos_seleccionados2):
    hijos = [nodos_seleccionados1, nodos_seleccionados2]
    nuevas_soluciones = soluciones_iniciales.copy()

    # Ordenamos población actual por tamaño (peores al principio)
    nuevas_soluciones.sort(key=len)

    # Reemplazamos hasta dos peores si los hijos son mejores
    reemplazos = 0
    for hijo in sorted(hijos, key=len, reverse=True):
        for i in range(len(nuevas_soluciones)):
            if len(hijo) > len(nuevas_soluciones[i]):
                nuevas_soluciones[i] = hijo
                reemplazos += 1
                break
        if reemplazos == 2:
            break

    #print("Reemplazo completado. Tamaños:", [len(s) for s in nuevas_soluciones])
    return nuevas_soluciones




if __name__ ==  "__main__":

    #Esta primera parte es para tomar los argumentos y usarlos para tener los archivos de cierto directorio
    choosen_dataset_path = "erdos_n1000_p0c0.1_1.graph"
    init_poblacion = 5
    determinismo = 0.1
    size_lista = 4
    mutation_prob = 0.4
    mutation_max = 1

    if len(sys.argv) == 10:
        if("erdos_n" not in sys.argv[2]):
            print("nombre de instancia no válido")
            sys.exit()
        choosen_dataset_path = ChooseInstance(sys.argv[2])
        init_poblacion = int(sys.argv[5])
        determinismo = float(sys.argv[6])
        size_lista = int(sys.argv[7])
        mutation_prob = float(sys.argv[8])
        mutation_max = int(sys.argv[9])
    elif len(sys.argv) >= 5 and len(sys.argv) < 10:
        choosen_dataset_path = ChooseInstance(sys.argv[2])
        if len(sys.argv) == 6:
            init_poblacion = int(sys.argv[5])
        elif len(sys.argv) == 7:
            #print("agregando size, node, temp, cool")
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
        elif len(sys.argv) == 8:
            #print("agregando node, temp, cool")
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
        elif len(sys.argv) == 9:
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
            mutation_prob = float(sys.argv[8])
            
    else:
        print("el modo correcto de ejecución es: python3 GA.py -i <instancia-problema> -t tiempo-máximo-segundos "
        "<población-inicial> <nivel-determinismo> <tamaño-lista-mejores> <mutation-prob> <mutation-max>")
        sys.exit()

    #directory = os.fsencode(choosen_dataset_path)
    

    #ya obtenido el directorio aquí hay que iterar por cada file instancia
    file = os.path.join(choosen_dataset_path, sys.argv[2])
    #print(file)



    start_time = time.time()
    best_solution = 0
    best_time = 0


    #esta parte toma una solución inicial
    total_nodes = 0
    nodes_selected = []
    init_matrix = []
    with open(file, 'r') as archivo:
        total_nodes = int(archivo.readline())
        FillInitialAdjMatrix(init_matrix, archivo, total_nodes)
        #edge_count = sum(sum(row) for row in init_matrix) / 2

    soluciones_iniciales = []
    encoders_soluciones = []
    timeout_seconds = float(sys.argv[4])

    #Esta parte es población inicial
    for i in range(init_poblacion):

        nodes_selected = egreedy3_fast(total_nodes, init_matrix, determinismo, size_lista)
            
        soluciones_iniciales.append(nodes_selected)
        encoders_soluciones.append(solution_encoding(nodes_selected, total_nodes))
        #print(len(nodes_selected))
        #print("next")

        if len(nodes_selected) >= best_solution:
            best_solution = len(nodes_selected)

        nodes_selected = []

    #print("Soluciones egreedy obtenidas!")

    while time.time() - start_time < timeout_seconds:

        (first, second) = Selection(soluciones_iniciales, total_nodes)
        
        
        (nodos_seleccionados1, nodos_seleccionados2) = Mutation(first, second, total_nodes)
        
        
        #Check si offspring son correctos
        Repare(nodos_seleccionados1, init_matrix)
        Reinsertar(nodos_seleccionados1, init_matrix)

        Repare(nodos_seleccionados2, init_matrix)
        Reinsertar(nodos_seleccionados2, init_matrix)

        
        if len(nodos_seleccionados1) > best_solution:
            best_solution = len(nodos_seleccionados1)
            best_time = time.time() - start_time
            print("Se encontró una mejor solución: " + str(best_solution) + " en " + str(best_time) + " segundos")
        
        soluciones_iniciales = Reemplazo(soluciones_iniciales, nodos_seleccionados1, nodos_seleccionados2)
    print("La mejor solución fue " + str(best_solution) + " y se encontró en " + str(best_time) + " segundos")