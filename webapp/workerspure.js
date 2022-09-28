import {addWorkersListener, addWorker} from "./database.js"
import {populateWorkersList, initList} from "./workerslist.js"

let initdone = false;
let namefield = null;
let emailfield = null;
let passfield = null;

function createWorkersOnShopChange(){
    document.getElementById("pagetitle").textContent = "Pracownicy";
    let allpanes = document.getElementsByClassName("contentpanel")
    for (let pane of allpanes){
        pane.style["display"] = "none";
    }
    let mypane = document.getElementById("workerscontent");
    mypane.style["display"] = "";


    if (!initdone){
        const MDCTextField = mdc.textField.MDCTextField;
        namefield = new MDCTextField(document.getElementById("workernameentry"))
        emailfield = new MDCTextField(document.getElementById("workeremailentry"))
        passfield = new MDCTextField(document.getElementById("workerpasswordentry"))
        initList();
        document.getElementById("workeraddbutton").addEventListener("click", () => {
            if (!passfield.valid){
                alert("Hasło musi zawierać małą i dużą literę, cyfrę, znak specjalny i mieć długość >= 8");
            } else {
                addWorker(namefield.value, emailfield.value, passfield.value)
                emailfield.value = "";
                namefield.value = "";
                passfield.value = "";
            }
        });
        initdone = true;
    }

    addWorkersListener((snapshot) => {
        const data = snapshot.val();
        populateWorkersList(data);
    })



}

export {createWorkersOnShopChange}


