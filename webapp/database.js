import {database, dbop, usercrauth, authop} from "./firebase.js"

let curUser = null;
let modemail = "";
let curShop = ""
let shopsListRef = null;
let prodRef = null;
let salesRef = null;
let workersRef = null;

function setDBUser(user){
    curUser = user;
    modemail = curUser.email
    modemail = modemail.replaceAll(".", "%")
}

function setDBShop(shopid){
    curShop = shopid;
}

function updateDB(productobj){
    if (productobj.barcode != undefined && productobj.barcode.length > 0){
        if (curShop.length > 0){
            let prodRef = dbop.ref(database, curShop + "/products/" + productobj.barcode);
            dbop.set(prodRef, productobj);
        }
    }
}

function deleteProduct(barcode){
    if (barcode != undefined && barcode.length > 0){
        if (curShop.length > 0){
            let prodRef = dbop.ref(database, curShop + "/products/" + barcode);
            dbop.set(prodRef, null);
        }
    } 
}

function addShopsListener(callb){
    if (shopsListRef != null){
        dbop.off(shopsListRef);
    }
    shopsListRef = dbop.ref(database, "owners/" + modemail)
    dbop.onValue(shopsListRef, (snapshot) => {
        const data = snapshot.val();
        const shops = {}
        let prmss = []
        let i = 0;
        for (let shid in data){
            let shopref = dbop.ref(database, shid + "/name");
            prmss.push(dbop.get(shopref).then((snap) => {
                shops[shid] = {}
                shops[shid].fname = snap.val();
                shops[shid].uid = shid;
                shops[shid].idx = i;
                i = i+1;
            }))
        }
        Promise.all(prmss).then(() => {
            callb(shops);
        })
    });
}

function addProductsListener(callb){
    if (prodRef != null){
        dbop.off(prodRef);
    }
    prodRef = dbop.ref(database, curShop + "/products");
    dbop.onValue(prodRef, callb);
}

function addSalesListener(callb){
    if (salesRef != null){
        dbop.off(salesRef);
    }
    salesRef = dbop.ref(database, curShop + "/sales");
    dbop.onValue(salesRef, callb);
}

function addWorkersListener(callb){
    if (workersRef != null){
        dbop.off(workersRef);
    }
    workersRef = dbop.ref(database, "workers/" + curShop);
    dbop.onValue(workersRef, callb);
}

function addWorker(name, email, pass){
    let emailsat = email.replaceAll(".", "%");
    let workerref = dbop.ref(database, "workers/" + curShop + "/" + emailsat);
    let workerref2 = dbop.ref(database, "workers_emails/" + emailsat);
    authop.createUserWithEmailAndPassword(usercrauth, email, pass)
    dbop.set(workerref, name);
    dbop.set(workerref2, curShop);
    
}

function removeWorker(email){
    let emailsat = email.replaceAll(".", "%");
    let workerref = dbop.ref(database, "workers/" + curShop + "/" + emailsat);
    let workerref2 = dbop.ref(database, "workers_emails/" + emailsat);
    dbop.set(workerref, null);
    dbop.set(workerref2, null);
}

export {setDBUser, setDBShop, updateDB, deleteProduct, addProductsListener, addShopsListener, addSalesListener,
        addWorkersListener, addWorker, removeWorker}
