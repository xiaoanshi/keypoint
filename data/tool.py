#coding:utf8
import torch as t
import numpy as np
from skimage import transform
from pylab import plt
from PIL import Image
from skimage import transform

def show_paf(img,paf,stride = 5,thres=0.1):
    """
    @param img: ndarry, HxWx3
    @param paf: ndarry, HxWxN
    """
    paf = transform.rescale(paf,img.shape[0]/paf.shape[0])
    h,w,n = paf.shape
    mask  = (paf**2).reshape(h,w,n/2,2).sum(axis=3).sum(axis=2)<thres
    paf[mask] = 0
    
#     img_size = img.shape[:2]
    X,Y = np.meshgrid(np.arange(0,w),np.arange(0,h))
    
    plt.imshow(img, alpha=0.5)
    res = plt.quiver( X[::stride,::stride],
                Y[::stride,::stride],
                -paf[::stride,::stride,::2].sum(axis=2),
                paf[::stride,::stride,1::2].sum(axis=2),            
                scale=20,
                units='width', headaxislength=0.01,
                    alpha=.8,
                    width=0.001,
                    color='r')
    return  res

def fig2np(fig):
    fig.canvas.draw()
    data = np.fromstring(ccc.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(ccc.canvas.get_width_height()[::-1] + (3,))
    return data

 
def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    h,w, d = buf.shape
    return Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf.reshape(h,w,4)



def PIL2array(img):
    return numpy.array(img.getdata(),
                    numpy.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)



def vis_paf(img,paf):
    #img = (img.cpu()*0.225+0.45).clamp(min=-1,max=1).numpy().transpose((1,2,0))
    img = img.numpy().transpose((1,2,0))
    paf =  paf.cpu().numpy().transpose((1,2,0))
    fig = show_paf(img,paf).get_figure()
    paf_img = fig2data(fig).astype(np.int32)
    plt.close()
    img4vis = t.from_numpy(paf_img[:,:,:3].transpose((2,0,1))/255.).float()
    return img4vis
    # vis.img('paf', img4vis)
    
