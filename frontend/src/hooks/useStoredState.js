import { useCallback, useState } from 'react';

function readStoredValue(key, fallback) {
  try {
    const value = window.localStorage.getItem(key);
    return value === null ? fallback : JSON.parse(value);
  } catch {
    return fallback;
  }
}

export function useStoredState(key, fallback) {
  const [value, setValue] = useState(() => readStoredValue(key, fallback));

  const updateValue = useCallback(nextValue => {
    setValue(currentValue => {
      const resolved = typeof nextValue === 'function' ? nextValue(currentValue) : nextValue;
      try {
        window.localStorage.setItem(key, JSON.stringify(resolved));
      } catch {
        // Reading remains usable when storage is blocked or full.
      }
      return resolved;
    });
  }, [key]);

  return [value, updateValue];
}
