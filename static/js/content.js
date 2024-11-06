const form = document.querySelector('form');

if (form) {
    // Enviar un mensaje al service worker para abrir el popup
    chrome.runtime.sendMessage({ action: 'open_popup' });
}