import numpy as np
import pandas as pd
import cv2

import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', help='Image Path')
args = vars(ap.parse_args())
img_path = args['image']
# reading image
img = cv2.imread(img_path)

# declare global
clicked = False
r = g = b = xpos = ypos = 0

# reading csv file with pandas and giving names to each column
index = ["color", "color_name", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# create a draw_function


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# create distance to get color name


def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"]) + abs(G -
                int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"])))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


while(1):
    cv2.imshow("HasilRGB", img)
    if(clicked):
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        # create text string to display (color name and RGB values)
        text = getColorName(r, g, b) + ' R=' + str(r) + \
            ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8,
                    (255, 255, 255), 2, cv2.LINE_AA)
        # for very light colours we'll display text in a black colour
        if(r+g+b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            clicked = False

        # break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break
cv2.destroyAllWindows()


# set a mouse callback event on a window
cv2.namedWindow('HasilRGB')
cv2.setMouseCallback('HasilRGB', draw_function)
