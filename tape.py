class Tape:
    def __init__(self, input_string):
        self.tape = list(input_string) + ['_'] * 100  #blanks
        self.head = 0  #posición inicial del lector

    def read(self):
        return self.tape[self.head]

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'L':
            self.head = max(0, self.head - 1)
        elif direction == 'R':
            self.head += 1