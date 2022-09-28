import {addSalesListener} from "./database.js"
import {drawCharts} from "./charts.js"

function createStatsOnShopChange(){
    document.getElementById("pagetitle").textContent = "Statystyki";
    let allpanes = document.getElementsByClassName("contentpanel")
    for (let pane of allpanes){
        pane.style["display"] = "none";
    }
    let mypane = document.getElementById("statscontent");
    mypane.style["display"] = "";

    addSalesListener((snapshot) => {
        const data = snapshot.val();
        drawCharts(data);
    })
}

export {createStatsOnShopChange}
