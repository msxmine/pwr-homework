vertices = []
geometry = []
posz = -2
posx = -0.5

var apressed = false
var wpressed = false
var spressed = false
var dpressed = false

function start(){
    vertices = []
    geometry = []
    posz = -2
    posx = -0.5
    for (i = 0; i < 4; i++){
        var zstart = Math.random()
        var xstart = Math.random()
        var sidx = vertices.length/3;
        vertices.push(xstart, 0, zstart, xstart+0.1, 0, zstart, xstart+0.1, 0, zstart+0.1, xstart, 0, zstart+0.1, xstart, 1, zstart, xstart+0.1, 1, zstart, xstart+0.1, 1, zstart+0.1, xstart, 1, zstart+0.1);
        geometry.push(sidx, sidx+1, sidx+1, sidx+2, sidx+2, sidx+3, sidx+3, sidx, sidx, sidx+4, sidx+1, sidx+5, sidx+2, sidx+6, sidx+3, sidx+7, sidx+4, sidx+5, sidx+5, sidx+6, sidx+6, sidx+7, sidx+7, sidx+4);
    }
    
    updateBufs();
    
    canvas = document.getElementById("my_canvas");
    canvas.addEventListener("keydown", event => {
        if (event.keyCode === 65){apressed = true;}
        if (event.keyCode === 87){wpressed = true;}
        if (event.keyCode === 83){spressed = true;}
        if (event.keyCode === 68){dpressed = true;}
    }, false);
    canvas.addEventListener("keyup", event => {
        if (event.keyCode === 65){apressed = false;}
        if (event.keyCode === 87){wpressed = false;}
        if (event.keyCode === 83){spressed = false;}
        if (event.keyCode === 68){dpressed = false;}
    }, false);
    
}

function colcheck(x,z){
    for(i = 0; i < vertices.length/24; i++){
        if (x > vertices[(24*i)] && x < (vertices[(24*i)] + 0.1) && z > vertices[(24*i)+2] && z < (vertices[(24*i)+2]+0.1)){
            return true;
        }
    }
    return false;
}

var last_time = 0;
function update(time){
    var deltat = time - last_time;
    last_time = time;
    
    var newx = posx;
    var newz = posz;
    
    if (wpressed){
        newz += 0.00009*deltat;
    }
    if (spressed){
        newz -= 0.00009*deltat;
    }
    if (dpressed){
        newx -= 0.00009*deltat;
    }
    if (apressed){
        newx += 0.00009*deltat;
    }
    if (!colcheck(-newx, -newz)){
        posx = newx;
        posz = newz;
    }
    
    if (posz > 0){
        alert("you win!");
        return
    }
    
    draw();
    window.requestAnimationFrame(update);
}
