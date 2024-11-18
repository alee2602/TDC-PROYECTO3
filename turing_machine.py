from tape import Tape

class TuringMachine:
    def __init__(self, config):
        self.states = config['q_states']['q_list']
        self.current_state = config['q_states']['initial']
        self.accept_states = config['q_states']['final']
        self.delta = config['delta']
        self.tape = None
        self.mem_cache = None

    def load_tape(self, input_string):
        self.tape = Tape(input_string)
        self.mem_cache = None
        self.current_state = 'q0'

    def execute(self):
        steps = 0
        max_steps = 1000

        print("\nStarting execution:")
        print(f"Initial state: {self.current_state}")
        print(f"Initial tape: {''.join(self.tape.tape[:20])}")
        print(f"Initial head position: {self.tape.head}")
        
        while self.current_state not in ['qaccept', 'qreject'] and steps < max_steps:
            symbol = self.tape.read()
            print(f"\nStep {steps}:")
            print(f"Current state: {self.current_state}")
            print(f"Current symbol: {symbol}")
            print(f"Memory cache: {self.mem_cache}")
            
            transition = self.find_transition(symbol)
            
            if transition is None:
                print(f"No transition found for state={self.current_state}, symbol={symbol}, mem_cache={self.mem_cache}")
                self.current_state = 'qreject'
                print("Input rejected")
                return False
            
            print("Applying transition:")
            print(f"  From state: {self.current_state}")
            print(f"  To state: {transition['output']['final_state']}")
            print(f"  Writing: {transition['output']['tape_output']}")
            print(f"  Moving: {transition['output']['tape_displacement']}")
            print(f"  New mem_cache: {transition['output']['mem_cache_value']}")
            
            self.apply_transition(transition)
            self.print_tape()
            steps += 1
            
        success = self.current_state == 'qaccept'
        print(f"\nFinal state: {self.current_state}")
        print("Input", "accepted" if success else "rejected")
        return success

    def find_transition(self, symbol):
        for transition in self.delta:
            params = transition['params']
            if params['initial_state'] == self.current_state and params['tape_input'] == symbol:
                if params['mem_cache_value'] is None or params['mem_cache_value'] == self.mem_cache: #Si no se especifíca un valor dentro de la caché
                    return transition
        return None

    def apply_transition(self, transition):
        self.current_state = transition['output']['final_state']
        self.mem_cache = transition['output']['mem_cache_value']
        self.tape.write(transition['output']['tape_output'])
        if transition['output']['tape_displacement'] != 'N':
            self.tape.move(transition['output']['tape_displacement'])

    def print_tape(self):
        tape_content = "".join(self.tape.tape[:50])
        head_position = " " * self.tape.head + "^"
        print(f"Tape: {tape_content}")
        print(f"Head: {head_position}")