/* English source strings are translation keys. Technical identifiers stay in the
 * original data; raw text nodes explicitly protect external and user names. */
VaultI18n.add({
  'VAULT configurator': 'VAULT 配置器',
  'stack composer · bill of materials · 3MF plate export': '堆叠配置 · 物料清单 · 3MF 打印盘导出',
  'Stack': '堆叠配置', 'Parts & hardware': '零件与五金', 'Plates & export': '打印盘与导出',
  'Name': '名称', 'Depth': '深度', '+ Add layer on top': '+ 在顶部添加一层', 'Start over': '重新开始',
  'Layers are listed top-down, like the drawing: the last card is the base layer.': '层按示意图从上到下排列：最后一张卡片为底层。',
  'Explain an option when you click it, in the Help box under the drawing': '点击选项时，在示意图下方的帮助框中显示说明',
  'Roof': '顶板', 'Type': '类型', 'none': '无', 'Gridfinity grid roof': 'Gridfinity 网格顶板',
  'Table roof': '平面顶板', 'Bowl roof': '托盘顶板', 'Under-table mount roof': '桌下安装顶板',
  'Heavyweight roof (L/XL)': '重载顶板（L/XL）', 'Top handle (grid roof)': '顶部提手（网格顶板）',
  'Modifications': '附加组件', "(designer's advice: 2U right above the base and right below the roof)": '（设计师建议：底座上方和顶板下方均使用 2U 模块）',
  'Base': '底座', 'Wheels': '车轮', 'Feet': '支脚', 'Casters (hardware only)': '脚轮（仅五金件）',
  'Backbone': '背板', 'wide (family width)': '宽背板（与系列同宽）', 'universal (2 per layer)': '通用背板（每层 2 块）',
  'Pull-out handle': '伸缩拉杆', 'Stationary handle': '固定把手', 'Module connectors': '模块连接件', 'Pegboard': '洞洞板', 'Wall mounts': '壁挂件',
  'Import a stack from ussadesign.com (Compose a stack)': '从 ussadesign.com 导入堆叠配置（Compose a stack）',
  'on the VAULT page press': '在 VAULT 页面点击', 'Export': '导出',
  '(the site prints its "Your build" summary as a PDF) and load that file here. The PDF lists modules and facades but not their order or the depth, so check the layer order afterwards.': '（网站会将“Your build”配置摘要保存为 PDF），然后在此加载该文件。PDF 仅包含模块和面板，不包含顺序和深度，导入后请检查层顺序。',
  'or open DevTools → Console on the VAULT page, run': '也可在 VAULT 页面打开开发者工具 → 控制台，运行',
  'and paste the result (keeps the layer order).': '并粘贴结果（保留层顺序）。', 'Import layers': '导入层', 'What you are building': '配置预览',
  "Front view built from the designer's own render sheets, as on ussadesign.com (original finish); roof, base, wheels and handle are drawn to the same scale around it. Parts mounted on the back (backbone, pegboards, wall mounts, connectors, stationary handle) appear in a separate BACK view.": '正视图使用设计师在 ussadesign.com 上的原始渲染图（原始配色），顶板、底座、车轮和把手按相同比例绘制。安装在背面的背板、洞洞板、壁挂件、连接件和固定把手在单独的背视图中显示。',
  'Help': '帮助', 'Click a dotted option on the left (or open its list): what each choice gives you, the real parts in your size and the manual page appear here.': '点击左侧带点状下划线的选项（或展开列表），此处将显示选项说明、对应尺寸的实际零件和手册页面。',
  'Totals': '汇总', 'Printed parts': '打印零件',
  "Colour = which filament slot prints the part. Tagged by default from the designer's renders; set the whole stack or one module at once here, or a single part in its row.": '颜色决定使用哪个耗材槽位打印零件。默认按设计师渲染图分配；可统一设置整个堆叠、单个模块，也可逐行设置零件。',
  'Drawer parts': '抽屉零件', 'Sustainer parts': '翻盖箱零件', 'Colour for ALL parts': '全部零件的颜色',
  'Join identical parts across layers (one row per part, quantities added up)': '合并各层的相同零件（每种零件一行，数量累加）',
  'Quantities follow the stack (divider and pegboard counts are set on the Stack tab). Click any picture to open the part in 3D.': '数量由堆叠配置决定（隔板和洞洞板数量在“堆叠配置”页设置）。点击图片可查看零件的 3D 模型。',
  'Part': '零件', 'Group': '分组', 'Qty': '数量', 'Colour': '颜色', 'time': '时间', 'size mm': '尺寸（mm）', 'fits': '适用打印机',
  'Hardware': '五金件', 'Item': '项目', 'Where': '用途', 'Step 1 · Printers': '第 1 步 · 打印机',
  'Use': '启用', 'Printer': '打印机', 'Bed X': '平台 X', 'Bed Y': '平台 Y', 'No tall parts': '限制高零件',
  'Max part height': '零件高度上限', 'Add printer': '添加打印机', 'Slicer, nozzle and presets per printer': '各打印机的切片软件、喷嘴与预设',
  'Slicer': '切片软件', 'Profile': '配置', 'Nozzle': '喷嘴', 'Machine preset': '打印机预设', 'Default process preset': '默认工艺预设',
  'Presets are read from the slicers\' own folders (your presets first). "0.20mm" in a process preset name is the layer height, not the nozzle; the nozzle is the column before it. The exported file is a full project: it opens with this machine, this process preset and the filaments from step 2 already set, with your colours. H2C bed is 325 × 320 × 320: what one nozzle alone reaches.': '从切片软件的配置目录读取预设（优先显示用户预设）。工艺预设名中的“0.20mm”是层高，喷嘴直径在前一列。导出文件为完整项目，已设置打印机、工艺及第 2 步中的耗材和颜色。H2C 的可用空间为 325 × 320 × 320 mm，即单个喷嘴的覆盖范围。',
  'Step 2 · Filaments & colours': '第 2 步 · 耗材与颜色',
  'Connect to Spoolman first (optional): fills the slots below from your real spools': '连接 Spoolman（可选）：使用实际料卷填充下方槽位',
  'Server': '服务器', 'Load spools': '加载料卷',
  "Per slot: pick the filament (brand · material), then one of the colours you have of it. The slot's colour, material and name follow.": '每个槽位先选择耗材（品牌 · 材料），再选择已有颜色，槽位的颜色、材料和名称会随之更新。',
  'Slot': '槽位', 'Filament': '耗材', 'Colour you own': '已有颜色',
  "Colour slots: pick the colour, then the material (written into the 3MF; the slicer's filament preset is chosen from it). A name is optional. Slots no part of this stack uses are hidden.": '颜色槽位：先选择颜色，再选择材料（写入 3MF，并用于选择切片软件的耗材预设）。名称可选。当前堆叠未使用的槽位会隐藏。',
  'Material': '材料', 'Name (optional)': '名称（可选）', 'Prints': '打印内容', 'Filament preset per printer (slicer)': '各打印机的耗材预设（切片软件）',
  'What prints in which colour': '零件颜色分配',
  "Every part is tagged with a colour role from the designer's renders. Pick the filament for each role; the pictures show real parts of your stack in that colour.": '每个零件按设计师渲染图分配颜色角色。为各角色选择耗材；图片会显示当前堆叠中使用该颜色的实际零件。',
  'Colour role': '颜色角色', 'Parts of your stack': '当前堆叠的零件',
  'Give a whole part group another colour (e.g. all facades in the accent colour)': '为整组零件指定其他颜色（例如将所有面板设为点缀色）',
  'Each row is one group of parts in your stack, pictured in the colour they get right now. Choose a colour role in the last column to move the whole group to another filament; "keep" leaves the designer\'s tagging.': '每行对应当前堆叠中的一组零件，图片显示当前颜色。在最后一列选择颜色角色，即可为整组更换耗材；选择“保留”则沿用设计师的分配。',
  'Part group': '零件分组', 'Parts, in their current colour': '零件及当前颜色', 'Change the whole group to': '整组更改为',
  'Step 3 · Plates & export': '第 3 步 · 打印盘与导出',
  'One 3MF project per printer, several plates inside, every plate a single filament. Parts of one colour are packed together (MaxRects, 90° rotation allowed); the biggest parts go to the biggest printer.': '每台打印机导出一个包含多个打印盘的 3MF 项目，每盘仅使用一种耗材。同色零件集中排版（MaxRects 算法，允许旋转 90°），最大零件分配给最大的打印机。',
  'Preview plates': '预览打印盘', 'Export 3MF (one project per printer)': '导出 3MF（每台打印机一个项目）',
  'Packing and estimate options': '排版与估算选项', 'Send parts to': '零件分配至',
  'all printers (balance print time)': '所有打印机（平衡打印时间）', 'Group plates by': '打印盘分组方式',
  'colour · fewest plates (recommended)': '按颜色 · 最少打印盘（推荐）', 'module and colour': '按模块与颜色',
  'Part spacing': '零件间距', 'Bed edge': '平台边缘留空', "Weight estimate uses the process preset's walls and infill": '使用工艺预设中的壁数和填充率估算重量',
  'Shell': '壳体厚度', 'Infill': '填充率', 'Seconds per gram': '每克打印秒数',
  "time guess for parts the designer's sheet does not cover; depends on your speeds, not in the preset": '用于估算设计师数据表未涵盖的零件耗时；取决于打印速度，不从预设读取',
  'Step 4 · Tune a process preset per part group (optional)': '第 4 步 · 按零件分组调整工艺预设（可选）',
  'Tick': '勾选', 'test': '测试', 'on the groups you want to tune, press': '需要调试的分组，然后点击',
  'Export test plates': '导出测试盘',
  ": each printer gets a TEST file with one plate per group holding one of each part (an assembly's parts together). Tune and save a preset in the slicer, press": '：每台打印机生成一个 TEST 文件，每组占一盘，各零件各放一个（同一装配的零件放在一起）。在切片软件中调整并保存预设，点击',
  'Rescan presets': '重新扫描预设', ', pick it here; the real export then applies it. Per-part rows override the group.': '，在此选择后，正式导出时便会应用。单个零件的设置优先于分组设置。',
  'Test': '测试', 'Group / part': '分组 / 零件', 'drag to orbit · wheel to zoom · right-drag to pan': '拖动旋转 · 滚轮缩放 · 右键拖动平移', 'Close': '关闭',
  'No layers yet. The first layer is the base and sets the family (S, M, L or XL) for the whole stack.': '尚未添加层。第一层为底层，决定整个堆叠的尺寸系列（S、M、L 或 XL）。',
  'Add a layer to see what you are building.': '添加一层以查看配置预览。',
  'L width · two S bays': 'L 宽度 · 两个 S 仓位', 'XL width · S + M bays': 'XL 宽度 · S + M 仓位',
  'move up': '上移', 'move down': '下移', 'Width': '宽度', 'Height': '高度', 'Facades': '面板组合',
  'Interior': '内部结构', 'Lock': '锁定方式', 'labels': '标签', 'geared rails': '齿条', 'manual support wall': '手动支撑壁',
  'baseplate · 1 handle': '底板 · 1 个提手', 'baseplate · 2 handles': '底板 · 2 个提手',
  'Width dividers': '宽向隔板数量', 'Depth dividers': '深向隔板数量', 'full drawer height': '与抽屉等高',
  'BACK (what is bolted on the rear)': '背视图（背面安装的组件）', 'wheels Ø160, TPU tyres, M16 axle': 'Ø160 车轮、TPU 轮胎、M16 车轴',
  'hidden key (flush, drawn as a disc)': '隐藏锁（齐平，图中以圆盘表示）', 'no lock (drawn as a plain disc)': '无锁（图中以光滑圆盘表示）',
  'grid roof + top handle': '网格顶板 + 顶部提手', '4 casters, M8 (hardware)': '4 个 M8 脚轮（五金件）',
  'pull-out handle, M16 rods (on the backbone)': '伸缩拉杆、M16 杆（安装在背板上）',
  '(inherit)': '（继承）', '(no presets found)': '（未找到预设）', 'your presets': '用户预设', 'system presets': '系统预设',
  'remove this printer': '移除此打印机', 'choose a printer…': '选择打印机…', 'Custom printer (type its bed size in the new row)': '自定义打印机（在新行中输入平台尺寸）',
  'click to open in 3D': '点击查看 3D 模型', 'e.g. Elegoo rapid PETG': '例如 Elegoo rapid PETG',
  'pick a filament first': '请先选择耗材', '(filament: brand · material)': '（耗材：品牌 · 材料）',
  "Enter the server URL and press Load spools; each slot can then take a spool's name, colour and material.": '输入服务器地址并点击“加载料卷”，随后可将料卷名称、颜色和材料应用到各槽位。',
  'build a stack first': '请先配置堆叠', 'Build a stack first.': '请先配置堆叠。',
  'keep (as tagged by the designer)': '保留（沿用设计师分配）', '(printer default)': '（打印机默认）', '(group)': '（跟随分组）',
  'Computing parts and geometry… (first run reads the STL files; later runs are instant)': '正在计算零件与几何数据…（首次需读取 STL 文件，之后会使用缓存）',
  'filament, all parts': '全部零件耗材', 'print time (sheet + estimate)': '打印时间（数据表 + 估算）',
  '(as tagged / mixed)': '（默认分配 / 混合）', '(as tagged / mixed) — set whole module': '（默认分配 / 混合）— 设置整个模块', '(as tagged)': '（默认分配）',
  'file missing': '文件缺失', 'no process preset found for the biggest printer; manual values used': '未找到最大打印机的工艺预设，使用手动设置',
  'open folder': '打开文件夹', 'Starting…': '正在启动…', 'Planning…': '正在排版…', 'planning…': '正在排版…',
  'Tick at least one group.': '请至少勾选一个分组。', 'loading…': '正在加载…', 'reading…': '正在读取…', 'done': '完成',
  'loading three.js…': '正在加载 three.js…', 'loading part…': '正在加载零件…',
  'No VAULT archive found: no STL files are indexed. Close the window, delete archive-path.txt and start again to choose the folder holding "01. DRAWERS" (Docker: mount it at /archive).': '未找到 VAULT 素材包，尚未索引任何 STL 文件。请关闭窗口，删除 archive-path.txt 并重新启动，选择包含“01. DRAWERS”的文件夹（Docker：挂载到 /archive）。',
});

VaultI18n.add({
  'main body': '主体', 'drawer inside': '抽屉内部', 'knob & handles': '旋钮与把手', 'accent': '点缀色',
  'main': '主体', 'knob': '旋钮与把手', 'tpu': 'TPU', 'drawers': '抽屉', 'sustainers': '翻盖箱',
  '(not found)': '（未找到）',
  'wide': '宽背板', 'universal': '通用背板', 'module connectors': '模块连接件', 'wall mounts': '壁挂件',
  'Drill the 2F board holes before use.': '使用前请先钻通 2F 背板上的孔。',
  'The USSA pegboard panels themselves are a separate product: https://www.ussadesign.com/products/multifunctional-bench': 'USSA 洞洞板本体需要另购：https://www.ussadesign.com/products/multifunctional-bench',
  'Fits an IKEA Skådis board (not included).': '适用于 IKEA Skådis 洞洞板（不含板材）。',
  'Sustainer lid. Split version used: one-piece file does not fit the enabled printers.': '翻盖箱盖。使用分体版本：整体文件超出已启用打印机的打印范围。',
  'all parts ready': '所有零件已就绪', 'slicer defaults': '切片软件默认值', 'placed diagonally': '已沿对角线放置',
  'fits no enabled printer (see the Stack tab warning for the reason)': '所有已启用的打印机均无法容纳（原因见“堆叠配置”页的警告）',
  'its module is not printed, so the brace is pointless': '对应模块不打印，无需打印支撑',
});

// Anchored templates translate only application-generated messages. Captured
// names/paths/numbers remain untouched; nested application phrases are explicit.
(() => {
  const t = value => VaultI18n.translate(value);
  const rule = (pattern, render) => VaultI18n.pattern(pattern, render);
  const group = value => t(value);
  rule(/^• (.*)$/, message => '• ' + t(message));
  rule(/^⚠ (.*)$/s, message => '⚠ ' + t(message));
  rule(/^(.*) \(pictures: (.*)\)$/s, (description, context) => `${t(description)}（图片：${t(context)}）`);
  rule(/^(L width · two S bays|XL width · S \+ M bays) \((.*?) body, (.*?) boxes\)$/, (layout, body, boxes) => `${t(layout)}（${body} 外壳，${boxes} 盒体）`);
  rule(/^Layer (\d+)( · base \(bottom\)| · top)? — (.*?) · (\d+)U · (Drawers|Sustainers)$/, (n, position, layout, height, type) => `第 ${n} 层${position === ' · base (bottom)' ? ' · 底层' : position ? ' · 顶层' : ''} — ${t(layout)} · ${height}U · ${t(type)}`);
  rule(/^Layer (\d+) · (.*?) (\d+) · (\d+)U (drawers|sustainers)$/, (n, layout, depth, height, type) => `第 ${n} 层 · ${t(layout)} 深度 ${depth} · ${height}U ${t(type)}`);
  rule(/^Bay (\d+) \((.*?)\) Facades$/, (n, family) => `仓位 ${n}（${family}）面板组合`);
  rule(/^(\d+)U (box|facade)$/, (n, kind) => `${n}U ${t(kind)}`);
  rule(/^bay (\d+): (\d+)U facade$/, (bay, n) => `仓位 ${bay}：${n}U 面板`);
  rule(/^brace for depth (\d+)$/, depth => `深度 ${depth} 的支撑`);
  rule(/^([SMLX]+\d+) base$/, family => `${family} 底座`);
  rule(/^backbone \((wide|universal)\)$/, kind => `背板（${t(kind)}）`);
  rule(/^(IKEA Skadis|USSA) pegboards$/, brand => `${brand} 洞洞板`);
  rule(/^(.*?) mm \(W × D × H, without wheels and handle\) · depth (\d+) × 42 mm grid$/, (size, depth) => `${size} mm（宽 × 深 × 高，不含车轮和把手）· 深度 ${depth} × 42 mm 网格`);
  rule(/^(\d+)h (\d+)m$/, (h, m) => `${h} 小时 ${m} 分钟`);
  rule(/^≈(\d+h \d+m)$/, time => '≈' + t(time));
  rule(/^(.*?) mm · ([\d,]+) triangles$/, (size, n) => `${size} mm · ${n} 个三角面`);
  rule(/^viewer failed: (.*)$/s, error => '查看器加载失败：' + error);
  rule(/^Could not parse: (.*)$/s, error => '无法解析：' + error);
  rule(/^(\d+) \(all\)$/, z => `${z}（全部）`);
  rule(/^(.*?) only$/, printer => `仅 ${printer}`);
  rule(/^(.*?) \(not installed\)$/, slicer => `${slicer}（未安装）`);
  rule(/^(.*?\))(, \d+U)$/, (context, height) => `${t(context)}${height}`);
  rule(/^· (\d+) keys$/, n => `· ${n} 项设置`);
  rule(/^(.*?) · (\d+) keys$/, (preset, n) => `${preset} · ${n} 项设置`);
  rule(/^(.*?) \(not found\)$/, preset => `${preset}（未找到）`);
  rule(/^\(auto: first (.*?) preset\)$/, material => `（自动：首个 ${material} 预设）`);
  rule(/^(.*?) (#[\da-fA-F]{6}) · (\d+) spools?, ([\d.]+) g left$/, (name, color, n, g) => `${name} ${color} · ${n} 卷，剩余 ${g} g`);
  rule(/^(.*?) · (\d+) colours$/, (filament, n) => `${filament} · ${n} 种颜色`);
  rule(/^slot (\d+)$/, n => `槽位 ${n}`);
  // A part group's role names are application metadata, filament names are user data.
  rule(/^(main body|drawer inside|knob & handles|accent|TPU tyres) → (.*)$/, (role, name) => `${t(role)} → ${name}`);
  rule(/^(\d+) parts · now (.*)$/, (n, name) => `${n} 种零件 · 当前使用 ${name}`);
  rule(/^· (\d+) parts$/, n => `· ${n} 种零件`);
  rule(/^printed pieces · (\d+) files$/, n => `打印件 · ${n} 个文件`);
  rule(/^(.*?) \((main|box|knob|accent|tpu)\)$/, (name, role) => `${name}（${({main:'主体',box:'抽屉内部',knob:'旋钮与把手',accent:'点缀色',tpu:'TPU'})[role]}）`);
  rule(/^in: (.*)$/, groups => '所在层：' + groups);
  rule(/^\* estimated from the mesh \(shell ([\d.]+) mm \+ infill (\d+) %(?:, from the process preset "(.*)")?\); other weights\/times come from the designer's component sheet \(H2S, basic settings\)\.$/, (shell, infill, preset) => `* 根据网格估算（壳体 ${shell} mm + 填充率 ${infill}%${preset ? '，来自工艺预设“' + preset + '”' : ''}）；其余重量和时间来自设计师的零件数据表（H2S，基础设置）。`);
  rule(/^(.*?): (\d+) walls × ([\d.]+) mm = ([\d.]+) mm shell, (\d+) % infill \((.*)\)$/, (printer, walls, line, shell, infill, preset) => `${printer}：${walls} 道壁 × ${line} mm = ${shell} mm 壳体，填充率 ${infill}%（${preset}）`);
  rule(/^✓ (.*?) — (\d+) plates, (\d+) parts(, every piece checked on its plate)?(?:, (\d+) objects with preset overrides)?; filaments: (.*?)(?: · ⚠ (.*))? \(([\d.]+)s\)$/, (file, plates, parts, checked, overrides, filaments, warning, seconds) => `✓ ${file} — ${plates} 个打印盘，${parts} 个零件${checked ? '，已检查每个零件均位于盘内' : ''}${overrides ? `，${overrides} 个对象使用独立预设` : ''}；耗材：${filaments === 'slicer defaults' ? t(filaments) : filaments}${warning ? ' · ⚠ ' + t(warning) : ''}（${seconds} 秒）`);
  rule(/^(.*?): (\d+) plates · ≈(\d+h \d+m)$/, (printer, n, time) => `${printer}：${n} 个打印盘 · ≈${t(time)}`);
  rule(/^(\d+) of (\d+) printed pieces are on plates( — nothing left out|; \d+ NOT exported \(listed below\))(?: · ⚠ (\d+) pieces unaccounted for, report this)?$/, (placed, pieces, remaining, missing) => `${pieces} 个打印件中有 ${placed} 个已排入打印盘${remaining.startsWith(' —') ? ' — 无遗漏' : `；${remaining.match(/\d+/)[0]} 个未导出（见下方）`}${missing ? ` · ⚠ ${missing} 个零件未计入，请反馈此问题` : ''}`);
  rule(/^✗ (\d+)× (.*?) \((.*?) mm\)(?: · (.*?))?: not exported, (.*)$/, (qty, name, size, sourceGroup, reason) => `✗ ${qty}× ${name}（${size} mm）${sourceGroup ? ' · ' + group(sourceGroup) : ''}：未导出，${t(reason)}`);
  rule(/^(.*?) · plate (\d+)$/, (printer, n) => `${printer} · 打印盘 ${n}`);
  rule(/^≈([\d.]+) g · ≈(\d+h \d+m) · max height (\d+) mm$/, (grams, time, height) => `≈${grams} g · ≈${t(time)} · 最大高度 ${height} mm`);
  rule(/^· bed (\d+)% used$/, fill => `· 平台利用率 ${fill}%`);
  rule(/^· placed diagonally$/, () => '· 沿对角线放置');
  rule(/^(\d+)% · (.*)$/s, (percent, message) => `${percent}% · ${t(message)}`);
  rule(/^done in ([\d.]+)s · files in output\/(.*)$/, (seconds, folder) => `已完成，用时 ${seconds} 秒 · 文件位于 output/${folder}`);
  rule(/^(\d+) spools$/, n => `${n} 卷耗材`);
  rule(/^(\d+) layers imported\.$/, n => `已导入 ${n} 层。`);
  rule(/^(\d+) STL files indexed(?: · (.*))?$/, (n, progress) => `已索引 ${n} 个 STL 文件${progress ? ' · ' + t(progress) : ''}`);
  rule(/^preparing parts (\d+)\/(\d+)$/, (done, total) => `正在准备零件 ${done}/${total}`);

  // Backend catalog descriptions are translated only on screen, never in the BOM
  // data used as override keys or written into slicer projects and saved stacks.
  rule(/^L(\d+) · ([SMLX]+\d+) (\d+)U drawers(?: \(split (.*?)\))?$/, (n, family, height, split) => `第 ${n} 层 · ${family} ${height}U 抽屉${split ? '（双仓 ' + split + '）' : ''}`);
  rule(/^L(\d+) · ([SMLX]+\d+) (\d+)U sustainer(?: \(bay (\d+)\))?$/, (n, family, height, bay) => `第 ${n} 层 · ${family} ${height}U 翻盖箱${bay ? '（仓位 ' + bay + '）' : ''}`);
  rule(/^Roof · (.*)$/, family => `顶板 · ${family}`);
  rule(/^Layer (\d+)\.(.*)$/s, (n, rest) => `第 ${n} 层。${rest ? t(rest) : ''}`);
  rule(/^Layer (\d+), (USSA Pegboard|IKEA Skadis Pegboard) attachment\.(.*)$/s, (n, brand, rest) => `第 ${n} 层，${brand === 'USSA Pegboard' ? 'USSA' : 'IKEA Skadis'} 洞洞板连接件。${t(rest)}`);
  rule(/^File not found: (.*) \((.*)\)$/, (name, hint) => `未找到文件：${name}（${hint}）`);
  rule(/^(.*) does not exist; plain baseplate used\.$/, name => `${name} 不存在；已使用普通底板。`);
  rule(/^Layer (\d+): (.*?) cannot stack on a (.*?) base\.$/, (n, layout, base) => `第 ${n} 层：${layout} 不能叠放在 ${base} 底座上。`);
  rule(/^Layer (\d+): XL-width modules \(XL and S\+M\) only exist in 1U\.$/, n => `第 ${n} 层：XL 宽度模块（XL 和 S+M）仅有 1U 规格。`);
  rule(/^(.*?) (\d+)U (drawers|sustainers) module without a partner for a (.*?) base; placed alone in a two-bay layer\.$/, (family, height, type, base) => `${family} ${height}U ${t(type)}模块缺少与 ${base} 底座匹配的另一模块；已单独放入双仓层。`);
  rule(/^Some facades in the PDF could not be matched to a module: (.*)$/, parts => 'PDF 中部分面板无法匹配模块：' + parts);
  rule(/^(M\d+ x [\d-]+ mm) (bolt|countersunk bolt|hex bolt)$/, (size, kind) => `${size} ${{bolt:'螺栓','countersunk bolt':'沉头螺栓','hex bolt':'六角螺栓'}[kind]}`);
  rule(/^M16 rod (\d+) mm \(axle\)$/, length => `M16 杆 ${length} mm（车轴）`);
  rule(/^(.*?): reading (.*) \((\d+)\/(\d+)\)$/, (printer, part, done, total) => `${printer}：正在读取 ${part}（${done}/${total}）`);
  rule(/^(.*?): writing (.*) \((\d+) plates\)$/, (printer, file, n) => `${printer}：正在写入 ${file}（${n} 个打印盘）`);
  rule(/^(.*?): checking every piece is on its plate$/, printer => `${printer}：正在检查每个零件是否位于盘内`);
  rule(/^(ValueError|RuntimeError): (preset not found: .*|an export is already running)$/, (kind, error) => `${kind}: ${t(error)}`);
  rule(/^preset not found: (.*)$/, names => '未找到预设：' + names);
  rule(/^(.*) · (\d+ piece\(s\) not entirely on their plate: .*)$/, (warning, outside) => `${t(warning)} · ${t(outside)}`);
  rule(/^(\d+) piece\(s\) not entirely on their plate: (.*)$/, (n, parts) => `${n} 个零件超出打印盘：${parts.replace(/ \(plate (\d+), ([\d.]+) mm\)(?=, |$)/g, '（打印盘 $1，超出 $2 mm）')}`);
  rule(/^(.*?): (\d+)× (.*?) \(([\d.]+×[\d.]+×[\d.]+) mm\) cannot be printed\. (.*?)\.(?: It fits a (.*)\.)?$/, (sourceGroup, qty, name, size, reasons, bigger) => `${group(sourceGroup)}：${qty}× ${name}（${size} mm）无法打印。${reasons.split('; ').map(t).join('；')}。${bigger ? '可使用 ' + bigger.replace(/ or a /g, ' 或 ') + '。' : ''}`);
  rule(/^(.*?): ([\d.]+) mm tall, limit ([\d.]+) mm \((no tall parts|Z)\)$/, (printer, height, limit, kind) => `${printer}：高度 ${height} mm，上限 ${limit} mm（${kind === 'Z' ? 'Z' : '限制高零件'}）`);
  rule(/^(.*?): footprint ([\d.]+×[\d.]+) mm does not fit ([\d.]+×[\d.]+) mm( bed|, what one nozzle reaches \(the 330 mm plate is only covered by both nozzles together\))(?:, minus your ([\d.]+) mm edge)?, even rotated$/, (printer, size, bed, nozzle, edge) => `${printer}：占地 ${size} mm，即使旋转也无法放入 ${bed} mm 平台${nozzle === ' bed' ? '' : '（单喷嘴覆盖范围，330 mm 平台需两个喷嘴共同覆盖）'}${edge ? `，另需扣除 ${edge} mm 边缘留空` : ''}`);
})();
