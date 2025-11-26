import rasterio
from rasterio.windows import Window
from rasterio.mask import mask
import numpy as np
from shapely.geometry import mapping

def compute_ndvi_windowed(red_path, nir_path, field_polygon, tile_size=1024):
    with rasterio.open(red_path) as red_src, rasterio.open(nir_path) as nir_src:
        profile = red_src.profile
        width, height = red_src.width, red_src.height
        ndvi_full = np.full((height, width), np.nan, dtype="float32")
        for row_off in range(0, height, tile_size):
            for col_off in range(0, width, tile_size):
                window = Window(
                    col_off, row_off,
                    min(tile_size, width - col_off),
                    min(tile_size, height - row_off)
                )
                red = red_src.read(1, window=window).astype("float32")
                nir = nir_src.read(1, window=window).astype("float32")
                denom = nir + red
                denom[denom == 0] = np.nan
                ndvi = (nir - red) / denom
                ndvi_full[row_off:row_off+ndvi.shape[0], col_off:col_off+ndvi.shape[1]] = ndvi

    with rasterio.open(red_path) as ref_src:
        ref_crop, transform = mask(ref_src, [mapping(field_polygon)], crop=True, filled=False)
        crop_h, crop_w = ref_crop.shape[1], ref_crop.shape[2]
        ref_mask = ref_crop[0].mask
        crop = ndvi_full[:crop_h, :crop_w]
        crop = np.where(ref_mask, np.nan, crop)

    stats = {
        "mean": float(np.nanmean(crop)),
        "min": float(np.nanmin(crop)),
        "max": float(np.nanmax(crop)),
    }
    return crop, transform, profile, stats
