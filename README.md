# kalibr2vins

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/alploskov/kalibr2vins/blob/master/LICENSE.txt)
[![Hits-of-Code](https://hitsofcode.com/github/alploskov/kalibr2vins?branch=main)](https://hitsofcode.com/github/alploskov/kalibr2vins/view?branch=main)

**kalibr2vins** is a tool for converting [kalibr](https://github.com/ethz-asl/kalibr) results to [vins-fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) configurations

## Usage:

1. Calibrate the cameras by following this [tutorial](https://github.com/ethz-asl/kalibr/wiki/calibrating-the-vi-sensor)

2. Install kalibr2vins

3. run `kalibr2vins --cameras-conf dataset-camchain-imucam.yaml --imu-conf dataset-imu.yaml`

4. run vins-fusion with generated configuration
