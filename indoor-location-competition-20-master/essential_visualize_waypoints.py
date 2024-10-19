import os, json, random
import matplotlib.pyplot as plt, numpy as np
from preprocessing import extract_waypoints
from extract_data_f import extract_data
from util_f import data_floors

def visualize_waypoints(waypoints, img, height, width, site, floor, wp_augment=False):
    fig, ax = plt.subplots()

    ax.imshow(img, extent=[0,width,0,height])

    wp_count = sum(len(wps) for wps in waypoints)
    for wps in waypoints:
        x, y = np.array(wps).T
        ax.plot(x , y, 'o-', markersize=2, linewidth=0.8)

    filename = '%s, %s%s' % (site,floor,', augmented' if wp_augment else '')
    ax.set_title('%s, %s, %d Waypoints %s' % (site,floor,wp_count,'Augmented' if wp_augment else ''))
    ax.set_xlabel('X coordinates (meters)')
    ax.set_ylabel('Y coordinates (meters)')

    return fig, filename, wp_count

if __name__ == '__main__':
    data_dir = os.path.join('.', 'data')
    save_dir = os.path.join('.', 'output', os.path.splitext(os.path.basename(__file__))[0])
    save_dpi = 200

    if not os.path.exists(save_dir): os.makedirs(save_dir)  # Embedded create_dir logic

    all_waypoints = {}
    for site, floor in data_floors(data_dir):
        traces, img, height, width, geo = extract_data(data_dir, site, floor)
        for augmented in [True, False]:
            waypoints = [extract_waypoints(data, augment=augmented) for data in traces]
            fig, fname, count = visualize_waypoints(waypoints, img, height, width, site, floor, wp_augment=augmented)
            fig.savefig(os.path.join(save_dir, fname), dpi=save_dpi, bbox_inches='tight')
            all_waypoints[(augmented, site, floor)] = count

    print('COMPLETED:', all_waypoints)
