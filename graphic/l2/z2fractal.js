sierp_vertices = []
koch_vertices = []
layer_offsets = []
//Licz wierzchołki trójkątów Sierpinskiego
function sierpinski(siz, recurs, startx, starty, z){
    //Przy stopniu 0 narysuj trojkat
    if (recurs == 0){
        sierp_vertices.push(startx, starty, z, startx+siz, starty, z, startx+(siz/2), starty+((siz/2)*Math.sqrt(3)), z)
    }
    //W wyszym rekursja
    else{
        sierpinski(siz/2, recurs-1, startx, starty, z)
        sierpinski(siz/2, recurs-1, startx+(siz/2), starty, z)
        sierpinski(siz/2, recurs-1, startx+(siz/4), starty+((siz/4)*Math.sqrt(3)), z)
    }
}
//Licz wierzchołki odcinków krzywej Kocha
function koch(siz, recurs, startx, starty, starthead, z){
    //Przechylony odcinek
    if (recurs == 0){
        koch_vertices.push(startx, starty, z, startx+(Math.sin(starthead)*siz), starty+(Math.cos(starthead)*siz), z)
    }
    //4 Odcinki z "rogiem"
    else{
        koch(siz/3, recurs-1, startx, starty, starthead, z)
        koch(siz/3, recurs-1, startx+((siz/3)*Math.sin(starthead)), starty+((siz/3)*Math.cos(starthead)), starthead-(Math.PI/3), z)
        koch(siz/3, recurs-1, startx+((siz/3)*Math.sqrt(3)*Math.sin(starthead-(Math.PI/6))), starty+((siz/3)*Math.sqrt(3)*Math.cos(starthead-(Math.PI/6))), starthead+(Math.PI/3), z)
        koch(siz/3, recurs-1, startx+(((2*siz)/3)*Math.sin(starthead)), starty+(((2*siz)/3)*Math.cos(starthead)), starthead, z)
    }
}

//3 obrocone krzywe Kocha
function kochflake(siz, recurs, startx, starty, z){
    koch(siz, recurs, startx, starty, Math.PI/6, z)
    koch(siz, recurs, startx+siz, starty, -Math.PI/2, z)
    koch(siz, recurs, startx+(siz/2), starty+((siz/2)*Math.sqrt(3)), (5*Math.PI)/6, z)
}
//Przygotuj stopnie 0-8
function calcfractals(){
    for(i = 0; i <= 8; i++){
        sierpinski(1, i, -1.5, -0.433, -i);
        kochflake(1, i, 0.5, -0.433, -i);
        //Tablica przesuniecia warstwy w shaderze
        layer_offsets.push(0,0)
    }
}
