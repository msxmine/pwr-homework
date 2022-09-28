form = document.getElementsByTagName("form")[0]
form.addEventListener("submit", function(e){
    anum = document.getElementById("recvaccnum").value
    browser.storage.local.set({
        "-1": anum
    })
    var customStyles = document.createElement('style')
    customStyles.appendChild(document.createTextNode(
        "form {visibility: hidden;}"
    ));
    document.documentElement.appendChild(customStyles)
    document.getElementById("recvaccnum").value = "123456789"
})
