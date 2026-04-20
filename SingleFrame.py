import json
from PIL import Image
import math
import colorsys
import os
import helpers

if __name__== "__main__":
    import sys
    if len(sys.argv) <3:
        print("Usage: python SingleFram.py <input_dir> <output_dir>")
        print("Optionally include the LpNorm used for redistributing [0,1] (defaults to 2)")
        sys.exit()
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    LpNorm = 2
    if len(sys.argv)>3:
        LpNorm = float(sys.argv[3])

    print("Loading Matrix...")
    save_location = open(input_dir)
    ETMatrix = json.load(save_location)

    print("Matrix Loaded")
    height = len(ETMatrix[0])
    width = len(ETMatrix)

    #We will normalize the matrix to having values between 0 and 1, first linearly, and then redistributing using the function above


    biggest = ETMatrix[0][0]
    smallest = ETMatrix[0][0]

    print("Computing highest and lowest values")

    for i in range(width):
        for j in range(height):
            biggest = max(biggest,ETMatrix[i][j])
            smallest = min(smallest,ETMatrix[i][j])

    print("Values range from",smallest,"to",biggest)

    print("Normalizing the values")

    for i in range(width):
        for j in range(height):
            ETMatrix[i][j] = (ETMatrix[i][j]-smallest)/(biggest-smallest)

    print("Redistributing the values")

    for i in range(width):
        for j in range(height):
            ETMatrix[i][j] = helpers.redistribute(ETMatrix[i][j],LpNorm)

    print("Making the pixel matrix")

    img = Image.new('RGB', (width, height), color = 'black')
    pixels = img.load()

    for i in range(width):
        for j in range(height):
            Hue = ETMatrix[i][j]
            if(Hue == 1):
                r,g,b=[0,0,0]
            else:
                nextcolor = colorsys.hsv_to_rgb(1-Hue,1,1)
                r,g,b = nextcolor
            pixels[i,j] = (int(255*r),int(255*g),int(255*b))

    print("Pixel matrix built.")
    print("Saving image...")
    img.save(output_dir)
    print("Saved")