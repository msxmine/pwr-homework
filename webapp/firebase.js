import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.5.0/firebase-app.js'
import { getAuth, setPersistence, createUserWithEmailAndPassword, signInWithEmailAndPassword, onAuthStateChanged, sendPasswordResetEmail } from 'https://www.gstatic.com/firebasejs/9.5.0/firebase-auth.js'
import { getDatabase, ref, set, child, get, onValue, update, push, remove, off, runTransaction } from 'https://www.gstatic.com/firebasejs/9.5.0/firebase-database.js'

const firebaseConfig = {
    apiKey: "deadbeef",
    authDomain: "deadbeef",
    databaseURL: "deadbeef",
    projectId: "deadbeef",
    storageBucket: "deadbeef",
    messagingSenderId: "deadbeef",
    appId: "deadbeef"
};

let app = initializeApp(firebaseConfig)
let usercrapp = initializeApp(firebaseConfig, "auth-worker")
let auth = getAuth()
let usercrauth = getAuth(usercrapp)
let database = getDatabase(app)

let authop = {
    signInWithEmailAndPassword: signInWithEmailAndPassword,
    onAuthStateChanged: onAuthStateChanged,
    sendPasswordResetEmail: sendPasswordResetEmail,
    createUserWithEmailAndPassword: createUserWithEmailAndPassword
}

let dbop = {
    ref: ref,
    set: set,
    child: child,
    get: get,
    onValue: onValue,
    update: update,
    push: push,
    remove: remove,
    off: off,
    runTransaction: runTransaction
}

export {app, auth, database, authop, dbop, usercrapp, usercrauth}
