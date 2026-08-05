/** Eight recurring ideas across the library, each grounded in verses that are
 *  actually in the corpus. Every `cites` id must resolve via `versesById` —
 *  ConceptsView drops any concept whose citations don't resolve, so a typo'd
 *  id fails silently closed rather than showing a dead link. */
export const CONCEPTS = [
  {
    id: 'atman',
    term: 'Ātman',
    sanskrit: 'आत्मन्',
    body: 'The self that is not the body, the mind, or any role you play — the witness beneath all of it. The Gita describes it as unborn and undying, changing form the way a person changes clothes.',
    cites: ['bg-2-20', 'bg-2-22'],
  },
  {
    id: 'karma-yoga',
    term: 'Karma-yoga',
    sanskrit: 'कर्मयोग',
    body: "Acting fully while releasing your grip on the outcome — the Gita's answer to Arjuna's paralysis, and the source of its most quoted line.",
    cites: ['bg-2-47'],
  },
  {
    id: 'three-gunas',
    term: 'The Three Guṇas',
    sanskrit: 'त्रिगुण',
    body: 'Sattva, rajas, and tamas — clarity, agitation, and inertia. The Gita treats these as the threads nature is woven from, shaping mood, food, and action alike.',
    cites: ['bg-14-5', 'bg-18-19'],
  },
  {
    id: 'chariot',
    term: 'The Chariot',
    sanskrit: 'रथ',
    body: "The Katha Upanishad's image for the inner instrument: the body as chariot, the senses as horses, the mind as reins, and the intellect as charioteer.",
    cites: ['katha-up-3-3', 'katha-up-3-9'],
  },
  {
    id: 'dharma',
    term: 'Dharma',
    sanskrit: 'धर्म',
    body: 'Not "religion" so much as the shape of right action for who you are, in the situation you’re actually in — a duty that shifts with role and circumstance.',
    cites: ['bg-2-31', 'bg-18-47'],
  },
  {
    id: 'maya',
    term: 'Māyā',
    sanskrit: 'माया',
    body: 'The veiling power that makes the changing world look more solid and separate than it is — not a trick played on you, but the nature of appearance itself.',
    cites: ['bg-7-14'],
  },
  {
    id: 'samsara',
    term: 'Saṃsāra',
    sanskrit: 'संसार',
    body: 'The cycle a soul stays bound to while it remains attached to the qualities born of nature — birth following birth until that attachment loosens.',
    cites: ['bg-13-22'],
  },
  {
    id: 'brahman',
    term: 'Brahman',
    sanskrit: 'ब्रह्मन्',
    body: 'The ground of everything — the Isha Upanishad opens by saying all that moves on earth is to be seen as pervaded by this. Where Atman is this seen from within, Brahman is the same thing seen as the whole.',
    cites: ['isha-up-1'],
  },
];
