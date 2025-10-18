import os
import sys
import time
import random
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
        
#f es un directorio de os.listdir(directory)
def egreedy(nodes_selected, choosen_dataset_path, file, init_mat, end_mat):
            
    
    #print("processing " + filename)
    inst_start = time.time()

    total_nodes = int(file.readline()) #Parece que esta línea es el número de nodos nomás
    nodes_in_mis = 0

    graph_matrix = [[0 for _ in range(total_nodes)] for _ in range(total_nodes)]

    #este loop rellena la matriz de adyacencia
    #print("filling adjacency matrix...")
    for line in file:
        ab_nodes = line.split()
        a_node = int(ab_nodes[0])
        b_node = int(ab_nodes[1])

        graph_matrix[a_node][b_node] += 1
        graph_matrix[b_node][a_node] += 1
    
        
    init_mat[:] = deepcopy(graph_matrix)
    
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
        

    end_mat[:] = deepcopy(graph_matrix)
    #print("repetidos? " + str(len(nodes_selected) != len(set(nodes_selected))))
    #print("Nodos en grafo: " + str(nodes_in_mis))
    #inst_end = time.time()
    #inst_total_time = inst_end - inst_start
    #print("Listo en " + str(inst_total_time) + " segundos")
    #total_density_time += inst_total_time
    #total_density_nodes += nodes_in_mis

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


if __name__ ==  "__main__":

    #Esta primera parte es para tomar los argumentos y usarlos para tener los archivos de cierto directorio
    choosen_dataset_path = "erdos_n1000_p0c0.1_1.graph"
    determinismo = 0.1
    size_lista = 4
    node_change = 8
    init_temp = 150
    cooling = 0.8


    if len(sys.argv) == 10:
        if("erdos_n" not in sys.argv[2]):
            print("nombre de instancia no válido")
            sys.exit()
        choosen_dataset_path = ChooseInstance(sys.argv[2])
        determinismo = float(sys.argv[5])
        size_lista = int(sys.argv[6])
        node_change = int(sys.argv[7])
        init_temp = int(sys.argv[8])
        cooling = float(sys.argv[9])
    elif len(sys.argv) >= 5 and len(sys.argv) < 10:
        choosen_dataset_path = ChooseInstance(sys.argv[2])
        if len(sys.argv) == 6:
            #print("agregando size, node, temp, cool")
            determinismo = float(sys.argv[5])
        elif len(sys.argv) == 7:
            #print("agregando node, temp, cool")
            determinismo = float(sys.argv[5])
            size_lista = int(sys.argv[6])
        elif len(sys.argv) == 8:
            #print("agregando temp, cool")
            determinismo = float(sys.argv[5])
            size_lista = int(sys.argv[6])
            node_change = int(sys.argv[7])
        elif len(sys.argv) == 9:
            #print("agregando cool")
            determinismo = float(sys.argv[5])
            size_lista = int(sys.argv[6])
            node_change = int(sys.argv[7])
            init_temp = int(sys.argv[8])
    else:
        print("el modo correcto de ejecución es: python3 SA.py -i <instancia-problema> -t tiempo-máximo-segundos <nivel-determinismo> "
        "<tamaño-lista-mejores> <nodos-borrados-local> <temperatura-inicial> <cooling>")
        sys.exit()

    #directory = os.fsencode(choosen_dataset_path)
    

    #ya obtenido el directorio aquí hay que iterar por cada file instancia
    file = os.path.join(choosen_dataset_path, sys.argv[2])
    #print(file)

    with open(file, 'r') as f:
        temp = init_temp
        start_time = time.time()
        best_solution = 0
        best_time = 0


        #esta parte toma una solución inicial
        nodes_selected = []
        init_matrix = []
        final_matrix = []
        
        egreedy(nodes_selected, choosen_dataset_path, f, init_matrix, final_matrix)
        best_solution = len(nodes_selected)
        current_solution = len(nodes_selected)
        best_time = time.time() - start_time
        print("Solución inicial es " + str(len(nodes_selected)))

        timeout_seconds = float(sys.argv[4])
        #aquí es templado simulado
        while time.time() - start_time < timeout_seconds:
            (current_solution, found_time, temp) = SimulatedAnnealing(current_solution, start_time, cooling, node_change, nodes_selected, temp, init_matrix, final_matrix)
            if current_solution > best_solution:
                print("Se encontró un mejor resultado: " + str(current_solution) + ", en " + str(found_time) + " segundos")
                #print("Anterior: " + str(best_solution))
                best_solution = current_solution
                best_time = found_time
        print("La mejor solución fue " + str(best_solution) + " y se encontró en " + str(best_time) + " segundos")
                