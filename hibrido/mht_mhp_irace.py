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

def build_adj_list_from_matrix(init_matrix):
    total_nodes = len(init_matrix)
    adj_list = [set() for _ in range(total_nodes)]
    for i in range(total_nodes):
        row = init_matrix[i]
        # vecinos: índices j tales que init_matrix[i][j] == 1
        adj_list[i] = {j for j in range(total_nodes) if row[j] == 1}
    return adj_list

def SimulatedAnnealing(best_sol, start_time, cooling, node_change, nodes, temp, init_mat, end_mat):
    if not nodes:
        return temp

    old_node_len = len(nodes)
    old_node_aux = deepcopy(nodes)
    init_mat_aux = deepcopy(init_mat)

    #elegir nodos al azar y sacarlos
    select_size = min(node_change, len(nodes))
    index_value_tuples = []
    for i in range(select_size):
        index = random.randint(0, len(nodes)-1)
        value = nodes[index]
        new_tuple = (index, value)
        index_value_tuples.append(new_tuple)
        nodes.pop(index)
        #print("se quitó el nodo " + str(value))

    # Get the set of nodes to preserve (those just removed)
    preserved_nodes = set(t[1] for t in index_value_tuples)

    # For every node in the current MIS (nodes), delete it and its neighbors from init_mat_aux
    for node in nodes:
        if node in preserved_nodes:
            continue  # Skip preserved nodes

        # Delete neighbors of node
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0

        # Delete the node itself
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][node] = 0
            init_mat_aux[node][j] = 0

    """"
    for i in range(len(init_mat)):
        if i == value or init_mat[value][i] != 1:
            continue

        #si el vecino seleccionado solo es adyacente a value, entonces puede entrar
        neighbor_count = 0
        neighbor_count = sum(init_mat[i][j] for j in range(len(init_mat)))
        if(neighbor_count == 1):
            nodes.append(i)
            print("se añadió el nodo " + str(i))
            break
    """

    #this part is to find which nodes are available to add to MIS
    available_nodes = []
    for i in range(len(init_mat_aux)):
        if i in nodes:
            continue
        if all(init_mat[i][j] == 0 for j in nodes):
            available_nodes.append(i)

    #this loop is to add as much nodes as possible in nodes (MIS)
    while available_nodes:
        #randomly chosen node
        i_chosen = random.randint(0, len(available_nodes) - 1)
        chosen_node = available_nodes[i_chosen]

        # Delete neighbors of chosen node
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[chosen_node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0

        #node added to MIS
        nodes.append(chosen_node)
        #print("se agregó el nodo " + str(chosen_node))
        
        # Delete the node itself
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][chosen_node] = 0
            init_mat_aux[chosen_node][j] = 0

        available_nodes = []
        #this loop is to refill available_nodes
        for i in range(len(init_mat_aux)):
            if i in nodes:
                continue  # Already in MIS

            if all(init_mat[i][j] == 0 for j in nodes):
                available_nodes.append(i)


    new_node_len = len(nodes)
    delta = new_node_len - old_node_len
    if new_node_len > old_node_len:
        return (new_node_len, time.time() - start_time, max(temp * cooling, 1e-5))

    acceptance_prob = 1
    try:
        acceptance_prob = math.exp(-delta / temp)
    except OverflowError:
        acceptance_prob = 0.0

    if delta < 0 and random.random() <= acceptance_prob:
        #print("Peor solución tomada")
        return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5))
    else:
        #print("Rollback")
        nodes[:] = old_node_aux
        
    return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5))

import random, math, time
from copy import deepcopy

def SimulatedAnnealingEncoding(best_sol, start_time, cooling, node_change, nodes, temp, init_mat):
    if not nodes:
        # Si no hay nodos, devolvemos encoding vacío
        encoding = [0] * len(init_mat)
        return temp, encoding

    old_node_len = len(nodes)
    old_node_aux = deepcopy(nodes)
    init_mat_aux = deepcopy(init_mat)

    # elegir nodos al azar y sacarlos
    select_size = min(node_change, len(nodes))
    index_value_tuples = []
    for i in range(select_size):
        index = random.randint(0, len(nodes)-1)
        value = nodes[index]
        new_tuple = (index, value)
        index_value_tuples.append(new_tuple)
        nodes.pop(index)

    # Get the set of nodes to preserve (those just removed)
    preserved_nodes = set(t[1] for t in index_value_tuples)

    # For every node in the current MIS (nodes), delete it and its neighbors from init_mat_aux
    for node in nodes:
        if node in preserved_nodes:
            continue  # Skip preserved nodes

        # Delete neighbors of node
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0

        # Delete the node itself
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][node] = 0
            init_mat_aux[node][j] = 0

    # find which nodes are available to add to MIS
    available_nodes = []
    for i in range(len(init_mat_aux)):
        if i in nodes:
            continue
        if all(init_mat[i][j] == 0 for j in nodes):
            available_nodes.append(i)

    # add as many nodes as possible
    while available_nodes:
        i_chosen = random.randint(0, len(available_nodes) - 1)
        chosen_node = available_nodes[i_chosen]

        # Delete neighbors of chosen node
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[chosen_node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0

        # node added to MIS
        nodes.append(chosen_node)
        
        # Delete the node itself
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][chosen_node] = 0
            init_mat_aux[chosen_node][j] = 0

        # refill available_nodes
        available_nodes = []
        for i in range(len(init_mat_aux)):
            if i in nodes:
                continue
            if all(init_mat[i][j] == 0 for j in nodes):
                available_nodes.append(i)

    # build encoding vector
    encoding = [1 if i in nodes else 0 for i in range(len(init_mat))]

    new_node_len = len(nodes)
    delta = new_node_len - old_node_len
    if new_node_len > old_node_len:
        return (new_node_len, time.time() - start_time, max(temp * cooling, 1e-5), encoding)

    acceptance_prob = 1
    try:
        acceptance_prob = math.exp(-delta / temp)
    except OverflowError:
        acceptance_prob = 0.0

    if delta < 0 and random.random() <= acceptance_prob:
        # Peor solución aceptada
        encoding = [1 if i in nodes else 0 for i in range(len(init_mat))]
        return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5), encoding)
    else:
        # Rollback
        nodes[:] = old_node_aux
        encoding = [1 if i in nodes else 0 for i in range(len(init_mat))]
        
    return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5), encoding)

import random, math, time
from copy import deepcopy

def SimulatedAnnealingSolution(best_sol, start_time, cooling, node_change, nodes, temp, init_mat):
    if not nodes:
        return temp, []

    old_node_len = len(nodes)
    old_node_aux = deepcopy(nodes)
    init_mat_aux = deepcopy(init_mat)

    # elegir nodos al azar y sacarlos
    select_size = min(node_change, len(nodes))
    index_value_tuples = []
    for i in range(select_size):
        index = random.randint(0, len(nodes)-1)
        value = nodes[index]
        new_tuple = (index, value)
        index_value_tuples.append(new_tuple)
        nodes.pop(index)

    preserved_nodes = set(t[1] for t in index_value_tuples)

    # eliminar vecinos de cada nodo en el MIS actual
    for node in nodes:
        if node in preserved_nodes:
            continue
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][node] = 0
            init_mat_aux[node][j] = 0

    # nodos disponibles para añadir
    available_nodes = []
    for i in range(len(init_mat_aux)):
        if i in nodes:
            continue
        if all(init_mat[i][j] == 0 for j in nodes):
            available_nodes.append(i)

    # añadir tantos nodos como sea posible
    while available_nodes:
        chosen_node = random.choice(available_nodes)
        for neighbor in range(len(init_mat_aux)):
            if init_mat_aux[chosen_node][neighbor] == 1 and neighbor not in preserved_nodes:
                for j in range(len(init_mat_aux)):
                    init_mat_aux[j][neighbor] = 0
                    init_mat_aux[neighbor][j] = 0
        nodes.append(chosen_node)
        for j in range(len(init_mat_aux)):
            init_mat_aux[j][chosen_node] = 0
            init_mat_aux[chosen_node][j] = 0

        available_nodes = []
        for i in range(len(init_mat_aux)):
            if i in nodes:
                continue
            if all(init_mat[i][j] == 0 for j in nodes):
                available_nodes.append(i)

    new_node_len = len(nodes)
    delta = new_node_len - old_node_len

    if new_node_len > old_node_len:
        return (new_node_len, time.time() - start_time, max(temp * cooling, 1e-5), nodes)

    try:
        acceptance_prob = math.exp(-delta / temp)
    except OverflowError:
        acceptance_prob = 0.0

    if delta < 0 and random.random() <= acceptance_prob:
        return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5), nodes)
    else:
        nodes[:] = old_node_aux
        return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5), nodes)

import random, math, time

def SimulatedAnnealingSolutionOptimized(best_sol, start_time, cooling, node_change, nodes, temp, adj_list):
    """
    adj_list: lista de sets, donde adj_list[i] contiene los vecinos del nodo i
    nodes: lista con nodos actuales en el MIS
    """

    if not nodes:
        return (0, time.time() - start_time, temp, [])

    old_node_len = len(nodes)
    old_node_aux = nodes.copy()

    # elegir nodos al azar y sacarlos
    select_size = min(node_change, len(nodes))
    removed = random.sample(nodes, select_size)
    for r in removed:
        nodes.remove(r)

    # construir set de nodos prohibidos (MIS actual + vecinos)
    forbidden = set(nodes)
    for node in nodes:
        forbidden.update(adj_list[node])

    # candidatos iniciales: nodos no prohibidos
    available_nodes = [i for i in range(len(adj_list)) if i not in forbidden]

    # añadir nodos mientras sea posible
    while available_nodes:
        chosen_node = random.choice(available_nodes)

        # ✅ Verificar independencia antes de añadir
        if all(chosen_node not in adj_list[n] for n in nodes):
            nodes.append(chosen_node)
            forbidden.add(chosen_node)
            forbidden.update(adj_list[chosen_node])

        # actualizar candidatos
        available_nodes = [i for i in available_nodes if i not in forbidden]

    new_node_len = len(nodes)
    delta = new_node_len - old_node_len

    # caso mejor solución
    if new_node_len > old_node_len:
        return (new_node_len, time.time() - start_time, max(temp * cooling, 1e-5), nodes)

    # probabilidad de aceptar peor solución
    try:
        acceptance_prob = math.exp(-delta / temp)
    except OverflowError:
        acceptance_prob = 0.0

    if delta < 0 and random.random() <= acceptance_prob:
        # aceptamos la peor solución
        return (new_node_len, time.time() - start_time, max(temp * cooling, 1e-5), nodes)
    else:
        # rollback
        nodes[:] = old_node_aux
        return (best_sol, time.time() - start_time, max(temp * cooling, 1e-5), nodes)

if __name__ ==  "__main__":

    #Esta primera parte es para tomar los argumentos y usarlos para tener los archivos de cierto directorio
    choosen_dataset_path = "erdos_n1000_p0c0.1_1.graph"
    init_poblacion = 5
    determinismo = 0.1
    size_lista = 4
    mutation_prob = 0.4
    mutation_max = 1
    node_change = 8
    init_temp = 150
    cooling = 0.8
    sa_iterations = 3

    if len(sys.argv) == 14:
        if("erdos_n" not in sys.argv[2]):
            print("nombre de instancia no válido")
            sys.exit()
        choosen_dataset_path = ChooseInstance(sys.argv[2])
        init_poblacion = int(sys.argv[5])
        determinismo = float(sys.argv[6])
        size_lista = int(sys.argv[7])
        mutation_prob = float(sys.argv[8])
        mutation_max = int(sys.argv[9])
        node_change = int(sys.argv[10])
        init_temp = float(sys.argv[11])
        cooling = float(sys.argv[12])
        sa_iterations = int(sys.argv[13])
    elif len(sys.argv) >= 5 and len(sys.argv) < 14:
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
        elif len(sys.argv) == 10:
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
            mutation_prob = float(sys.argv[8])
            mutation_max = int(sys.argv[9])
        elif len(sys.argv) == 11:
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
            mutation_prob = float(sys.argv[8])
            mutation_max = int(sys.argv[9])
            node_change = int(sys.argv[10])
        elif len(sys.argv) == 12:
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
            mutation_prob = float(sys.argv[8])
            mutation_max = int(sys.argv[9])
            node_change = int(sys.argv[10])
            init_temp = int(sys.argv[11])
        elif len(sys.argv) == 13:
            init_poblacion = int(sys.argv[5])
            determinismo = float(sys.argv[6])
            size_lista = int(sys.argv[7])
            mutation_prob = float(sys.argv[8])
            mutation_max = int(sys.argv[9])
            node_change = int(sys.argv[10])
            init_temp = int(sys.argv[11])
            sa_iterations = int(sys.argv[12])
            
    else:
        print("el modo correcto de ejecución es: python3 GA.py -i <instancia-problema> -t tiempo-máximo-segundos "
        "<población-inicial> <nivel-determinismo> <tamaño-lista-mejores> <mutation-prob> <mutation-max> <nodos-borrados-local> "
        "<temperatura-inicial> <cooling> <iteraciones-templado>")
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

    adj_list = build_adj_list_from_matrix(init_matrix)

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

        #Inicio templado simulado
        best_solution_first_child = len(nodos_seleccionados1)
        temp1 = init_temp
        new_solution1 = []
        for i in range(sa_iterations):
            (best_solution_first_child, seconds_passed, temp1, new_solution1) = SimulatedAnnealingSolutionOptimized(best_solution_first_child, start_time, cooling, node_change,
                                       nodos_seleccionados1, temp1, adj_list)
        if(len(nodos_seleccionados1) < len(new_solution1)):
            nodos_seleccionados1 = new_solution1
            
        best_solution_second_child = len(nodos_seleccionados2)
        temp2 = init_temp
        new_solution2 = []
        for i in range(sa_iterations):
            (best_solution_second_child, seconds_passed, temp2, new_solution2) = SimulatedAnnealingSolutionOptimized(best_solution_second_child, start_time, cooling, node_change,
                                       nodos_seleccionados2, temp2, adj_list)
        if(len(nodos_seleccionados2) < len(new_solution2)):
            nodos_seleccionados2 = new_solution2
        #Fin templado simulado

        if len(nodos_seleccionados1) > best_solution:
            best_solution = len(nodos_seleccionados1)
            best_time = time.time() - start_time
            #print("Se encontró una mejor solución: " + str(best_solution) + " en " + str(best_time) + " segundos")
        elif len(nodos_seleccionados2) > best_solution:
            best_solution = len(nodos_seleccionados2)
            best_time = time.time() - start_time
            #print("Se encontró una mejor solución: " + str(best_solution) + " en " + str(best_time) + " segundos")
        
        soluciones_iniciales = Reemplazo(soluciones_iniciales, nodos_seleccionados1, nodos_seleccionados2)
    print(-best_solution)