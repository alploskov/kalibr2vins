PINHOLE_RADTAN = """%YAML:1.0
---
model_type: PINHOLE
camera_name: {name}
image_width: {resolution[0]}
image_height: {resolution[1]}

distortion_parameters:
   k1: {distortion_coeffs[0]}
   k2: {distortion_coeffs[1]}
   p1: {distortion_coeffs[2]}
   p2: {distortion_coeffs[3]}
projection_parameters:
   fx: {intrinsics[0]}
   fy: {intrinsics[1]}
   cx: {intrinsics[2]}
   cy: {intrinsics[3]}
"""

OMNI_RADTAN = """%YAML:1.0
---
model_type: MEI
camera_name: {name}
image_width: {resolution[0]}
image_height: {resolution[1]}

mirror_parameters:
   xi: {intrinsics[0]}
distortion_parameters:
   k1: {distortion_coeffs[0]}
   k2: {distortion_coeffs[1]}
   p1: {distortion_coeffs[2]}
   p2: {distortion_coeffs[3]}
projection_parameters:
   gamma1: {intrinsics[1]}
   gamma2: {intrinsics[2]}
   u0: {intrinsics[3]}
   v0: {intrinsics[4]}
"""

TEMPLATES = {
    'pinhole-radtan': PINHOLE_RADTAN,
    'omni-radtan': OMNI_RADTAN,
}
