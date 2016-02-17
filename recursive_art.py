""" This program will create a video of art with specified resolution for a randomly generated function.  """

import random
from math import *
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    if min_depth < 1:
        chance = 1.0/(max_depth-min_depth)
        myrand = random.uniform(0,1)
        if chance > myrand:
            xory = random.randint(0,2)
            print xory
            if xory == 0:
                return "x"
            elif xory == 1:
                return "y"
            elif xory == 2:
                return "t"
    if max_depth == 0:
        xory = random.randint(0,2)
        if xory == 0:
            return "x"
        elif xory == 1:
            return "y"
        elif xory == 2:
            return "t"
    funcchoice = random.randint(1, 9)
    if funcchoice == 1:
        return ["prod", build_random_function(min_depth-1, max_depth-1),build_random_function(min_depth-1, max_depth-1),build_random_function(min_depth-1, max_depth-1) ]
    elif funcchoice == 2:
        return ["avg", build_random_function(min_depth-1, max_depth-1),build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 3:
        return ["cos_pi", build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 4:
        return ["sin_pi",build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 5:
        return ["x" ,build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 6:
        return ["absrt", build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 7:
        return ["arctangentthing", build_random_function(min_depth-1, max_depth-1)]
    elif funcchoice == 8:
        return ["t" , build_random_function(min_depth-1, max_depth-1)]
    else:
        return ["y" , build_random_function(min_depth-1, max_depth-1)]
   


def evaluate_random_function(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod",["sin_pi",["x"]],["cos_pi",["x"]]],0.1,0.02)
        0.293892626146
    """
    if len(f) == 1:
        if f[0] == "x":
            return x
        elif f[0] == "y":
            return y
        elif f[0] == "t":
            return t
    if f[0] == "prod":
        return evaluate_random_function(f[1], x, y, t)*evaluate_random_function(f[2], x, y,t)*evaluate_random_function(f[3], x, y,t)
    if f[0] == "avg":
        return (evaluate_random_function(f[1], x, y,t)+evaluate_random_function(f[2], x, y,t))*.5
    if f[0] == "cos_pi":
        return cos(1.4*pi*evaluate_random_function(f[1],x, y, t))
    if f[0] == "sin_pi":
        return sin(1.5*pi*evaluate_random_function(f[1], x, y,t))
    if f[0] == "x":
        return evaluate_random_function(f[1], x, y,t)
    if f[0] == "y":
        return evaluate_random_function(f[1], x, y, t)
    if f[0] == "t":
        return evaluate_random_function(f[1], x, y, t)
    if f[0] == "absrt":
        return sin((evaluate_random_function(f[1], x, y, t))*sqrt(fabs(evaluate_random_function(f[1], x, y, t))))
    if f[0] == "arctangentthing":
        return atan(evaluate_random_function(f[1], x, y,t))**3

def sign(x):
    if x <= 0:
        return -1
    else:
        return 1

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(-5, -6, -4, 3, 5)
        4.0
    """
    originallength = 0.0 + input_interval_end - input_interval_start
    originalvallength = 0.0 + val - input_interval_start
    originalfraction = originalvallength/originallength
    newvallength = 0.0 + originalfraction*(output_interval_end - output_interval_start)
    output = newvallength + output_interval_start
    return output


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350, time=60):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """

    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,13)
    green_function = build_random_function(7,13)
    blue_function = build_random_function(7,13)
    for w in range(time):
        print time
        t = -1.0+2*(w+0.0)/time
        print t
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y,t)),
                        color_map(evaluate_random_function(blue_function, x, y,t))
                        )
        filename = "movie_2_"+str(w)+'.png'
        im.save(filename)


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
generate_art("movie_2_", 450, 450, 60)
# func = build_random_function(5,6)
# for i in range(100):
#     t = (0.0+i)/100.0
#     print evaluate_random_function(func, .5, .5, t)