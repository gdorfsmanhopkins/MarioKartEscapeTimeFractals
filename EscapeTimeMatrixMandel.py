#Usage
#python EscapeTimeMatrixMande.py <output_json> <center> <xRange> <resolution> <aspectRatio> <bound>
#this makes a mandelbrot set centered at center
#From resolution on, these arugments are optional

#from PIL import Image
import json
import ast
import helpers
from fractions import Fraction


def createPixelMatrix():
    M = [[bound]*height for i in range(width)]
    counter = 0
    percentage = 0
    for row in range(height):
        for col in range(width):
            #print(col)
            #I want percentage to print
            if((100*counter/(width*height))>percentage):
                print('Pixel Matrix Progress:',percentage,'%')
                percentage+=1
            
            #Now do the thing
            a = xMin + col * xRange / width
            b = yMax - row * yRange / height
            c = [a,b]
            if helpers.cMag(c)>=2:
                M[col][row] = 0
            else:
                M[col][row] = helpers.computeEscapeTimeMandelbrot(c,bound,pixelSize)
            counter +=1
    return M

if __name__ == "__main__":
    import sys
    l = len(sys.argv)
    if l<2:
        print("You must provide a savestring")
        sys.exit()
    saveString = sys.argv[1]

    #Here are the default parameters
    #This just creates a view of the full mandelbrot set
    bound = 500
    width = 1000 #pixel width
    x,y = [-.65,0] #center
    xRange = 3
    aspectRatio = 4/3

    #Update them if given
    if l>2:
        center = ast.literal_eval(sys.argv[2])
        if len(center)!=2:
            print("Center point should be a 2d array")
            sys.exit(1)
        x,y = center
    if l>3:
        xRange = float(sys.argv[3])
    if l>4:
        resolution = int(sys.argv[4])
    if l>5:
        aspectRatio = float(Fraction(sys.argv[5]))
    if l>6:
        bound = int(sys.argv[6])
    
    #Calculate dependent parameters based of this data
    height = round(width/aspectRatio)
    yRange = xRange/aspectRatio
    xMin,xMax = x-xRange/2,x+xRange/2
    yMin,yMax = y-yRange/2,y+yRange/2
    pixelSize = xRange/width

    print("Computing matrix...")
    M = createPixelMatrix()
    print("Matrix computed")
    print("Saving...")
    save_location = open(saveString,'w')
    json.dump(M,save_location)
    print("Done")    