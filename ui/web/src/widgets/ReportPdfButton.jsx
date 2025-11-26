import { api } from "../api.js";
import jsPDF from "jspdf";

export default function ReportPdfButton({fieldId}){
  const gen = async ()=>{
    const {data} = await api.get("/reports/weekly", {params:{field_id:fieldId}});
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text("Sahool Weekly Report", 10, 15);
    doc.setFontSize(12);
    doc.text(`Field ID: ${fieldId}`, 10, 25);

    doc.text("NDVI (last weeks):", 10, 35);
    let y=42;
    data.ndvi_last_weeks.forEach(r=>{
      doc.text(`${r.date}: mean=${r.mean}`, 12, y);
      y+=7;
    });

    y+=5;
    doc.text("Alerts:", 10, y);
    y+=7;
    data.alerts.forEach(a=>{
      doc.text(`${a.date}: ${a.message}`, 12, y);
      y+=7;
    });

    doc.save(`weekly_report_field_${fieldId}.pdf`);
  };

  return (
    <button onClick={gen} className="w-full bg-green-600 text-white py-2 rounded-xl">
      Download Weekly PDF
    </button>
  );
}
