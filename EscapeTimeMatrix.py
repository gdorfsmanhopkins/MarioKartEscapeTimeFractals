#Usage
#python EscapeTimeMatrix.py <c> <output_json> <resolution> <bound> <xRange> <center> <aspectRatio>
#here c is the Julia set
#From resolution on, these arugments are optional

#from PIL import Image
import json
import ast
import helpers


def createPixelMatrix(c):
    M = [[bound]*height for i in range(width)]
    counter = 0
    percentage = 0
    for row in range(height):
        for col in range(width):
            #I want percentage to print
            if((100*counter/(width*height))>percentage):
                print('Pixel Matrix Progress:',percentage,'%')
                percentage+=1
            
            #Now do the thing
            a = xMin + col * xRange / width
            b = yMax - row * yRange / height
            z = [a,b]
            if helpers.cMag(z)>=2:
                M[col][row] = 0
            else:
                M[col][row] = helpers.computeEscapeTimeJulia(z,c,bound,pixelSize)
            counter +=1
    return M

if __name__ == "__main__":
    import sys
    l = len(sys.argv)
    if l<2:
        print("You must provide a Julia set and savestring")
        sys.exit()
    c = ast.literal_eval(sys.argv[1])
    saveString = sys.argv[2]

    #Here are the default parameters
    #For now we're just doing a centered square between -2 and 2
    bound = 500
    width = 1000 #pixel width
    x,y = [0,0] #center
    xRange = 4
    aspectRatio = 1

    #Update them if given
    if l>3:
        width = int(sys.argv[3])
    if l>4:
        bound = int(sys.argv[4])
    if l>5:
        xRange = float(sys.argv[5])
    if l>6:
        center = ast.literal_eval(sys.argv[6])
        if len(center)!=2:
            print("Center point should be a 2d array")
            sys.exit(1)
        x,y = center
    if l>7:
        aspectRatio = float(sys.argv[7])
    
    #Calculate dependent parameters based of this data
    height = round(width/aspectRatio)
    yRange = xRange/aspectRatio
    xMin,xMax = x-xRange/2,x+xRange/2
    yMin,yMax = y-yRange/2,y+yRange/2
    pixelSize = xRange/width

    print("Computing matrix...")
    M = createPixelMatrix(c)
    print("Matrix computed")
    print("Saving...")
    save_location = open(saveString,'w')
    json.dump(M,save_location)
    print("Done")    