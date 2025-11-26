import requests
from app.core.config import settings

CATALOGUE = "https://catalogue.dataspace.copernicus.eu/odata/v1"
DOWNLOAD = "https://download.dataspace.copernicus.eu/odata/v1"
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

def get_access_token():
    data = {
        "client_id": "cdse-public",
        "username": settings.cdse_user,
        "password": settings.cdse_pass,
        "grant_type": "password",
    }
    r = requests.post(TOKEN_URL, data=data, timeout=60)
    r.raise_for_status()
    return r.json()["access_token"]

def search_latest_s2_l2a(intersects_wkt: str, max_cloud=30):
    filt = (
        "Collection/Name eq 'SENTINEL-2' and "
        "Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' "
        "and att/OData.CSC.StringAttribute/Value eq 'S2MSI2A') and "
        f"Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' "
        f"and att/OData.CSC.DoubleAttribute/Value le {max_cloud}) and "
        f"intersects(area=geography'{intersects_wkt}')"
    )
    url = f"{CATALOGUE}/Products"
    params = {"$filter": filt, "$orderby": "ContentDate/Start desc", "$top": 1}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    values = r.json().get("value", [])
    return values[0] if values else None

def download_product(product_id: str, out_zip: str, token: str):
    url = f"{DOWNLOAD}/Products({product_id})/$value"
    headers = {"Authorization": f"Bearer {token}"}
    with requests.get(url, headers=headers, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(out_zip, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)
    return out_zip
