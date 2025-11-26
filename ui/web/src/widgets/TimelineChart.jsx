import { useEffect, useState } from "react";
import { api } from "../api.js";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function TimelineChart({fieldId}){
  const [points, setPoints] = useState([]);

  useEffect(()=>{
    api.get("/satellite/ndvi/timeline", {params:{field_id:fieldId, limit:20}})
      .then(r=>setPoints(r.data));
  },[fieldId]);

  if(!points.length){
    return <div className="bg-white rounded-xl p-4 shadow">No NDVI points yet.</div>
  }

  const labels = points.map(p=>new Date(p.date).toLocaleDateString());
  const data = {
    labels,
    datasets: [{label:"NDVI mean", data: points.map(p=>p.mean), tension:0.3}]
  };

  return (
    <div className="bg-white rounded-xl p-4 shadow">
      <div className="font-semibold mb-2">NDVI Timeline</div>
      <Line data={data}/>
    </div>
  );
}
