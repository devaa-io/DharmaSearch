const RELOAD_GUARD = 'ds_sw_update_reload';

export function registerServiceWorker() {
  if (process.env.NODE_ENV !== 'production' || !('serviceWorker' in navigator)) return;

  window.addEventListener('load', async () => {
    const hadController = Boolean(navigator.serviceWorker.controller);
    try {
      const registration = await navigator.serviceWorker.register('/service-worker.js', {
        scope: '/',
        updateViaCache: 'none',
      });

      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (!hadController || sessionStorage.getItem(RELOAD_GUARD)) return;
        sessionStorage.setItem(RELOAD_GUARD, '1');
        window.location.reload();
      });

      await registration.update();
      sessionStorage.removeItem(RELOAD_GUARD);
    } catch (error) {
      // The reader remains fully usable online if registration is blocked.
      console.warn('Offline reader unavailable:', error);
    }
  });
}
