#! python3



import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from HexGrid import HexCell, drawHexes, chain

import random


arm = list(HexCell(0,0).generate_disc(2)) +\
      list(HexCell(0,0).generate_line_to(HexCell(7,0))) +\
      list(HexCell(3,1).generate_line_to(HexCell(4,-1))) +\
      list(HexCell(5,2).generate_line_to(HexCell(7,2)))

hexes = arm[::]

for h in arm:
    hexes.append(h.rot60(1))
    hexes.append(h.rot60(2))
    hexes.append(h.rot60(3))
    hexes.append(h.rot60(4))
    hexes.append(h.rot60(5))
    

drawHexes(hexes)
