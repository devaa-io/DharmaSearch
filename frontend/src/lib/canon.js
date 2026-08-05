/** The traditional Śruti/Smṛti/Darśana structure of the wider canon, with the
 *  actual `texts` entries from scripture-data.json slotted into it by id.
 *  Grouping is fixed scholarship; which ids are complete/preview/missing
 *  entirely is read live from the data, not hardcoded here. */
export const CANON = [
  {
    id: 'shruti',
    label: 'Śruti',
    note: '"that which was heard"',
    groups: [
      { id: 'vedas', label: 'The Four Vedas', note: 'Ṛg, Yajur, Sāma, Atharva', textIds: ['vedas'] },
      {
        id: 'upanishads',
        label: 'Upaniṣads',
        note: 'of 108 traditionally counted',
        textIds: [
          'isha-upanishad', 'kena-upanishad', 'katha-upanishad', 'mundaka-upanishad',
          'prashna-upanishad', 'mandukya-upanishad', 'chandogya-upanishad', 'upanishads',
        ],
      },
    ],
  },
  {
    id: 'smriti',
    label: 'Smṛti',
    note: '"that which is remembered"',
    groups: [
      {
        id: 'itihasa',
        label: 'Itihāsa',
        note: 'the two great epics',
        textIds: ['ramayana', 'adhyatma-ramayanam', 'mahabharata', 'bhagavad-gita'],
      },
      {
        id: 'puranas',
        label: 'Purāṇas',
        note: '18 traditionally counted',
        textIds: ['puranas', 'devi-mahatmyam', 'srimad-bhagavatam'],
      },
      {
        id: 'stotra',
        label: 'Stotra',
        note: 'devotional hymns of praise',
        textIds: [
          'vishnu-sahasranama', 'soundarya-lahari', 'lalita-sahasranama',
          'hanuman-chalisa', 'narayaneeyam',
        ],
      },
    ],
  },
  {
    id: 'darshana',
    label: 'Darśana',
    note: 'philosophical systems',
    groups: [
      { id: 'yoga-vedanta', label: 'Yoga & Vedānta', note: '', textIds: ['yoga-sutras', 'vivekachudamani'] },
    ],
  },
];
