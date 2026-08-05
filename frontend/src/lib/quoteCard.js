import { toPng } from 'html-to-image';

const CARD_WIDTH = 1080;
const CARD_HEIGHT = 1350; // 4:5 — the safe ratio for Instagram feed and Stories

/** Builds the off-screen DOM node captured into the quote-card PNG. Uses
 *  inline styles throughout: html-to-image rasterises computed style, and an
 *  off-screen node never resolves the app's `.library-app`-scoped CSS
 *  variables, so those custom properties would otherwise capture as blank. */
function buildCardNode({ text, sourceLine }) {
  const node = document.createElement('div');
  node.style.cssText = `
    position: fixed;
    top: -10000px;
    left: -10000px;
    width: ${CARD_WIDTH}px;
    height: ${CARD_HEIGHT}px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 48px;
    padding: 120px 100px;
    background: #fdf6e6;
    background-image: repeating-linear-gradient(0deg, transparent 0 31px, rgba(148, 112, 35, 0.05) 31px 32px);
    font-family: Georgia, 'Times New Roman', serif;
    box-sizing: border-box;
  `;

  const quote = document.createElement('p');
  quote.textContent = text;
  quote.style.cssText = `
    margin: 0;
    color: #241b15;
    font-size: ${text.length > 180 ? 44 : 56}px;
    line-height: 1.5;
    text-align: center;
    max-width: 100%;
  `;

  const rule = document.createElement('div');
  rule.style.cssText = 'width: 64px; height: 2px; background: #a83220;';

  const source = document.createElement('p');
  source.textContent = sourceLine;
  source.style.cssText = `
    margin: 0;
    color: #62513d;
    font-size: 30px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-family: 'Courier New', monospace;
  `;

  const watermark = document.createElement('p');
  watermark.style.cssText = `
    position: absolute;
    bottom: 72px;
    margin: 0;
    color: #947023;
    font-size: 26px;
    letter-spacing: 0.08em;
    font-family: 'Courier New', monospace;
  `;
  watermark.innerHTML = 'Dharma<span style="color:#a83220">Search</span>';

  node.append(quote, rule, source, watermark);
  return node;
}

async function waitForFonts() {
  try {
    await document.fonts?.ready;
  } catch {
    // Font readiness is a nicety; capture proceeds with system fallbacks.
  }
}

async function renderCardPng(verse, script) {
  const text = (script?.text || verse.en || '').trim();
  const chapter = verse.ch != null ? `Ch. ${verse.ch}, ` : '';
  const sourceLine = `${verse.tn} — ${chapter}Verse ${verse.vn}`;

  const node = buildCardNode({ text, sourceLine });
  document.body.appendChild(node);
  await waitForFonts();

  try {
    return await toPng(node, {
      width: CARD_WIDTH,
      height: CARD_HEIGHT,
      pixelRatio: 2,
      backgroundColor: '#fdf6e6',
    });
  } finally {
    node.remove();
  }
}

function dataUrlToFile(dataUrl, filename) {
  const [header, base64] = dataUrl.split(',');
  const mime = header.match(/:(.*?);/)[1];
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return new File([bytes], filename, { type: mime });
}

function downloadDataUrl(dataUrl, filename) {
  const link = document.createElement('a');
  link.href = dataUrl;
  link.download = filename;
  link.click();
}

/** Generates the quote card and hands it to the platform's native flow: Web
 *  Share with the image file where supported (mobile), otherwise a direct
 *  PNG download (desktop). Returns a short status the caller can toast. */
export async function shareVerseAsImage(verse, script) {
  const dataUrl = await renderCardPng(verse, script);
  const filename = `dharmasearch-${verse.id}.png`;
  const file = dataUrlToFile(dataUrl, filename);

  if (navigator.canShare?.({ files: [file] })) {
    try {
      await navigator.share({
        files: [file],
        title: `${verse.tn} — Verse ${verse.vn}`,
      });
      return 'shared';
    } catch {
      // Cancelling the share sheet is a choice, not an error worth a toast.
      return 'cancelled';
    }
  }

  downloadDataUrl(dataUrl, filename);
  return 'downloaded';
}
