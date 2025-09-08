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
            unknown = file.readline() #Parece que esta línea es el número de instancias nomás

        sys.exit()
        

    