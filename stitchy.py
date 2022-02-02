from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path
from scipy import spatial
import os,glob,argparse



def get_tiles(folder:str,size = 10):
    """ import the photos from the folder and get them into the wanted format
    returns an array of Images 
    """
    p = os.getcwd()
    tiles_names = [name for name in glob.glob(f'{p}{folder}/*')]
    tiles = []
    for name in tiles_names:
        tile = Image.open(name)
        print(tile)
        tile = tile.resize((size,size))
        tiles.append(tile)
    return tiles

def average_color(image):
    """get the average rgb color of the image"""
    npimg = np.array(image)
    return tuple(np.round(np.average(npimg,axis=(0,1))))

def most_common_color(image):
    """find the most common rgb color from an image"""
    npimg = np.array(image)
    unique,counts = np.unique(npimg.reshape(-1,3) , axis = 0 , return_counts = True )
    return tuple(unique[np.argmax(counts)])

def top_three_colors(image):
    """return top three colors form the image"""
    npimg = np.array(image)
    cluster = KMeans(n_clusters = 3)
    cluster.fit(npimg.reshape(-1,3))
    return (cluster.cluster_centers_)




def split(image:Image,granulation:int):
    """ split the main image into smaller chunks of size granulation
        
        returns an array of images
    """
    W,H = image.size
    n = granulation
    w,h = int(np.round(W/n)), int(np.round(H/n))
    imgs = []

    for i in range(h):
        for j in range(w):
            imgs.append(image.crop((j*n,i*n,(j+1)*n,(i+1)*n)))

    return imgs



def main():
    parser = argparse.ArgumentParser(description = "Create a simple mosaic out of given images")
    parser.add_argument("-b", dest = "main_image",required = True ,help = "the name of the image you want to make a mosaic out of")
    parser.add_argument("-f", dest = "folder",required = True, help ="the name of the folder in which you have the images used as tiles")
    # how fine the art should be (the size of the side of the tiles in which the main image is split in pixels)
    parser.add_argument('-g', dest = "granulation", required = False, help = "the granulation of the image; how big you want the silces to be inside your image in pixels; default value = 10px")    

    args = parser.parse_args()



    main = Image.open(f'{os.getcwd()}/{args.main_image}')
    # main.show()
    # print(average_color(main)) 
    # print(most_common_color(main))
    # print(top_three_colors(main))
    
    for image in split(main,500):
        image.show()
if __name__ == "__main__":
    main()

