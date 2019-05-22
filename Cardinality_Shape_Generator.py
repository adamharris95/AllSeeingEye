"""
Author: Adam Harris

Create a set of images containing a random number of shapes in arbitrary configurations,
alongside a CSV of image labels (the number of shapes contained in the image).

"""

from PIL import Image, ImageDraw
import numpy as np
import pandas as pd

num = 10000  # How many images do you want
WIDTH, HEIGHT = 500, 500  # Dimensions of image in pixels
xaxis = [50, 150, 250, 350, 450]  # Possible x-axis positions where an image could be placed
yaxis = [50, 150, 250, 350, 450]  # Possible y-axis positions where an image could be placed
BG = 255  # Background colour
BLACK = 0
label = np.zeros((num,), dtype=int)  # Initialise vector for image labels

outputDirName = r"/Users/AdamHarris/Desktop/ShapeData"  # Where would you like to save the dataset

'''
Generate collection of circles and squares
For each image, an random threshold number between 0-1 is generated.
For each x,y coordinate pair within that image, a second number, prop is generated.
If variable Prob is less than the threshold for that image, a shape is drawn
in that location, with a randomly selected size and x,y jitter.

'''

for image in range(num):
    # Create blank canvas with properties specified above
    img = Image.new('L', (WIDTH, HEIGHT), BG)
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
                size = np.random.randint(10, 30)
                x_jitter, y_jitter = np.random.randint(-30, 30), np.random.randint(-30, 30)
                position = [(xaxis[i] - (size)) + x_jitter, (yaxis[t] - size) + y_jitter, (xaxis[i] + size) + x_jitter, (yaxis[t] + size) + y_jitter]
                which_shape = np.random.randint(0, 2)

                if which_shape is 0:
                    shape = draw.rectangle(position, fill=BLACK, outline=None)
                elif which_shape is 1:
                    shape = draw.ellipse(position, fill=BLACK, outline=None)

    #  save
    img.save(outputDirName + "/Images/" + str(image + 1).zfill(5) + ".png")
    print(label[image])

# Print labels for dataset and save them to a csv
print(label)
df = pd.DataFrame(label)
df.to_csv(outputDirName + '/labels.csv', index=False, header=False)
