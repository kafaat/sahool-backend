import rasterio
def save_ndvi_tif(ndvi_array, transform, profile, out_path):
    profile.update(dtype=rasterio.float32, count=1, compress="lzw", transform=transform)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(ndvi_array.astype(rasterio.float32), 1)
