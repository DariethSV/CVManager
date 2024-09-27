

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'open_popup') {
        chrome.storage.local.set({ form_detected: true });
        chrome.action.openPopup();

    }
});
