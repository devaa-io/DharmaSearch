"""Chillu normalisation for transliterated Malayalam.

indic_transliteration has no chillu support (there is no mention of it anywhere in
the package), so it renders every pure consonant with an explicit chandrakkala:
കര്മ where modern typesetting has കർമ. This module closes that gap.

WHAT THIS MAY AND MAY NOT BE APPLIED TO
=======================================
Only to Malayalam produced by transliterating Devanagari Sanskrit. It must never
be run over Malayalam somebody wrote as Malayalam, because a word-final
chandrakkala there is usually samvrtokaram, a reduced /u/, not a pure consonant:
നാളാണ് ("it is the day") would be corrupted into നാളാൺ, and ആണ് ("is") into ആൺ
("male"). In transliterated Sanskrit that ambiguity does not arise, because the
transliterator only emits a chandrakkala where the Devanagari had a virama, which
is a genuine pure consonant.

THE RULES
=========
Conservative on purpose. Two cases are safe, and everything else is left alone.

1. Word-final pure consonant -> chillu, for the five letters that have one:
   ണ ന ര ല ള. കാമാന് -> കാമാൻ. Unambiguous in transliterated Sanskrit.

2. ര് before another consonant -> ർ. This is the reph, and modern orthography
   writes it as a chillu: കര്മ -> കർമ, ധര്മ -> ധർമ, സര്വ -> സർവ.
   Exception: ര്യ keeps its conjunct, because കാര്യ is the standard spelling and
   കാർയ is not. ര്ര is excluded on the same caution.

Deliberately NOT converted: ന് ണ് ല് ള് before a consonant. Those form the
traditional conjuncts a reader expects to see joined, and breaking them apart is
a visible error: അനന്ത must not become അനൻത, nor പുണ്യ പുൺയ, nor അന്ന അൻന.
Mid-word chillu does occur in some compounds, but which ones is a judgement a
native reader has to make, not a rule this can safely infer.
"""

import re

VIRAMA = "്"          # chandrakkala
CHILLU = {
    "ണ": "ൺ",
    "ന": "ൻ",
    "ര": "ർ",
    "ല": "ൽ",
    "ള": "ൾ",
}

_CONSONANT = re.compile(r"[ക-ഹ]")
_LETTER = re.compile(r"[ഀ-ൿ]")

# ര് keeps its conjunct before these.
_RA_KEEPS_CONJUNCT = {"യ", "ര"}


def to_chillu(text: str) -> str:
    """Rewrite pure consonants as chillu letters where modern usage does.

    Only for Malayalam transliterated from Devanagari. See the module docstring.
    """
    if not text:
        return text

    out = []
    i, length = 0, len(text)
    while i < length:
        char = text[i]
        if char in CHILLU and i + 1 < length and text[i + 1] == VIRAMA:
            following = text[i + 2] if i + 2 < length else ""
            word_final = not following or not _LETTER.match(following)
            reph = (
                char == "ര"
                and bool(_CONSONANT.match(following))
                and following not in _RA_KEEPS_CONJUNCT
            )
            if word_final or reph:
                out.append(CHILLU[char])
                i += 2
                continue
        out.append(char)
        i += 1
    return "".join(out)
