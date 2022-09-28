posz = 0.9
//Przygotuj fraktale
calcfractals()
fillBufs()
updateOffsets()
//Sledzenie stanu klawiszy
var apressed = false
var wpressed = false
var spressed = false
var dpressed = false
var qpressed = false
var epressed = false
//Event listener do klawiszy
canvas = document.getElementById("my_canvas");
canvas.addEventListener("keydown", event => {
    if (event.keyCode === 65){apressed = true;}
    if (event.keyCode === 87){wpressed = true;}
    if (event.keyCode === 83){spressed = true;}
    if (event.keyCode === 68){dpressed = true;}
    if (event.keyCode === 81){qpressed = true;}
    if (event.keyCode === 69){epressed = true;}
}, false);
canvas.addEventListener("keyup", event => {
    if (event.keyCode === 65){apressed = false;}
    if (event.keyCode === 87){wpressed = false;}
    if (event.keyCode === 83){spressed = false;}
    if (event.keyCode === 68){dpressed = false;}
    if (event.keyCode === 81){qpressed = false;}
    if (event.keyCode === 69){epressed = false;}
}, false);
//Określ najbliższą warstwe i zaktualizuj parametry shadera (przesuniecie)
function movefrontlayer(deltax, deltay){
    layer_idx = Math.ceil(-posz)
    layer_offsets[2*layer_idx] += deltax
    layer_offsets[(2*layer_idx)+1] += deltay
}

//Sledzenie akcji uzytkownika i renderowanie
var last_time = 0;
function update(time){
    var deltat = time - last_time;
    last_time = time;
    
    
    if (wpressed){
        posz -= 0.0009*deltat;
    }
    if (spressed){
        posz += 0.0009*deltat;
    }
    if (dpressed){
        movefrontlayer(0.00009*deltat, 0);
        updateOffsets()
    }
    if (apressed){
        movefrontlayer(-0.00009*deltat, 0);
        updateOffsets()
    }
    if (qpressed){
        movefrontlayer(0, 0.00009*deltat);
        updateOffsets()
    }
    if (epressed){
        movefrontlayer(0, -0.00009*deltat);
        updateOffsets()
    }


    
    draw();
    window.requestAnimationFrame(update);
}

update(0)
