from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path
from scipy import spatial
import os,glob,argparse



def get_tiles(folder,size = 10):
    """ import the photos from the folder and resize them into the wanted size
    returns an array of Images 
    """
    p = os.getcwd()
    tiles_names = [name for name in glob.glob(f'{p}/{folder}/*')]
    tiles = []
    for name in tiles_names:
        tile = Image.open(name)
        tile = tile.resize((size,size))
        tiles.append(tile)
    return tiles

def average_color(image):
    """get the average rgb color of the image"""
    npimg = np.array(image)
    avg = np.round(np.average(npimg,axis=(0,1)))
    if type(avg) is not type(npimg):
        print(npimg)
    print(npimg)

    return avg


def most_common_color(image):
    """find the most common rgb color from an image"""
    npimg = np.array(image)
    unique,counts = np.unique(npimg.reshape(-1,3) , axis = 0 , return_counts = True )
    return tuple(unique[np.argmax(counts)])

def top_three_colors(image):
    # this I don't really understand nor do I really need and will probably delete it 
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


def best_match_index(color,colors_arr):
    """reuturns the best match for a given color out of a given colors array"""
    color = np.array(color)
    colors = np.array(colors_arr)
    # color = np.expand_dims(color,axis = 1) 
    # since rgb values can be interpreted as 3d-vectors the smallest distance between them is going to give us the color out of the array that best matches the given one
    for current_col in colors:
        distances = np.sqrt(np.sum((current_col-color)**2,axis = 1))
    return np.where(distances == np.amin(distances))
    
def glue_images(images):
    """given an array of images returns a new image of n by n where n is the granulation inputed by the user resulted form stitching the smaller images together"""
    w,h = images[0].size
    tile_width = max([img.size[0] for img in imagesI])
    tile_height = max([img.size[1] for img in images])
    main_img = Image.new("RGB",(w*tile_width,h*tile_height))
    
    for i in range(len(images)):
        row = int(index/n)
        col = index - w*row 
        grid_img.paste(images[index], (col*width, row*height))

    return main_img

def generate_mosaic(main_image,images,granulation):
    """generate the mosaic given a main image and an array of input images"""

    print("The main image is being sliced")
    target_images = split(main_image,granulation)

    print("Finding the best placement for the images")
    output_images = []
    # for user feedback
    count = 0
    batch_size = int(len(target_images)/10)
    
    avgs = []
    for image in images:
        avgs.append(average_color(image))
    print(np.array(target_images))
    for image in target_images:
        target_avg = average_color(image)
        match_index = best_match_index(target_avg,avgs)
        output_images.append(images[match_index]) 

        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print('processed %d of %d...' %(count, len(target_images)))
        count += 1
    print("generating the mosaic")

    mosaic = glue_images(output_images)

def main():
    parser = argparse.ArgumentParser(description = "Create a simple mosaic out of given images")
    parser.add_argument("-b", dest = "main_image",required = True ,help = "the name of the image you want to make a mosaic out of")
    parser.add_argument("-f", dest = "folder",required = True, help ="the name of the folder in which you have the images used as tiles")
    # how fine the art should be (the size of the side of the tiles in which the main image is split in pixels)
    parser.add_argument('-g', dest = "granulation", required = False, help = "the granulation of the image; how big you want the silces to be inside your image in pixels; default value = 10px")    

    args = parser.parse_args()




    print("unpacking the photos...")    

    main = Image.open(f'{os.getcwd()}/{args.main_image}')
    input_images = get_tiles(args.folder,int(args.granulation))
    if input_images == []:
      print('No input images found in %s. Exiting.' % (args.folder, ))
      exit()

    print('generating the mosaic...')

    mosaic = generate_mosaic(main,input_images,int(args.granulation))
    mosaic.save("generated","PNG")
    print("done here,come back for more")




if __name__ == "__main__":
    main()

