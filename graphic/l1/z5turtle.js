posx = 0
posy = 0
posz = 0
roty = 0
rotx = 0
penstate = true
color = [0.0, 0.0, 0.0, 1.0] //RGBA
minX = -1
minY = -1
minZ = -1
maxX = 1
maxY = 1
maxZ = 1
geochanged = false

traces = [];

function clear(){
    //Okno
    traces = [
    minX, minY, minZ, 0,0,0,0.2, maxX, minY, minZ, 0,0,0,0.2,
    maxX, minY, minZ, 0,0,0,0.2, maxX, maxY, minZ, 0,0,0,0.2,
    maxX, maxY, minZ, 0,0,0,0.2, minX, maxY, minZ, 0,0,0,0.2,
    minX, maxY, minZ, 0,0,0,0.2, minX, minY, minZ, 0,0,0,0.2,
    
    minX, minY, maxZ, 0,0,0,0.2, maxX, minY, maxZ, 0,0,0,0.2,
    maxX, minY, maxZ, 0,0,0,0.2, maxX, maxY, maxZ, 0,0,0,0.2,
    maxX, maxY, maxZ, 0,0,0,0.2, minX, maxY, maxZ, 0,0,0,0.2,
    minX, maxY, maxZ, 0,0,0,0.2, minX, minY, maxZ, 0,0,0,0.2,
    
    minX, minY, minZ, 0,0,0,0.2, minX, minY, maxZ, 0,0,0,0.2,
    maxX, minY, minZ, 0,0,0,0.2, maxX, minY, maxZ, 0,0,0,0.2,
    minX, maxY, minZ, 0,0,0,0.2, minX, maxY, maxZ, 0,0,0,0.2,
    maxX, maxY, minZ, 0,0,0,0.2, maxX, maxY, maxZ, 0,0,0,0.2
    ];
    posx = 0;
    posy = 0;
    posz = 0;
    roty = 0;
    rotx = 0;
    penstate = true;
    color = [0.0, 0.0, 0.0, 1.0]
    geochanged = true
}

clear();

function goto(x,y,z){
    var len = Math.sqrt( ((x-posx)**2) + ((y-posy)**2) + ((z-posz)**2))
    var lfx = len/(x-posx)
    var lfy = len/(y-posy)
    var lfz = len/(z-posz)
    
    var draw_start = [posx, posy, posz]
    var draw_end = [x,y,z]
    
    //Aby ograniczyć odcinki do naszego prostopadłościanu "okna"
    //wykonaj raycast i przenieś punkty startu i końca do punktów
    //zderzenia ze ścianami
    var startinbox = false
    if (posx >= minX && posx <= maxX && posy >= minY && posy <= maxY && posz >= minZ && posz <= maxZ){
        startinbox = true
    }
    if (!startinbox){
        var t1 = (minX - posx)*lfx
        var t2 = (maxX - posx)*lfx
        var t3 = (minY - posy)*lfy
        var t4 = (maxY - posy)*lfy
        var t5 = (minZ - posz)*lfz
        var t6 = (maxZ - posz)*lfz
        
        var tmin = Math.max(Math.min(t1,t2), Math.min(t3,t4), Math.min(t5,t6))
        var tmax = Math.min(Math.max(t1,t2), Math.max(t3,t4), Math.max(t5,t6))
        
        if (tmax >= tmin && tmax >= 0){
            if (tmin <= len){
                draw_start = [x - ((x - posx)*(1-(tmin/len))), y - ((y - posy)*(1-(tmin/len))), z - ((z - posz)*(1-(tmin/len)))]
                startinbox = true;
            }
        }
    }
    
    var endinbox = false;
    if (x >= minX && x <= maxX && y >= minY && y <= maxY && z >= minZ && z <= maxZ){
        endinbox = true
    }
    if (!endinbox){
        var t1 = (x - minX)*lfx
        var t2 = (x - maxX)*lfx
        var t3 = (y - minY)*lfy
        var t4 = (y - maxY)*lfy
        var t5 = (z - minZ)*lfz
        var t6 = (z - maxZ)*lfz
        
        var tmin = Math.max(Math.min(t1,t2), Math.min(t3,t4), Math.min(t5,t6))
        var tmax = Math.min(Math.max(t1,t2), Math.max(t3,t4), Math.max(t5,t6))
        
        if (tmax >= tmin && tmax >= 0){
            if (tmin <= len){
                draw_end = [posx - ((posx - x)*(1-(tmin/len))),  posy - ((posy - y)*(1-(tmin/len))), posz - ((posz -z)*(1-(tmin/len)))]
                endinbox = true;
            }
        }
    }
    
    if (startinbox && endinbox && penstate){
        traces.push(draw_start[0], draw_start[1], draw_start[2], color[0], color[1], color[2], color[3], draw_end[0], draw_end[1], draw_end[2], color[0], color[1], color[2], color[3])
        geochanged = true
    }
    
    posx = x
    posy = y
    posz = z
    
}

function forward(distance){
    var deltay = distance*Math.sin(rotx);
    var deltaxz = distance*Math.cos(rotx);
    var deltax = deltaxz*Math.sin(roty);
    var deltaz = deltaxz*Math.cos(roty);
    goto(posx+deltax, posy+deltay, posz+deltaz);
}

function backward(distance){
    forward(-distance);
}

function right(deg){
    roty += (Math.PI * deg/180)
}

function left(deg){
    right(-deg)
}

function up(deg){
    rotx += (Math.PI * deg/180)
}

function down(deg){
    up(-deg);
}

function penup(){
  penstate = false
}

function pendown(){
  penstate = true
}

function setcolor(r, g, b, a){
    color = [r,g,b,a]
}

function setrot(degy, degx){
    roty = (Math.PI * degy/180)
    rotx = (Math.PI * degx/180)
}
