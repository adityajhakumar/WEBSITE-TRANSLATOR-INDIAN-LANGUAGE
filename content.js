chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action == "translate") {
      var language = request.language;
      // Implement translation logic here
      console.log("Translating to", language);
      // For demonstration, let's just log the selected language
    }
  });
  