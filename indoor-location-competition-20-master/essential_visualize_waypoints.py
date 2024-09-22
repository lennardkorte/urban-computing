import os, json, random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from preprocessing import extract_waypoints
from extract_data_f import extract_data

def visualize_waypoints(waypoints, img, height, width, site, floor, wp_augment=False):
    plt.clf()
    fig, ax = plt.subplots()
    plt.tight_layout()
    random.seed(30)
    
    sns.set(style='white')
    ax.imshow(img, extent=[0,width,0,height])
    # map_scaler = (img.shape[0] / height + img.shape[1] / width) / 2

    for wps in waypoints:
        x, y = np.array(wps).T
        ax.plot(x , y, 'o-', markersize=2, linewidth=0.8)
    wp_count = sum(len(wps) for wps in waypoints)

    title = '%s, %s, %d Waypoints %s' % (
        site,
        floor,
        wp_count,
        'Augmented' if wp_augment else ''
    )
    filename = '%s, %s%s' % (
        site,
        floor,
        ', augmented' if wp_augment else ''
    )
    ax.set_title(title)
    ax.set_xlabel('X coordinates (meters)')
    ax.set_ylabel('Y coordinates (meters)')
    return fig, filename, sum(len(wps) for wps in waypoints)

if __name__ == '__main__':
    DATA_DIR = os.path.join('.', 'data')
    OUT_DIR = os.path.join('.', 'output', os.path.splitext(os.path.basename(__file__))[0])

    save_dir = OUT_DIR
    save_dpi = 200
    if not os.path.exists(save_dir): os.makedirs(save_dir)  # Embedded create_dir logic

    all_waypoints = {}

    for site in os.scandir(DATA_DIR):
        if not site.is_dir(): 
            continue
        for f in os.scandir(site.path):
            if not f.is_dir(): 
                continue
            traces, img, height, width, geo = extract_data(DATA_DIR, site.name, f.name)
            for augmented in [True, False]:
                waypoints = [extract_waypoints(data, augment=augmented) for data in traces]
                fig, filename, count = visualize_waypoints(waypoints, img, height, width, site.name, f.name, wp_augment=augmented)
                fig.savefig(os.path.join(save_dir, filename), dpi=save_dpi)
                all_waypoints[(augmented, site.name, f.name)] = count
                break
            break
        break

    print('COMPLETED:', all_waypoints)
