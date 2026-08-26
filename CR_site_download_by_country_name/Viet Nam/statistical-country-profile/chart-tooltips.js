(() => {
  const node = document.getElementById('chart-data');
  if (!node) return;
  const charts = JSON.parse(node.textContent);
  const number = new Intl.NumberFormat(undefined, {maximumFractionDigits: 2});
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const show = (box, lines, event) => {
    box.replaceChildren(...lines.map((line, index) => {
      const div = document.createElement('div');
      div.textContent = line.text;
      if (index === 0) div.className = 'tooltip-heading';
      if (line.target) div.classList.add('tooltip-target');
      return div;
    }));
    box.hidden = false;
    const host = box.parentElement.getBoundingClientRect();
    const x = clamp(event.clientX - host.left + 14, 8, Math.max(8, host.width - box.offsetWidth - 8));
    const y = clamp(event.clientY - host.top + 14, 8, Math.max(8, host.height - box.offsetHeight - 8));
    box.style.left = `${x}px`;
    box.style.top = `${y}px`;
  };
  document.querySelectorAll('.interactive-chart').forEach((host) => {
    const payload = charts[host.dataset.chart];
    const box = host.querySelector('.chart-tooltip');
    if (!payload || !box) return;
    const move = (event) => {
      const rect = host.getBoundingClientRect();
      if (payload.type === 'trend') {
        const fraction = clamp((event.clientX - rect.left - rect.width * 0.075) / (rect.width * 0.855), 0, 1);
        const intended = payload.year_min + fraction * (payload.year_max - payload.year_min);
        const years = [...new Set(payload.points.map((point) => point.year))];
        const year = years.reduce((best, candidate) => Math.abs(candidate - intended) < Math.abs(best - intended) ? candidate : best, years[0]);
        const values = payload.points.filter((point) => point.year === year).sort((a, b) => a.country.localeCompare(b.country));
        const lines = [{text: String(year)}].concat(values.map((point) => ({
          text: `${point.country}: ${number.format(point.value)} ${payload.unit}`,
          target: point.country === payload.target
        })));
        show(box, lines, event);
      } else {
        const top = rect.height * 0.14;
        const bottom = rect.height * 0.88;
        const fraction = clamp((event.clientY - rect.top - top) / Math.max(1, bottom - top), 0, 1);
        const index = Math.round((1 - fraction) * (payload.rows.length - 1));
        const row = payload.rows[index];
        if (!row) return;
        const period = payload.type === 'change_bar' ? `${row.year_start}–${row.year_end}` : String(row.year);
        const value = payload.type === 'change_bar' ? `${row.value >= 0 ? '+' : ''}${number.format(row.value)}` : number.format(row.value);
        const lines = [{text: row.country, target: row.country === payload.target}, {text: `${period}: ${value} ${payload.unit}`}];
        if (payload.type === 'change_bar') lines.push({text: `${number.format(row.value_start)} → ${number.format(row.value_end)} ${payload.unit}`});
        show(box, lines, event);
      }
    };
    host.addEventListener('mousemove', move);
    host.addEventListener('mouseleave', () => { box.hidden = true; });
    host.addEventListener('click', move);
  });
})();
