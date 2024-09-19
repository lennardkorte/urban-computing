import numpy as np
from compute_f import compute_step_positions

def parse_txt(txt_path: str, augment_wp=False):
    data = {"wp": [], "mg": [], "accel": [], "rotate": []}
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = line.strip().split('\t')
            if len(line_data) < 3 or line_data[0] == '#':
                continue
            
            unix_time, data_type = int(line_data[0]), line_data[1]
            try:
                values = list(map(float, line_data[2:]))
            except ValueError:
                continue
            
            if data_type == 'TYPE_WAYPOINT' and len(values) >= 2:
                data['wp'].append([unix_time, *values[:2]])
            elif data_type == 'TYPE_MAGNETIC_FIELD' and len(values) >= 3:
                data['mg'].append([unix_time, *values[:3]])
            elif augment_wp and len(values) >= 3:
                # Safely handle unexpected types
                key = data_type.split('_')[-1].lower()
                if key in data:
                    data[key].append([unix_time, *values[:3]])
                else:
                    print(f"Unexpected data type encountered: {data_type}")

    return {k: np.array(v) for k, v in data.items()}

def augment_waypoints(accel, rotate, wp):
    return compute_step_positions(np.array(accel), np.array(rotate), wp)

def get_waypoints(txt_path: str, xy_only=True, augment_wp=False):
    data = parse_txt(txt_path, augment_wp)
    wp = augment_waypoints(data['accel'], data['rotate'], data['wp']) if augment_wp else data['wp']
    return wp[:, 1:] if xy_only else wp

def get_magnetic_positions(txt_path: str, augment_wp=False):
    data = parse_txt(txt_path, augment_wp)
    wp = augment_waypoints(data['accel'], data['rotate'], data['wp']) if augment_wp else data['wp']
    
    mg, wp_time = data['mg'], wp[:, 0]
    mg[:, 0] = [wp_time[np.argmin(abs(wp_time - m[0]))] for m in mg]

    wp_magnetic = [[time, x_pos, y_pos, np.mean(np.linalg.norm(mg[mg[:, 0] == time, 1:], axis=1))] 
                   for time, x_pos, y_pos in wp]
    
    return wp_magnetic, len(data['mg']), len(wp)
