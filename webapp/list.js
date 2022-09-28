import {bindDialog, openDialog} from "./dialog.js"

let productList = null;
let boundProducts = []

function initList(){
    const MDCList = mdc.list.MDCList;
    productList = new MDCList(document.getElementById("productlist"))
    productList.listen("MDCList:action", (ev) => {
        bindDialog(boundProducts[ev.detail.index]);
        document.getElementById("productdeletionbutton").style = ""
        openDialog();
    })
}

function createListElement(uptext, lowtext){
    var plist = document.getElementById("productlist")
    var itemcontainer = document.createElement('li')
    itemcontainer.classList = ["mdc-list-item"]
    var rip = document.createElement("span")
    rip.classList = ["mdc-list-item__ripple"]
    itemcontainer.appendChild(rip)
    var text = document.createElement("span")
    text.classList = ["mdc-list-item__text"]
    itemcontainer.appendChild(text)
    var firstline = document.createElement("span")
    firstline.classList = ["mdc-list-item__primary-text"]
    text.appendChild(firstline)
    var secondline = document.createElement("span")
    secondline.classList = ["mdc-list-item__secondary-text"]
    text.appendChild(secondline)
    firstline.textContent = (uptext == undefined ? "<NO_NAME>" : uptext)
    secondline.textContent = (lowtext == undefined ? "<NO_CODE>" : lowtext)
    plist.appendChild(itemcontainer)
}

function populateProductList(products){
    let listnode = document.getElementById("productlist")
    listnode.innerHTML = "";
    boundProducts = []
    for (let prdcode in products){
        let product = products[prdcode]
        boundProducts.push(product);
        createListElement(product.name, product.barcode)
    }
}

export {initList, populateProductList}
