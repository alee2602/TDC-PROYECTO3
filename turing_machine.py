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

    def generate_instant_description(self):
        while self.tape.head >= len(self.tape.tape):
            self.tape.tape.append('_')

        if self.tape.head < 0:
            current_symbol = '_'
            right_tape = ''.join(self.tape.tape)
            left_tape = '' 
        else:
            current_symbol = self.tape.tape[self.tape.head]
            right_tape = ''.join(self.tape.tape[self.tape.head + 1:])
            left_tape = ''.join(self.tape.tape[:self.tape.head])
        
        cache_value = self.mem_cache if self.mem_cache is not None else 'null'
        description = f"{left_tape}[{self.current_state}, {cache_value}]{current_symbol}{right_tape}"
        return description

    def execute(self):
        steps = 0
        max_steps = 1000
        
        print("\nEjecución de la máquina de Turing:")
        initial_desc = self.generate_instant_description()
        print(f"Descripción inicial:  ⊢ {initial_desc}")
        
        while self.current_state not in ['qaccept', 'qreject'] and steps < max_steps:
            symbol = self.tape.read()
            transition = self.find_transition(symbol)
            
            if transition is None:
                print(f"No se encontró transición para el estado={self.current_state}, símbolo={symbol}, cache={self.mem_cache}")
                self.current_state = 'qreject'
                final_desc = self.generate_instant_description()
                print(f"Descripción final (rechazado): {final_desc}")
                return False
            
            self.apply_transition(transition)
            
            current_desc = self.generate_instant_description()
            print(f" ⊢ {current_desc}")
            steps += 1
        
        success = self.current_state == 'qaccept'
        final_desc = self.generate_instant_description()
        #print(f"\nDescripción final ({'aceptado' if success else 'rechazado'}): {final_desc}")
        return success

    def find_transition(self, symbol):
        for transition in self.delta:
            params = transition['params']
            if params['initial_state'] == self.current_state and params['tape_input'] == symbol:
                if params['mem_cache_value'] is None or params['mem_cache_value'] == self.mem_cache:
                    return transition
        return None

    def apply_transition(self, transition):
        self.current_state = transition['output']['final_state']
        self.mem_cache = transition['output']['mem_cache_value']
        self.tape.write(transition['output']['tape_output'])
        if transition['output']['tape_displacement'] != 'N':
            self.tape.move(transition['output']['tape_displacement'])