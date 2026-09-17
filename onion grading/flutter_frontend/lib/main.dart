import 'dart:convert';
import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';

const apiBase =
    String.fromEnvironment('API_URL', defaultValue: 'http://127.0.0.1:8000');

Map<String, String> translations = {};
String tr(String key) => translations[key] ?? key;
String localeFor(String lang) =>
    {
      'en': 'en_IN',
      'hi': 'hi_IN',
      'kn': 'kn_IN',
      'ta': 'ta_IN',
      'mr': 'mr_IN',
      'bn': 'bn_IN'
    }[lang] ??
    'en_IN';
String number(double value, String lang, {int decimals = 0}) =>
    NumberFormat.decimalPatternDigits(
            locale: localeFor(lang), decimalDigits: decimals)
        .format(value);

void main() => runApp(const PyaazManiApp());

class PyaazManiApp extends StatefulWidget {
  const PyaazManiApp({super.key});
  @override
  State<PyaazManiApp> createState() => _PyaazManiAppState();
}

class _PyaazManiAppState extends State<PyaazManiApp> {
  bool dark = false;
  String role = 'farmer';
  String lang = 'en';
  int page = 0;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, String>>(
      future: Api.translations(lang),
      builder: (context, snapshot) {
        if (!snapshot.hasData)
          return const MaterialApp(
              home: Scaffold(body: Center(child: CircularProgressIndicator())));
        translations = snapshot.data!;
        return MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'PyaazMani',
          theme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(
              seedColor:
                  dark ? const Color(0xfff3a6bc) : const Color(0xffa7194b),
              brightness: dark ? Brightness.dark : Brightness.light,
            ),
            fontFamily: 'Georgia',
          ),
          home: Shell(
            dark: dark,
            role: role,
            lang: lang,
            page: page,
            onPage: (value) => setState(() => page = value),
            onRole: (value) => setState(() {
              role = value;
              page = 0;
            }),
            onTheme: () => setState(() => dark = !dark),
            onLang: (value) => setState(() => lang = value),
          ),
        );
      },
    );
  }
}

class Shell extends StatelessWidget {
  const Shell(
      {super.key,
      required this.dark,
      required this.role,
      required this.lang,
      required this.page,
      required this.onPage,
      required this.onRole,
      required this.onTheme,
      required this.onLang});
  final bool dark;
  final String role;
  final String lang;
  final int page;
  final ValueChanged<int> onPage;
  final ValueChanged<String> onRole;
  final VoidCallback onTheme;
  final ValueChanged<String> onLang;

  String _userName() {
    const names = {
      'farmer': 'Ramesh Kumar',
      'inspector': 'Anjali Sharma',
      'official': 'Saurabh Nair',
    };
    return names[role] ?? 'User';
  }

  String _userInitials() {
    final parts = _userName().trim().split(RegExp(r'\s+'));
    if (parts.length == 1) {
      return parts.first.substring(0, 1).toUpperCase();
    }
    return '${parts.first[0]}${parts.last[0]}'.toUpperCase();
  }

  List<Map<String, dynamic>> _navItems() {
    final items = [
      {
        'title': tr('home_chapters_title'),
        'icon': Icons.grid_view_rounded,
        'index': 0
      },
      {'title': tr('nav_grade'), 'icon': Icons.biotech_outlined, 'index': 1},
      {'title': tr('nav_mandi'), 'icon': Icons.storefront_outlined, 'index': 2},
      {
        'title': tr('nav_analytics'),
        'icon': Icons.insights_outlined,
        'index': 4
      },
      {'title': tr('nav_settings'), 'icon': Icons.tune_outlined, 'index': 5},
    ];
    if (role == 'official') {
      items.insert(3, {
        'title': tr('nav_reports'),
        'icon': Icons.description_outlined,
        'index': 3
      });
    }
    return items;
  }

  @override
  Widget build(BuildContext context) {
    final roleNames = {
      'farmer': tr('role_farmer'),
      'inspector': tr('role_inspector'),
      'official': tr('role_official'),
    };
    return Scaffold(
      appBar: AppBar(
        leading: Builder(
          builder: (context) => IconButton(
            tooltip: 'Open menu',
            onPressed: () => Scaffold.of(context).openDrawer(),
            icon: const Icon(Icons.menu_rounded),
          ),
        ),
        title: Text(tr('app_brand'),
            style:
                const TextStyle(fontWeight: FontWeight.w900, letterSpacing: 1)),
        actions: [
          DropdownButton<String>(
              value: role,
              underline: const SizedBox(),
              items: roleNames.entries
                  .map((entry) => DropdownMenuItem(
                      value: entry.key, child: Text(entry.value)))
                  .toList(),
              onChanged: (value) {
                if (value != null) onRole(value);
              }),
          const SizedBox(width: 12),
          IconButton(
              tooltip: 'Toggle theme',
              onPressed: onTheme,
              icon: Icon(
                  dark ? Icons.light_mode_outlined : Icons.dark_mode_outlined)),
          const SizedBox(width: 12),
        ],
      ),
      drawer: Drawer(
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primaryContainer,
                ),
                child: Row(
                  children: [
                    CircleAvatar(
                      radius: 24,
                      backgroundColor: Theme.of(context).colorScheme.primary,
                      child: Text(
                        _userInitials(),
                        style: const TextStyle(
                            fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _userName(),
                            style: Theme.of(context)
                                .textTheme
                                .titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            roleNames[role] ?? '',
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: ListView(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  children: _navItems()
                      .map((item) => ListTile(
                            selected: page == (item['index'] as int),
                            selectedTileColor: Theme.of(context)
                                .colorScheme
                                .primaryContainer
                                .withOpacity(0.35),
                            leading: Icon(item['icon'] as IconData),
                            title: Text(item['title'] as String),
                            onTap: () {
                              onPage(item['index'] as int);
                              Navigator.pop(context);
                            },
                          ))
                      .toList(),
                ),
              ),
            ],
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: _content(),
      ),
    );
  }

  Widget _content() {
    switch (page) {
      case 1:
        return GradePage(role: role, lang: lang);
      case 2:
        return MandiPage(lang: lang);
      case 3:
        return role == 'official'
            ? ReportsPage(role: role, lang: lang)
            : HomePage(onPage: onPage, role: role);
      case 4:
        return AnalyticsPage(lang: lang);
      case 5:
        return SettingsPage(
            dark: dark, lang: lang, onTheme: onTheme, onLang: onLang);
      default:
        return HomePage(onPage: onPage, role: role);
    }
  }
}

class Api {
  static Future<List<dynamic>> mandis(String lang) async {
    final response =
        await http.get(Uri.parse('$apiBase/api/mandis?lang=$lang'));
    return jsonDecode(response.body)['items'];
  }

  static Future<List<dynamic>> records() async {
    final response = await http.get(Uri.parse('$apiBase/api/records'));
    return jsonDecode(response.body)['items'];
  }

  static Future<Map<String, dynamic>> analytics() async {
    final response = await http.get(Uri.parse('$apiBase/api/analytics'));
    return jsonDecode(response.body);
  }

  static Future<Map<String, String>> translations(String lang) async {
    final response =
        await http.get(Uri.parse('$apiBase/api/translations?lang=$lang'));
    return Map<String, String>.from(jsonDecode(response.body));
  }

  static Future<Map<String, dynamic>> analyze(
      Uint8List bytes, String fileName, Map<String, String> fields) async {
    final request =
        http.MultipartRequest('POST', Uri.parse('$apiBase/api/analyze'))
          ..fields.addAll(fields)
          ..files.add(
              http.MultipartFile.fromBytes('image', bytes, filename: fileName));
    final response = await request.send();
    final body = await response.stream.bytesToString();
    if (response.statusCode >= 400)
      throw Exception(jsonDecode(body)['detail'] ?? body);
    return jsonDecode(body);
  }

  static Future<void> save(Map<String, dynamic> result) async {
    await http.post(Uri.parse('$apiBase/api/records'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(result));
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key, required this.onPage, required this.role});
  final ValueChanged<int> onPage;
  final String role;
  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.sizeOf(context).width < 600;
    final chapterCards = [
      ActionCard(
          icon: Icons.biotech,
          accent: Colors.green,
          title: tr('nav_grade'),
          text: tr('nav_grade_desc'),
          onTap: () => onPage(1)),
      ActionCard(
          icon: Icons.storefront,
          accent: Colors.orange,
          title: tr('nav_mandi'),
          text: tr('nav_mandi_desc'),
          onTap: () => onPage(2)),
      if (role == 'official')
        ActionCard(
            icon: Icons.description_outlined,
            accent: Colors.indigo,
            title: tr('nav_reports'),
            text: tr('nav_reports_desc'),
            onTap: () => onPage(3)),
      ActionCard(
          icon: Icons.insights,
          accent: Colors.purple,
          title: tr('nav_analytics'),
          text: tr('nav_analytics_desc'),
          onTap: () => onPage(4)),
    ];

    return ListView(children: [
      Header(
          eyebrow: tr('app_tagline'),
          title: tr('home_hero_title'),
          subtitle: tr('home_hero_desc')),
      const SizedBox(height: 30),
      GridView.count(
        crossAxisCount: isMobile ? 2 : 4,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        childAspectRatio: isMobile ? 0.96 : 1.08,
        children: chapterCards,
      ),
      const SizedBox(height: 28),
      Card(
        child: Padding(
          padding: const EdgeInsets.all(22),
          child: Row(
            children: [
              const Icon(Icons.verified_user_outlined, size: 30),
              const SizedBox(width: 16),
              Expanded(
                child: Text(
                  tr('footer_text'),
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ),
              const Icon(Icons.arrow_forward),
            ],
          ),
        ),
      ),
    ]);
  }
}

class GradePage extends StatefulWidget {
  const GradePage({super.key, required this.role, required this.lang});
  final String role;
  final String lang;
  @override
  State<GradePage> createState() => _GradePageState();
}

class _GradePageState extends State<GradePage> {
  final name = TextEditingController(text: 'Ramesh Kumar');
  final farmerId = TextEditingController(text: 'FARM-1042');
  final lot = TextEditingController(text: 'LOT-2026-N89');
  final quantity = TextEditingController(text: '250');
  Uint8List? bytes;
  String fileName = '';
  Map<String, dynamic>? result;
  bool loading = false;
  String error = '';

  Future<void> pick() async {
    final picked = await FilePicker.platform
        .pickFiles(type: FileType.image, withData: true);
    if (picked != null && picked.files.single.bytes != null)
      setState(() {
        bytes = picked.files.single.bytes;
        fileName = picked.files.single.name;
      });
  }

  Future<void> run() async {
    if (bytes == null) {
      setState(() => error = 'Choose an onion photo first.');
      return;
    }
    setState(() {
      loading = true;
      error = '';
    });
    try {
      result = await Api.analyze(bytes!, fileName, {
        'farmer_name': name.text,
        'farmer_id': farmerId.text,
        'lot_id': lot.text,
        'center': 'Nashik',
        'quantity': quantity.text,
        'role': widget.role,
        'lang': widget.lang
      });
    } catch (exception) {
      error = exception.toString();
    }
    setState(() => loading = false);
  }

  @override
  Widget build(BuildContext context) => ListView(children: [
        Header(
            eyebrow: tr('section_photo'),
            title: tr('grade_header'),
            subtitle: tr('grade_subtitle')),
        const SizedBox(height: 26),
        SectionCard(
            title: tr('section_lot_info'),
            child: Wrap(spacing: 14, runSpacing: 14, children: [
              field(tr('farmer_name'), name),
              field(tr('farmer_id'), farmerId),
              field(tr('lot_id'), lot),
              field(tr('quantity_kg'), quantity)
            ])),
        const SizedBox(height: 16),
        SectionCard(
            title: tr('section_photo'),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              OutlinedButton.icon(
                  onPressed: pick,
                  icon: const Icon(Icons.upload_file),
                  label: Text(
                      bytes == null ? tr('upload_dropzone_title') : fileName)),
              if (bytes != null)
                Padding(
                    padding: const EdgeInsets.only(top: 16),
                    child:
                        Image.memory(bytes!, height: 180, fit: BoxFit.cover)),
              const SizedBox(height: 16),
              FilledButton.icon(
                  onPressed: loading ? null : run,
                  icon: const Icon(Icons.auto_awesome),
                  label: Text(
                      loading ? tr('analyzing_spinner') : tr('btn_grade'))),
              if (error.isNotEmpty)
                Padding(
                    padding: const EdgeInsets.only(top: 12),
                    child: Text(error,
                        style: TextStyle(
                            color: Theme.of(context).colorScheme.error))),
            ])),
        if (result != null)
          ResultCard(result: result!, role: widget.role, lang: widget.lang),
      ]);

  Widget field(String label, TextEditingController controller) => SizedBox(
      width: 230,
      child: TextField(
          controller: controller,
          decoration: InputDecoration(
              labelText: label, border: const OutlineInputBorder())));
}

class ResultCard extends StatefulWidget {
  const ResultCard(
      {super.key,
      required this.result,
      required this.role,
      required this.lang});
  final Map<String, dynamic> result;
  final String role;
  final String lang;
  @override
  State<ResultCard> createState() => _ResultCardState();
}

class _ResultCardState extends State<ResultCard> {
  bool saved = false;
  @override
  Widget build(BuildContext context) {
    final result = widget.result;
    final grade = result['grade'];
    final rejected = result['rejected'] == true;
    return Padding(
        padding: const EdgeInsets.only(top: 22),
        child: SectionCard(
            title: tr('results_title'),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(22),
                  color: rejected
                      ? Colors.red.shade700
                      : grade == 'A'
                          ? Colors.green.shade700
                          : grade == 'B'
                              ? Colors.orange.shade700
                              : Colors.red.shade700,
                  child: Text(
                      rejected
                          ? 'REJECTED'
                          : grade == null
                              ? 'NO GRADE'
                              : 'GRADE $grade',
                      style: const TextStyle(
                          color: Colors.white,
                          fontSize: 30,
                          fontWeight: FontWeight.bold))),
              if (rejected)
                Container(
                  width: double.infinity,
                  margin: const EdgeInsets.only(top: 18),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.red.shade300),
                  ),
                  child: Text(
                    result['message'] ??
                        'This onion cannot be consumed. It has been rejected and cannot be assigned a grade.',
                    style: TextStyle(
                      color: Colors.red.shade900,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                )
              else ...[
                const SizedBox(height: 18),
                Wrap(spacing: 12, runSpacing: 12, children: [
                  Metric(
                      label: tr('confidence'),
                      value:
                          '${number((result['confidence'] as num).toDouble() * 100, widget.lang, decimals: 1)}%'),
                  Metric(
                      label: tr('quality_score'),
                      value:
                          '${number((result['quality_score'] as num).toDouble(), widget.lang, decimals: 1)}/${number(100, widget.lang)}'),
                  Metric(
                      label: tr('urs_percentage'),
                      value:
                          '${number((result['urs_percentage'] as num).toDouble(), widget.lang, decimals: 1)}%'),
                  Metric(
                      label: tr('estimated_rate'),
                      value:
                          '₹${number((result['price_per_kg'] as num).toDouble(), widget.lang, decimals: 1)}/kg')
                ]),
                const Divider(height: 30),
                Text(
                    '${result['disease_name']} - ${result['disease_severity']}',
                    style: Theme.of(context).textTheme.titleLarge),
                const SizedBox(height: 6),
                Text(result['remedy']),
                if (widget.role != 'farmer')
                  Padding(
                      padding: const EdgeInsets.only(top: 18),
                      child: FilledButton.icon(
                          onPressed: saved
                              ? null
                              : () async {
                                  await Api.save(widget.result);
                                  setState(() => saved = true);
                                },
                          icon: const Icon(Icons.save_outlined),
                          label: Text(saved
                              ? tr('record_saved')
                              : tr('btn_save_record')))),
              ],
            ])));
  }
}

class MandiPage extends StatefulWidget {
  const MandiPage({super.key, required this.lang});
  final String lang;
  @override
  State<MandiPage> createState() => _MandiPageState();
}

class _MandiPageState extends State<MandiPage> {
  late Future<List<dynamic>> future;
  @override
  void initState() {
    super.initState();
    future = Api.mandis(widget.lang);
  }

  @override
  Widget build(BuildContext context) => ListView(children: [
        Header(
            eyebrow: tr('nearest_mandi'),
            title: tr('mandi_header'),
            subtitle: tr('mandi_subtitle')),
        const SizedBox(height: 24),
        FutureBuilder<List<dynamic>>(
            future: future,
            builder: (context, snapshot) {
              if (!snapshot.hasData)
                return const Center(child: CircularProgressIndicator());
              return Column(
                  children: snapshot.data!
                      .map((mandi) => Card(
                            child: ListTile(
                              leading: const CircleAvatar(
                                  child: Icon(Icons.storefront)),
                              title: Text(mandi['name']),
                              subtitle: Text(
                                  '${mandi['district']}, ${mandi['state']}  |  ${number((mandi['distance_km'] as num).toDouble(), widget.lang, decimals: 1)} ${tr('distance_away')}\n${tr('daily_arrivals_lbl')}: ${number((mandi['arrivals_qtl'] as num).toDouble(), widget.lang)} ${tr('qtl_unit')}  |  ${tr('price_trend')}: ${tr('trend_${mandi['trend']}')}'),
                              trailing: Text(
                                  '₹${number((mandi['modal_price_per_kg'] as num).toDouble(), widget.lang, decimals: 2)}/kg',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.bold)),
                            ),
                          ))
                      .toList());
            }),
      ]);
}

class ReportsPage extends StatefulWidget {
  const ReportsPage({super.key, required this.role, required this.lang});
  final String role;
  final String lang;
  @override
  State<ReportsPage> createState() => _ReportsPageState();
}

class _ReportsPageState extends State<ReportsPage> {
  late Future<List<dynamic>> future;
  @override
  void initState() {
    super.initState();
    future = Api.records();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.role != 'official')
      return Header(
          eyebrow: tr('badge_gov_exclusive'),
          title: tr('reports_header'),
          subtitle: tr('gov_restricted_msg'));
    return ListView(children: [
      Header(
          eyebrow: tr('reports_header'),
          title: tr('reports_header'),
          subtitle: tr('reports_subtitle')),
      const SizedBox(height: 24),
      FutureBuilder<List<dynamic>>(
          future: future,
          builder: (context, snapshot) {
            if (!snapshot.hasData)
              return const Center(child: CircularProgressIndicator());
            if (snapshot.data!.isEmpty) return Text(tr('no_records'));
            return Column(
                children: snapshot.data!
                    .map((record) => Card(
                          child: ListTile(
                            leading: CircleAvatar(
                                child: Text(record['grade']
                                    .toString()
                                    .split('_')
                                    .last)),
                            title: Text(
                                '${record['lot_id']}  |  ${record['farmer_name']}'),
                            subtitle: Text(
                                '${record['center']}  |  ${record['timestamp']}\n${tr('quality_score')}: ${number((record['quality_score'] as num).toDouble(), widget.lang, decimals: 1)}  |  ${record['disease_name']}'),
                            trailing: IconButton(
                              tooltip: 'Download PDF',
                              icon: const Icon(Icons.picture_as_pdf),
                              onPressed: () => launchUrl(Uri.parse(
                                  '$apiBase/api/records/${record['id']}/pdf')),
                            ),
                          ),
                        ))
                    .toList());
          })
    ]);
  }
}

class AnalyticsPage extends StatelessWidget {
  const AnalyticsPage({super.key, required this.lang});
  final String lang;
  @override
  Widget build(BuildContext context) => FutureBuilder<Map<String, dynamic>>(
      future: Api.analytics(),
      builder: (context, snapshot) {
        if (!snapshot.hasData)
          return const Center(child: CircularProgressIndicator());
        final data = snapshot.data!;
        final counts = Map<String, dynamic>.from(data['grade_counts']);
        return ListView(children: [
          Header(
              eyebrow: tr('nav_analytics'),
              title: tr('analytics_header'),
              subtitle: tr('analytics_subtitle')),
          const SizedBox(height: 24),
          Wrap(spacing: 14, runSpacing: 14, children: [
            Metric(
                label: tr('stat_total_lots'),
                value: number((data['total_lots'] as num).toDouble(), lang)),
            Metric(
                label: tr('stat_total_volume'),
                value:
                    '${number((data['total_quantity'] as num).toDouble(), lang)} kg'),
            Metric(
                label: tr('stat_avg_score'),
                value:
                    '${number((data['average_score'] as num).toDouble(), lang, decimals: 1)} / ${number(100, lang)}')
          ]),
          const SizedBox(height: 24),
          SectionCard(
              title: tr('chart_grade_dist'),
              child: Column(
                  children: ['A', 'B', 'C']
                      .map((grade) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 7),
                            child: Row(children: [
                              SizedBox(
                                  width: 28,
                                  child: Text(grade,
                                      style: const TextStyle(
                                          fontWeight: FontWeight.bold))),
                              Expanded(
                                  child: LinearProgressIndicator(
                                      value: (counts[grade] ?? 0) /
                                          (data['total_lots'] == 0
                                              ? 1
                                              : data['total_lots']),
                                      minHeight: 12)),
                              const SizedBox(width: 12),
                              Text(number(
                                  (counts[grade] as num? ?? 0).toDouble(),
                                  lang)),
                            ]),
                          ))
                      .toList())),
        ]);
      });
}

class SettingsPage extends StatelessWidget {
  const SettingsPage(
      {super.key,
      required this.dark,
      required this.lang,
      required this.onTheme,
      required this.onLang});
  final bool dark;
  final String lang;
  final VoidCallback onTheme;
  final ValueChanged<String> onLang;
  @override
  Widget build(BuildContext context) => ListView(children: [
        Header(
            eyebrow: tr('lang_section'),
            title: tr('settings_header'),
            subtitle: tr('settings_subtitle')),
        const SizedBox(height: 24),
        SectionCard(
            title: tr('theme_section'),
            child: SwitchListTile(
                contentPadding: EdgeInsets.zero,
                title: Text(tr('theme_dark')),
                value: dark,
                onChanged: (_) => onTheme())),
        const SizedBox(height: 16),
        SectionCard(
            title: tr('lang_section'),
            child: DropdownButtonFormField<String>(
                value: lang,
                items: const [
                  DropdownMenuItem(value: 'en', child: Text('English')),
                  DropdownMenuItem(value: 'hi', child: Text('हिन्दी')),
                  DropdownMenuItem(value: 'kn', child: Text('ಕನ್ನಡ')),
                  DropdownMenuItem(value: 'ta', child: Text('தமிழ்')),
                  DropdownMenuItem(value: 'mr', child: Text('मराठी')),
                  DropdownMenuItem(value: 'bn', child: Text('বাংলা')),
                ],
                onChanged: (value) {
                  if (value != null) onLang(value);
                },
                decoration:
                    const InputDecoration(border: OutlineInputBorder())))
      ]);
}

class Header extends StatelessWidget {
  const Header(
      {super.key,
      required this.eyebrow,
      required this.title,
      required this.subtitle});
  final String eyebrow;
  final String title;
  final String subtitle;
  @override
  Widget build(BuildContext context) =>
      Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(eyebrow,
            style: TextStyle(
                color: Theme.of(context).colorScheme.primary,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.5)),
        const SizedBox(height: 8),
        Text(title,
            style: Theme.of(context)
                .textTheme
                .displaySmall
                ?.copyWith(fontWeight: FontWeight.w900)),
        const SizedBox(height: 8),
        Text(subtitle, style: Theme.of(context).textTheme.titleMedium)
      ]);
}

class SectionCard extends StatelessWidget {
  const SectionCard({super.key, required this.title, required this.child});
  final String title;
  final Widget child;
  @override
  Widget build(BuildContext context) => Card(
      child: Padding(
          padding: const EdgeInsets.all(22),
          child:
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(title,
                style: Theme.of(context)
                    .textTheme
                    .titleLarge
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 18),
            child
          ])));
}

class ActionCard extends StatelessWidget {
  const ActionCard(
      {super.key,
      required this.icon,
      required this.accent,
      required this.title,
      required this.text,
      required this.onTap});
  final IconData icon;
  final Color accent;
  final String title;
  final String text;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => Card(
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 54,
                  height: 54,
                  decoration: BoxDecoration(
                    color: accent.withOpacity(0.14),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(icon, size: 30, color: accent),
                ),
                const SizedBox(height: 18),
                Text(
                  title,
                  style: Theme.of(context)
                      .textTheme
                      .titleLarge
                      ?.copyWith(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Expanded(
                  child: Text(
                    text,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ),
                const SizedBox(height: 8),
                const Align(
                  alignment: Alignment.centerRight,
                  child: Icon(Icons.arrow_forward),
                ),
              ],
            ),
          ),
        ),
      );
}

class Metric extends StatelessWidget {
  const Metric({super.key, required this.label, required this.value});
  final String label;
  final String value;
  @override
  Widget build(BuildContext context) => Container(
      width: 172,
      height: 110,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(10)),
      child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(value,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context)
                    .textTheme
                    .titleLarge
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Text(label, maxLines: 2, overflow: TextOverflow.ellipsis)
          ]));
}
