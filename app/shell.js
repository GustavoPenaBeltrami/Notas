(() => {
  const PAGINAS = [['notas', 'notas.html'], ['exámenes', 'examen.html']];

  window.montarShell = actual => {
    document.body.insertAdjacentHTML('afterbegin', `
      <header class="waybar">
        <div class="wb-izq">
          <span class="wb-logo" aria-hidden="true"><svg viewBox="0 0 20 20" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5.2C8.4 4 6.2 3.5 3 3.5v11.8c3.2 0 5.4.5 7 1.7 1.6-1.2 3.8-1.7 7-1.7V3.5c-3.2 0-5.4.5-7 1.7z"/><path d="M10 5.2V17"/></svg></span>
          <nav class="wb-mod workspaces">${PAGINAS.map(([nombre, href], i) =>
            `<a href="${href}"${nombre === actual ? ' aria-current="page"' : ''}>${i + 1}<span>${nombre}</span></a>`).join('')}</nav>
        </div>
        <div class="wb-centro"><span class="wb-mod reloj" id="reloj"></span></div>
        <div class="wb-der">
          <div class="wb-herr" id="herramientas"></div>
          <div class="wb-mod"><span class="etq">tema</span>${selectorTema()}</div>
        </div>
      </header>
      <div class="cuerpo">
        <aside class="explorer"><div class="marco">
          <span class="marco-titulo">explorer</span>
          <nav class="arbol" id="arbol"></nav>
        </div></aside>
        <main class="panel" id="app"></main>
      </div>
      <footer class="statusline">
        <span class="modo" id="modo">NORMAL</span>
        <span class="ruta-sl" id="ruta">~/notes</span>
        <span class="sl-der">
          <span id="estado"></span>
          <span class="sl-ctl" title="Zoom del contenido">
            <svg viewBox="0 0 20 20" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="8.5" cy="8.5" r="5.5"/><path d="m12.7 12.7 4.8 4.8"/></svg>
            <button data-ajuste="zoom" data-paso="-10" aria-label="Menos zoom">−</button><input id="zoom" type="number" min="50" max="250" step="10" aria-label="Zoom en %">%<button data-ajuste="zoom" data-paso="10" aria-label="Más zoom">+</button>
          </span>
          <span class="sl-ctl" title="Ancho del texto">
            <span aria-hidden="true">↔</span>
            <button data-ajuste="ancho" data-paso="-40" aria-label="Más angosto">−</button><input id="ancho" type="number" min="320" max="2400" step="20" aria-label="Ancho en px">px<button data-ajuste="ancho" data-paso="40" aria-label="Más ancho">+</button>
          </span>
          <span class="sl-mod">utf-8[unix]</span>
          <span class="pos" id="pos">Top</span>
        </span>
      </footer>`);

    document.getElementById('tema-sel').onchange = e => elegirTema(e.target.value);

    const reloj = document.getElementById('reloj');
    const tic = () => {
      const d = new Date();
      reloj.textContent = d.toLocaleDateString('es-AR', { weekday: 'short', day: 'numeric', month: 'short' }).replace(',', '')
        + '   ' + d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit', hour12: false });
    };
    tic();
    setInterval(tic, 15000);

    const app = document.getElementById('app');
    const AJUSTES = {
      zoom: { clave: 'zoom', defecto: 100, aplicar: v => app.style.zoom = v / 100 },
      ancho: { clave: 'ancho-' + actual, defecto: actual === 'notas' ? 736 : 960,
               aplicar: v => document.documentElement.style.setProperty('--ancho', v + 'px') },
    };
    const ajustar = (nombre, valor) => {
      const a = AJUSTES[nombre], campo = document.getElementById(nombre);
      const v = Math.min(+campo.max, Math.max(+campo.min, Math.round(+valor || a.defecto)));
      campo.value = v;
      a.aplicar(v);
      localStorage.setItem(a.clave, v);
    };
    Object.entries(AJUSTES).forEach(([nombre, a]) => {
      ajustar(nombre, localStorage.getItem(a.clave) || a.defecto);
      document.getElementById(nombre).onchange = e => ajustar(nombre, e.target.value);
    });
    document.querySelectorAll('[data-ajuste]').forEach(b => b.onclick = () =>
      ajustar(b.dataset.ajuste, +document.getElementById(b.dataset.ajuste).value + +b.dataset.paso));

    const pos = document.getElementById('pos');
    const scroll = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      pos.textContent = max <= 0 ? 'All' : scrollY <= 0 ? 'Top' : scrollY >= max - 1 ? 'Bottom'
        : Math.round(scrollY / max * 100) + '%';
    };
    addEventListener('scroll', scroll, { passive: true });
    addEventListener('resize', scroll);
    new ResizeObserver(scroll).observe(document.body);

    return {
      app,
      arbol: document.getElementById('arbol'),
      herramientas: document.getElementById('herramientas'),
      ruta: t => document.getElementById('ruta').textContent = t,
      modo: (t, clase = '') => Object.assign(document.getElementById('modo'), { textContent: t, className: 'modo ' + clase }),
    };
  };
})();
