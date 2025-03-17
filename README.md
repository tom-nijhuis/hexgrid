# hexgrid

- Python infinite Hexagonal grid implementation
- as described in https://www.redblobgames.com/grids/hexagons/
- An exercise in Python objects and dunder-methods. 


### HexCell object features 
- initialise with Cubic coordinates q and r: `HexCell(0,0)`
- Multiton model: Multiple instantiations with the same cubic coordinates will be mapped onto the same instance (suppress this behaviour with `singleInstance=False`)
- Allowed vector arithmetic on HexCell instances:
  - addition, subtraction 
  - multiplication, division with float or int
  - abs(): hex distance from the origin HexCell(0,0)
  - round(): rounding fractional coordinates to the nearest hexcell ([see here](https://www.redblobgames.com/grids/hexagons/#rounding))
- A generic data store in `HexCell.data`


![example](example-grid.png)
