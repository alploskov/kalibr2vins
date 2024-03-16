from dataclasses import dataclass
import numpy as np
from jinja2 import Template

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
    body_T_cam0: np.array = tuple([[0,1,3,4],[0,1,3,4],[0,1,3,4],[0,1,3,4]])
    body_T_cam1: np.array = tuple([[0,1,3,4],[0,1,3,4],[0,1,3,4],[0,1,3,4]])

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

    
TMP = Template('''%YAML:1.0

#common parameters
imu: {{imu}}
num_of_cam: {{num_of_cam}}

{% if imu %}imu_topic: "{{imu_topic}}"{% endif %}
image0_topic: "{{image0_topic}}"
{% if num_of_cam > 1 %}image1_topic: "{{image1_topic}}"{% endif %}
output_path: "{{output_path}}"

cam0_calib: "{{cam0_calib}}"
{% if num_of_cam > 1 %}cam1_calib: "{{cam1_calib}}"{% endif %}
image_width: {{image_width}}
image_height: {{image_height}}

# Extrinsic parameter between IMU and Camera.
estimate_extrinsic: {{estimate_extrinsic}}   # 0  Have an accurate extrinsic parameters. We will trust the following imu^R_cam, imu^T_cam, don't change it.
                        # 1  Have an initial guess about extrinsic parameters. We will optimize around your initial guess.

body_T_cam0: !!opencv-matrix
   rows: 4
   cols: 4
   dt: d
   data: [{{body_T_cam0[0][0]}}, {{body_T_cam0[0][1]}}, {{body_T_cam0[0][2]}}, {{body_T_cam0[0][3]}},
          {{body_T_cam0[1][0]}}, {{body_T_cam0[1][1]}}, {{body_T_cam0[1][2]}}, {{body_T_cam0[1][3]}},
          {{body_T_cam0[2][0]}}, {{body_T_cam0[2][1]}}, {{body_T_cam0[2][2]}}, {{body_T_cam0[2][3]}},
          {{body_T_cam0[3][0]}}, {{body_T_cam0[3][1]}}, {{body_T_cam0[3][2]}}, {{body_T_cam0[3][3]}}]
{% if num_of_cam > 1 %}
body_T_cam1: !!opencv-matrix
   rows: 4
   cols: 4
   dt: d
   data: [{{body_T_cam1[0][0]}}, {{body_T_cam1[0][1]}}, {{body_T_cam1[0][2]}}, {{body_T_cam1[0][3]}},
          {{body_T_cam1[1][0]}}, {{body_T_cam1[1][1]}}, {{body_T_cam1[1][2]}}, {{body_T_cam1[1][3]}},
          {{body_T_cam1[2][0]}}, {{body_T_cam1[2][1]}}, {{body_T_cam1[2][2]}}, {{body_T_cam1[2][3]}},
          {{body_T_cam1[3][0]}}, {{body_T_cam1[3][1]}}, {{body_T_cam1[3][2]}}, {{body_T_cam1[3][3]}}]
{% endif %}

#Multiple thread support
multiple_thread: {{multiple_thread}}

#feature traker paprameters
max_cnt: {{max_cnt}}            # max feature number in feature tracking
min_dist: {{min_dist}}            # min distance between two features
freq: {{freq}}                # frequence (Hz) of publish tracking result. At least 10Hz for good estimation. If set 0, the frequence will be same as raw image 
F_threshold: {{F_threshold}}        # ransac threshold (pixel)
show_track: {{show_track}}           # publish tracking image as topic
flow_back: {{flow_back}}            # perform forward and backward optical flow to improve feature tracking accuracy

#optimization parameters
max_solver_time: {{max_solver_time}}  # max solver itration time (s), to guarantee real time
max_num_iterations: {{max_num_iterations}}   # max solver itrations, to guarantee real time
keyframe_parallax: {{keyframe_parallax}} # keyframe selection threshold (pixel)

#imu parameters       The more accurate parameters you provide, the better performance
acc_n: {{acc_n}}          # accelerometer measurement noise standard deviation. #0.2   0.04
gyr_n: {{gyr_n}}         # gyroscope measurement noise standard deviation.     #0.05  0.004
acc_w: {{acc_w}}        # accelerometer bias random work noise standard deviation.  #0.02
gyr_w: {{gyr_w}}       # gyroscope bias random work noise standard deviation.     #4.0e-5
g_norm: {{g_norm}}     # gravity magnitude

#unsynchronization parameters
estimate_td: {{estimate_td}}                      # online estimate time offset between camera and imu
td: {{td}}            # initial value of time offset. unit: s. readed image clock + td = real image clock (IMU clock)

#loop closure parameters
load_previous_pose_graph: {{load_previous_pose_graph}}        # load and reuse previous pose graph; load from 'pose_graph_save_path'
pose_graph_save_path: "{{pose_graph_save_path}}" # save and load path
save_image: {{save_image}}                   # save image in pose graph for visualization prupose; you can close this function by setting 0
''')
