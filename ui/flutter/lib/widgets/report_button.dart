import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import '../core/api.dart';

class ReportButton extends StatelessWidget {
  final int fieldId;
  const ReportButton({super.key, required this.fieldId});

  Future<Uint8List> _buildPdf() async {
    final res = await Api.dio.get("/reports/weekly", queryParameters: {
      "field_id": fieldId,
    });
    final data = res.data;

    final pdf = pw.Document();
    pdf.addPage(
      pw.Page(
        build: (ctx) => pw.Column(
          crossAxisAlignment: pw.CrossAxisAlignment.start,
          children: [
            pw.Text("Sahool Weekly Report", style: pw.TextStyle(fontSize: 20)),
            pw.SizedBox(height: 10),
            pw.Text("Field ID: $fieldId"),
            pw.SizedBox(height: 10),
            pw.Text("NDVI last weeks:"),
            pw.Column(
              children: (data["ndvi_last_weeks"] as List)
                .map((r) => pw.Text("${r["date"]}: mean=${r["mean"]}"))
                .toList(),
            ),
            pw.SizedBox(height: 10),
            pw.Text("Alerts:"),
            pw.Column(
              children: (data["alerts"] as List)
                .map((a) => pw.Text("${a["date"]}: ${a["message"]}"))
                .toList(),
            ),
          ],
        ),
      ),
    );
    return pdf.save();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12),
      child: ElevatedButton.icon(
        icon: const Icon(Icons.picture_as_pdf),
        label: const Text("Generate Weekly PDF"),
        onPressed: () async {
          final bytes = await _buildPdf();
          await Printing.layoutPdf(onLayout: (_) async => bytes);
        },
      ),
    );
  }
}
