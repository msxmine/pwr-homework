import {authop, auth} from "./firebase.js"

let loginbutton = document.getElementById("loginbutton")
let loginstatus = document.getElementById("login-info")
let presetbutton = document.getElementById("presetbutton")

function attemptlogin(){
    authop.signInWithEmailAndPassword(auth, emailfield.value, passwordfield.value).then(
        (userCredentials) => {
            window.location = "main.html"
        }
    ).catch(
        (error) => {
            loginstatus.textContent = "Blad logowania"
        }
    )
}

function resetpassword(){
    authop.sendPasswordResetEmail(auth, emailfield.value).then(() => {
        loginstatus.textContent = "Wysłano e-mail odzyskujący"
    }).catch((error) => {
        loginstatus.textContent = "Nie można było zresetować hasła dla tego emaila"
    })
}

loginbutton.addEventListener("click", attemptlogin)
presetbutton.addEventListener("click", resetpassword)

