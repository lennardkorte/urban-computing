import os
import matplotlib
from extract_data_f import extract_data
from visualize_2_f import visualize_magnetic_heatmap 
from preprocessing import scale_floor_geometry, process_magnetic_data
from glob import iglob

if __name__ == '__main__':
    matplotlib.use('agg')
    DATA_BASE_PATH = os.path.join('..', '..', 'indoor-location-competition-20', 'data')
    OUTPUT_PATH = os.path.join('..', 'output', 'essential_geomagnetic')
    if not os.path.exists(OUTPUT_PATH): 
        os.makedirs(OUTPUT_PATH)
    file_template = '%s_%s_magnetic.png'
    
    print('essential task: visualize geomagnetic heat map')
    for i,floor_path in enumerate(iglob(os.path.join(DATA_BASE_PATH, '*', '*'))):
        parts = floor_path.split(os.path.sep)
        floor_name = parts[-1]
        site_name = parts[-2]
        
        
        print('%s %s (reading data)'%(site_name, floor_name))
        data = []
        traces, floor_image, height, width, floor_geo = extract_data(DATA_BASE_PATH, site_name, floor_name)
        
        print('%s %s (processing data)'%(site_name, floor_name))
        paths = scale_floor_geometry(floor_geo, height, width)
        for trace in traces:
            process_magnetic_data(trace, dst=data)
        _, _, _, _, mag, _, x, y = zip(*data)
        
        print('%s %s (generating heatmap)'%(site_name, floor_name))
        fig = visualize_magnetic_heatmap(x, y, mag, floor_image, height, width, site_name, floor_name, paths)
        output_filename = file_template % (site_name, floor_name)
        output_path = os.path.join(OUTPUT_PATH, output_filename)

        print('%s %s (saving as %s)'%(site_name, floor_name, output_filename))
        fig.savefig(output_path)

    print('COMPLETE')
