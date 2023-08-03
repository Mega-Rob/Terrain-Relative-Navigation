import numpy as np
import os, pickle
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from PIL import ImageDraw

def reverseCoordinates(point):
    point = [point[1], point[0]]
    return point

def searchForFartestPoint(points):
    maxdis = 0;
    farpoints = [points[0],points[1]]
    for k in range(0,len(points)):
        for l in range(k,len(points)):
            i, j = points[k], points[l]
            newdis = np.sqrt(np.square(i[0]-j[0]) + np.square(i[1]-j[1]))
            if (newdis > maxdis):
                maxdis = newdis
                farpoints = [i,j]
    # farpoints = [[farpoints[0][1], farpoints[0][0]], [farpoints[1][1], farpoints[1][0]]]
    return (maxdis, farpoints)

def findClosestPointTo(point, edgecluster):
    mindistance = 999
    closestpoint = edgecluster[1]
    for point2 in edgecluster:
        newdis = np.sqrt(np.square(point[0]-point[0]) + np.square(point[1]-point2[1]))
        if (newdis < mindistance):
            mindistance = newdis
            closestpoint = point2
    return (mindistance, closestpoint)


def drawpoint(draw, point, width):
    draw.line((point[0], point[1] - 1, point[0], point[1] + 1),outline='#31ff00', width = width)
    draw.line((point[0] - 1, point[1], point[0] + 1, point[1]),outline='#31ff00', width = width)

def findEdges(points, imagematrix):
    edges = []
    for point in points:
        x = point[0]
        y = point[1]
        if (imagematrix[x+1,y]==255 or
            imagematrix[x,y+1]==255 or
            imagematrix[x-1,y]==255 or
            imagematrix[x,y-1]==255):
            edges.append([x,y])
    return edges

def RGBToGray(rgb):
    return 255 - np.dot(rgb[..., :3], [0, 0.5, 0.5])

def showGray(img):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(img, cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))
    plt.title("Image from showGray")
    plt.show()


def saveData(datapath, allCombinations, file):
    dir_path = os.path.join(os.curdir, datapath + "reference_preprocess")
    combinationsfile = os.path.join(dir_path, file)
    combinationdata = pickle.dumps(allCombinations, protocol=0)
    f = open(combinationsfile, "wb")
    f.write(combinationdata)
    f.close()

# def loadData(datapath, file):
#     f = open(os.path.join(os.curdir, datapath + "reference_preprocess", file), "rb")
#     layers_data = f.read()
#     return pickle.loads(layers_data)

def loadData(datapath, file):
    with open(os.path.join(datapath, "reference_preprocess", file), "rb") as f:
        layers_data = pickle.load(f, encoding='latin1')
    return layers_data

def plotClusters(mat):
    mat = np.array(mat)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(4,4)
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.scatter(mat[:, 0], mat[:, 1], edgecolors='none')
    # plt.gca().invert_yaxis()
    # plt.gca().invert_xaxis()
    plt.savefig('./method2.png', dpi = 128)

    # plt.savefig("method2.png", bbox_inches= 'tight', padding_inches=0)
    # plt.show()

def calculateMiddlePoint(diameter, fartestpoints):
    x = ((fartestpoints[0][0] + fartestpoints[1][0]) / 2) #- diameter / 8
    y = ((fartestpoints[0][1] + fartestpoints[1][1]) / 2) #+ diameter / 4
    return y, x


def draw_ellipse(image, bounds, width=0.1, outline='#31ff00', antialias=2):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)
    return image


