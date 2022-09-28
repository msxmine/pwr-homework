import {addProductsListener} from "./database.js"
import {initDialog, clearDialog, openDialog} from "./dialog.js"
import {initList, populateProductList} from "./list.js"

let initdone = false;

function createProductsOnShopChange(){
    document.getElementById("pagetitle").textContent = "Produkty";
    let allpanes = document.getElementsByClassName("contentpanel")
    for (let pane of allpanes){
        pane.style["display"] = "none";
    }
    let mypane = document.getElementById("productscontent");
    mypane.style["display"] = "";

    if (!initdone){
        initDialog();
        initList();
        document.getElementById("addproductbutton").addEventListener("click", () => {
            document.getElementById("productdeletionbutton").style = "display: none;"
            clearDialog();
            openDialog();
        });
        initdone = true;
    }
    addProductsListener((snapshot) => {
        const data = snapshot.val();
        window.gotdbdata = data;
        populateProductList(data);
    })

}

export {createProductsOnShopChange}


