import os
import numpy as np
import pandas as pd
from collections import defaultdict
from extract_data_f import extract_data
from preprocessing import process_wifi_data, process_magnetic_data
from util_f import data_floors
from sklearn.preprocessing import LabelEncoder


PAR_DIR = os.path.split(__file__)[0]
DATA_DIR = os.path.join(PAR_DIR, '.', 'data')
OUT_DIR = os.path.join(PAR_DIR, '.', 'output', 'localization')
n = 10
train_test_split = 0.8

for i, (site_name, floor_name) in enumerate(data_floors(DATA_DIR)):
    print('%s %s (reading data)'%(site_name, floor_name))
    traces, floor_image, height, width, floor_geo = extract_data(DATA_DIR, site_name, floor_name)
    
    wifi_data = defaultdict(list)
    data = []

    for trace in traces:
        wifi_trajectory_data = process_wifi_data(trace, group_var='ssid', augment=True)
        process_magnetic_data(trace, dst=data)
        
        for tdata in wifi_trajectory_data:
            ts, x, y = tdata[0][0], tdata[0][1], tdata[0][2]
            all_wifi_data = tdata[1]
            for ssid, rssi in all_wifi_data.items():
                wifi_data[ssid].append((ts, x, y, rssi))
    
    # Obtain WiFi data
    topn = {k: len(v) for k, v in wifi_data.items()}
    topn = sorted(topn.items(), key=lambda x: x[1], reverse=True)
    topn = topn[1:n+1]
    wifi_df = None

    for wifi_ssid in topn:
        _df = pd.DataFrame(wifi_data[wifi_ssid[0]], columns=['ts', 'x', 'y', 'rssi'])
        _df['wifi_ap'] = wifi_ssid[0]
        if wifi_df is None:
            wifi_df = _df
        else:
            wifi_df = pd.concat([wifi_df, _df], axis=0)

    # Obtain Mag data
    mag_df = pd.DataFrame(data, columns=['mag_t', 'mag_x', 'mag_y', 'mag_z', 'mag_mag', 'ts', 'x', 'y'])

    # Join
    df = pd.merge(wifi_df, mag_df, on=['ts', 'x', 'y'], how='inner')
    df = df.drop_duplicates(subset=['x', 'y']).reset_index(drop=True)

    # Pre-Processing
    df = df[['ts', 'x', 'y', 'rssi', 'wifi_ap', 'mag_x', 'mag_y', 'mag_z', 'mag_mag']]
    df = df.sort_values(by='ts')
    le = LabelEncoder()
    le.fit(df['wifi_ap'])
    df['wifi_ap'] = le.transform(df['wifi_ap'])
    
    # Train-Test Split
    n_test = int(train_test_split * len(df))
    train, test = df[:n_test], df[n_test:]
    train.to_csv(os.path.join(OUT_DIR, f"train_{site_name}_{floor_name}.csv"), index=False)
    test.to_csv(os.path.join(OUT_DIR, f"test_{site_name}_{floor_name}.csv"), index=False)