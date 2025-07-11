import { writable } from 'svelte/store';
import { browser } from '$app/environment';

let initial = null;

if (browser) {
  try {
    const storedUser = localStorage.getItem('user');
    initial = storedUser ? JSON.parse(storedUser) : null;
  } catch (e) {
    console.error("Error reading localStorage:", e);
    initial = null;
  }
}

export const user = writable(initial);

if (browser) {
  user.subscribe((val) => {
    if (val) {
      localStorage.setItem('user', JSON.stringify(val));
    } else {
      localStorage.removeItem('user');
    }
  });
}
