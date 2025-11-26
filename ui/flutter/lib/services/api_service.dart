import 'package:dio/dio.dart';

class ApiService {
  final String baseUrl;
  late final Dio _dio;

  ApiService({required this.baseUrl}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));
  }

  // Farms
  Future<List<dynamic>> getFarms() async {
    try {
      final response = await _dio.get('/farms/');
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> createFarm(Map<String, dynamic> data) async {
    try {
      final response = await _dio.post('/farms/', data: data);
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Fields
  Future<List<dynamic>> getFields({int? farmId}) async {
    try {
      final response = await _dio.get(
        '/fields/',
        queryParameters: farmId != null ? {'farm_id': farmId} : null,
      );
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getField(int fieldId) async {
    try {
      final response = await _dio.get('/fields/$fieldId');
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> createField(Map<String, dynamic> data) async {
    try {
      final response = await _dio.post('/fields/', data: data);
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Satellite Images
  Future<Map<String, dynamic>> fetchSatelliteImage(int fieldId) async {
    try {
      final response = await _dio.post(
        '/satellite/images/fetch',
        data: {'field_id': fieldId},
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<dynamic>> getSatelliteImages(int fieldId) async {
    try {
      final response = await _dio.get(
        '/satellite/images/',
        queryParameters: {'field_id': fieldId},
      );
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // NDVI Processing
  Future<Map<String, dynamic>> processNDVI(int imageId) async {
    try {
      final response = await _dio.post(
        '/satellite/ndvi/process',
        data: {'image_id': imageId},
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<dynamic>> getNDVIResults(int fieldId) async {
    try {
      final response = await _dio.get(
        '/satellite/ndvi/',
        queryParameters: {'field_id': fieldId},
      );
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getNDVIResult(int resultId) async {
    try {
      final response = await _dio.get('/satellite/ndvi/$resultId');
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // NDVI Timeline
  Future<List<dynamic>> getNDVITimeline(int fieldId) async {
    try {
      final response = await _dio.get(
        '/satellite/ndvi/timeline',
        queryParameters: {'field_id': fieldId},
      );
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Change Detection
  Future<Map<String, dynamic>> processChangeDetection({
    required int fieldId,
    required int oldNdviId,
    required int newNdviId,
  }) async {
    try {
      final response = await _dio.post(
        '/satellite/change/process',
        data: {
          'field_id': fieldId,
          'old_ndvi_id': oldNdviId,
          'new_ndvi_id': newNdviId,
        },
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Alerts
  Future<List<dynamic>> getAlerts(int fieldId) async {
    try {
      final response = await _dio.get(
        '/alerts/',
        queryParameters: {'field_id': fieldId},
      );
      return response.data as List<dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Weather
  Future<Map<String, dynamic>> getCurrentWeather({
    required double lat,
    required double lon,
  }) async {
    try {
      final response = await _dio.get(
        '/weather/current',
        queryParameters: {'lat': lat, 'lon': lon},
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getDailyWeather({
    required double lat,
    required double lon,
  }) async {
    try {
      final response = await _dio.get(
        '/weather/daily',
        queryParameters: {'lat': lat, 'lon': lon},
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Reports
  Future<Map<String, dynamic>> getWeeklyReport(int fieldId) async {
    try {
      final response = await _dio.get(
        '/reports/weekly',
        queryParameters: {'field_id': fieldId},
      );
      return response.data as Map<String, dynamic>;
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Helper method for tile URLs
  String getTileUrl(int resultId, int z, int x, int y) {
    return '$baseUrl/satellite/ndvi/tiles/$resultId/$z/$x/$y.png';
  }

  String getLegendUrl() {
    return '$baseUrl/satellite/ndvi/legend.png';
  }

  // Error handling
  String _handleError(dynamic error) {
    if (error is DioException) {
      if (error.response != null) {
        return error.response?.data['detail'] ?? 'حدث خطأ في الخادم';
      } else {
        return 'فشل الاتصال بالخادم';
      }
    }
    return 'حدث خطأ غير متوقع';
  }
}
