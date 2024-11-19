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
        if not isinstance(input_string, str):
            raise ValueError("La cinta inicial debe ser una cadena.")
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
        return {
            "left_tape": left_tape,
            "current_state": self.current_state,
            "cache_value": cache_value,
            "current_symbol": current_symbol,
            "right_tape": right_tape
        }


    def execute_step(self):
        if self.current_state in ['qaccept', 'qreject']:
            return {
                "description": self.generate_instant_description(),
                "result": "accepted" if self.current_state == "qaccept" else "rejected"
            }

        symbol = self.tape.read()
        transition = self.find_transition(symbol)

        if transition:
            self.apply_transition(transition)
            # Siempre devolver el estado actual después de aplicar la transición
            return {
                "description": self.generate_instant_description()
            }
        else:
            self.current_state = 'qreject'
            # Siempre devuelve un diccionario, incluso si no se encuentra transición
            return {
                "description": self.generate_instant_description(),
                "result": "rejected"
            }



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
