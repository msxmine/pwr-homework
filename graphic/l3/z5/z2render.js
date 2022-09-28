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
uniform mat4 uModelMatrix;
uniform mat4 uViewMatrix;
uniform mat3 uNormalMatrix;
uniform mat4 uProjectionMatrix;
void main(void) {
 //Rzut na ekran
 gl_Position = uProjectionMatrix * uViewMatrix * uModelMatrix * vec4(aVertexPosition, 1.);
 //Przekazanie do fragment shader przez interpolacje
 vNormal = uNormalMatrix * aVertexNormal;
 vPosition = vec3( (uModelMatrix * vec4(aVertexPosition, 1.)).xyz );
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

//Shadery do rysowania tekstury
pixelVertSrc = `
attribute vec2 aPosition;
attribute vec2 aTexPosition;
varying vec2 vTexPosition;
void main(void) {
    vTexPosition = aTexPosition;
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

pixelFragSrc = `
varying mediump vec2 vTexPosition;
uniform sampler2D uSampler;
void main(void) {
    gl_FragColor = texture2D(uSampler, vTexPosition);
}
`;

//Tworzenie i kompilacja shaderow
var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
var frag_shader = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader, fsSource);
gl.compileShader(frag_shader);
var vert_shader_pix = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader_pix, pixelVertSrc);
gl.compileShader(vert_shader_pix);
var frag_shader_pix = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader_pix, pixelFragSrc);
gl.compileShader(frag_shader_pix);

//Zlaczenie shaderow w gotowy program/ linking
var shader = gl.createProgram();
gl.attachShader(shader, vert_shader);
gl.attachShader(shader, frag_shader);
gl.linkProgram(shader);
var pixshader = gl.createProgram();
gl.attachShader(pixshader, vert_shader_pix);
gl.attachShader(pixshader, frag_shader_pix);
gl.linkProgram(pixshader);

//Pobieranie odniesien do zmiennych shadera
//Parametry stale dla przejscia rysujacego (oswietlenie)
var _color = gl.getUniformLocation(shader, "color");
var _lightPos = gl.getUniformLocation(shader, "lightPos");
var _lightColor = gl.getUniformLocation(shader, "lightColor");

//Parametry stale (perspektywa)
var _Pmatrix = gl.getUniformLocation(shader, "uProjectionMatrix");
var _Vmatrix = gl.getUniformLocation(shader, "uViewMatrix");
//Przeksztalcenia modelu
var _Mmatrix = gl.getUniformLocation(shader, "uModelMatrix");
var _Nmatrix = gl.getUniformLocation(shader, "uNormalMatrix");

//Parametry wierzcholkow
var _position = gl.getAttribLocation(shader, "aVertexPosition");
var _normal = gl.getAttribLocation(shader, "aVertexNormal");

//Tekstura czytana
var _PixPos = gl.getAttribLocation(pixshader, "aPosition");
var _TexPos = gl.getAttribLocation(pixshader, "aTexPosition");
var _TexRef = gl.getUniformLocation(pixshader, "uSampler");



//Prostokat do rysowania tekstury
var stub_buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, stub_buf)
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1.0,-1.0, -1.0,1.0, 1.0,-1.0, 1.0,1.0]), gl.STATIC_DRAW)
var tex_stub_buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, tex_stub_buf)
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0,0, 0,1, 1,0, 1,1]), gl.STATIC_DRAW)

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
//funkcja g
var ver_buf_2 = gl.createBuffer();
var normal_buf_2 = gl.createBuffer();
var loaded_bufs_2 = 0;
function updateBufs(){
gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf)
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(func1.normals), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(func1.results), gl.STATIC_DRAW);
loaded_bufs = func1.results.length/3;
gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf_2)
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(func2.normals), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf_2);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(func2.results), gl.STATIC_DRAW);
loaded_bufs_2 = func2.results.length/3;
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
    return m
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
    return m
}

//mat3(transpose(inverse(matrix)))
function normalMatrix(matrix) {

    var a00 = matrix[0], a01 = matrix[1], a02 = matrix[2], a03 = matrix[3],
        a10 = matrix[4], a11 = matrix[5], a12 = matrix[6], a13 = matrix[7],
        a20 = matrix[8], a21 = matrix[9], a22 = matrix[10], a23 = matrix[11],
        a30 = matrix[12], a31 = matrix[13], a32 = matrix[14], a33 = matrix[15],
  
        b00 = a00 * a11 - a01 * a10,
        b01 = a00 * a12 - a02 * a10,
        b02 = a00 * a13 - a03 * a10,
        b03 = a01 * a12 - a02 * a11,
        b04 = a01 * a13 - a03 * a11,
        b05 = a02 * a13 - a03 * a12,
        b06 = a20 * a31 - a21 * a30,
        b07 = a20 * a32 - a22 * a30,
        b08 = a20 * a33 - a23 * a30,
        b09 = a21 * a32 - a22 * a31,
        b10 = a21 * a33 - a23 * a31,
        b11 = a22 * a33 - a23 * a32,
  
        // Wyznacznik
        det = b00 * b11 - b01 * b10 + b02 * b09 + b03 * b08 - b04 * b07 + b05 * b06;
  
    if (!det) { 
      return null; 
    }
    det = 1.0 / det;
    
    var result = []
  
    result[0] = (a11 * b11 - a12 * b10 + a13 * b09) * det;
    result[1] = (a12 * b08 - a10 * b11 - a13 * b07) * det;
    result[2] = (a10 * b10 - a11 * b08 + a13 * b06) * det;
  
    result[3] = (a02 * b10 - a01 * b11 - a03 * b09) * det;
    result[4] = (a00 * b11 - a02 * b08 + a03 * b07) * det;
    result[5] = (a01 * b08 - a00 * b10 - a03 * b06) * det;
  
    result[6] = (a31 * b05 - a32 * b04 + a33 * b03) * det;
    result[7] = (a32 * b02 - a30 * b05 - a33 * b01) * det;
    result[8] = (a30 * b04 - a31 * b02 + a33 * b00) * det;
  
    return result;
}
//Macierz jednostkowa
function identityMatrix(){
    return [
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        0,0,0,1
    ]
}

//Wykorzystaj bufer Z aby rysowac w dobrej kolejnosci
gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LESS);

//Nie usuwaj wielokatow zwroconych w zla strone
//Aby mozna bylo patrzec na wykres od spodu
gl.disable(gl.CULL_FACE)

//Aktywuj mieszanie
gl.enable(gl.BLEND)

//Parametry czyszczenia buforow glebokosci/ekranu
//Domyslne wartosci
//Domyslnie przezroczystosc
gl.clearColor(0.0,0.0,0.0,0.0);
//Domyslnie bardzo daleko/gleboko w ekran
gl.clearDepth(1.0);

//Daj GL informacje o oknie
gl.viewport(0.0, 0.0, canvas.width, canvas.height);

//Stworz teksture dla rysowania wykresu 1
var target1 = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, target1);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, canvas.width, canvas.height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
//Wylacz mipmapy
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
//Stworz bufor glebokosci
var target1depth = gl.createRenderbuffer();
gl.bindRenderbuffer(gl.RENDERBUFFER, target1depth)
gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, canvas.width, canvas.height);
//Polacz w cel dla renderowania
var framebuf1 = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuf1);
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, target1, 0);
gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, target1depth);


//Obroty wykresow w przestrzeni swiata
var frotation = 0
var grotation = 0

//Glowna funkcja rysujaca
var time_prev = 0;
var draw = function(time){
    //Czas od poprzedniego rysowania
    var deltat = time - time_prev;
    time_prev = time;

    //Animacja obracania
    frotation += deltat/2000
    grotation -= deltat/2000
    
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

    //Liczenie obrotu macierz modelu/normalnych
    mmat1 = rotateY(identityMatrix(), frotation)
    nmat1 = normalMatrix(mmat1)
    mmat2 = rotateY(identityMatrix(), grotation)
    nmat2 = normalMatrix(mmat2)
    

    var cl = [0,1,0,0.5] //Kolor powierzchni RGBA
    var cl2 = [1,0,0,0.5] //Kolor punktow RGBA
    var cl3 = [0,1,1,0.5] //Kolor powierzchni RGBA
    var cl4 = [1,0,1,0.5] //Kolor punktow RGBA
    var lpos = [0,1,1] //Pozycja swiatla XYZ
    var lcolor = [1,1,1] //Kolor swiatla RGB

    //Rysuj do tekstury 1
    gl.bindFramebuffer(gl.FRAMEBUFFER, framebuf1);
    //Wyczysc teksture
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    //Ladowanie shadera
    gl.useProgram(shader);
    gl.enableVertexAttribArray(_position);
    gl.enableVertexAttribArray(_normal);

    //Ustaw widok
    gl.uniformMatrix4fv(_Pmatrix, false, pmat);
    gl.uniformMatrix4fv(_Vmatrix, false, vmat);
    //Swiatlo
    gl.uniform3fv(_lightPos, lpos)
    gl.uniform3fv(_lightColor, lcolor)

    //Podepnij indeksy
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, surf_buf)

    //f(x,y)
    //Wylacz mieszanie
    gl.blendFuncSeparate(gl.ONE, gl.ZERO, gl.ONE, gl.ZERO)
    //Przeksztalcenia geometryczne
    gl.uniformMatrix4fv(_Mmatrix, false, mmat1)
    gl.uniformMatrix3fv(_Nmatrix, false, nmat1)
    //Podepnij bufor normalnych
    gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf);
    gl.vertexAttribPointer(_normal, 3, gl.FLOAT, false, 4*3, 0);
    //Podepnij bufor wspolrzednych
    gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    //Ustaw kolor powierzchni i ja narysuj
    gl.uniform4fv(_color, cl)
    gl.drawElements(gl.TRIANGLES, surf_idx_num, gl.UNSIGNED_INT, 0)
    //Ustaw kolor punktow i je narysuj
    gl.uniform4fv(_color, cl2)
    gl.drawArrays(gl.POINTS, 0, loaded_bufs);


    //Przelacz na rysowanie do canvas
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    //Wyczysc ekran
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    //g(x,y)
    //Wylacz mieszanie
    gl.blendFuncSeparate(gl.ONE, gl.ZERO, gl.ONE, gl.ZERO)
    //Przeksztalcenia geometryczne
    gl.uniformMatrix4fv(_Mmatrix, false, mmat2)
    gl.uniformMatrix3fv(_Nmatrix, false, nmat2)
    //Podepnij bufor normalnych
    gl.bindBuffer(gl.ARRAY_BUFFER, normal_buf_2);
    gl.vertexAttribPointer(_normal, 3, gl.FLOAT, false, 4*3, 0);
    //Podepnij bufor wspolrzednych
    gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf_2);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    //Ustaw kolor powierzchni i ja narysuj
    gl.uniform4fv(_color, cl3)
    gl.drawElements(gl.TRIANGLES, surf_idx_num, gl.UNSIGNED_INT, 0)
    //Ustaw kolor punktow i je narysuj
    gl.uniform4fv(_color, cl4)
    gl.drawArrays(gl.POINTS, 0, loaded_bufs_2);

    //Naloz teksture z wykresem 1
    //Nic -> Pelna przezroczystosc, 1 Wykres -> Pelne kolory i 1/2 przezroczystosc, 2 Wykresy -> Zmieszane kolory i 0 przezroczystosci
    //Nasladuje wynik z zadania 4
    gl.blendFuncSeparate(gl.ONE_MINUS_DST_ALPHA, gl.DST_ALPHA, gl.ONE, gl.ONE)
    //Shader teksturujacy
    gl.useProgram(pixshader)
    gl.enableVertexAttribArray(_PixPos);
    gl.enableVertexAttribArray(_TexPos);
    //Prostokat na caly ekran
    gl.bindBuffer(gl.ARRAY_BUFFER, tex_stub_buf);
    gl.vertexAttribPointer(_TexPos, 2, gl.FLOAT, false, 4*2,0);
    gl.bindBuffer(gl.ARRAY_BUFFER, stub_buf);
    gl.vertexAttribPointer(_PixPos, 2, gl.FLOAT, false, 4*2,0);
    //Tekstura z narysowanym wykresem 1
    gl.activeTexture(gl.TEXTURE0)
    gl.uniform1i(_TexRef, 0);
    gl.bindTexture(gl.TEXTURE_2D, target1);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

    //Zakoncz rysowanie
    gl.flush();
    //Zarejestruj sie na nastepna klatke
    window.requestAnimationFrame(draw);
};
//Rozpocznij
draw(0);

