//Znajdz canvas w html
canvas = document.getElementById("your_canvas");
//Powieksz go do rozmiaru okna przegladarki
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
//Context GL
gl = canvas.getContext("webgl");

//Rozszerzenie pozwalajace na 32-bitowe indexy w tablicy wierzcholkow
var ext = gl.getExtension("OES_element_index_uint");

//Shadery
vsSource = `
attribute vec3 aVertexPosition;
attribute vec3 aVertexNormal;
varying vec3 vNormal;
varying vec3 vPosition;
uniform mat4 uViewMatrix;
uniform mat4 uProjectionMatrix;
void main(void) {
 //Rzut na ekran
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(aVertexPosition, 1.);
 //Przekazanie do fragment shader przez interpolacje
 vNormal = aVertexNormal;
 vPosition = vec3(aVertexPosition.x, aVertexPosition.y, aVertexPosition.z);
 gl_PointSize = 1.0;
}
`;

fsSource = `
uniform mediump vec3 lightPos;
uniform mediump vec3 lightColor;
uniform mediump vec4 color;
varying mediump vec3 vNormal;
varying mediump vec3 vPosition;
void main(void) {
 //Wektor normalny w danym punkcie i kierunek oswietlenia
 mediump vec3 norm = normalize(vNormal);
 mediump vec3 lightDir = normalize(lightPos - vPosition);
 //Natezenie swiatla diffuse
 mediump float diff = max(dot(norm, lightDir), 0.0);
 mediump vec3 diffuse = diff * lightColor;
 //Ambient
 mediump vec3 ambient = 0.1 * lightColor;
 //Polaczenie
 mediump vec4 final = vec4((ambient+diffuse), 1.0);
 gl_FragColor = final*color;
}`;

//Tworzenie i kompilacja shaderow
var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
var frag_shader = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader, fsSource);
gl.compileShader(frag_shader);

//Zlaczenie shaderow w gotowy program/ linking
var shader = gl.createProgram();
gl.attachShader(shader, vert_shader);
gl.attachShader(shader, frag_shader);
gl.linkProgram(shader);

//Pobieranie odniesien do zmiennych shadera
//Parametry stale dla przejscia rysujacego (oswietlenie)
var _color = gl.getUniformLocation(shader, "color");
var _lightPos = gl.getUniformLocation(shader, "lightPos");
var _lightColor = gl.getUniformLocation(shader, "lightColor");

//Parametry stale (perspektywa)
var _Pmatrix = gl.getUniformLocation(shader, "uProjectionMatrix");
var _Vmatrix = gl.getUniformLocation(shader, "uViewMatrix");

//Parametry wierzcholkow
var _position = gl.getAttribLocation(shader, "aVertexPosition");
var _normal = gl.getAttribLocation(shader, "aVertexNormal");
gl.enableVertexAttribArray(_position);
gl.enableVertexAttribArray(_normal);

//Ladowanie shadera
gl.useProgram(shader);

//Bufor indexow/odniesien do koordynatow w kolejnosci dla gl.TRIANGLES
//Indeksy sie nigdy nie zmieniaja
var surf_buf = gl.createBuffer();
var surf_idx_num = surface_idx.length;
gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, surf_buf)
gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(surface_idx), gl.STATIC_DRAW)


//Tworzenie/odswierzanie buforow wspolrzednych i normalnych
var ver_buf = gl.createBuffer();
var normal_buf = gl.createBuffer();
var loaded_bufs = 0;
function updateBufs(){
gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf)
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(normals), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(results), gl.STATIC_DRAW);
loaded_bufs = results.length/3;
}
updateBufs();

//Przeksztalcenie perspektywy
var pmat = [
    1/(Math.tan(Math.PI/8)*(canvas.width/canvas.height)), 0, 0, 0,
    0, 1/Math.tan(Math.PI/8), 0, 0,
    0, 0, -(100+0.1)/(100-0.1), -1,
    0, 0, -(2*100*0.1)/(100-0.1), 0
   ];

//Sledzenie myszki dla obracania przez przeciaganie
var drag = false;
var old_x, old_y;
var dX = 0, dY = 0; //delta/zmiana
var THETA = 0; //kat obrotu poziomego
var PHI = 0.4; //kot obrotu pionowego

var mouseDown = function(e){
    drag = true;
    old_x = e.pageX, old_y = e.pageY;
    e.preventDefault();
    return false;
}

var mouseUp = function(e){
    drag = false;
};

var mouseMove = function(e) {
    if (!drag) return false;
    dX = (e.pageX-old_x)*2*Math.PI/canvas.width,
    dY = (e.pageY-old_y)*2*Math.PI/canvas.height;
    THETA += dX;
    PHI += dY;
    old_x = e.pageX, old_y = e.pageY;
    e.preventDefault();
}
//Rejestrowanie funkcji sledzacych
canvas.addEventListener("mousedown", mouseDown, false);
canvas.addEventListener("mouseup", mouseUp, false);
canvas.addEventListener("mouseout", mouseUp, false);
canvas.addEventListener("mousemove", mouseMove, false);

//Przeksztalcenia na macierzach
//Obroty
function rotateX(m, angle) {
    var c = Math.cos(angle);
    var s = Math.sin(angle);
    var mv1 = m[1], mv5 = m[5], mv9 = m[9];

    m[1] = m[1]*c-m[2]*s;
    m[5] = m[5]*c-m[6]*s;
    m[9] = m[9]*c-m[10]*s;

    m[2] = m[2]*c+mv1*s;
    m[6] = m[6]*c+mv5*s;
    m[10] = m[10]*c+mv9*s;
}

function rotateY(m, angle) {
    var c = Math.cos(angle);
    var s = Math.sin(angle);
    var mv0 = m[0], mv4 = m[4], mv8 = m[8];

    m[0] = c*m[0]+s*m[2];
    m[4] = c*m[4]+s*m[6];
    m[8] = c*m[8]+s*m[10];

    m[2] = c*m[2]-s*mv0;
    m[6] = c*m[6]-s*mv4;
    m[10] = c*m[10]-s*mv8;
}

//Wykorzystaj bufer Z aby rysowac w dobrej kolejnosci
gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LESS);

//Nie usuwaj wielokatow zwroconych w zla strone
//Aby mozna bylo patrzec na wykres od spodu
gl.disable(gl.CULL_FACE)

//Poprawne liczenie przezroczystości
gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
gl.enable(gl.BLEND);

//Parametry czyszczenia buforow glebokosci/ekranu
//Domyslne wartosci
//Domyslnie przezroczystosc (na wiekszosci przegladarek domyslny html = bialy)
gl.clearColor(0.0,0.0,0.0,0.0);
//Domyslnie bardzo daleko/gleboko w ekran
gl.clearDepth(1.0);

//Daj GL informacje o oknie
gl.viewport(0.0, 0.0, canvas.width, canvas.height);

//Glowna funkcja rysujaca
var time_prev = 0;
var draw = function(time){
    //Czas od poprzedniego rysowania
    var deltat = time - time_prev;
    time_prev = time;
    
    //Macierz przeksztalcenia koncowego (widok/pozycja kamery)
    //Kamera odsunieta w Z
    var vmat = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, -2.5, 1
    ];

    //Zastosuj na wstepnej macierzy najnowsze wartosci ze sledzonej myszki
    rotateY(vmat, THETA);
    rotateX(vmat, PHI);
    

    var cl = [0,1,0,1] //Kolor powierzchni RGBA
    var cl2 = [1,0,0,1] //Kolor punktow RGBA
    var lpos = [0,5,0] //Pozycja swiatla XYZ
    var lcolor = [1,1,1] //Kolor swiatla RGB

    //Wyczysc ekran
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    //Ustaw widok
    gl.uniformMatrix4fv(_Pmatrix, false, pmat);
    gl.uniformMatrix4fv(_Vmatrix, false, vmat);
    //Swiatlo
    gl.uniform3fv(_lightPos, lpos)
    gl.uniform3fv(_lightColor, lcolor)
    //Podepnij bufor normalnych
    gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf);
    gl.vertexAttribPointer(_normal, 3, gl.FLOAT, false, 4*3, 0);
    //Podepnij bufoe wspolrzednych
    gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    //Podepnij indeksy
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, surf_buf)
    //Ustaw kolor powierzchni i ja narysuj
    gl.uniform4fv(_color, cl)
    gl.drawElements(gl.TRIANGLES, surf_idx_num, gl.UNSIGNED_INT, 0)
    //Ustaw kolor punktow i je narysuj
    gl.uniform4fv(_color, cl2)
    gl.drawArrays(gl.POINTS, 0, loaded_bufs);
    //Zakoncz rysowanie
    gl.flush();
    //Zarejestruj sie na nastepna klatke
    window.requestAnimationFrame(draw);
};
//Rozpocznij
draw(0);

