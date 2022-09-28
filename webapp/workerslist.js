import {removeWorker} from "./database.js"

let workersList = null;

function initList(){
    const MDCList = mdc.list.MDCList;
    workersList = new MDCList(document.getElementById("workerslist"))
}

function createListElement(uptext, lowtext, emailid){
    var plist = document.getElementById("workerslist")
    var itemcontainer = document.createElement('li')
    itemcontainer.classList = ["mdc-deprecated-list-item"]
    var rip = document.createElement("span")
    rip.classList = ["mdc-deprecated-list-item__ripple"]
    itemcontainer.appendChild(rip)
    var avat = document.createElement("span")
    avat.classList = ["mdclist-avatar material-icons"]
    avat.textContent = "account_circle"
    itemcontainer.appendChild(avat)
    var text = document.createElement("span")
    text.classList = ["mdc-deprecated-list-item__text"]
    itemcontainer.appendChild(text)
    var firstline = document.createElement("span")
    firstline.classList = ["mdc-deprecated-list-item__primary-text"]
    text.appendChild(firstline)
    var secondline = document.createElement("span")
    secondline.classList = ["mdc-deprecated-list-item__secondary-text"]
    text.appendChild(secondline)
    firstline.textContent = (uptext == undefined ? "<NO_NAME>" : uptext)
    secondline.textContent = (lowtext == undefined ? "<NO_CODE>" : lowtext)
    var endsect = document.createElement("span");
    endsect.classList = ["mdc-deprecated-list-item__meta"]
    var endbut = document.createElement("button")
    endbut.classList = ["mdc-icon-button material-icons"]
    endbut.addEventListener("click", () => {
        removeWorker(emailid);
    })
    var endbutrippl = document.createElement("div");
    endbutrippl.classList = ["mdc-icon-button__ripple"]
    endbut.appendChild(endbutrippl);
    var endbuticon = document.createTextNode("delete");
    endbut.appendChild(endbuticon);
    endsect.appendChild(endbut);
    itemcontainer.appendChild(endsect);
    plist.appendChild(itemcontainer)
}

function populateWorkersList(workers){
    let listnode = document.getElementById("workerslist")
    listnode.innerHTML = "";
    window.workdbg = workers;
    for (let wrkmail in workers){
        let wrkname = workers[wrkmail]
        createListElement(wrkname, wrkmail.replaceAll("%", "."), wrkmail)
    }
}

export {initList, populateWorkersList}
