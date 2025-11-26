from fastapi import APIRouter, Response
from app.modules.satellite.services.legend import generate_legend_png

router = APIRouter()

@router.get("/legend.png")
def legend_png():
    return Response(generate_legend_png(), media_type="image/png")
