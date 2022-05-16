//set the button in "idle mode" initially
chrome.runtime.onInstalled.addListener(function(){
  chrome.storage.sync.set({activ: false});
})

//function to check if the current tab is part of the list of sites
function match(url, tabId){
  chrome.storage.sync.get(['sites'], function(result){
    for (i in result.sites){
      if (url.includes(result.sites[i])) {
        //if true, run the script that displays an alert
        chrome.scripting.executeScript({
          target: {tabId: tabId},
          function: message
        });
        break;
      }
    }
  });
}

function message() {
    alert("Stop Procrastinating, do something more productive!\n To stop these messages, disable the extension.");
}

//when current tab is updated
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  //get the button mode
  chrome.storage.sync.get(['activ'], function(result) {
    //if its active and tab has a url, call match function
    if (result.activ == true && changeInfo.url != undefined) {
      match(changeInfo.url, tabId);
    }
  });
}); 

//when a tab is activated
chrome.tabs.onActivated.addListener(function() {
  chrome.storage.sync.get(['activ'], function(result) {
    //if the button is active, call match function
    if (result.activ == true){
      //this time is to avoid a devtool bug
      setTimeout(function() {
        chrome.tabs.query({"active": true, "lastFocusedWindow": true}, function (tabs) {
          tabURL = tabs[0].url;
          tabID = tabs[0].id;
          match(tabURL, tabID);
        });
      }, 500);
    } 
  });
});