import numpy as np
from math import pi, sin, cos
import random as rand
from pyglet.gl import *
import sys

AMOUNT_TO_SHRINK = rand.uniform(0.50, 0.75)
# Becareful of setting this too high as it will take longer to create the tree the higher you put it.
# At values higher than 15(2^15 branches) is where you will notice this and it will probably hang for quite some time.
TREE_DEPTH = rand.randint(10, 13)

SIN_MEMOIZED_VALUES = {}
COS_MEMOIZED_VALUES = {}

# Change these RGB colors to your liking to create BEAUTIFUL colored trees.
BRANCH_COLOUR = (101, 67, 33,  101, 67, 33)
BRANCH_LEAF_COLUR = (0, 100, 0, 0, 100, 0)

def memoizedSin(degree):
    if degree not in SIN_MEMOIZED_VALUES:
        SIN_MEMOIZED_VALUES[degree] = sin(np.deg2rad(degree))
    return SIN_MEMOIZED_VALUES[degree]

def memoizedCos(degree):
    if degree not in COS_MEMOIZED_VALUES:
        COS_MEMOIZED_VALUES[degree] = cos(np.deg2rad(degree))
    return COS_MEMOIZED_VALUES[degree]

def rotateVector(vector, degree):
    cosAlpha = memoizedCos(degree)
    sinAlpha = memoizedSin(degree)
    return np.matmul(vector, [[cosAlpha, -sinAlpha], [sinAlpha ,cosAlpha]]) # Rotational counter-clockwise matrix

class Branch:
    def __init__(self, begin, end, color):
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.vertices = pyglet.graphics.vertex_list(2, ('v2f', (self.begin[0], self.begin[1], self.end[0] ,self.end[1])),
                                                       ('c3B', color)
                                                    )

    def branch(self, degree, color):
        dir = self.end - self.begin
        dir = rotateVector(dir, degree);
        dir = dir * AMOUNT_TO_SHRINK
        newEnd = self.end + dir
        branch = Branch(self.end, newEnd, color)
        return branch

    def displayBranch(self):
        glLineWidth(2.0)
        self.vertices.draw(GL_LINES)

class FractalTree:
    def __init__(self, height):
        self.branches = []
        self.branches.append(Branch([0, -(height / height)], [0, 0], BRANCH_COLOUR))

    def createTree(self):
        totalBranchesToVisit = int(pow(2, TREE_DEPTH - 1)) - 1
        currBranchIndex = 0
 
        while(currBranchIndex < totalBranchesToVisit):
                degree = rand.randrange(30, 61)
                self.branches.append(self.branches[currBranchIndex].branch(-degree, BRANCH_COLOUR))
                self.branches.append(self.branches[currBranchIndex].branch(degree, BRANCH_COLOUR))
                currBranchIndex += 1

        totalBranches = len(self.branches)
        
        for branchIndex in range(currBranchIndex, totalBranches):
            self.branches[branchIndex].vertices.colors = BRANCH_LEAF_COLUR

    def displayTree(self):
        for branch in self.branches:
            branch.displayBranch()
            
    
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        if(sys.version_info > (3, 0)):
            super().__init__(*args, **kwargs)
        else:
            super(Window, self).__init__(*args, **kwargs)
 
        self.set_minimum_size(640, 480)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glScalef(0.4, 0.4, 0.4)

        windowSize = self.get_size()
        
        self.tree = FractalTree(windowSize[1]) # We want the height of the window
        self.tree.createTree()

    def on_draw(self):
        self.clear()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.tree.displayTree()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

if __name__ == "__main__":    
    window = Window(640, 480, "Fractal Trees Demonstration", resizable=True)
    pyglet.app.run()
