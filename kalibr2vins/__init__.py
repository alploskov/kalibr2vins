from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import yaml
import typer
import numpy as np


kalibr2vins = typer.Typer()

@dataclass
class Conf:
    imu: int = 0
    num_of_cam: int = 0
    imu_topic: str = ""

    image0_topic: str = ""
    image1_topic: str = ""
    output_path: str = "output"

    cam0_calib: str = "cam0.yaml"
    cam1_calib: str = "cam1.yaml"
    image_width: int = 0
    image_height: int = 0

    estimate_extrinsic: int = 0  # 0  Have an accurate extrinsic parameters. We will trust the following imu^R_cam, imu^T_cam, don't change it.
                                 # 1  Have an initial guess about extrinsic parameters. We will optimize around your initial guess.
    body_T_cam0: np.array = None
    body_T_cam1: np.array = None

    multiple_thread: int = 1 #Multiple thread support

    #feature traker paprameters
    max_cnt: int = 200         # max feature number in feature tracking
    min_dist: int = 30         # min distance between two features
    freq: int = 10             # frequence (Hz) of publish tracking result. At least 10Hz for good estimation. If set 0, the frequence will be same as raw image
    F_threshold: float = 1.0           # ransac threshold (pixel)
    show_track: int = 1                # publish tracking image as topic
    flow_back: int = 1                 # perform forward and backward optical flow to improve feature tracking accuracy

    #optimization parameters
    max_solver_time: float = 0.05      # max solver itration time (s), to guarantee real time
    max_num_iterations: int = 8        # max solver itrations, to guarantee real time
    keyframe_parallax: int = 10        # keyframe selection threshold (pixel)

    #imu parameters       The more accurate parameters you provide, the better performance
    acc_n: float = 0.1          # accelerometer measurement noise standard deviation. #0.2   0.04
    gyr_n: float = 0.01         # gyroscope measurement noise standard deviation.     #0.05  0.004
    acc_w: float = 0.001        # accelerometer bias random work noise standard deviation.  #0.02
    gyr_w: float = 1.0e-4       # gyroscope bias random work noise standard deviation.     #4.0e-5
    g_norm: float = 9.81007     # gravity magnitude

    #unsynchronization parameters
    estimate_td: int = 0        # online estimate time offset between camera and imu
    td: float = 0.0             # initial value of time offset. unit: s. readed image clock + td = real image clock (IMU clock)

    #loop closure parameters
    load_previous_pose_graph: int = 0        # load and reuse previous pose graph; load from 'pose_graph_save_path'
    pose_graph_save_path: str = "./output/pose_graph/" # save and load path
    save_image: int = 0                    # save image in pose graph for visualization prupose; you can close this function by setting 0

@kalibr2vins.command()
def gen(cameras_conf: Path = typer.Option(help="Path to file with cameras config from kalibr. Its name usually ends with `-imucam.yaml`"),
        imu_conf: Optional[Path] = typer.Option(default=None, help="Optional path to file with imu config from kalibr. Its name usually ends with `-imu.yaml`"),
        output_dir: Optional[Path] = typer.Option(default=Path('.'), help="Path to dirrectory for vins configuration.")):
    """
    translate kalibr config to vins-fusion
    """
    if not input_dir.is_dir():
        print("you must ")
        raise typer.Exit(code=1)
    typer.echo(input_dir, output_dir)
