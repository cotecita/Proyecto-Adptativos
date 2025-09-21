import os
import sys
import time

def ChooseInstance(instance):
    dataset_path = "dataset_grafos_no_dirigidos"
    first_dataset_path = os.path.join(dataset_path, "new_1000_dataset")
    second_dataset_path = os.path.join(dataset_path, "new_2000_dataset")
    third_dataset_path = os.path.join(dataset_path, "new_3000_dataset")

    script_dir = os.path.dirname(__file__)

    first_dataset_path = os.path.join(script_dir, first_dataset_path)
    second_dataset_path = os.path.join(script_dir, second_dataset_path)
    third_dataset_path = os.path.join(script_dir, third_dataset_path)

    if instance == "1000":
        return first_dataset_path
    elif instance == "2000":
        return second_dataset_path
    elif instance == "3000":
        return third_dataset_path
        

if __name__ ==  "__main__":

    #Esta primera parte es para tomar los argumentos y usarlos para tener los archivos de cierto directorio
    choosen_dataset_path = ""

    if len(sys.argv) == 3:
        choosen_dataset_path = ChooseInstance(sys.argv[2])
    else:
        print("el modo correcto de ejecución es: python3 greedy.py -i <instancia-problema>")
        sys.exit()

    directory = os.fsencode(choosen_dataset_path)
    

    #ya obtenido el directorio aquí hay que iterar por cada file instancia

    density = 0.1
    while density < 1.0:
        total_density_nodes = 0
        total_density_time = 0
        for f in os.listdir(directory):
            filename = os.fsdecode(f)


            if f"{density:.1f}" not in filename or f"{density+0.05:.2f}" in filename:
                continue
            
            #print("se encontró un " + str(density))

            #print("filename es " + filename);

            nodes_selected = []
                    
            with open(os.path.join(choosen_dataset_path, filename) , "r") as file:
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

                    if(min_index == -1):
                        break

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
                print("Nodos en grafo: " + str(nodes_in_mis))
                inst_end = time.time()
                inst_total_time = inst_end - inst_start
                print("Listo en " + str(inst_total_time) + " segundos")
                total_density_time += inst_total_time
                total_density_nodes += nodes_in_mis

        print("Media de nodos: " + str(total_density_nodes/30))
        print("Tiempo total de todas las instancias con p=" + f"{density:.1f}" + ": " + str(total_density_time))        
        print("Tiempo promedio de ejecución: " + str(total_density_time/30))
        density += 0.1
            
        

    
