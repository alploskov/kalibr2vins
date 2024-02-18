from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

import yaml
import typer
import numpy as np
from pprint import pprint

from . import vins_config
from . import cameras_templates


kalibr2vins = typer.Typer()
    
@kalibr2vins.command()
def main(cameras_conf: Path = typer.Option(help="Path to file with cameras config from kalibr. Its name usually ends with `-camchain-imucam.yaml`"),
        imu_conf: Optional[Path] = typer.Option(default=None, help="Optional path to file with imu config from kalibr. Its name usually ends with `-imu.yaml`"),
        output_dir: Optional[Path] = typer.Option(default=Path('.'), help="Path to dirrectory for vins configuration.")):
    """
    translate kalibr config to vins-fusion
    """
    _cameras_conf = yaml.load(cameras_conf.open(), Loader=yaml.FullLoader)
    out_conf = vins_config.Conf()
    out_conf.image0_topic = _cameras_conf['cam0']['rostopic']

    if 'cam1' in _cameras_conf:
        out_conf.num_of_cam = 2
        out_conf.image1_topic = _cameras_conf['cam1']['rostopic']

    out_conf.imu = 1 if imu_conf is not None else 0
    print(vins_config.TMP.format(**asdict(out_conf)))
