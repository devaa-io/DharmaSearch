import React from 'react';
import { Download, X } from 'lucide-react';
import { useInstallPrompt } from '../../hooks/useInstallPrompt';

export function InstallBanner() {
  const { canInstall, promptInstall, dismiss } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <div className="install-banner" role="complementary" aria-label="Install DharmaSearch">
      <p>
        <strong>Install DharmaSearch</strong>
        Read offline, straight from your home screen.
      </p>
      <button className="library-button" type="button" onClick={promptInstall} data-testid="install-app">
        <Download aria-hidden="true" /> Install
      </button>
      <button
        className="install-banner__dismiss"
        type="button"
        onClick={dismiss}
        aria-label="Dismiss install prompt"
        data-testid="install-dismiss"
      >
        <X aria-hidden="true" />
      </button>
    </div>
  );
}
