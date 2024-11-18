from turing_machine import TuringMachine
from yaml_loader import load_yaml

def main():
    palindrome_config = load_yaml('machines/recognitionconfig.yaml')
    tm_palindrome = TuringMachine(palindrome_config)

    print("Testing Palindrome Turing Machine...")
    for test_input in palindrome_config['simulation_strings']:
        print(f"\nTesting input: {test_input}")
        tm_palindrome.load_tape(test_input)
        tm_palindrome.execute()
        tm_palindrome.print_tape()

if __name__ == "__main__":
    main()
