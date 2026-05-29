import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:intl/intl.dart';

void main() {
  runApp(const GestorTarefasApp());
}

class GestorTarefasApp extends StatelessWidget {
  const GestorTarefasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gestor de Tarefas Plus',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF10b981)),
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const TarefasPage(),
    );
  }
}

// ── Modelo ────────────────────────────────────────────────────────────────────

class Tarefa {
  String nome;
  String info;
  String data; // DD/MM/AAAA

  Tarefa({required this.nome, required this.info, required this.data});

  DateTime? get dataObj {
    try {
      return DateFormat('dd/MM/yyyy').parse(data);
    } catch (_) {
      return null;
    }
  }

  int get diasRestantes {
    final d = dataObj;
    if (d == null) return 0;
    return d.difference(DateTime.now().copyWith(hour: 0, minute: 0, second: 0, millisecond: 0, microsecond: 0)).inDays;
  }

  StatusTarefa get status {
    final dias = diasRestantes;
    if (dataObj == null) return StatusTarefa.invalida;
    if (dias < 0) return StatusTarefa.atrasada;
    if (dias == 0) return StatusTarefa.hoje;
    return StatusTarefa.emDia;
  }

  String toLinha() => '$nome | $info | $data';

  static Tarefa? fromLinha(String linha) {
    final partes = linha.split(' | ');
    if (partes.length != 3) return null;
    return Tarefa(nome: partes[0], info: partes[1], data: partes[2]);
  }
}

enum StatusTarefa { atrasada, hoje, emDia, invalida }

extension StatusExt on StatusTarefa {
  Color get cor {
    switch (this) {
      case StatusTarefa.atrasada: return const Color(0xFFdc2626);
      case StatusTarefa.hoje:     return const Color(0xFFd97706);
      case StatusTarefa.emDia:    return const Color(0xFF16a34a);
      case StatusTarefa.invalida: return Colors.grey;
    }
  }

  String get label {
    switch (this) {
      case StatusTarefa.atrasada: return 'Atrasada';
      case StatusTarefa.hoje:     return 'Vence Hoje';
      case StatusTarefa.emDia:    return 'Em dia';
      case StatusTarefa.invalida: return 'Data inválida';
    }
  }

  IconData get icone {
    switch (this) {
      case StatusTarefa.atrasada: return Icons.warning_amber_rounded;
      case StatusTarefa.hoje:     return Icons.notifications_active;
      case StatusTarefa.emDia:    return Icons.check_circle_outline;
      case StatusTarefa.invalida: return Icons.error_outline;
    }
  }
}

// ── Página principal ──────────────────────────────────────────────────────────

class TarefasPage extends StatefulWidget {
  const TarefasPage({super.key});

  @override
  State<TarefasPage> createState() => _TarefasPageState();
}

class _TarefasPageState extends State<TarefasPage> {
  List<Tarefa> _tarefas = [];
  int? _selecionada;
  int? _editando;

  final _nomeCtrl = TextEditingController();
  final _infoCtrl = TextEditingController();
  final _dataCtrl = TextEditingController();
  String _erro = '';

  @override
  void initState() {
    super.initState();
    _carregar();
  }

  // ── Persistência ────────────────────────────────────────────────────────────

  Future<void> _carregar() async {
    final prefs = await SharedPreferences.getInstance();
    final linhas = prefs.getStringList('tarefas') ?? [];
    setState(() {
      _tarefas = linhas
          .map(Tarefa.fromLinha)
          .whereType<Tarefa>()
          .toList();
      _ordenar();
    });
  }

  Future<void> _salvar() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('tarefas', _tarefas.map((t) => t.toLinha()).toList());
  }

  void _ordenar() {
    _tarefas.sort((a, b) {
      final da = a.dataObj ?? DateTime(9999);
      final db = b.dataObj ?? DateTime(9999);
      return da.compareTo(db);
    });
  }

  // ── Ações ───────────────────────────────────────────────────────────────────

  void _salvarTarefa() {
    final nome = _nomeCtrl.text.trim();
    final info = _infoCtrl.text.trim();
    final data = _dataCtrl.text.trim();

    if (nome.isEmpty || info.isEmpty || data.isEmpty) {
      setState(() => _erro = 'Preencha todos os campos!');
      return;
    }

    try {
      DateFormat('dd/MM/yyyy').parseStrict(data);
    } catch (_) {
      setState(() => _erro = 'Data inválida! Use DD/MM/AAAA.');
      return;
    }

    setState(() {
      _erro = '';
      final nova = Tarefa(nome: nome, info: info, data: data);
      if (_editando != null) {
        _tarefas[_editando!] = nova;
        _editando = null;
      } else {
        _tarefas.add(nova);
      }
      _ordenar();
      _selecionada = null;
      _nomeCtrl.clear();
      _infoCtrl.clear();
      _dataCtrl.clear();
    });
    _salvar();
  }

  void _prepararEdicao(int idx) {
    final t = _tarefas[idx];
    setState(() {
      _editando = idx;
      _selecionada = idx;
      _nomeCtrl.text = t.nome;
      _infoCtrl.text = t.info;
      _dataCtrl.text = t.data;
      _erro = '';
    });
  }

  void _remover(int idx) {
    setState(() {
      _tarefas.removeAt(idx);
      _selecionada = null;
      _editando = null;
      _nomeCtrl.clear();
      _infoCtrl.clear();
      _dataCtrl.clear();
      _erro = '';
    });
    _salvar();
  }

  void _cancelar() {
    setState(() {
      _editando = null;
      _selecionada = null;
      _nomeCtrl.clear();
      _infoCtrl.clear();
      _dataCtrl.clear();
      _erro = '';
    });
  }

  // ── Seletor de data ─────────────────────────────────────────────────────────

  Future<void> _selecionarData() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
      locale: const Locale('pt', 'BR'),
    );
    if (picked != null) {
      _dataCtrl.text = DateFormat('dd/MM/yyyy').format(picked);
    }
  }

  // ── Build ───────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    final atrasadas = _tarefas.where((t) => t.status == StatusTarefa.atrasada).length;
    final hoje      = _tarefas.where((t) => t.status == StatusTarefa.hoje).length;
    final emDia     = _tarefas.where((t) => t.status == StatusTarefa.emDia).length;

    return Scaffold(
      backgroundColor: const Color(0xFFf3f4f6),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        title: const Row(
          children: [
            Icon(Icons.checklist_rounded, color: Color(0xFF10b981)),
            SizedBox(width: 10),
            Text('Gestor de Tarefas Plus',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: Color(0xFF111827))),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            // ── Cards de resumo ──
            Row(children: [
              _cardResumo('Atrasadas', atrasadas, const Color(0xFFef4444), Icons.warning_amber_rounded),
              const SizedBox(width: 8),
              _cardResumo('Hoje', hoje, const Color(0xFFf59e0b), Icons.notifications_active),
              const SizedBox(width: 8),
              _cardResumo('Em dia', emDia, const Color(0xFF10b981), Icons.check_circle_outline),
            ]),
            const SizedBox(height: 16),

            // ── Formulário ──
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 8)],
              ),
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _editando != null ? '✏️ Editando Tarefa' : '➕ Nova Tarefa',
                    style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14, color: Color(0xFF111827)),
                  ),
                  const SizedBox(height: 12),
                  _campo('Nome da Tarefa', _nomeCtrl, Icons.task_alt),
                  const SizedBox(height: 10),
                  _campo('Informação / Categoria', _infoCtrl, Icons.folder_outlined),
                  const SizedBox(height: 10),
                  _campoData(),
                  if (_erro.isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Text(_erro, style: const TextStyle(color: Color(0xFFef4444), fontSize: 12)),
                  ],
                  const SizedBox(height: 14),
                  Row(children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: _salvarTarefa,
                        icon: Icon(_editando != null ? Icons.save : Icons.add),
                        label: Text(_editando != null ? 'Salvar Edição' : 'Adicionar'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: _editando != null ? const Color(0xFF6366f1) : const Color(0xFF10b981),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                      ),
                    ),
                    if (_editando != null) ...[
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: _cancelar,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF6b7280),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                        child: const Text('✕'),
                      ),
                    ],
                  ]),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // ── Lista de tarefas ──
            Text('Tarefas (${_tarefas.length})',
                style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14, color: Color(0xFF111827))),
            const SizedBox(height: 8),

            if (_tarefas.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                child: const Center(
                  child: Text('Nenhuma tarefa cadastrada.', style: TextStyle(color: Colors.grey)),
                ),
              ),

            ..._tarefas.asMap().entries.map((entry) {
              final i = entry.key;
              final t = entry.value;
              final sel = _selecionada == i;
              return _cardTarefa(t, i, sel);
            }),

            // ── Painel de detalhes ──
            if (_selecionada != null && _selecionada! < _tarefas.length) ...[
              const SizedBox(height: 16),
              _painelDetalhes(_tarefas[_selecionada!]),
            ],

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  // ── Widgets auxiliares ────────────────────────────────────────────────────

  Widget _cardResumo(String label, int val, Color cor, IconData icone) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: cor.withOpacity(0.3)),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 6)],
        ),
        child: Column(children: [
          Icon(icone, color: cor, size: 20),
          const SizedBox(height: 4),
          Text('$val', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: cor)),
          Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey), textAlign: TextAlign.center),
        ]),
      ),
    );
  }

  Widget _campo(String hint, TextEditingController ctrl, IconData icone) {
    return TextField(
      controller: ctrl,
      decoration: InputDecoration(
        hintText: hint,
        prefixIcon: Icon(icone, size: 18, color: Colors.grey),
        filled: true,
        fillColor: const Color(0xFFf9fafb),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFFe5e7eb))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFFe5e7eb))),
        contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
      ),
    );
  }

  Widget _campoData() {
    return TextField(
      controller: _dataCtrl,
      keyboardType: TextInputType.number,
      maxLength: 10,
      decoration: InputDecoration(
        hintText: 'DD/MM/AAAA',
        prefixIcon: const Icon(Icons.calendar_today, size: 18, color: Colors.grey),
        counterText: '',
        filled: true,
        fillColor: const Color(0xFFf9fafb),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFFe5e7eb))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFFe5e7eb))),
        contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
      ),
      onChanged: (val) {
        // Formata automaticamente DD/MM/AAAA enquanto digita
        String digits = val.replaceAll('/', '');
        String formatted = '';
        for (int i = 0; i < digits.length && i < 8; i++) {
          if (i == 2 || i == 4) formatted += '/';
          formatted += digits[i];
        }
        if (formatted != val) {
          _dataCtrl.value = TextEditingValue(
            text: formatted,
            selection: TextSelection.collapsed(offset: formatted.length),
          );
        }
      },
    );
  }

  Widget _cardTarefa(Tarefa t, int i, bool sel) {
    final s = t.status;
    final dias = t.diasRestantes;
    String diasTxt = '';
    if (s == StatusTarefa.atrasada) diasTxt = ' (${dias.abs()} dias)';
    if (s == StatusTarefa.emDia)    diasTxt = ' ($dias dias)';

    return GestureDetector(
      onTap: () => setState(() => _selecionada = sel ? null : i),
      child: Container(
        margin: const EdgeInsets.only(bottom: 6),
        decoration: BoxDecoration(
          color: sel ? const Color(0xFFf0f4ff) : Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: sel ? const Color(0xFF6366f1) : const Color(0xFFe5e7eb), width: sel ? 2 : 1),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 4)],
        ),
        child: Row(
          children: [
            // Barra lateral colorida
            Container(width: 5, height: 60, decoration: BoxDecoration(color: s.cor, borderRadius: const BorderRadius.only(topLeft: Radius.circular(10), bottomLeft: Radius.circular(10)))),
            const SizedBox(width: 10),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(t.nome, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: Color(0xFF111827))),
                    const SizedBox(height: 2),
                    Text('${t.info} · ${t.data}', style: const TextStyle(fontSize: 11, color: Colors.grey)),
                  ],
                ),
              ),
            ),
            // Status badge
            Container(
              margin: const EdgeInsets.only(right: 8),
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(color: s.cor.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                Icon(s.icone, size: 12, color: s.cor),
                const SizedBox(width: 3),
                Text('${s.label}$diasTxt', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: s.cor)),
              ]),
            ),
            // Botões editar/remover
            IconButton(icon: const Icon(Icons.edit, size: 18, color: Color(0xFFf59e0b)), onPressed: () => _prepararEdicao(i)),
            IconButton(icon: const Icon(Icons.delete, size: 18, color: Color(0xFFef4444)), onPressed: () => _remover(i)),
          ],
        ),
      ),
    );
  }

  Widget _painelDetalhes(Tarefa t) {
    final s = t.status;
    final dias = t.diasRestantes;
    String diasTxt = '';
    if (s == StatusTarefa.atrasada) diasTxt = ' (${dias.abs()} dias de atraso)';
    if (s == StatusTarefa.emDia)    diasTxt = ' (faltam $dias dias)';

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFe5e7eb)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Informações Completas', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 13, color: Color(0xFF111827))),
          const Divider(height: 16),
          _detalheRow('📌', 'Tarefa', t.nome),
          _detalheRow('📂', 'Informação', t.info),
          _detalheRow('📅', 'Data', t.data),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(color: s.cor.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Icon(s.icone, size: 14, color: s.cor),
              const SizedBox(width: 6),
              Text('${s.label}$diasTxt', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12, color: s.cor)),
            ]),
          ),
        ],
      ),
    );
  }

  Widget _detalheRow(String icone, String label, String valor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(children: [
        Text('$icone ', style: const TextStyle(fontSize: 13)),
        Text('$label: ', style: const TextStyle(fontSize: 12, color: Colors.grey)),
        Expanded(child: Text(valor, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF111827)))),
      ]),
    );
  }
}

