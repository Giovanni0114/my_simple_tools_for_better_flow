
#   y
#   1 2 3 4 5
#x 1
#  2
#  3
#  4
#  5

# -1 -1 | -1 0 | -1 +1 
#  0 -1 | XXXX |  0 +1
# +1 -1 | +1 0 | +1 +1
MATRIX = []

def get_neighbour(x, y, used_whis_word) -> list[str]:
    arr = []
    for y_m in range(-1,2):
        for x_m in range(-1,2):
            if x + x_m >= 0 and y + y_m >= 0 and x + x_m <= 5 and y + y_m <= 5 and (x,y) not in used_whis_word:
                arr.append(MATRIX[x][y])

    return arr


if __name__=="__main__":
    with open("matrix") as file:
        for line in file.readlines():
            MATRIX.append([f.upper for f in line.split()])

    if len(MATRIX) != 5 and len(MATRIX[0]) != 5:
        raise Exception("MATRIX ERROR")

    start = MATRIX[0][0]