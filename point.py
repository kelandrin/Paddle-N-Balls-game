'''This module was adapted from the point module done in class, its purpose is to deal with all of the conversions
between pixels and fractional coordinates and return the point in whatever form requested. '''

class Point:
    def __init__(self, frac_x: float, frac_y: float):
        '''takes in a fractional x and fractional y and initializes a point. The number represents the fraction of
         the window available'''

        self._frac_x = frac_x
        self._frac_y = frac_y

    def as_frac(self) -> tuple:
        '''returns a tuple with the fractional x and fractional y of the point '''

        return (self._frac_x, self._frac_y)

    def as_pixel(self, width: int, height: int) -> tuple:
        '''returns a tuple with the pixel x and y coordinates of the point'''

        return (self._frac_x * width, self._frac_y * height)

def from_frac(frac_x: float, frac_y: float) -> Point:
    '''takes in a fractional x and fractional y and creates a point with those attributes'''

    return Point(frac_x,frac_y)

def from_pixel(pix_width: int, pix_height: int, window_width: int, window_height: int) -> Point:
    '''takes in a pixel width, pixel height, window width and window height and creates a point with the fractional attributes'''

    return Point(pix_width / window_width, pix_height / window_height)





