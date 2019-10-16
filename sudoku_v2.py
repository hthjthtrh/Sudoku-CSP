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
        i, j = self.gridSelection()
        self.backTrackSearch(i, j)
        return self.ans

    def preparse(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    self.domainMatrix[i][j] = set([self.puzzle[i][j]])
                else:
                    self.unassignedGrids.append((i,j))

        for unassignedGrid in self.unassignedGrids:
            self.enforceArcConsistency(unassignedGrid[0],unassignedGrid[1])
            # print "position: {},{} domain:{}".format(unassignedGrid[0], unassignedGrid[1], self.domainMatrix[unassignedGrid[0]][unassignedGrid[1]])

        '''
        for i in range(9):
            for j in range(9):
                print "position: {},{} domain:{}".format(i, j, self.domainMatrix[i][j])
        '''
        

    def enforceArcConsistency(self, i, j):
        #print "position: {},{}".format(i, j)
        tempDomain = copy.deepcopy(self.domainMatrix[i][j])
        
        for val in tempDomain:
            deletedFlag = False
            for col in range(9):
                if col == j: continue
                domainToCheck = self.domainMatrix[i][col]
                if (val in domainToCheck) and (len(domainToCheck) == 1):
                    #print "removed value {} by {},{}".format(val, i, col)
                    self.domainMatrix[i][j].discard(val)
                    deletedFlag = True
                    break
            
            if deletedFlag: continue
            
            for row in range(9):
                if row == i: continue
                domainToCheck = self.domainMatrix[row][j]
                if (val in domainToCheck) and (len(domainToCheck) == 1):                    
                    #print "removed value {} by {},{}".format(val, row, j)
                    self.domainMatrix[i][j].discard(val)      
                    deletedFlag = True
                    break

            if deletedFlag: continue

            for pos in range(9):
                tempRow = i // 3 * 3 + pos // 3
                tempCol = j // 3 * 3 + pos % 3
                if tempRow == i and tempCol == j: continue       
                domainToCheck = self.domainMatrix[tempRow][tempCol]
                if (val in domainToCheck) and (len(domainToCheck) == 1):                    
                    #print "removed value {} by {},{}".format(val, tempRow, tempCol)
                    self.domainMatrix[i][j].discard(val)
                    break

    def backTrackSearch(self, i, j):
        self.enforceArcConsistency(i, j)
        domain = self.domainMatrix[i][j]
        for val in domain:
            self.ans[i][j] = val
            tempSet = copy.deepcopy(self.domainMatrix[i][j])
            self.domainMatrix[i][j] = set([val])
            if len(self.unassignedGrids) == 0:
                return True
            if self.forwardChecking(i, j):
                gridRow, gridCol = self.gridSelection()
                if self.backTrackSearch(gridRow, gridCol):
                    return True

            self.ans[i][j] = 0
            self.domainMatrix[i][j] = tempSet
        
        self.unassignedGrids.append((i, j))
        return False

    def forwardChecking(self, i, j):
        return True

    def gridSelection(self):
        return self.unassignedGrids.pop()
    

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
