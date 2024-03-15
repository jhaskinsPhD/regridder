import os
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


# get the preferred geos chem colormap:
current_dir =os.path.dirname(os.path.abspath(__file__)) + '/gcpy/'
rgb_WhGrYlRd = np.genfromtxt(current_dir + '/colormaps/WhGrYlRd.txt', delimiter=' ')
WhGrYlRd = mcolors.ListedColormap(rgb_WhGrYlRd / 255.0)


def pretty_US_map(xarr, axis, title: str = '',  cbar_label: str = '', 
                  vmin: int = -99, vmax: int = 99, cmap=WhGrYlRd ):
    
    if (vmin==-99) and (vmax==99): 
        im1=xarr.plot.imshow(x='lon', y='lat', cmap=cmap,ax=axis,
                        add_colorbar=False)
    else: 
        im1=xarr.plot.imshow(x='lon', y='lat', cmap=cmap,ax=axis,
                        add_colorbar=False,vmin=vmin, vmax=vmax)
            
    cb = plt.colorbar(im1, orientation="vertical",ax=axis)
    cb.set_label(label=cbar_label)
    cb.ax.tick_params(labelsize='large')
    
    axis.coastlines()
    axis.set_global()
    axis.set_extent( [-130, -65, 20, 50.5]) # Boudns for showing just the US. 
    axis.set_title(title)
    
    return plt
