from turing_machine import TuringMachine
from yaml_loader import load_yaml

def main():
    while True:
        print("\n¿Cuál Máquina de Turing deseas ejecutar?")
        print("0. Salir")
        print("1. Máquina de Reconocimiento (Palíndromos)")
        print("2. Máquina de Transformación (Invertir y Complementar)")
        opt = input("Ingrese la opción: ")

        if opt == "0":
            print("Saliendo del programa...")
            break
        
        elif opt == "1":
            config = load_yaml('machines/recognitionconfig.yaml')
            machine_name = "Máquina de Reconocimiento"
        elif opt == "2":
            config = load_yaml('machines/alteringconfig.yaml')
            machine_name = "Máquina de Transformación"
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            continue

        tm = TuringMachine(config)

        print(f"\nEjecutando {machine_name}...")
        for test_input in config['simulation_strings']:
            print(f"\nProbando entrada: {test_input}")
            tm.load_tape(test_input)  
            success = tm.execute()    
            result = "aceptada" if success else "rechazada"
            print(f"Resultado: La entrada '{test_input}' fue {result}.\n")

if __name__ == "__main__":
    main()

