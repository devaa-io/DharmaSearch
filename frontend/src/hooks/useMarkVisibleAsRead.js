import { useCallback, useEffect, useRef } from 'react';

/** Marks a verse read once it has genuinely been on screen, rather than asking
 *  the reader to confirm something they have plainly just read.
 *
 *  Returns a ref callback to put on each verse element; the element needs a
 *  data-verse-id attribute.
 *
 *  Half the element on screen counts as a read rather than a glance. A verse
 *  with six scripts and a translation can be taller than a phone screen though,
 *  and such an element can never reach half visibility, so filling most of the
 *  viewport counts too. Without that second test the longest verses would be
 *  the ones that never registered.
 */
export function useMarkVisibleAsRead(onSeen) {
  const observerRef = useRef(null);
  const seenRef = useRef(new Set());

  const attach = useCallback(node => {
    if (!node || typeof IntersectionObserver === 'undefined') return;
    if (!observerRef.current) {
      observerRef.current = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          const id = entry.target.dataset.verseId;
          if (!id || seenRef.current.has(id) || !entry.isIntersecting) return;
          const fillsViewport = entry.intersectionRect.height
            >= (window.innerHeight || 0) * 0.6;
          if (entry.intersectionRatio >= 0.5 || fillsViewport) {
            seenRef.current.add(id);
            onSeen(id);
          }
        });
      }, { threshold: [0.25, 0.5, 0.75] });
    }
    observerRef.current.observe(node);
  }, [onSeen]);

  useEffect(() => () => observerRef.current?.disconnect(), []);
  return attach;
}
