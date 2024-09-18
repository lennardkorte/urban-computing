# AI6128 - Course Project 1

A real-world case study: smartphone-based indoor localization.

## Members

+ Jack Zhu Zhi Cheng
+ Tan Meng Xuan
+ Ong Jia Hui, Karyl

## Topic

+ Use a publicly available dataset to study indoor localization for smartphone

### Dataset

+ Source: Sample data from [Microsoft Indoor Location Competition 2.0](https://github.com/location-competition/indoor-location-competition-20)

+ Data collected by a Android smartphone in two multi-storey commercial building:

  + Site 1: 5 floors
  + Site 2: 9 floors

  

## Essential Tasks (100%)

1. Visualize way points (ground-truth locations)

   

2. Visualize geomagnetic heatmap

   

3. Visualize RSS heat maps of 3 Wi-Fi APs

   

## Bonus Tasks

+ Build a deep learning-based location fingerprint model.
+ Study the performance improvement brought by multi-modal machine learning.
+ Study the performance improvement brought by integrating temporal relationship via SLAM.
+ Any other claimable.



## Sample Result Visualizations

### Task 1 (Waypoint Visualization)

![site1--B1](README.assets/site1--B1.png)

### Task 2 (Geomagnetic Heatmap Visualization)

![site1--B1](README.assets/site1--B1-1607676174337.png)

### Task 3 (RSS Heatmap Visualization)

![0a-74-9c-2e-da-9b](README.assets/0a-74-9c-2e-da-9b.png)

## Pre-requisites
+ Python
+ Matplotlib
+ Numpy
+ Seaborn
+ Pandas
+ PyTorch
+ Jupyter 
+ Scikit-Learn

Otherwise, use the following Anaconda command to setup your environment:

```shell
conda env create --file env/ai6128uc_p1.yml
```


## Source Files
+ E1 - src/1_visualize_waypoints.py
+ E2 - src/2_visualize_geomagnetic.py
+ E3 - src/2_visualize_rss.py
+ B1 - src/maintrain_final.ipynb
