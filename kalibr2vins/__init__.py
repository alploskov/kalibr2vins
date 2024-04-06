from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

import yaml
import typer
import numpy as np

from . import vins_config
from . import cameras_templates


kalibr2vins = typer.Typer()

def write_camera_conf(output_dir: Path, name: str, _camera_conf):
    if _camera_conf is None:
        return
    with (output_dir / f'{name}.yaml').open('w') as cam_file:
        camera_model = _camera_conf['camera_model'] + '-' + _camera_conf['distortion_model']
        cam_file.write(cameras_templates.TEMPLATES[camera_model].format(
            name=name,
            distortion_coeffs=_camera_conf['distortion_coeffs'],
            intrinsics=_camera_conf['intrinsics'],
            resolution=_camera_conf['resolution']
        ))
    
@kalibr2vins.command()
def main(cameras_conf: Path = typer.Option(help="Path to file with cameras config from kalibr. Its name usually ends with `-camchain-imucam.yaml`"),
        imu_conf: Optional[Path] = typer.Option(default=None, help="Optional path to file with imu config from kalibr. Its name usually ends with `-imu.yaml`"),
        output_dir: Path = typer.Option(Path('vins_config'), '-o', '--out', help="Path to dirrectory for vins configuration.")):
    """
    translate kalibr config to vins-fusion
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    _cameras_conf = yaml.load(cameras_conf.open(), Loader=yaml.FullLoader)
    _imu_conf = {}
    if imu_conf:
        _imu_conf = yaml.load(imu_conf.open(), Loader=yaml.FullLoader).get('imu0', {})
    write_camera_conf(output_dir, 'cam0', _cameras_conf.get('cam0'))
    write_camera_conf(output_dir, 'cam1', _cameras_conf.get('cam1'))

    out_conf = vins_config.Conf()
    out_conf.imu = 1 if imu_conf is not None else 0
    out_conf.num_of_cam = 2 if ('cam1' in _cameras_conf) else 1

    out_conf.imu_topic = _imu_conf.get('rostopic', '')
    out_conf.image0_topic = _cameras_conf.get('cam0', {}).get('rostopic', '')
    out_conf.image1_topic = _cameras_conf.get('cam1', {}).get('rostopic', '')
    out_conf.image_width = _cameras_conf.get('cam0', {}).get('resolution', [0, 0])[0]
    out_conf.image_height = _cameras_conf.get('cam0', {}).get('resolution', [0, 0])[1]

    if 'T_cam_imu' in  _cameras_conf.get('cam0', {}):
        out_conf.body_T_cam0 = np.linalg.inv(np.array(_cameras_conf.get('cam0', {}).get('T_cam_imu')))
    if 'T_cam_imu' in  _cameras_conf.get('cam1', {}):
        out_conf.body_T_cam1 = np.linalg.inv(np.array(_cameras_conf.get('cam1', {}).get('T_cam_imu')))
    with (output_dir / f'{output_dir.name}.yaml').open('w') as conf_file:
        conf_file.write(vins_config.TMP.render(**asdict(out_conf)))
