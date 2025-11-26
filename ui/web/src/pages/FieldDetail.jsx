import MapNdvi from "../widgets/MapNdvi.jsx";
import TimelineChart from "../widgets/TimelineChart.jsx";
import BeforeAfter from "../widgets/BeforeAfter.jsx";
import ReportPdfButton from "../widgets/ReportPdfButton.jsx";

export default function FieldDetail({fieldId, latestNdviId}){
  return (
    <div className="p-3 space-y-3">
      <MapNdvi latestNdviId={latestNdviId}/>
      <TimelineChart fieldId={fieldId}/>
      <BeforeAfter fieldId={fieldId}/>
      <ReportPdfButton fieldId={fieldId}/>
    </div>
  );
}
