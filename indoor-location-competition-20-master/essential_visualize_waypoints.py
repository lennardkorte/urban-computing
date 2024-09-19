import os, json, random
import seaborn as sns, matplotlib.pyplot as plt, numpy as np
from process_data import get_waypoints

def visualize_waypoints(site, floor, save_dir=None, save_dpi=160, wp_augment=False):
    plt.clf()
    random.seed(30)
    floor_path = os.path.join("./data", site, floor)

    waypoints = [get_waypoints(os.path.join(floor_path, "path_data_files", f), xy_only=True, augment_wp=wp_augment) 
                 for f in os.listdir(os.path.join(floor_path, "path_data_files"))]

    with open(os.path.join(floor_path, "floor_info.json")) as file:
        map_info = json.load(file)['map_info']

    img = plt.imread(os.path.join(floor_path, "floor_image.png"))
    sns.set(style='white')
    plt.imshow(img)
    map_scaler = (img.shape[0] / map_info['height'] + img.shape[1] / map_info['width']) / 2

    for wps in waypoints:
        x, y = np.array(wps).T
        plt.plot(x * map_scaler, img.shape[0] - y * map_scaler, 'o-', markersize=3, linewidth=0.8)

    plt.title(f"{site}, {floor}, {sum(len(wps) for wps in waypoints)} Waypoints {'Augmented' if wp_augment else ''}")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{site}, {floor}{', augmented' if wp_augment else ''}"), dpi=save_dpi) if save_dir else plt.show()
    return sum(len(wps) for wps in waypoints)

if __name__ == '__main__':
    save_dir = os.path.join("./output", os.path.splitext(os.path.basename(__file__))[0])
    if not os.path.exists(save_dir): os.makedirs(save_dir)  # Embedded create_dir logic
    
    for augmented in [False, True]:
        all_waypoints = { 
            (site.name, f.name): visualize_waypoints(site.name, f.name, save_dir, 200, augmented)
            for site in os.scandir("./data") if site.is_dir() 
            for f in os.scandir(site.path) if f.is_dir()  # Embedded get_site_floors logic
        }
    
    print('COMPLETED:', all_waypoints)
