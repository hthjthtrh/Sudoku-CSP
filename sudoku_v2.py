import sys
import copy
import time

class Sudoku(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.ans = copy.deepcopy(puzzle)
        self.unassignedGrids = list()
        self.domainMatrix = [[set(i for i in range(1,10)) for _ in range(9)] for _ in range(9)]

    def solve(self):
        self.preparse()
        # self.backTrackSearch()
        return self.ans

    def preparse(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    self.domainMatrix[i][j] = set([i])
                    outCome = self.enforceArcConsistency(i,j)
                    if outCome is False:
                        return
                else:
                    self.unassignedGrids.append((i,j))

    def enforceArcConsistency(self, i, j):

        for val in self.domainMatrix(i, j):
            for col in range(9):
                if col == j or self.ans[i][col] != 0: continue
                


    def enforceArcConsistency(self, i, j):
        tempDomain = copy.deepcopy(self.domainMatrix[i][j])
        for val in tempDomain:
            if val in self.domainMatrix[i][j]:
                # grids of same row
                for col in range(9):
                    # skip the current grid or already assigned
                    if col == j or self.ans[i][col] != 0: continue
                    domainToReduce = self.domainMatrix[i][col]
                    if val in domainToReduce:
                        domainToReduce.remove(val)
                        if len(domainToReduce) == 0:
                            return False
                        else:
                            self.enforceArcConsistency(i, col)

                # grids of same column
                for row in range(9):
                    # skip the current grid or already assigned
                    if row == i or self.ans[row][j] != 0: continue
                    domainToReduce = self.domainMatrix[row][j]
                    if val in domainToReduce:
                        domainToReduce.remove(val)
                        if len(domainToReduce) == 0:
                            return False
                        else:
                            self.enforceArcConsistency(row, j)
                    
                # grids of same box
                for pos in range(9):
                    tempRow = i // 3 * 3 + pos // 3
                    tempCol = j // 3 * 3 + pos % 3

                    # skip the current grid or already assigned
                    if (tempRow == i and tempCol == j) or self.ans[tempRow][tempCol] != 0: continue
                    domainToReduce = self.domainMatrix[tempRow][tempCol]
                    if val in domainToReduce:
                        domainToReduce.remove(val)
                        if len(domainToReduce) == 0:
                            return False
                        else:
                            self.enforceArcConsistency(tempRow, tempCol)
        


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    start = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    print time.time()-start

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
