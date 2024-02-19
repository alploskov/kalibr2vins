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

TEMPLATES = {
    'pinhole-radtan': PINHOLE_RADTAN
}
