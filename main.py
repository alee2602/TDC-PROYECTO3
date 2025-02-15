from turing_machine import TuringMachine
from yaml_loader import load_yaml

def main():
    while True:
        print("\n¿Cuál Máquina de Turing deseas ejecutar?")
        print("0. Salir")
        print("1. Máquina de Reconocimiento (Palíndromos)")
        print("2. Máquina de Transformación (Invertir y Complementar)")
        print("3. Máquina de Fibonacci")
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
        elif opt == "3":
            config = load_yaml('machines/fiboconfig.yaml')
            machine_name = "Máquina de Fibonacci"
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            continue

        tm = TuringMachine(config)
        report = []
        print(f"\nEjecutando {machine_name}...")
        for test_input in config['simulation_strings']:
            print(f"\nProbando entrada: {test_input}")
            tm.load_tape(test_input)  
            success, ProcessingTime, steps = tm.execute()
            report.append([test_input, ProcessingTime, steps])
            result = "aceptada" if success else "rechazada"
            print(f"Resultado: La entrada '{test_input}' fue {result}.\n")
            
        print("Reporte final:")
        col_widths = [15, 10, 10]
        print(f"| {'Input':<{col_widths[0]}} | {'Time':<{col_widths[1]}} | {'Steps':<{col_widths[2]}} |")
        print("-" * (sum(col_widths) + 7))
        for i in report:
            print(f"| {i[0]:<{col_widths[0]}} | {i[1]:<{col_widths[1]}.5f} | {i[2]:<{col_widths[2]}} |")

if __name__ == "__main__":
    main()

