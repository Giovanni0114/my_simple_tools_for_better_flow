class pole:
    def __init__(self, letter):
        self.letter = letter
        self.used = False

with open("slowa.txt", "r") as file:
    WORDS = file.readlines()
    WORDS = [l.rstrip() for l in WORDS]

    assert len(WORDS), "Invalid words file"

with open("gra.txt", "r") as file:
    _let = file.readlines()
    _let = [l.rstrip() for l in _let]

    for i in _let:
        assert len(i) == 12, "Invalid board file"


    BOARD = [[pole(i) for i in l] for l in _let]

def search(board):
    global WORDS
    
    for l in board:
        for w in WORDS:
            if w in "".join([i.letter for i in l]):
                print(f"{w} found!")
                poz = 0
                while w in "".join([i.letter for i in l[poz+1:]]):
                    poz += 1

                for i in range(poz, poz + len(w)):
                    l[i].used = True

                WORDS.pop(WORDS.index(w))

    return board


BOARD = search(BOARD)

BOARD = [l[::-1] for l in BOARD] 

BOARD = search(BOARD) 

BOARD = [l[::-1] for l in BOARD] 

BOARD = [[BOARD[j][i] for j in range(12)] for i in range(12)]

BOARD = search(BOARD) 

BOARD = [l[::-1] for l in BOARD] 

BOARD = search(BOARD)

BOARD = [l[::-1] for l in BOARD] 
BOARD = [[BOARD[j][i] for j in range(12)] for i in range(12)]

for i in BOARD:
    for j in i:
        print(j.letter if not j.used else " ", end='')
    print()

