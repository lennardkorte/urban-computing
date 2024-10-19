import os
from extract_data_f import extract_data
from visualize_2_f import visualize_magnetic_heatmap 
from preprocessing import scale_floor_geometry, process_magnetic_data
from util_f import data_floors

if __name__ == '__main__':
    import matplotlib
    matplotlib.use('agg')

    PAR_DIR = os.path.split(__file__)[0]
    DATA_DIR = os.path.join(PAR_DIR, '..', 'data')
    OUT_DIR = os.path.join(PAR_DIR, '..', 'output', 'essential_geomagnetic')

    if not os.path.exists(OUT_DIR): os.makedirs(OUT_DIR)

    file_template = '%s_%s_magnetic.png'
    
    print('essential task: visualize geomagnetic heat map')
    for i, (site_name, floor_name) in enumerate(data_floors(DATA_DIR)):
        print('%s %s (reading data)'%(site_name, floor_name))
        data = []
        traces, floor_image, height, width, floor_geo = extract_data(DATA_DIR, site_name, floor_name)
        
        print('%s %s (processing data)'%(site_name, floor_name))
        paths = scale_floor_geometry(floor_geo, height, width)
        for trace in traces:
            process_magnetic_data(trace, dst=data)
        _, _, _, _, mag, _, x, y = zip(*data)
        
        print('%s %s (generating heatmap)'%(site_name, floor_name))
        fig = visualize_magnetic_heatmap(x, y, mag, floor_image, height, width, site_name, floor_name, paths)
        output_filename = file_template % (site_name, floor_name)
        output_path = os.path.join(OUT_DIR, output_filename)

        print('%s %s (saving as %s)'%(site_name, floor_name, output_filename))
        fig.savefig(output_path, bbox_inches='tight')

    print('COMPLETE')
