function setcookie(cname, cval){
    browser.tabs.query({"active": true, "currentWindow": true}).then(actabs => {
        let activeurl = actabs[0].url
        if (activeurl != undefined){
            browser.cookies.set({
                "url": activeurl,
                "name": cname,
                "value": cval
            })
        }
    })
}

function display(datajson){
    let corg = document.getElementById("maincontainer")
    let ccopy = corg.cloneNode(false)
    corg.parentNode.replaceChild(ccopy, corg)
    let container = ccopy
    for (let host in datajson){
        let newhostentry = document.createElement("div")
        container.appendChild(newhostentry)
        let hostnamecontainer = document.createElement("h2")
        let hostname = document.createTextNode(host)
        newhostentry.appendChild(hostnamecontainer)
        hostnamecontainer.appendChild(hostname)
        for (let cookie in datajson[host]){
            let newcookieentry = document.createElement("div")
            newcookieentry.className = "cookieentry"
            newhostentry.appendChild(newcookieentry)
            let cookiename = document.createTextNode(cookie + " : " + datajson[host][cookie])
            newcookieentry.appendChild(cookiename)
            newcookieentry.onclick = function() {setcookie(cookie, datajson[host][cookie])}
        }
    }
}

fetch("http://localhost:5555").then(response => response.json()).then(data => display(data))