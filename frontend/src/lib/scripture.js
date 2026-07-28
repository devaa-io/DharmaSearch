export const LANGUAGE_NAMES = {
  en: 'English',
  dev: 'Devanagari',
  iast: 'IAST',
  roman: 'Transliteration',
  ml: 'Malayalam',
  ta: 'Tamil',
  te: 'Telugu',
  kn: 'Kannada',
  hi: 'Hindi',
};

// BCP-47 tags for speech synthesis / TTS voice selection, keyed by script code.
// Sanskrit has no widely available voice, so Devanagari and IAST borrow Hindi,
// which is the closest commonly installed approximation.
export const SPEECH_LANGS = {
  en: 'en-GB',
  dev: 'hi-IN',
  iast: 'hi-IN',
  roman: 'hi-IN',
  hi: 'hi-IN',
  ml: 'ml-IN',
  ta: 'ta-IN',
  te: 'te-IN',
  kn: 'kn-IN',
};

// English leads: it is the entry point for most readers, and the original
// scripts are one tap away rather than the first thing to decipher.
export function scriptsFor(verse) {
  const scripts = [];
  if (verse.en) scripts.push({ code: 'en', text: verse.en });
  if (verse.dev) scripts.push({ code: 'dev', text: verse.dev });
  if (verse.iast) scripts.push({ code: 'iast', text: verse.iast });
  else if (verse.roman) scripts.push({ code: 'roman', text: verse.roman });
  ['ml', 'ta', 'te', 'kn', 'hi'].forEach(code => {
    if (verse.scripts?.[code]) scripts.push({ code, text: verse.scripts[code] });
  });
  return scripts;
}

export function searchBlob(verse) {
  return [
    verse.roman,
    verse.dev,
    verse.iast,
    verse.en,
    verse.kw,
    verse.cn,
    ...Object.values(verse.scripts || {}),
  ].filter(Boolean).join(' ').toLocaleLowerCase();
}

export function dailyIndex(length, offset = 0) {
  const today = new Date();
  const start = new Date(today.getFullYear(), 0, 0);
  const day = Math.floor((today - start) / 86400000);
  return (today.getFullYear() * 1000 + day + offset) % length;
}
