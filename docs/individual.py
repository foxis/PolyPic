import numpy as np
import random as rn
import circle
import ellipse
import triangle
import quadrilateral
import cv2

class IndividualGen(object):
    ''''
        Individual Class

        An individual is defined as a set of polygons (genes)
        that generates an image. The fitness of the individual
        is measure on the similarity given a target image.
    '''

    def __init__( self, *args ):

        if len(args) == 5 :

            # Randomly generate an individual taking as inputs: size , height , width ,  type , maxopacity

            self.size = args[0]
            self.height = args[1]
            self.width = args[2]
            self.type = args[3]

            self.genes = []

            for i in range(self.size):

                if self.type == 1:

                    self.genes.append(circle.Circle(args[1], args[2], args[4]))

                elif self.type == 2:

                    self.genes.append(ellipse.Ellipse(args[1], args[2], args[4]))

                elif self.type == 3:

                    self.genes.append(triangle.Triangle(args[1],args[2],args[4]))

                elif self.type == 4:

                    self.genes.append(quadrilateral.Quadrilateral(args[1], args[2], args[4]))


        else:  # len(args) == 1 :

            # Implicity define an individual based on its genes encoding

            file = open(args[0], 'r')

            self.size = int(file.readline())
            self.height = int(file.readline())
            self.width = int(file.readline())
            self.type = int(file.readline())

            self.maxopacity = 0.3

            self.genes = []

            for i in range(self.size):

                if self.type == 1:

                    self.genes.append(circle.Circle(self.height, self.width, self.maxopacity, file.readline()))

                elif self.type == 2:

                    self.genes.append(ellipse.Ellipse(self.height, self.width, self.maxopacity, file.readline()))

                elif self.type == 3:

                    self.genes.append(triangle.Triangle(self.height, self.width, self.maxopacity, file.readline()))

                elif self.type == 4:

                    self.genes.append(quadrilateral.Quadrilateral(self.height, self.width , self.maxopacity, file.readline()))

            file.close()


    def generate( self ):

        # Create black background image and fill it up with random polygons

        img = np.zeros((self.height, self.width, 3), np.uint8)

        overlay = img.copy()
        output = img.copy()

        for i in range(self.size):

            info = self.genes[i].getInfo()

            if self.type == 1:

                cv2.circle(overlay,info[0],  info[1], info[2], -1)
                cv2.addWeighted(overlay, info[3], output, 1 - info[3], 0, output)

            elif self.type == 2:

                cv2.ellipse(overlay,info[0],info[1],info[2],0,360,info[3],-1)
                cv2.addWeighted(overlay, info[4], output, 1 - info[4], 0, output)

            elif self.type == 3:

                cv2.fillConvexPoly(overlay,np.asarray(info[0]), info[1])
                cv2.addWeighted(overlay, info[2], output, 1 - info[2], 0, output)

            elif self.type == 4:

                cv2.fillConvexPoly(overlay, np.asarray(info[0]), info[1])
                cv2.addWeighted(overlay, info[2], output, 1 - info[2], 0, output  )

        return output

    def write( self , filename):

        # Write image in file

        cv2.imwrite(filename,self.generate())


    def fitness( self , target ):

        # Calculate dissimilarity in pictures by MSE

        current = self.generate()
        err = np.sum((current.astype("float") - target.astype("float")) ** 2)
        err /= float(current.shape[0] * current.shape[1]* current.shape[2] )
        return err


    def mutate( self ):

        # Pick a random subset of polygons and randomize its properties

        index = rn.randint(0,self.size-1)
        self.genes[index].randomize()
        #for index in range(self.size):
        #    if np.random.rand() < 0.7:
        #        self.genes[index].randomize()


    def encode( self , filename ):

        # Store the current state of the individual in txt file

        file = open(filename, "w")

        file.write(str(self.size)+"\n")
        file.write(str(self.height)+"\n")
        file.write(str(self.width)+"\n")
        file.write(str(self.type)+"\n")

        for i in range ( self.size ):
            file.write(self.genes[i].encodeGene())

        file.close()