from PIL import Image
import numpy as np, os

def save_ndvi_png(ndvi_array, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ndvi_norm = (ndvi_array + 1) / 2.0
    ndvi_norm = np.clip(ndvi_norm, 0, 1)
    rgb = np.zeros((ndvi_norm.shape[0], ndvi_norm.shape[1], 3), dtype=np.uint8)
    rgb[..., 0] = (255 * (1 - ndvi_norm)).astype(np.uint8)
    rgb[..., 1] = (255 * ndvi_norm).astype(np.uint8)
    Image.fromarray(rgb).save(out_path)
    return out_path
