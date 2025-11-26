import { useEffect, useState } from "react";
import { api } from "../api.js";
import ReactCompareImage from "react-compare-image";

const API_BASE = "http://localhost:8000";

export default function BeforeAfter({fieldId}){
  const [beforeUrl, setBefore] = useState(null);
  const [afterUrl, setAfter] = useState(null);

  useEffect(()=>{
    api.get("/satellite/ndvi", {params:{field_id:fieldId}})
      .then(r=>{
        const list=r.data;
        if(list.length>=2){
          setAfter(`${API_BASE}/${list[0].ndvi_png_path}`);
          setBefore(`${API_BASE}/${list[1].ndvi_png_path}`);
        }
      });
  },[fieldId]);

  if(!beforeUrl||!afterUrl){
    return <div className="bg-white rounded-xl p-4 shadow">Need two NDVI results for before/after.</div>
  }

  return (
    <div className="bg-white rounded-xl p-4 shadow">
      <div className="font-semibold mb-2">Before / After NDVI</div>
      <div style={{height:260}}>
        <ReactCompareImage leftImage={beforeUrl} rightImage={afterUrl}/>
      </div>
    </div>
  );
}
