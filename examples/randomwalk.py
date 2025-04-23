#! python3

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import random
from HexGrid import HexCell, drawHexes


def randomwalk(h0 = HexCell(0,0)):
    h = h0
    h.data['colour'] = 'darkblue'
    index = 0
    while True:
        h.data['visited'] = True
        # h.data['text'] = f'{index}'
        unvisited_neighbours = [nh for nh in h.neighbours if 'visited' not in nh.data]
        if len(unvisited_neighbours) ==0: # The random walk ends when it gets stuck 
             h.data['colour'] = 'red'
             h.data['text'] = f'{index}'
             yield h
             return index
        yield h
        h = random.choice(unvisited_neighbours)
        index+=1



drawHexes(randomwalk())













