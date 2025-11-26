import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

class FieldDrawPage extends StatefulWidget {
  final String apiBaseUrl; // e.g. http://yourserver:8000
  const FieldDrawPage({super.key, required this.apiBaseUrl});

  @override
  State<FieldDrawPage> createState() => _FieldDrawPageState();
}

class _FieldDrawPageState extends State<FieldDrawPage> {
  final MapController mapController = MapController();
  final List<LatLng> polygonPoints = [];
  String shape = "polygon"; // polygon|circle|rectangle|semicircle

  // circle settings
  LatLng? circleCenter;
  double circleRadiusM = 100;

  // rectangle settings
  LatLng? rectStart;
  LatLng? rectEnd;

  // semicircle settings
  String semiDirection = "up";

  void onTapMap(TapPosition pos, LatLng latlng) {
    setState(() {
      if (shape == "polygon") {
        polygonPoints.add(latlng);
      } else if (shape == "circle") {
        circleCenter = latlng;
      } else if (shape == "rectangle") {
        if (rectStart == null) rectStart = latlng;
        else rectEnd = latlng;
      } else if (shape == "semicircle") {
        circleCenter = latlng;
      }
    });
  }

  Future<void> saveField() async {
    Map<String, dynamic> payload;

    if (shape == "polygon") {
      if (polygonPoints.length < 3) return;
      payload = {
        "name": "Flutter Field",
        "shape": "polygon",
        "data": {
          "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [
              polygonPoints.map((p) => [p.longitude, p.latitude]).toList()
                ..add([polygonPoints.first.longitude, polygonPoints.first.latitude])
            ]
          }
        }
      };
    } else if (shape == "circle") {
      if (circleCenter == null) return;
      payload = {
        "name": "Flutter Circle",
        "shape": "circle",
        "data": {
          "center_lat": circleCenter!.latitude,
          "center_lon": circleCenter!.longitude,
          "radius_m": circleRadiusM
        }
      };
    } else if (shape == "rectangle") {
      if (rectStart == null || rectEnd == null) return;
      payload = {
        "name": "Flutter Rect",
        "shape": "rectangle",
        "data": {
          "lat1": rectStart!.latitude,
          "lon1": rectStart!.longitude,
          "lat2": rectEnd!.latitude,
          "lon2": rectEnd!.longitude,
        }
      };
    } else {
      if (circleCenter == null) return;
      payload = {
        "name": "Flutter Semi",
        "shape": "semicircle",
        "data": {
          "center_lat": circleCenter!.latitude,
          "center_lon": circleCenter!.longitude,
          "radius_m": circleRadiusM,
          "direction": semiDirection
        }
      };
    }

    final res = await http.post(
      Uri.parse("${widget.apiBaseUrl}/fields/"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(payload),
    );

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(res.statusCode == 200 ? "Saved!" : "Error: ${res.body}")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Draw Field"),
        actions: [
          IconButton(onPressed: saveField, icon: const Icon(Icons.save))
        ],
      ),
      body: Column(
        children: [
          _shapePicker(),
          Expanded(
            child: FlutterMap(
              mapController: mapController,
              options: MapOptions(
                initialCenter: const LatLng(24.7, 46.7),
                initialZoom: 12,
                onTap: onTapMap,
              ),
              children: [
                TileLayer(
                  urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                  userAgentPackageName: "com.sahool.app",
                ),
                if (shape == "polygon" && polygonPoints.length >= 2)
                  PolygonLayer(
                    polygons: [
                      Polygon(points: polygonPoints, color: Colors.green.withOpacity(0.3), borderColor: Colors.green)
                    ],
                  ),
                if (shape == "circle" && circleCenter != null)
                  CircleLayer(circles: [
                    CircleMarker(point: circleCenter!, radius: circleRadiusM / 2, useRadiusInMeter: true, color: Colors.blue.withOpacity(0.3))
                  ]),
                if (shape == "rectangle" && rectStart != null && rectEnd != null)
                  PolygonLayer(polygons: [
                    Polygon(points: [
                      rectStart!,
                      LatLng(rectStart!.latitude, rectEnd!.longitude),
                      rectEnd!,
                      LatLng(rectEnd!.latitude, rectStart!.longitude),
                    ], color: Colors.orange.withOpacity(0.3), borderColor: Colors.orange)
                  ]),
                if (shape == "semicircle" && circleCenter != null)
                  CircleLayer(circles: [
                    CircleMarker(point: circleCenter!, radius: circleRadiusM / 2, useRadiusInMeter: true, color: Colors.purple.withOpacity(0.3))
                  ]),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _shapePicker() {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Row(
        children: [
          DropdownButton<String>(
            value: shape,
            items: const [
              DropdownMenuItem(value: "polygon", child: Text("Polygon")),
              DropdownMenuItem(value: "circle", child: Text("Circle")),
              DropdownMenuItem(value: "rectangle", child: Text("Rectangle")),
              DropdownMenuItem(value: "semicircle", child: Text("Semi Circle")),
            ],
            onChanged: (v) => setState(() {
              shape = v!;
              polygonPoints.clear();
              rectStart = rectEnd = null;
              circleCenter = null;
            }),
          ),
          const SizedBox(width: 12),
          if (shape == "circle" || shape == "semicircle")
            Expanded(
              child: Slider(
                min: 20, max: 500, divisions: 48,
                label: "${circleRadiusM.round()}m",
                value: circleRadiusM,
                onChanged: (v) => setState(() => circleRadiusM = v),
              ),
            ),
          if (shape == "semicircle")
            DropdownButton<String>(
              value: semiDirection,
              items: const [
                DropdownMenuItem(value: "up", child: Text("Up")),
                DropdownMenuItem(value: "down", child: Text("Down")),
                DropdownMenuItem(value: "left", child: Text("Left")),
                DropdownMenuItem(value: "right", child: Text("Right")),
              ],
              onChanged: (v) => setState(() => semiDirection = v!),
            )
        ],
      ),
    );
  }
}
