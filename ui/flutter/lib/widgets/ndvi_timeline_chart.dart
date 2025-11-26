import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../core/api.dart';

class NDVITimelineChart extends StatefulWidget {
  final int fieldId;
  const NDVITimelineChart({super.key, required this.fieldId});

  @override
  State<NDVITimelineChart> createState() => _NDVITimelineChartState();
}

class _NDVITimelineChartState extends State<NDVITimelineChart> {
  List<Map<String, dynamic>> points = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final res = await Api.dio.get("/satellite/ndvi/timeline", queryParameters: {
      "field_id": widget.fieldId,
      "limit": 20,
    });
    setState(() => points = List<Map<String, dynamic>>.from(res.data));
  }

  @override
  Widget build(BuildContext context) {
    if (points.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(12),
        child: Text("No NDVI points yet."),
      );
    }

    final spots = <FlSpot>[];
    for (int i = 0; i < points.length; i++) {
      spots.add(FlSpot(i.toDouble(), (points[i]["mean"] ?? 0).toDouble()));
    }

    return Card(
      margin: const EdgeInsets.all(12),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: SizedBox(
          height: 180,
          child: LineChart(
            LineChartData(
              minY: 0, maxY: 1,
              titlesData: const FlTitlesData(show: false),
              lineBarsData: [
                LineChartBarData(
                  spots: spots,
                  isCurved: true,
                  dotData: const FlDotData(show: false),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
