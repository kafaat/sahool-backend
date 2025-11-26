import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const API_BASE = "http://localhost:8000";

export default function MapNdvi({latestNdviId}){
  const ndviTiles = `${API_BASE}/satellite/ndvi/tiles/${latestNdviId}/{z}/{x}/{y}.png`;
  return (
    <div className="bg-white rounded-xl shadow overflow-hidden">
      <div className="p-2 font-semibold">NDVI Map</div>
      <div style={{height:320}}>
        <MapContainer center={[24.7,46.7]} zoom={12} style={{height:"100%"}}>
          <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <TileLayer url={ndviTiles} opacity={0.7}/>
        </MapContainer>
      </div>
    </div>
  );
}
