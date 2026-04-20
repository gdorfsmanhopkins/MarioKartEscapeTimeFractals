#Most of the math happens here.  Ther rest of the scripts are just data management.
import math

#Compute the magnitude of a complex point a+bi
def cMag(z):
    a,b = z
    return math.sqrt(a*a+b*b)

#Compute the distance between two complex points z = a+bi by taking their difference and computing the magnitude
def computeDistance(z1,z2):
    z = [z2[i]-z1[i] for i in range(2)]
    return cMag(z)


#Multiply two complex points
def cMult(z1,z2):
    a1,b1 = z1
    a2,b2 = z2
    a = a1*a2-b1*b2
    b = a1*b2 + a2*b1
    return [a,b]

#Add two complex points
def cAdd(z1,z2):
    a1,b1 = z1
    a2,b2 = z2
    a = a1+a2
    b = b1+b2
    return [a,b]

#If z1 is in the circle and z2 escapes, we want to compute the "fraction of a step" it takes to escape
#We do this by intersecting the line z1z2 with the circle, and computing how for along the segment the circle gets hit
def MarioKartPrecision(z1,z2,pixelSize):
    x1,y1 = z1
    x2,y2 = z2
    
    #First deal with the case that the line moves vertically (up to pixel precision)
    if abs(x1-x2)<pixelSize:
        #Solve x^2 + y1^2 = 4 for x
        y = math.sqrt(4-x1**2)

        #make sure we're on the correct side of the cirlce
        if y2<0:
            y = -y

        #compute the ratio of the total distance and the distance inside the circle
        dist = y2 - y1
        insideDist = y - y1
        return insideDist/dist

    #Otherwise, we can compute the equation of the line y=mx+b
    m = (y2-y1)/(x2-x1)
    b = y1-m*x1

    #intersect it with the circle x^2+y^2=4
    #this is x^2 + (mx+b)^2 = 4
    #we use the quadratic fomula to solve (aQ)x^2 + (bQ)x + (cQ) = 0 where...
    aQ = m**2 + 1
    bQ = 2*m*b
    cQ = b**2 - 4

    xPlus = (-bQ + math.sqrt(bQ**2 - 4*aQ*cQ))/(2*aQ)
    yPlus = m*xPlus + b
    zPlus = [xPlus,yPlus]

    xMinus = (-bQ - math.sqrt(bQ**2 - 4*aQ*cQ))/(2*aQ)
    yMinus = m*xMinus + b
    zMinus = [xMinus,yMinus]

    #Figure out which point is closer to (x2,y2), that's our exit point
    if computeDistance(zPlus,z2) < computeDistance(zMinus,z2):
        return computeDistance(z1,zPlus)/computeDistance(z1,z2)
    else:
        return computeDistance(z1,zMinus)/computeDistance(z1,z2)


#In the Julia Set z^2+c, we'd like to compute the escape time of the point starting at z
def computeEscapeTimeJulia(z,c,bound,pixelSize):
    z0 = z
    for i in range(bound):
        z1 = cAdd(cMult(z0,z0),c) #iterating z^2+c
        if cMag(z1)>2:
            return i+MarioKartPrecision(z0,z1,pixelSize)
        z0 = z1
    return bound

def computeEscapeTimeMandelbrot(c,bound,pixelSize):
    z0 = c
    for i in range(bound):
        z1 = cAdd(cMult(z0,z0),c) #iterating z^2+c
        if cMag(z1)>2:
            return i+MarioKartPrecision(z0,z1,pixelSize)
        z0 = z1
    return bound


def redistribute(x,n):
    #Circular
    return((1 - (1-x)**n)**(1/n))