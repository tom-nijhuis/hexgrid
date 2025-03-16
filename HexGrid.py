#! python3

'''
    Implemented from 
    https://www.redblobgames.com/grids/hexagons/
'''

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def chain(*iterables):
    """ Convenience chaining iterables """ 
    for iterable in iterables:
        yield from iterable

class HalvesSqrt3:
    """
    Implements numbers of the form a + b*sqrt(3) and allows exact math on them
    Convenient for math on mulitples of 60°

    """
         
    SQRT3 = 1.7320508075688772935274463415

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        if isinstance(other, HalvesSqrt3):
            return HalvesSqrt3(self.a + other.a, self.b+other.b)
        if not isinstance(other, (int, float)):
            raise TypeError(f"Expected HalvesSqrt3, int or float, got {type(other).__name__}")
        return HalvesSqrt3(self.a + other, self.b)


    def __mul__(self, other): # implement self*other
        """ only for float, int other """ 
        if isinstance(other, halvessqrt3):
            return halvessqrt3(self.a*other.a + 3*self.b*other.b,
                               self.a*other.b + self.b*other.a)
        if not isinstance(other, (int, float)):
            raise TypeError(f"Expected HalvesSqrt3, int or float, got {type(other).__name__}")
        return HalvesSqrt3(self.a*other, self.b*other)

    __rmul__ = __mul__

    def __float__(self):
        return self.a + self.b*HalvesSqrt3.SQRT3

    def __repr__(self):
        return f'{self.a:+}{self.b:+}√3'





class HexCell:
    _instances = {} # Store earlier instances

    UNIT_CORNERS = [(math.cos(i*math.pi/3), math.sin(i*math.pi/3)) for i in range(6) ]
    DIRECTIONS = [ # Todo: Do these directions match the ordering of the unit corners?
            (+1, 0, -1), 
            (+1, -1, 0), 
            (0, -1, +1), 
            (-1, 0, +1), 
            (-1, +1, 0), 
            (0, +1, -1),
    ]

    class AxesException(Exception):
        def __init__(self, message):
            self.message = message 
            super().__init__(self, message)


    def __new__(cls, *args):
        # Create new if it does not exist yet. 
        # This assures that coordinates always point to the same instance
        if args not in cls._instances:
            cls._instances[args] = super(HexCell, cls).__new__(cls)
        return cls._instances[args]


    def __init__(self, q, r, s = None):
        # Set axes
        q = q if not q is None else -r-s # Axial coordinate q
        r = r if not r is None else -q-s # Axial coordinate r
        s = s if not s is None else -q-r # Axial coordinate s
        if q+r+s!=0:
            raise HexCell.AxesException(f'Axes mismatch. q+r+s!=0 ({q}+{r}+{s}!=0)')
        self.q, self.r = q,r

    @property
    def s(self): # The third axis is calculated from the first two.
        return -self.q-self.r

    @property
    def qrs(self):
        return (self.q, self.r, self.s)

    @property
    def neighbours(self):
        yield from [self + HexCell(*self.DIRECTIONS[i]) for i in range(6) ]

    @property
    def polygon(self):
        size = 1 
        px = size * (                                    3 /2 * self.r)
        py = size * (math.sqrt(3) * self.q  +  math.sqrt(3)/2 * self.r)
        return [(px + size*x, py + size*y) for (x,y) in self.UNIT_CORNERS]



    def __truediv__(self, other):
        return 1/other*self
    def __mul__(self, other): # implement self*other
        return HexCell(self.q*other, self.r*other)
    __rmul__ = __mul__

    def __neg__(self):
        return -1*self

    def __add__(self, other):
        return HexCell(self.q + other.q, self.r + other.r)

    def __sub__(self, other): # self-other
        return self + -other

    def __abs__(self):
        q,r,s = self.qrs
        return (abs(q)+abs(r) + abs(s) ) //2

    def __round__(self):
        """ Implements cube rounding """
        q,r,s = (round(t) for t in self.qrs)
        q_diff = abs(q - self.q)
        r_diff = abs(r - self.r)
        s_diff = abs(s - self.s)
        if q_diff > r_diff and q_diff > s_diff:
            q = -(r)-(s)
        elif r_diff > s_diff:
            r = -(q)-(s)
        else:
            s = -(q)-(r)
        return HexCell(q,r,s)


    def generate_line_to(self, other):
        dist = abs(other-self)
        for i in range(0,dist+1):
            yield round(self + i / dist * (other - self))



    def generate_span(self, max_dist):
        for qq in range(-max_dist, max_dist + 1, 1):
            for rr in range(max(-max_dist,-max_dist - qq), min(max_dist+1, max_dist+1-qq), 1):
                yield HexCell(self.q+qq, self.r+rr)

    def generate_disc(self, dist):
        yield self
        for i in range(dist):
            yield from self.generate_circle(i)

    def generate_circle(self, dist):
        # Move dist in q-direction:
        for i in range(6):
            h = self + dist*HexCell(*self.DIRECTIONS[i])
            for j in range(0, dist):
                yield h+j*HexCell(*self.DIRECTIONS[(i+2)%6])


    def __repr__(self):
        return f'HexCell @ {self.qrs}'

    def __hash__(self):
        return (self.q,self.r).__hash__()

    def __lt__(self, other):
        return self.qrs < other.qrs

    def __eq__(self, other):
        return self.qrs == other.qrs


def drawHexes(hexes, colours = []):
    # Create a figure and an axis
    fig, ax = plt.subplots()

    xmin, xmax = 0,0
    ymin, ymax = 0,0
    # Pad the iterator with 'lightblue' if it runs out
    colours = chain(colours, iter(lambda : 'lightblue', None))
    for hex, col in zip(hexes, colours):

        vertices = hex.polygon
        for x,y in vertices:
           xmin,xmax = min(xmin, x), max(xmax, x)
           ymin,ymax = min(ymin, y), max(ymax, y)
        polygon = patches.Polygon(vertices, closed=True, fill=True, edgecolor='black', facecolor=col)
        ax.add_patch(polygon)


    # Set limits and aspect
    ax.set_xlim(xmin*1.1, xmax*1.1)
    ax.set_ylim(ymin*1.1, ymax*1.1)
    ax.set_aspect('equal')


    # Show the plot
    plt.show()



if __name__ == "__main__":
    
    h = HexCell(0,0)
    hexes= list(h.generate_line_to(HexCell(11, 6)))


    # h = HexCell(1.2,3.4)
    # print(h)
    # print(round(h))

    drawHexes(hexes)
    

    










