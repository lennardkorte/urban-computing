import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize as mpl_Normalize
from matplotlib.cm import ScalarMappable as mpl_ScalarMappable

def visualize_geometry(ax, paths):
    for path in paths['inner']:
        p = Polygon(path, fc='lightblue', ec='grey', linewidth=.5)
        ax.add_patch(p)

    for path in paths['outer']:
        p = Polygon(path, fc='none', ec='black', linewidth=1)
        ax.add_patch(p)

def visualize_labels(ax, title, site, floor, height, width):
    title = '%s, %s, %s' % (site, floor, title)
    xlabel = 'X-coordinates (meters)'
    ylabel = 'Y-coordinates (meters)'

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([0,width])
    ax.set_ylim([0,height])

def visualize_magnetic_heatmap(x,y,mag,floor_image,height,width,site,floor,paths):
    cmap = 'rainbow'
    title = 'Geomagnetic Heat Map'
    clabel = '\xB5T: micro-Tesla'
    hex_gridsize = int(width)//2
    width_ratios = [.95, .05]

    fig, axs = plt.subplots(1,2,width_ratios=width_ratios)
    ax, cax = axs.flatten()

    # heatmap title, labels, ticks
    visualize_labels(ax, title, site, floor, height, width)
    
    # plot background image
    # ax.imshow(floor_image, extent=(0,width,0,height))

    # plot hexbins
    h = ax.hexbin(x=x,y=y,C=mag,gridsize=hex_gridsize,cmap=cmap)
    
    # plot geometry
    visualize_geometry(ax, paths)
    
    # plot colorbar, and label
    vs = h.get_array().data
    plt.colorbar(mpl_ScalarMappable(norm=mpl_Normalize(vmin=vs.min(), vmax=vs.max()), cmap=cmap), cax=cax, label=clabel)
    
    return fig

def visuaize_wifi_scatter(x,y,mag,floor_image,height,width,site,floor,bssid):
    cmap = 'rainbow'
    fig, ax = plt.subplots()
    ax.imshow(floor_image, extent=[0,width,0,height])
    ax.set_title(f"{site}, {floor}, Wifi Heat map for {bssid}")
    ax.set_xlabel('X coordinates (meters)')
    ax.set_ylabel('Y coordinates (meters)')
    
    im = ax.scatter(x, y, c=mag, s=10, cmap=cmap)
    cbar = fig.colorbar(im, orientation='vertical', shrink=0.8)
    cbar.set_label('dBm: decibels')
    return fig