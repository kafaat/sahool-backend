import 'package:flutter/material.dart';
import 'package:before_after/before_after.dart';
import '../core/api.dart';

class BeforeAfterSection extends StatefulWidget {
  final int fieldId;
  const BeforeAfterSection({super.key, required this.fieldId});

  @override
  State<BeforeAfterSection> createState() => _BeforeAfterSectionState();
}

class _BeforeAfterSectionState extends State<BeforeAfterSection> {
  String? beforeUrl;
  String? afterUrl;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final res = await Api.dio.get("/satellite/ndvi", queryParameters: {
      "field_id": widget.fieldId,
    });
    final list = List<Map<String, dynamic>>.from(res.data);
    if (list.length >= 2) {
      setState(() {
        afterUrl = _fileUrl(list[0]["ndvi_png_path"]);
        beforeUrl = _fileUrl(list[1]["ndvi_png_path"]);
      });
    }
  }

  String _fileUrl(String? path) {
    if (path == null) return "";
    // if you serve storage via nginx/static, replace with your base
    return "${Api.baseUrl}/$path";
  }

  @override
  Widget build(BuildContext context) {
    if (beforeUrl == null || afterUrl == null) {
      return const Padding(
        padding: EdgeInsets.all(12),
        child: Text("Need at least two NDVI results for before/after."),
      );
    }

    return Card(
      margin: const EdgeInsets.all(12),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: SizedBox(
          height: 220,
          child: BeforeAfter(
            before: Image.network(beforeUrl!, fit: BoxFit.cover),
            after: Image.network(afterUrl!, fit: BoxFit.cover),
          ),
        ),
      ),
    );
  }
}
