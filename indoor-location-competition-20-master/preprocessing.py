import numpy as np
from compute_f import compute_step_positions

def extract_waypoints(path: str, xy_only=True, augment=False):
    waypoints, accelerometer, rotation = [], [], []

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split('\t')
            if not line or line[0] == '#':
                continue
            if data[1] == 'TYPE_WAYPOINT':
                waypoints.append([int(data[0]), float(data[2]), float(data[3])])
            elif augment and data[1] == 'TYPE_ACCELEROMETER':
                accelerometer.append([int(data[0]), float(data[2]), float(data[3]), float(data[4])])
            elif augment and data[1] == 'TYPE_ROTATION_VECTOR':
                rotation.append([int(data[0]), float(data[2]), float(data[3]), float(data[4])])

    waypoints = np.array(waypoints)
    if augment:
        accelerometer, rotation = np.array(accelerometer), np.array(rotation)
        waypoints = compute_step_positions(accelerometer, rotation, waypoints)

    return waypoints[:, 1:] if xy_only else waypoints

def extract_magnetic_data(path: str, augment=False):
    magnetic, waypoints, accelerometer, rotation = [], [], [], []

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split('\t')
            if not line or line[0] == '#':
                continue
            if data[1] == 'TYPE_MAGNETIC_FIELD':
                magnetic.append([int(data[0]), float(data[2]), float(data[3]), float(data[4])])
            elif data[1] == 'TYPE_WAYPOINT':
                waypoints.append([int(data[0]), float(data[2]), float(data[3])])
            elif augment and data[1] == 'TYPE_ACCELEROMETER':
                accelerometer.append([int(data[0]), float(data[2]), float(data[3]), float(data[4])])
            elif augment and data[1] == 'TYPE_ROTATION_VECTOR':
                rotation.append([int(data[0]), float(data[2]), float(data[3]), float(data[4])])

    magnetic, waypoints = np.array(magnetic), np.array(waypoints)
    original_magnetic_count = len(magnetic)

    if augment:
        accelerometer, rotation = np.array(accelerometer), np.array(rotation)
        waypoints = compute_step_positions(accelerometer, rotation, waypoints)

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
