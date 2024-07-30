import { writable } from 'svelte/store';

function createWritableWithLocalStorage<T>(key: string, startValue: T) {
  const isBrowser = typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  const storedValue = isBrowser ? localStorage.getItem(key) : null;
  const value: T = storedValue ? JSON.parse(storedValue) : startValue;
  const { subscribe, set } = writable(value);

  return {
    subscribe,
    set: (value: T) => {
      if (isBrowser) {
        localStorage.setItem(key, JSON.stringify(value));
      }
      set(value);
    },
    update: (fn: (value: T) => T) => {
      const updatedValue = fn(value);
      if (isBrowser) {
        localStorage.setItem(key, JSON.stringify(updatedValue));
      }
      set(updatedValue);
    },
    useLocalStorage: () => {
      if (isBrowser) {
        const storedValue = localStorage.getItem(key);
        if (storedValue) {
          set(JSON.parse(storedValue));
        }
      }
    }
  };
}

export const isAuthenticated = createWritableWithLocalStorage<boolean>('isAuthenticated', false);
export const userRole = createWritableWithLocalStorage<string>('userRole', 'guest');
export const usuario = createWritableWithLocalStorage<string>('usuario', '');
