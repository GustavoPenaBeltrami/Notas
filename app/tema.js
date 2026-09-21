(() => {
  const TEMAS = { hypr: 'hypr', claro: 'claro', eink: 'e-ink', sakura: 'sakura', bosque: 'bosque', ambar: 'ámbar crt' };
  const raiz = document.documentElement;
  const aplicar = t => { if (TEMAS[t]) raiz.dataset.tema = t; else delete raiz.dataset.tema; };

  const guardado = localStorage.getItem('tema');
  aplicar(guardado === 'oscuro' ? 'hypr' : guardado);

  const actual = () => raiz.dataset.tema || (matchMedia('(prefers-color-scheme: light)').matches ? 'claro' : 'hypr');

  window.selectorTema = () => `<select id="tema-sel" aria-label="Tema">${Object.entries(TEMAS).map(([k, nombre]) =>
    `<option value="${k}"${k === actual() ? ' selected' : ''}>${nombre}</option>`).join('')}</select>`;

  window.elegirTema = t => {
    aplicar(t);
    localStorage.setItem('tema', t);
  };
})();
