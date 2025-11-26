import rasterio, numpy as np, os
from app.modules.satellite.services.raster_ops import save_ndvi_tif

def compute_delta_ndvi(old_tif, new_tif, out_path):
    with rasterio.open(old_tif) as old_src, rasterio.open(new_tif) as new_src:
        old = old_src.read(1).astype("float32")
        new = new_src.read(1).astype("float32")
        profile = new_src.profile; transform = new_src.transform
    delta = new - old
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    save_ndvi_tif(delta, transform, profile, out_path)
    valid = ~np.isnan(delta)
    stats = {
        "mean_delta": float(np.nanmean(delta)),
        "min_delta": float(np.nanmin(delta)),
        "max_delta": float(np.nanmax(delta)),
        "degraded_area_pct": float(np.sum(delta < -0.1)/np.sum(valid)*100) if np.sum(valid) else 0.0
    }
    return out_path, stats
