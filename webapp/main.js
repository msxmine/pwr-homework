import {auth, authop} from "./firebase.js"
import {setDBUser, setDBShop, addShopsListener} from "./database.js"
import {createStatsOnShopChange} from "./statspure.js"
import {createProductsOnShopChange} from "./mainpure.js"
import {createWorkersOnShopChange} from "./workerspure.js"

let shopDm = null;
let shopCreateFun = createProductsOnShopChange;

function createShopOption(textval, dataval){
    var optionlist = document.getElementById("shop-option-list");
    var newcontainer = document.createElement("li");
    newcontainer.classList = ["mdc-deprecated-list-item"]
    newcontainer.setAttribute("role", "option");
    var newcontripple = document.createElement("span");
    newcontripple.classList = ["mdc-deprecated-list-item__ripple"];
    newcontainer.appendChild(newcontripple);
    var newcontcontent = document.createElement("span");
    newcontcontent.classList = ["mdc-deprecated-list-item__text"];
    newcontcontent.textContent = textval;
    newcontainer.setAttribute("data-value", dataval);
    newcontainer.setAttribute("role", "option");
    newcontainer.setAttribute("aria-selected", "false");
    newcontainer.appendChild(newcontcontent);
    optionlist.appendChild(newcontainer);
}

function updateShops(shoplist){
    for (let sop in shoplist){
        createShopOption(shoplist[sop].fname, sop);
    }
    shopDm.layoutOptions();
}

function shopSelect(){
    const MDCSelect = mdc.select.MDCSelect;
    shopDm = new MDCSelect(document.getElementById("bar-dropdown-shopid"))

}

function createPage(){

    shopSelect()

    addShopsListener((shopsobj) => {
        updateShops(shopsobj);

        let setto = 0;
        let lastid = sessionStorage.getItem("LastShop")
        if (lastid != null){
            if (lastid in shopsobj){
                setto = shopsobj[lastid].idx
            }
        }

        shopDm.listen("MDCSelect:change", (ev) => {
            setDBShop(ev.detail.value)
            sessionStorage.setItem("LastShop", ev.detail.value)
            shopCreateFun();
        })

        shopDm.selectedIndex = setto;
    })

}


document.getElementById("logoutbutton").addEventListener("click", () => {
    auth.signOut();
});

document.getElementById("productslink").addEventListener("click", () => {
    shopCreateFun = createProductsOnShopChange;
    shopCreateFun();
});

document.getElementById("statslink").addEventListener("click", () => {
    shopCreateFun = createStatsOnShopChange;
    shopCreateFun();
});

document.getElementById("workerslink").addEventListener("click", () => {
    shopCreateFun = createWorkersOnShopChange;
    shopCreateFun();
});

authop.onAuthStateChanged(auth, (user) => {
    if (user) {
        setDBUser(user);
        createPage()
    } else {
        window.location = "test.html";
    }
})