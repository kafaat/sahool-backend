import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'pages/home_page.dart';
import 'pages/farms_page.dart';
import 'pages/fields_page.dart';
import 'pages/field_detail_page.dart';
import 'services/api_service.dart';

void main() {
  runApp(const SahoolApp());
}

class SahoolApp extends StatelessWidget {
  const SahoolApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiService>(
          create: (_) => ApiService(baseUrl: 'http://localhost:8000'),
        ),
      ],
      child: MaterialApp(
        title: 'Sahool - Agricultural Monitoring',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.green,
          primaryColor: const Color(0xFF367C2B),
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF367C2B),
            brightness: Brightness.light,
          ),
          textTheme: GoogleFonts.cairoTextTheme(),
          useMaterial3: true,
          appBarTheme: AppBarTheme(
            backgroundColor: const Color(0xFF367C2B),
            foregroundColor: Colors.white,
            elevation: 0,
            centerTitle: true,
            titleTextStyle: GoogleFonts.cairo(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          cardTheme: CardTheme(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF367C2B),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const HomePage(),
          '/farms': (context) => const FarmsPage(),
          '/fields': (context) => const FieldsPage(),
        },
        onGenerateRoute: (settings) {
          if (settings.name == '/field-detail') {
            final args = settings.arguments as Map<String, dynamic>;
            return MaterialPageRoute(
              builder: (context) => FieldDetailPage(fieldId: args['fieldId']),
            );
          }
          return null;
        },
      ),
    );
  }
}
