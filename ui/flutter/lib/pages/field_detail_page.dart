import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../core/api.dart';
import '../widgets/ndvi_timeline_chart.dart';
import '../widgets/before_after_slider.dart';
import '../widgets/report_button.dart';

class FieldDetailPage extends StatefulWidget {
  final int fieldId;
  final int ndviResultId; // latest result id to show tiles
  const FieldDetailPage({super.key, required this.fieldId, required this.ndviResultId});

  @override
  State<FieldDetailPage> createState() => _FieldDetailPageState();
}

class _FieldDetailPageState extends State<FieldDetailPage> {
  bool showNdvi = true;

  @override
  Widget build(BuildContext context) {
    final tilesUrl =
        "${Api.baseUrl}/satellite/ndvi/tiles/${widget.ndviResultId}/{z}/{x}/{y}.png";

    return Scaffold(
      appBar: AppBar(title: const Text("Field Detail")),
      body: ListView(
        children: [
          SizedBox(
            height: 320,
            child: FlutterMap(
              options: const MapOptions(
                initialCenter: LatLng(24.7, 46.7),
                initialZoom: 12,
              ),
              children: [
                TileLayer(
                  urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                if (showNdvi)
                  TileLayer(
                    urlTemplate: tilesUrl,
                    // NDVI tiles are PNG with transparency
                  ),
              ],
            ),
          ),
          SwitchListTile(
            value: showNdvi,
            onChanged: (v) => setState(() => showNdvi = v),
            title: const Text("Show NDVI Layer"),
          ),
          NDVITimelineChart(fieldId: widget.fieldId),
          const SizedBox(height: 12),
          BeforeAfterSection(fieldId: widget.fieldId),
          const SizedBox(height: 12),
          ReportButton(fieldId: widget.fieldId),
        ],
      ),
    );
  }
}
