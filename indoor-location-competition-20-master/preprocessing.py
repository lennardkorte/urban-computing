import numpy as np
from compute_f import compute_step_positions

class Scaler2D:
    def __init__(self, target_h, target_w):
        self.xy_min = np.Infinity * np.ones((1,2))
        self.xy_max = -np.Infinity * np.ones((1,2))
        self.target_h = target_h
        self.target_w = target_w
    
    def update(self, ls):
        self.xy_min = np.vstack([self.xy_min, ls]).min(axis=0)
        self.xy_max = np.vstack([self.xy_max, ls]).max(axis=0)
   
    def scale(self, ls):
        out = np.zeros_like(ls)
        x_min = self.xy_min[0]
        y_min = self.xy_min[1]
        x_max = self.xy_max[0]
        y_max = self.xy_max[1]

        out[:, 0] = (ls[:, 0] - x_min) * self.target_w / (x_max - x_min)
        out[:, 1] = (ls[:, 1] - y_min) * self.target_h / (y_max - y_min)

        return out

def extract_waypoints(data, xy_only=True, augment=False):
    waypoints, accelerometer, rotation = [], [], []
    waypoints = data.waypoint
    if augment:
        waypoints = compute_step_positions(data.acce, data.ahrs, waypoints)

    return waypoints[:, 1:] if xy_only else waypoints

def extract_magnetic_data(data, augment=False):
    magnetic = data.magns
    original_magnetic_count = magnetic.shape[0]
    
    waypoints = extract_waypoints(data, augment=augment)

    wp_times = waypoints[:, 0]
    for row in magnetic:
        closest_idx = np.argmin(abs(wp_times - row[0]))
        row[0] = wp_times[closest_idx]

    result = []
    for time, x, y in waypoints:
        matching_mag = np.array([[m[1], m[2], m[3]] for m in magnetic if m[0] == time])
        mag_data = [time, x, y, 0.]
        if len(matching_mag) > 0:
            mag_data[3] = np.mean(np.sqrt(np.sum(matching_mag ** 2, axis=1)))
        result.append(mag_data)

    return result, original_magnetic_count, len(result)


def scale_floor_geometry(geo, height, width):
    scaler = Scaler2D(height, width)
    outer = []
    inner = []
    
    for i, feature in enumerate(geo):
        is_outer = i == 0

        for c in feature['geometry']['coordinates']:
            c = np.array(c).squeeze()
            if is_outer:
                scaler.update(c)
                outer.append(c)
            else:
                inner.append(c)
    
    outer = list(map(scaler.scale, outer)) 
    inner = list(map(scaler.scale, inner)) 

    return {'outer': outer, 'inner': inner}

def process_magnetic_data(data, dst=[]):
    step_positions = compute_step_positions(data.acce, data.ahrs, data.waypoint)
    mag_magnitudes = np.sqrt(np.sum(data.magn[:, 1:4]**2, axis=1))

    n = data.magn.shape[0]
    for i in range(n):
        mag_t, mag_x, mag_y, mag_z = data.magn[i, 0:4]
        mag_mag = mag_magnitudes[i]
        match_index = np.argmin(np.abs(mag_t - step_positions[:, 0]))
        step_t = step_positions[match_index, 0]
        step_x = step_positions[match_index, 1]
        step_y = step_positions[match_index, 2]

        dst.append([mag_t, mag_x, mag_y, mag_z, mag_mag, step_t, step_x, step_y])

    return dst
