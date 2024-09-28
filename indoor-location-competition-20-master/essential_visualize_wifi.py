import os
import numpy as np
from extract_data_f import extract_data
from visualize_2_f import visualize_magnetic_heatmap, visuaize_wifi_scatter
from preprocessing import scale_floor_geometry, process_wifi_data
from collections import defaultdict
from util_f import data_floors
import argparse
import matplotlib
matplotlib.use('agg')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bssid', type=str, help='WiFi BSSID to be visualized')
    args = parser.parse_args()
    print('here', args.bssid)
    PAR_DIR = os.path.split(__file__)[0]
    DATA_DIR = os.path.join(PAR_DIR, '.', 'data')
    OUT_DIR = os.path.join(PAR_DIR, '.', 'output', 'essential_wifi')

    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)

    file_template = '%s_%s_%s_wifi.png'
    
    print('essential task: visualize wifi heat map')
    for i, (site_name, floor_name) in enumerate(data_floors(DATA_DIR)):
        print('%s %s (reading data)'%(site_name, floor_name))
        wifi_data = defaultdict(list)
        traces, floor_image, height, width, floor_geo = extract_data(DATA_DIR, site_name, floor_name)
        
        print('%s %s (processing data)'%(site_name, floor_name))
        paths = scale_floor_geometry(floor_geo, height, width)

        for trace in traces:
            trajectory_data = process_wifi_data(trace)
            for tdata in trajectory_data:
                x, y = tdata[0][1], tdata[0][2]
                all_wifi_data = tdata[1]
                for bssid, rssi in all_wifi_data.items():
                    wifi_data[bssid].append((x, y, rssi))
        
        viz_bssid = list(wifi_data.keys())[0] if args.bssid is None else args.bssid 
        print('%s %s %s(generating heatmap)'%(site_name, floor_name, viz_bssid))
        viz_rssi = np.array(wifi_data[viz_bssid])
        # fig = visualize_magnetic_heatmap(viz_rssi[:, 0], viz_rssi[:,1], viz_rssi[:,2], floor_image, height, width, site_name, floor_name, paths, viz_bssid, 'wifi')
        fig = visuaize_wifi_scatter(viz_rssi[:, 0], viz_rssi[:,1], viz_rssi[:,2], floor_image, height, width, site_name, floor_name, viz_bssid)
        output_filename = file_template % (site_name, floor_name, viz_bssid)
        output_filename = output_filename.replace(':', '-')
        output_path = os.path.join(OUT_DIR, output_filename)

        print('%s %s (saving as %s)'%(site_name, floor_name, output_filename))
        fig.savefig(output_path, bbox_inches='tight')

    print('COMPLETE')
