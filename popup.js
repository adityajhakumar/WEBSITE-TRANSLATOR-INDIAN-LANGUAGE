document.addEventListener('DOMContentLoaded', function() {
    var languageSelector = document.getElementById('languageSelector');
  
    languageSelector.addEventListener('change', function() {
      var selectedLanguage = languageSelector.value;
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var currentTab = tabs[0];
        var currentUrl = encodeURIComponent(currentTab.url);
        var googleTranslateUrl = 'https://translate.google.com/translate?sl=auto&tl=' + selectedLanguage + '&u=' + currentUrl;
  
        // Open the translated URL in the current tab
        chrome.tabs.update(currentTab.id, {url: googleTranslateUrl});
      });
    });
  });
  