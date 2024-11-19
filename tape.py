class Tape:
    def __init__(self, input_string):
        self.tape = list(input_string)
        self.head = 0
    
    def read(self):
        if self.head < 0 or self.head >= len(self.tape):
            return '_'
        return self.tape[self.head]

    def write(self, symbol):
        if self.head < 0:
            self.tape = ['_'] * abs(self.head) + self.tape
            self.head = 0 
        elif self.head >= len(self.tape):
            self.tape += ['_'] * (self.head - len(self.tape) + 1)
        
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'L':
            self.head -= 1
        elif direction == 'R':
            self.head += 1
