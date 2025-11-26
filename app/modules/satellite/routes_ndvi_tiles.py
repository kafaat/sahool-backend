from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import NDVIResult
from app.modules.satellite.services.tiles import get_tile_from_tif
from PIL import Image
import io

router = APIRouter()

@router.get("/tiles/{result_id}/{z}/{x}/{y}.png")
def ndvi_tile(result_id: int, z: int, x: int, y: int, db: Session = Depends(get_db)):
    r = db.query(NDVIResult).get(result_id)
    if not r:
        raise HTTPException(404, "NDVIResult not found")
    rgb = get_tile_from_tif(r.ndvi_tif_path, z, x, y)
    if rgb is None:
        raise HTTPException(404, "Empty tile")
    buff = io.BytesIO()
    Image.fromarray(rgb).save(buff, format="PNG")
    return Response(buff.getvalue(), media_type="image/png")
