import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('سهول - نظام المراقبة الزراعية'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Welcome Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    Icon(
                      Icons.agriculture,
                      size: 64,
                      color: Theme.of(context).primaryColor,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'مرحباً بك في سهول',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'نظام متكامل لمراقبة وتحليل الأراضي الزراعية باستخدام صور الأقمار الصناعية',
                      style: Theme.of(context).textTheme.bodyMedium,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Features Grid
            Text(
              'الميزات الرئيسية',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              childAspectRatio: 1.1,
              children: [
                _buildFeatureCard(
                  context,
                  icon: Icons.map,
                  title: 'المزارع والحقول',
                  description: 'إدارة المزارع والحقول',
                  color: Colors.green,
                  onTap: () => Navigator.pushNamed(context, '/farms'),
                ),
                _buildFeatureCard(
                  context,
                  icon: Icons.satellite_alt,
                  title: 'صور الأقمار',
                  description: 'تحليل صور Sentinel-2',
                  color: Colors.blue,
                  onTap: () => Navigator.pushNamed(context, '/fields'),
                ),
                _buildFeatureCard(
                  context,
                  icon: Icons.analytics,
                  title: 'تحليل NDVI',
                  description: 'مؤشر الغطاء النباتي',
                  color: Colors.orange,
                  onTap: () => Navigator.pushNamed(context, '/fields'),
                ),
                _buildFeatureCard(
                  context,
                  icon: Icons.notifications_active,
                  title: 'التنبيهات',
                  description: 'تنبيهات التغيرات',
                  color: Colors.red,
                  onTap: () => Navigator.pushNamed(context, '/fields'),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Quick Actions
            Text(
              'الإجراءات السريعة',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            _buildActionButton(
              context,
              icon: Icons.add_location,
              title: 'إضافة حقل جديد',
              onTap: () => Navigator.pushNamed(context, '/fields'),
            ),
            const SizedBox(height: 12),
            _buildActionButton(
              context,
              icon: Icons.cloud_download,
              title: 'تحديث صور الأقمار',
              onTap: () => Navigator.pushNamed(context, '/fields'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String description,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: color),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                description,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildActionButton(
    BuildContext context, {
    required IconData icon,
    required String title,
    required VoidCallback onTap,
  }) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: Theme.of(context).primaryColor),
        title: Text(title),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: onTap,
      ),
    );
  }
}
