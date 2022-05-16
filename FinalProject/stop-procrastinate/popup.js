//events
document.querySelector("#but-actived").addEventListener("click", active);

let el = document.querySelectorAll("button");
for (i = 0; i < el.length; i++) {
    el[i].addEventListener("click", function(){
        hide(this.id);
    });
}

//initial values
chrome.storage.sync.get(['sites'], function(result){
    if (!result.sites){
        var site = ["facebook", "instagram"];
        chrome.storage.sync.set({sites: site});
    }  
    initialDisplay();
});

//initial display, before modifications
function initialDisplay(){
    //table
    chrome.storage.sync.get(['sites'], function(result){
        for (i in result.sites) {
            addLineTable(result.sites[i]);
        }
    });

    //div-default
    chrome.storage.sync.get(['activ'], function(result){
        styleActive(result.activ);
    });
}

function active(){
    chrome.storage.sync.get(['activ'], function(result){
        if(result.activ == false){
            chrome.storage.sync.set({activ: true});
            styleActive(true);
            chrome.action.setBadgeText({text: 'ON'});
            chrome.action.setBadgeBackgroundColor({color: 'red'});
        } else {
            chrome.storage.sync.set({activ: false});
            styleActive(false);
            chrome.action.setBadgeText({text: ''});
        }
    });
}

//changes the div-default style when the button is turned on or off 
function styleActive(activ){
    img = document.querySelector("#but-actived");
    pSites = document.querySelector("#p-sites");
    pActived = document.querySelector("#p-actived");
    pImg = document.querySelector("#p-img");

    if (activ == true){
        //style when turned on
        img.src = "images/on.png";
        pActived.textContent = "Click the button to turn off the extension";
        pSites.textContent = "Blocked sites";
        pImg.style.animation = "shadowOn 2.5s infinite";
    } else {
        //style when turned off
        img.src = "images/off.png";
        pActived.textContent = "Click the button to turn on the extension";
        pSites.textContent = "Sites to block";
        pImg.style.animation = "";
    }
}

//add a new site 
function add(event){
    event.preventDefault();//doesn't allow page to reload after form submission as default

    let form = document.querySelector("#form-add");
    formSite = form.site.value.toLowerCase();

    addLineTable(formSite);
    store(formSite, "add");

    form.reset();
}

//create a new line in the table
function addLineTable(site){
    let tr = document.createElement("tr");
    let td = document.createElement("td");
    let del = document.createElement("td");
    let edit = document.createElement("td");
    let imgDel = document.createElement("img");
    let imgEdit = document.createElement("img");
    
    td.textContent = site;
    td.className = "site";
    del.className = "delete";
    edit.className = "edit";

    imgDel.src = "images/delete.png";
    imgDel.style.height = "5vw";
    imgEdit.style.height = "5vw";
    imgEdit.src = "images/edit.png";

    tr.appendChild(td);
    del.appendChild(imgDel);
    edit.appendChild(imgEdit);
    tr.appendChild(del);
    tr.appendChild(edit);

    document.querySelector("#tab-sites").appendChild(tr);
}

//delete the sites
function delet(){
    let table = document.querySelectorAll(".delete");
    for (i = 0; i < table.length; i++) {
        table[i].addEventListener("click", function() {
            let tr = this.parentNode;
            var site = tr.children[0].textContent;
            
            //deleting from table
            this.parentNode.remove();

            store(site, "del");
        });
    }
}

//edit the sites
function edit(){
    //when edit button in clicked
    let table = document.querySelectorAll(".edit");
    for (i = 0; i < table.length; i++) {
        table[i].addEventListener("click", function() {
            editLine(this);
        });
    }

    //when clicking on the site you want to edit
    let el = document.querySelectorAll("td");
    for (i = 0; i < el.length; i++) {
        if(el[i].className == "site"){
            el[i].addEventListener("click", function(event){
                editLine(this);
            });
        }   
    }
}

function editLine(click){
    let tr = click.parentNode;
    var oldSite = tr.children[0].textContent;
    let td = tr.children[0];
    let input = document.createElement("input");

    input.type = "text";
    input.value = oldSite;
    td.textContent = "";
    td.appendChild(input);
    td.children[0].focus();

    //when enter is clicked (save)
    td.addEventListener("keypress", function(e){
        //enter is rated 13
        if(e.which == 13){
            //editing from table
            let newSite = this.children[0].value; //"this" refers to the td that contains the input in this scope
            this.textContent = newSite;

            store(oldSite, "edit", newSite);
        }
    });

    //when exiting the input without saving
    td.children[0].addEventListener("blur", function(){
        this.parentNode.textContent = oldSite;
    });
}

//changes the storage
function store(site, action, newSite){
    //get the sites in an array
    chrome.storage.sync.get(['sites'], function(result){
        var arrSites = [];
        for (i = 0; i < result.sites.length; i++){
            arrSites.push(result.sites[i]);
        }
    
        //add or delete the site, depending on specified action
        if(action == "add"){
            arrSites.push(site);
        } else{
            siteID = arrSites.indexOf(site);
            if(siteID > -1){//if the information is not found it returns -1
                if(action == "del"){
                    arrSites.splice(siteID, 1);
                } else if(action == "edit"){
                    arrSites.splice(siteID, 1, newSite);
                }
            }
        }

        //add the new array to storage
        chrome.storage.sync.set({sites: arrSites});
    });
}

//allows the add sites div and personalize sites div to appear and hide
function hide(butId){
    let divDefault = document.querySelector("#div-default");
    let divSites = document.querySelector("#div-sites");
    let divAdd = document.querySelector("#div-add");

    //appear add screen
    if(butId == "but-add"){
        divSites.style.display = 'none';
        divAdd.style.display = 'flex';
        divDefault.style.display = 'none';
    //appear initial screen (list)
    } else if(butId == "but-apply"){
        divSites.style.display = 'none';
        divAdd.style.display = 'none';
        divDefault.style.display = 'flex';
    //appear table screen
    //NAO VOLTA NA TELA CERTA QUANDO CLICAK EM BACK E NAO DELETA NEM EDITA O SITE RECEM ADICIONADO SE NAO TROCAR DE TELA ANTES
    } else if(butId == "but-default" || butId == "but-submit" || butId == "but-back"){
        if(butId == "but-submit"){
            add(event);
        }
        divSites.style.display = 'flex';
        divAdd.style.display = 'none';
        divDefault.style.display = 'none';
        delet();
        edit();
    }
}