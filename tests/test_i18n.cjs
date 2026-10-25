// Run with: node --test tests/test_i18n.cjs (no dependencies or archive needed).
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function load(saved, unavailable = false) {
  const context = vm.createContext({
    document: {documentElement: {}},
    localStorage: {getItem() { if (unavailable) throw Error('blocked'); return saved; }},
  });
  for (const file of ['i18n.js', 'i18n-help.js', 'i18n-ui.js']) {
    vm.runInContext(fs.readFileSync(path.join(__dirname, '..', file), 'utf8'), context, {filename: file});
  }
  return {context, t: source => vm.runInContext(`VaultI18n.translate(${JSON.stringify(source)})`, context)};
}

test('Chinese defaults and unavailable/invalid language storage', () => {
  for (const saved of [undefined, 'fr', 'zh-CN']) {
    const {context, t} = load(saved);
    assert.equal(context.document.documentElement.lang, 'zh-CN');
    assert.equal(t('Stack'), '堆叠配置');
  }
  assert.equal(load(undefined, true).t('Stack'), '堆叠配置');
});

test('English preserves every source message verbatim', () => {
  const {t} = load('en');
  for (const source of ['Stack', '  Depth ', 'Layer 2 · top — S · 2U · Drawers', '57% · My printer: reading Key (1/2)']) {
    assert.equal(t(source), source);
  }
});

test('dynamic help, layer and export progress preserve parameters', () => {
  const {t} = load();
  assert.equal(t('Layer 2 · top — L width · two S bays · 2U · Drawers'), '第 2 层 · 顶层 — L 宽度 · 两个 S 仓位 · 2U · 抽屉');
  assert.equal(t('The two kinds of module in the system: (pictures: S5, 2U)'), '系统包含两类模块：（图片：S5, 2U）');
  assert.equal(t('57% · My printer: reading Key (Turn On Supports) (1/2)'), '57% · My printer：正在读取 Key (Turn On Supports)（1/2）');
  assert.equal(t('done in 1.2s · files in output/my-vault'), '已完成，用时 1.2 秒 · 文件位于 output/my-vault');
  assert.equal(t(' 3 layers imported. '), ' 已导入 3 层。 ');
  assert.equal(t('The two kinds of module in the system: (pictures: L width · two S bays (L3² body, S+S boxes), 2U)'), '系统包含两类模块：（图片：L 宽度 · 两个 S 仓位（L3² 外壳，S+S 盒体）, 2U）');
});

test('backend warnings retain original part names, dimensions and printer limits', () => {
  const {t} = load();
  const source = 'L1 · S5 2U drawers: 1× Label (100.0×100.0×330.0 mm) cannot be printed. My printer: 330 mm tall, limit 320 mm (Z). It fits a Bambu Lab H2S (340×320×340 mm).';
  const translated = t(source);
  assert.match(translated, /第 1 层/);
  assert.match(translated, /1× Label（100\.0×100\.0×330\.0 mm）无法打印/);
  assert.match(translated, /My printer：高度 330 mm，上限 320 mm（Z）/);
  assert.match(translated, /Bambu Lab H2S \(340×320×340 mm\)/);
  assert.equal(t('File not found: Key (Turn On Supports) (drawers universal)'), '未找到文件：Key (Turn On Supports)（drawers universal）');
});

test('plate summaries translate complete and incomplete allocations', () => {
  const {t} = load();
  assert.equal(t('10 of 10 printed pieces are on plates — nothing left out'), '10 个打印件中有 10 个已排入打印盘 — 无遗漏');
  assert.equal(t('8 of 10 printed pieces are on plates; 1 NOT exported (listed below) · ⚠ 1 pieces unaccounted for, report this'), '10 个打印件中有 8 个已排入打印盘；1 个未导出（见下方） · ⚠ 1 个零件未计入，请反馈此问题');
  assert.equal(t('≈110 g · ≈2h 03m · max height 100 mm'), '≈110 g · ≈2 小时 03 分钟 · 最大高度 100 mm');
});

test('joined catalog notes and export warnings translate while retaining names', () => {
  const {t} = load();
  assert.equal(t('Sustainer lid. Split version used: one-piece file does not fit the enabled printers.'), '翻盖箱盖。使用分体版本：整体文件超出已启用打印机的打印范围。');
  assert.equal(t('no slicer preset chosen for this printer; opened file keeps the slicer\'s current presets · 1 piece(s) not entirely on their plate: Label (plate 2, 3 mm)'), '未为此打印机选择切片预设；打开文件后将沿用切片软件当前的预设 · 1 个零件超出打印盘：Label（打印盘 2，超出 3 mm）');
});

test('unknown external errors, filenames and arbitrary names remain unchanged', () => {
  const {t} = load();
  for (const source of ['Spoolman: HTTP Error 503: Service Unavailable', 'TypeError: external SDK failure', '01. DRAWERS/S5/Label.stl', 'My PETG · special edition', '<b>external error</b>']) {
    assert.equal(t(source), source);
  }
});
