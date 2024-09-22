from os.path import join as path_join
from glob import iglob
from json import load as json_load
from PIL.Image import open as open_image
from io_f import read_data_file

def extract_data(data_dir, site, floor):
    floor_info_path = path_join(data_dir, site, floor, 'floor_info.json')
    floor_image_path = path_join(data_dir, site, floor, 'floor_image.png')
    floor_data_path = path_join(data_dir, site, floor, 'path_data_files', '*.txt')
    floor_geo_path = path_join(data_dir, site, floor, 'geojson_map.json')

    floor_info = json_load(open(floor_info_path))['map_info']
    height = floor_info['height']
    width = floor_info['width']
    
    traces = []
    
    floor_image = open_image(floor_image_path)

    floor_geo = json_load(open(floor_geo_path))['features']

    for j, filepath in enumerate(iglob(floor_data_path)):
        data = read_data_file(filepath)
        traces.append(data)
  
    return traces, floor_image, height, width, floor_geo
