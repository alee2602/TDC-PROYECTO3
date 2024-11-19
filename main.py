from turing_machine import TuringMachine
from yaml_loader import load_yaml

def main():

    while True:
        print("¿Cuál Máquina de Turing deseas ejecutar?")
        print("0. Salir")
        print("1. Máquina de Reconocimiento")
        print("2. Máquina de Transformación")
        opt = input("Ingrese la opción: ")
        if opt == "0":
            break
        elif opt == "1":
            palindrome_config = load_yaml('machines/recognitionconfig.yaml')
            tm = TuringMachine(palindrome_config)
        elif opt == "2":
            altering_config = load_yaml('machines/alteringconfig.yaml')
            tm = TuringMachine(altering_config)
        else:
            print("Opción no válida")

        print("Testing Palindrome Turing Machine...")
        for test_input in palindrome_config['simulation_strings']:
            print(f"\nTesting input: {test_input}")
            tm.load_tape(test_input)
            tm.execute()
            tm.print_tape()

if __name__ == "__main__":
    main()
