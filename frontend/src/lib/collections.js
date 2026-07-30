/** Themed collections — entering the library by need rather than by text.
 *
 *  Most people do not arrive wanting "chapter 12". They arrive anxious, or
 *  grieving, or unable to start something. These are short sets (about five
 *  verses) that meet that, chosen by hand: the corpus has no keyword data, and
 *  picking verses for grief is not a job for a substring match.
 *
 *  Every id below must be a real verse in app_data.json. Keep the sets short —
 *  the point is a complete reading in about two minutes.
 */
export const COLLECTIONS = [
  {
    id: 'anxious',
    title: 'When you are anxious',
    need: 'Racing thoughts, dread about what comes next',
    why: 'The Gita spends much of its length on a man too overwhelmed to act. These are the answers he is given.',
    verses: ['bg-2-47', 'bg-2-14', 'bg-6-5', 'bg-2-70', 'bg-18-66'],
  },
  {
    id: 'starting',
    title: 'When you cannot start',
    need: 'Paralysed, procrastinating, the task feels too large',
    why: 'Arjuna puts down his bow and refuses to move. Krishna does not comfort him — he argues him back into action.',
    verses: ['bg-2-3', 'bg-3-8', 'bg-2-31', 'bg-6-6', 'bg-3-35'],
  },
  {
    id: 'grief',
    title: 'When you have lost someone',
    need: 'Grief, mourning, the fear of death',
    why: 'The Gita opens on a battlefield where the enemy is family. Its first real subject is what survives loss.',
    verses: ['bg-2-13', 'bg-2-20', 'bg-2-22', 'bg-2-27', 'katha-up-2-18'],
  },
  {
    id: 'stillness',
    title: 'Before sleep',
    need: 'Winding down, quieting the mind',
    why: 'Older and quieter than the Gita, the Upanishads are less argument than description of something already still.',
    verses: ['isha-up-1', 'mandukya-up-2', 'katha-up-2-20', 'mundaka-up-5-1', 'isha-up-6'],
  },
  {
    id: 'work',
    title: 'On doing the work',
    need: 'Effort without obsessing over the result',
    why: 'The teaching the Gita is best known for: act fully, then let go of your grip on how it turns out.',
    verses: ['bg-2-47', 'bg-3-19', 'bg-4-20', 'bg-18-9', 'bg-12-12'],
  },
  {
    id: 'who-am-i',
    title: 'What am I, really',
    need: 'The big question, asked plainly',
    why: 'The Upanishads circle one question for centuries, each time getting closer to something that cannot quite be said.',
    verses: ['mandukya-up-7', 'katha-up-1-20', 'kena-up-1-3', 'mundaka-up-5-1', 'isha-up-7'],
  },
];

/** Resolve a collection's ids to verse objects, silently dropping any that are
 *  missing so a bad id degrades to a shorter set rather than a crash. */
export function versesForCollection(collection, versesById) {
  return collection.verses.map(id => versesById[id]).filter(Boolean);
}
