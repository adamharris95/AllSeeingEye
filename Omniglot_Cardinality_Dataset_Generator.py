"""
Author: Adam Harris

Create a set of images containing a random number of omniglot charachters in arbitrary configurations,
alongside a CSV of image labels (the number of charachters contained in the image).

Omniglot characters downloaded from https://github.com/brendenlake/omniglot

Lake, B. M., Salakhutdinov, R., and Tenenbaum, J. B. (2015). Human-level concept learning through probabilistic program induction. Science, 350(6266), 1332-1338.

"""

from PIL import Image, ImageDraw
import numpy as np
import os
import pandas as pd


num = 1000  # How many images do you want
WIDTH, HEIGHT = 500, 500  # Dimensions of image in pixels
xaxis = [50, 150, 250, 350, 450]  # Possible x-axis positions where an image could be placed
yaxis = [50, 150, 250, 350, 450]  # Possible y-axis positions where an image could be placed
BG = 255, 255, 255  # Background colour
label = np.zeros((num,), dtype=int)  # Initialise vector for image labels

dirName = r"/Users/AdamHarris/Desktop/images_background"  # Where are you omniglot charachters stored?
outputDirName = r"/Users/AdamHarris/Desktop/OmniglotData"  # Where would you like to save the dataset

'''
Search the directory containing the omniglot characters and store the paths to the images
'''


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


omniglot = getListOfFiles(dirName)

'''
Generate dataset using the image paths.
For each image, an random threshold number between 0-1 is generated.
For each x,y coordinate pair within that image, a second number, prop is generated.
If variable Prob is less than the threshold for that image, a random omniglot charachter is pasted
in that location, with a randomly selected size and x,y jitter.

The function to choose an arbitrary orientation has been
'''

for image in range(num):
    # Create blank canvas with properties specified above
    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    # set threshold for this image
    thresh = np.random.uniform(0, 1)

    # Cycles through each x,y coordinate pair
    for i in range(len(xaxis)):
        for t in range(len(yaxis)):

            # Will this location have an image?
            prob = np.random.uniform(0, 1)

            if prob < thresh:

                # Counter for the image label
                label[image] += 1

                # Select random omniglot charachter
                index = np.random.randint(0, len(omniglot))
                path = omniglot[index]
                character = Image.open(path)

                #angle = np.random.randint(0, 360)
                #shape = shape.rotate(angle, expand=1)

                # X,y jitter to reduce to ouvert grid configuration (hardcoded bounds)
                x_jitter, y_jitter = np.random.randint(-30, 30), np.random.randint(-30, 30)

                # Resize charachter with hardcoded bounds to prevent overlap
                size = np.random.randint(10, 40)
                character = character.resize((2 * size, 2 * size))
                character = character.convert('RGBA')

                # Paste in resized charachter at jittered position
                position = [(xaxis[i] - (size)) + x_jitter, (yaxis[t] - size) + y_jitter, (xaxis[i] + size) + x_jitter, (yaxis[t] + size) + y_jitter]
                img.paste(character, position, character)

    # Connvertto greyscale an save
    img = img.convert('L')
    img.save(outputDirName + "/" + str(image + 1) + ".png")

# Print labels for dataset and save them to a csv
print(label)
df = pd.DataFrame(label)
df.to_csv(outputDirName + '/labels.csv', index=False, header=False)
