import mercantile, numpy as np
from PIL import Image
import rasterio

def ndvi_to_rgb(ndvi_tile):
    ndvi_norm = (ndvi_tile + 1) / 2.0
    ndvi_norm = np.clip(ndvi_norm, 0, 1)
    rgb = np.zeros((ndvi_tile.shape[0], ndvi_tile.shape[1], 3), dtype=np.uint8)
    rgb[..., 0] = (255 * (1 - ndvi_norm)).astype(np.uint8)
    rgb[..., 1] = (255 * ndvi_norm).astype(np.uint8)
    return rgb

def get_tile_from_tif(tif_path, z, x, y, tile_size=256):
    bounds = mercantile.bounds(x, y, z)
    minx, miny, maxx, maxy = bounds.west, bounds.south, bounds.east, bounds.north
    with rasterio.open(tif_path) as src:
        row_min, col_min = src.index(minx, maxy)
        row_max, col_max = src.index(maxx, miny)
        if row_min >= row_max or col_min >= col_max:
            return None
        window = rasterio.windows.Window.from_slices((row_min, row_max), (col_min, col_max))
        ndvi = src.read(1, window=window)
        if ndvi.size == 0:
            return None
    img = Image.fromarray(ndvi).resize((tile_size, tile_size), resample=Image.BILINEAR)
    return ndvi_to_rgb(np.array(img).astype("float32"))
