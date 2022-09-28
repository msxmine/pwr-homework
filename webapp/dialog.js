import {updateDB, deleteProduct} from "./database.js"
import {categories} from "./values.js"

let barcodeIn = null;
let nameIn = null;
let categoryDm = null;
let shelfIn = null;
let warehouseIn = null;
let expiryIn = null;
let priceIn = null;
let salePriceIn = null;
let saleIn = null;
let editPopup = null;
let deleteConfirmation = null;

function createDropdownOption(textval){
    var optionlist = document.getElementById("category-option-list");
    var newcontainer = document.createElement("li");
    newcontainer.classList = ["mdc-deprecated-list-item"]
    newcontainer.setAttribute("role", "option");
    var newcontripple = document.createElement("span");
    newcontripple.classList = ["mdc-deprecated-list-item__ripple"];
    newcontainer.appendChild(newcontripple);
    var newcontcontent = document.createElement("span");
    newcontcontent.classList = ["mdc-deprecated-list-item__text"];
    newcontcontent.textContent = textval;
    newcontainer.setAttribute("data-value", textval);
    newcontainer.setAttribute("role", "option");
    newcontainer.setAttribute("aria-selected", "false");
    newcontainer.appendChild(newcontcontent);
    optionlist.appendChild(newcontainer);
}

function initDropdown(){
    for (let opt of categories){
        createDropdownOption(opt);
    }
}

function initDialog(){
    const MDCDialog = mdc.dialog.MDCDialog;
    const MDCTextField = mdc.textField.MDCTextField;
    const MDCSelect = mdc.select.MDCSelect;

    initDropdown();
    
    editPopup = new MDCDialog(document.getElementById("producteditdialog"));
    deleteConfirmation = new MDCDialog(document.getElementById("deleteconfirmdialog"));
    barcodeIn = new MDCTextField(document.getElementById("dialog-input-barcode"));
    nameIn = new MDCTextField(document.getElementById("dialog-input-name"));
    categoryDm = new MDCSelect(document.getElementById("dialog-dropdown-category"))
    shelfIn = new MDCTextField(document.getElementById("dialog-input-shelf"));
    warehouseIn = new MDCTextField(document.getElementById("dialog-input-warehouse"));
    expiryIn = document.getElementById("dialog-input-expiry");
    priceIn = new MDCTextField(document.getElementById("dialog-input-price"));
    salePriceIn = new MDCTextField(document.getElementById("dialog-input-saleprice"));
    saleIn = document.getElementById("dialog-checkbox-sale-form");



    editPopup.listen("MDCDialog:closed", (ev) => {
        if (ev.detail.action == "ok"){
            let x = {}
            getDialogContent(x);
            updateDB(x);
        }
        if (ev.detail.action == "delete"){
            let deleteHandler = function(ev){
                if (ev.detail.action == "discard"){
                    let x = {}
                    getDialogContent(x);
                    deleteProduct(x.barcode);
                }
                deleteConfirmation.unlisten("MDCDialog:closed", deleteHandler);
            }
            deleteConfirmation.listen("MDCDialog:closed", deleteHandler);
            deleteConfirmation.open()
        }
    })
}

function bindDialog(product){
    barcodeIn.value = product.barcode;
    barcodeIn.disabled = true;
    nameIn.value = (product.name == undefined ? "" : product.name);
    categoryDm.selectedIndex = (product.category == undefined ? 0 : product.category+1);
    shelfIn.value = (product.amountStore == undefined ? "" : product.amountStore);
    warehouseIn.value = (product.amountWarehouse == undefined ? "" : product.amountWarehouse);
    expiryIn.valueAsDate = (product.expiryDate == undefined ? new Date() : new Date(product.expiryDate));
    priceIn.value = (product.price == undefined ? "" : product.price.toFixed(2));
    salePriceIn.value = (product.priceOnSale == undefined ? "" : product.priceOnSale.toFixed(2));
    saleIn.checked = (product.onSale == undefined ? false : product.onSale);
}

function clearDialog(){
    barcodeIn.value = "";
    barcodeIn.disabled = false;
    nameIn.value = "";
    categoryDm.selectedIndex = 0;
    shelfIn.value = "";
    warehouseIn.value = "";
    expiryIn.valueAsDate = new Date();
    priceIn.value = "";
    salePriceIn.value = "";
    saleIn.checked = false;
}

function getDialogContent(productres){
    if(barcodeIn.value != ""){productres.barcode = barcodeIn.value}
    if(nameIn.value != ""){productres.name = nameIn.value;}
    if(categoryDm.selectedIndex != 0){productres.category = categoryDm.selectedIndex-1;}
    if(!isNaN(parseInt(shelfIn.value))){productres.amountStore = parseInt(shelfIn.value);}
    if(!isNaN(parseInt(warehouseIn.value))){productres.amountWarehouse = parseInt(warehouseIn.value);}
    productres.expiryDate = expiryIn.valueAsDate.valueOf()
    if(!isNaN(parseFloat(priceIn.value))){productres.price = parseFloat(priceIn.value);}
    if(!isNaN(parseFloat(salePriceIn.value))){productres.priceOnSale = parseFloat(salePriceIn.value);}
    productres.onSale = saleIn.checked;
}

function openDialog(){
    editPopup.open();
}

export {initDialog, bindDialog, clearDialog, getDialogContent, openDialog}
