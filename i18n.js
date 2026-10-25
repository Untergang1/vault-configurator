/* Presentation-only localization. Bind English source text once and retain the
 * same DOM nodes when switching languages: inputs, listeners and jobs survive. */
const VaultI18n = (() => {
  const storageKey = 'vault-configurator-language';
  const dictionary = Object.create(null), patterns = [];
  const sources = new WeakMap(), attributes = new WeakMap(), limits = new WeakMap();
  let language = 'zh-CN';
  try { if (localStorage.getItem(storageKey) === 'en') language = 'en'; } catch {}
  document.documentElement.lang = language;

  function translate(value) {
    const source = String(value ?? '');
    if (language === 'en') return source;
    const key = source.trim();
    let translated = dictionary[key];
    if (translated === undefined) {
      for (const [pattern, render] of patterns) {
        const match = key.match(pattern);
        if (match) { translated = render(...match.slice(1)); break; }
      }
    }
    return translated === undefined ? source : source.replace(key, () => translated);
  }

  function clip(value, limit) {
    if (!limit) return value;
    let width = 0, result = '';
    for (const character of value) {
      width += character.codePointAt(0) > 255 ? 2 : 1;
      if (width > limit) return result + '…';
      result += character;
    }
    return result;
  }

  function text(value, limit) {
    if (value instanceof Node) return value;
    const source = String(value ?? '');
    const node = document.createTextNode(clip(translate(source), limit));
    sources.set(node, source);
    if (limit) limits.set(node, limit);
    return node;
  }

  function attribute(node, name, value) {
    const source = String(value);
    if (!attributes.has(node)) attributes.set(node, new Map());
    attributes.get(node).set(name, source);
    node.setAttribute(name, translate(source));
  }

  function setText(node, value) { node.replaceChildren(text(value)); }

  function refresh() {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (sources.has(node)) node.nodeValue = clip(translate(sources.get(node)), limits.get(node));
      const attrs = attributes.get(node);
      if (attrs) for (const [name, source] of attrs) node.setAttribute(name, translate(source));
    }
    document.documentElement.lang = language;
    document.title = translate('VAULT configurator');
    const button = document.getElementById('languageToggle');
    button.textContent = language === 'en' ? '中文' : 'English';
    button.setAttribute('aria-label', language === 'en' ? '切换到简体中文' : 'Switch to English');
    button.title = button.getAttribute('aria-label');
  }

  function setLanguage(next) {
    language = next === 'en' ? 'en' : 'zh-CN';
    try { localStorage.setItem(storageKey, language); } catch {}
    refresh();
  }

  function init() {
    // Only the original static markup is scanned. Dynamic content is explicitly
    // bound by the element helpers or setText; no observer rewrites user content.
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (node.parentElement.closest('script, style, code, textarea, #languageToggle')) continue;
      if (node.nodeValue.trim()) sources.set(node, node.nodeValue);
    }
    document.querySelectorAll('[title], [placeholder], optgroup[label]').forEach(node => {
      for (const name of ['title', 'placeholder', 'label']) {
        if (node.hasAttribute(name)) attribute(node, name, node.getAttribute(name));
      }
    });
    document.getElementById('languageToggle').onclick = () => setLanguage(language === 'en' ? 'zh-CN' : 'en');
    refresh();
  }

  return {
    add: entries => Object.assign(dictionary, entries),
    pattern: (pattern, render) => patterns.push([pattern, render]),
    translate, text, attribute, setText, init, setLanguage,
    clipped: value => text(value, 52),
    // Use raw for filenames, external preset names and user-provided names.
    raw: value => document.createTextNode(String(value ?? '')),
    get language() { return language; },
  };
})();
