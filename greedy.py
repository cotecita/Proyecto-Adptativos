import os
import sys

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
        print("el modo correcto de ejecución es: python main.py -i <instancia-problema>")
        sys.exit()

    directory = os.fsencode(choosen_dataset_path)
    

    #ya obtenido el directorio aquí hay que iterar por cada file instancia
    for f in os.listdir(directory):
        filename = os.fsdecode(f)
        
        with open(os.path.join(choosen_dataset_path, filename) , "r") as file:
            total_nodes = int(file.readline()) #Parece que esta línea es el número de nodos nomás

            graph_matrix = [[0 for _ in range(total_nodes)] for _ in range(total_nodes)]

            #este loop rellena la matriz de adyacencia
            for line in file:
                ab_nodes = line.split()
                a_node = int(ab_nodes[0])
                b_node = int(ab_nodes[1])

                graph_matrix[a_node][b_node] += 1
                
            total_neighbors = [0 for _ in range(total_nodes)]
            
            #aquí se cuentan los vecinos de cada nodo
            for i in range(total_nodes):
                for j in range(total_nodes):
                    if(graph_matrix[i][j] == 1):
                        total_neighbors[i] += 1


        sys.exit()
        

    
