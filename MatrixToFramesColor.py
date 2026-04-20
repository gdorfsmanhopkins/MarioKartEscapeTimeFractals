import json
from PIL import Image
import math
import colorsys
from pathlib import Path
import helpers

#Redistribute the numbers 0-->1 along a smooth curve

if __name__=="__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python SingleFram.py <input_dir> <output_dir> <NUM_FRAMES>")
        print("Optionally, one could also specify the Lp norm used for distribution (defaults to 2)")
        print("Optionally, one could also specify the number of loops through the color spectrum (defaults to 1)")
        sys.exit()
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    NUM_FRAMES = int(sys.argv[3])
    NUM_DIGS = int(math.log10(NUM_FRAMES)) #For naming the files correctly
    STEP_SIZE = 1/NUM_FRAMES

    LpNorm = 2
    if len(sys.argv) > 4:
        LpNorm = float(sys.argv[4])

    NUM_SPECTRAL_LOOPS = 1
    if len(sys.argv) > 5:
        NUM_SPECTRAL_LOOPS = int(sys.argv[5])

    print("Loading Matrix...")
    save_location = open(input_dir)
    ETMatrix = json.load(save_location)


    #We will normalize the matrix to having values between 0 and 1, first linearly, and then redistributing using the function above
    height = len(ETMatrix[0])
    width = len(ETMatrix)

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

    print("Making the Frames!")
    Path(output_dir).mkdir(exist_ok=True)

    img = Image.new('RGB', (width, height), color = 'white')
    pixels = img.load()

    t=0
    for v in range(NUM_FRAMES):
        for i in range(width):
            for j in range(height):
                if ETMatrix[i][j]<t:
                    ETMatrix[i][j]=1
                    Hue = v*NUM_SPECTRAL_LOOPS/NUM_FRAMES - math.floor(v*NUM_SPECTRAL_LOOPS/NUM_FRAMES)
                    nextcolor = colorsys.hsv_to_rgb(1-Hue,1,1)
                    r,g,b = nextcolor
                    pixels[i,j] = (int(255*r),int(255*g),int(255*b))
        img.save(output_dir + '/frame'+str(int(v+10**(NUM_DIGS+1)))+'.png')
        print("Made Frame #",v+1,"out of",NUM_FRAMES)
        t += STEP_SIZE