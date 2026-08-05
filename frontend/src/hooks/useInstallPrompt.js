import { useCallback, useEffect, useState } from 'react';
import { useStoredState } from './useStoredState';

function isStandalone() {
  return typeof window !== 'undefined'
    && (window.matchMedia?.('(display-mode: standalone)').matches
      || window.navigator.standalone === true);
}

/** Chrome/Android fire beforeinstallprompt when the app is installable and not
 *  already installed; iOS Safari never fires it, so the banner simply never
 *  appears there rather than showing a broken "Install" button. */
export function useInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [dismissed, setDismissed] = useStoredState('ds_install_dismissed', false);
  const [installed, setInstalled] = useState(isStandalone);

  useEffect(() => {
    const onBeforeInstall = event => {
      event.preventDefault();
      setDeferredPrompt(event);
    };
    const onInstalled = () => {
      setInstalled(true);
      setDeferredPrompt(null);
    };
    window.addEventListener('beforeinstallprompt', onBeforeInstall);
    window.addEventListener('appinstalled', onInstalled);
    return () => {
      window.removeEventListener('beforeinstallprompt', onBeforeInstall);
      window.removeEventListener('appinstalled', onInstalled);
    };
  }, []);

  const promptInstall = useCallback(async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice.catch(() => {});
    setDeferredPrompt(null);
  }, [deferredPrompt]);

  const dismiss = useCallback(() => setDismissed(true), [setDismissed]);

  const isMobile = typeof window !== 'undefined'
    && window.matchMedia?.('(pointer: coarse)').matches;

  return {
    canInstall: Boolean(deferredPrompt) && !installed && !dismissed && isMobile,
    promptInstall,
    dismiss,
  };
}
