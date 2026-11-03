// Tab, the mascot: tab(expression, options) returns SVG markup for viewBox '-10 -6 220 212'.
(() => {
const K = '#15120f', O = '#e8572c', C = '#f6efe3', P = '#fffaf2', G = '#ffd166';
// eyes: [lx, ly, rx, ry] variations; brows; mouth path
const EXPR = {
  neutral:  { brows: 'M62 92 h22 M116 92 h22', eyes: 'round', mouth: 'M86 138 q14 6 28 0' },
  sceptic:  { brows: 'M60 96 l24 -4 M116 84 l24 8', eyes: 'squint', mouth: 'M86 140 h28' },
  excited:  { brows: 'M60 84 q12 -8 24 0 M116 84 q12 -8 24 0', eyes: 'big', mouth: 'M82 132 q18 22 36 0 z' },
  thinking: { brows: 'M60 90 h24 M116 84 l24 4', eyes: 'up', mouth: 'M92 140 q8 -4 16 0' },
  A:        { brows: 'M62 90 h22 M116 90 h22', eyes: 'round', mouth: 'M84 130 q16 30 32 0 z' },
  O:        { brows: 'M62 88 h22 M116 88 h22', eyes: 'round', mouth: 'O' },
  E:        { brows: 'M62 90 h22 M116 90 h22', eyes: 'round', mouth: 'M82 134 h36 q-4 12 -18 12 q-14 0 -18 -12 z' },
};
function eyes(kind) {
  if (kind === 'squint') return `<rect x="64" y="104" width="20" height="8" rx="4" fill="${K}"/><rect x="118" y="100" width="18" height="18" rx="9" fill="${K}"/>`;
  if (kind === 'big') return `<circle cx="74" cy="110" r="13" fill="${K}"/><circle cx="126" cy="110" r="13" fill="${K}"/><circle cx="78" cy="106" r="4" fill="${P}"/><circle cx="130" cy="106" r="4" fill="${P}"/>`;
  if (kind === 'up') return `<circle cx="76" cy="104" r="9" fill="${K}"/><circle cx="128" cy="104" r="9" fill="${K}"/>`;
  return `<circle cx="74" cy="110" r="10" fill="${K}"/><circle cx="126" cy="110" r="10" fill="${K}"/><circle cx="77" cy="107" r="3" fill="${P}"/><circle cx="129" cy="107" r="3" fill="${P}"/>`;
}
function mouth(m) { return m === 'O' ? `<ellipse cx="100" cy="140" rx="10" ry="13" fill="${K}"/>` : `<path d="${m}" fill="${m.endsWith('z') ? K : 'none'}" stroke="${K}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`; }
// one character; opts: spark (AI on), rings (calendar), sticker, arms pose
function tab(expr = 'neutral', { spark = true, glow = false, rings = true, sticker = false, arms = 'down', screen = P } = {}) {
  const e = EXPR[expr];
  const armsSvg = {
    down: `<path d="M34 130 q-18 14 -14 36" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M166 130 q18 14 14 36" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/>`,
    crossed: `<path d="M28 128 q30 44 88 34" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M172 128 q-30 44 -88 34" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/>`,
    up: `<path d="M34 120 q-24 -20 -18 -50" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M166 120 q24 -20 18 -50" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M8 66 l8 6 6 -8 M178 62 l8 6 6 -8" stroke="${K}" stroke-width="5" fill="none" stroke-linecap="round"/>`,
    point: `<path d="M34 130 q-18 14 -14 36" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M166 124 q26 -6 30 -26" stroke="${K}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M186 92 l14 -4 -4 14 z" fill="${K}"/>`,
  }[arms];
  return `
  ${spark ? `<path d="M100 40 v-14" stroke="${K}" stroke-width="5" stroke-linecap="round"/>
    ${glow ? `<circle cx="100" cy="16" r="18" fill="${G}" opacity=".55"/>` : ''}
    <path d="M100 2 l5 10 11 2 -8 8 2 11 -10 -5 -10 5 2 -11 -8 -8 11 -2 z" fill="${glow ? G : O}" stroke="${K}" stroke-width="3" stroke-linejoin="round"/>` : ''}
  ${arms === 'crossed' ? '' : armsSvg}
  <path d="M86 186 v10 M114 186 v10" stroke="${K}" stroke-width="7" stroke-linecap="round"/>
  <rect x="30" y="40" width="140" height="148" rx="22" fill="${screen}" stroke="${K}" stroke-width="6"/>
  <path d="M30 62 a22 22 0 0 1 22 -22 h96 a22 22 0 0 1 22 22 v12 h-140 z" fill="${O}" stroke="${K}" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="50" cy="58" r="4.5" fill="${K}"/><circle cx="64" cy="58" r="4.5" fill="${K}"/><circle cx="78" cy="58" r="4.5" fill="${K}"/>
  ${rings ? `<rect x="104" y="30" width="10" height="22" rx="5" fill="${C}" stroke="${K}" stroke-width="4"/><rect x="134" y="30" width="10" height="22" rx="5" fill="${C}" stroke="${K}" stroke-width="4"/>` : ''}
  <path d="${e.brows}" stroke="${K}" stroke-width="6" stroke-linecap="round" fill="none"/>
  ${eyes(e.eyes)}
  <circle cx="58" cy="128" r="8" fill="${O}" opacity=".35"/><circle cx="142" cy="128" r="8" fill="${O}" opacity=".35"/>
  ${mouth(e.mouth)}
  ${arms === 'crossed' ? armsSvg : ''}
  ${sticker ? `<g transform="rotate(-14 150 160)"><rect x="112" y="148" width="84" height="30" rx="6" fill="${K}"/><text x="154" y="169" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="18" fill="${C}">BOOKED</text></g>` : ''}`;
}
window.tab = tab; window.TAB_VIEWBOX = '-10 -6 220 212';
})();
