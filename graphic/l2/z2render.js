//Znajdz referencje do canvas i dopasuj rozmiar do ekranu oraz zinicjalizuj context opengl
canvas = document.getElementById("my_canvas");
canvas.width = window.innerWidth - 100;
canvas.height = window.innerHeight - 100;
gl = canvas.getContext("webgl");

//Vertex shader wykonuje projekcje współrzednych i liczy kolor w zaleznosci od z
vsSource = `
attribute mediump vec3 aVertexPosition;
uniform mediump mat4 uViewMatrix;
uniform mediump mat4 uProjectionMatrix;
uniform mediump vec2 uLayerOffsets[10];
varying mediump vec4 vColor;
void main(void) {
 //Czyta offset x y z tablicy uniform w zaleznosci od warstwy
 highp int layernum = int((aVertexPosition.z * -1.0) + 0.1);
 mediump vec3 realPos = vec3(aVertexPosition.x + uLayerOffsets[layernum][0], aVertexPosition.y + uLayerOffsets[layernum][1], aVertexPosition.z);
    
 //Smieszny efekt (dalej = wieksze (X,Y) mnozone razy dystans^2)
 //gl_Position = uProjectionMatrix * uViewMatrix * vec4(0.3*realPos.x*max((uViewMatrix[3][2] + realPos.z)*(uViewMatrix[3][2] + realPos.z),2.0), 0.3*realPos.y*max((realPos.z + uViewMatrix[3][2])*(uViewMatrix[3][2] + realPos.z),2.0), realPos.z, 1.);
 //Normalna perspektywa
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(realPos, 1.0);
 gl_PointSize = 1.0;
 vColor = vec4(fract(sin(aVertexPosition.z)), fract(cos(aVertexPosition.z)), fract(sin(aVertexPosition.z * 100.0)), 1.0);
}
`;
//Pixel shader ustawia kolor
fsSource = `
varying mediump vec4 vColor;
void main(void) {
 gl_FragColor = vColor;
}`;
//Kompilacja
var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
console.log(gl.getShaderInfoLog(vert_shader));
var frag_shader = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader, fsSource);
gl.compileShader(frag_shader);
var shader = gl.createProgram();
gl.attachShader(shader, vert_shader);
gl.attachShader(shader, frag_shader);

//Parametry z indexami ustawionymi przez programiste
var _position = 0
gl.bindAttribLocation(shader, _position, "aVertexPosition");
gl.linkProgram(shader);
//Parametry z indexami przydzielonymi przez sterownik
var _Pmatrix = gl.getUniformLocation(shader, "uProjectionMatrix");
var _Vmatrix = gl.getUniformLocation(shader, "uViewMatrix");
var _Loffsets = gl.getUniformLocation(shader, "uLayerOffsets");

//Ozacz atrybut pozycji jako aktywny
gl.enableVertexAttribArray(_position);
//Oznacz shader jako aktywny
gl.useProgram(shader);

//Zaladuj wspolrzedne do buforow
var sierp_buf = gl.createBuffer();
var koch_buf = gl.createBuffer();
function fillBufs(){
gl.bindBuffer(gl.ARRAY_BUFFER, sierp_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(sierp_vertices), gl.STATIC_DRAW);
sierp_triangles = sierp_vertices.length/9
gl.bindBuffer(gl.ARRAY_BUFFER, koch_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(koch_vertices), gl.STATIC_DRAW);
koch_lines = koch_vertices.length/6
}

function updateOffsets(){
    gl.uniform2fv(_Loffsets, layer_offsets)
}

//Rzut perspektywy
var pmat = [
 1/(Math.tan(Math.PI/4)*(canvas.width/canvas.height)), 0, 0, 0,
 0, 1/Math.tan(Math.PI/4), 0, 0,
 0, 0, -(100+0.001)/(100-0.001), -1,
 0, 0, -(2*100*0.001)/(100-0.001), 0
];
gl.uniformMatrix4fv(_Pmatrix, false, pmat);

//Rysuj Z blizsze ekranu na wierzchu
gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LEQUAL);



function draw(){
    //Kamera przesuwa się po Z
    var vmat = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
    ];
    vmat[14] = -posz
    gl.uniformMatrix4fv(_Vmatrix, false, vmat);
    
    //Wyczysc ekran
    gl.clearColor(0.0,0.0,0.0,0.0);
    gl.clearDepth(1.0);

    //Podłącz bufer z koordynatami, załaduj koorynaty z bufora i rysuj
    gl.bindBuffer(gl.ARRAY_BUFFER, sierp_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    gl.drawArrays(gl.TRIANGLES, 0, sierp_triangles*3);
    //Koch
    gl.bindBuffer(gl.ARRAY_BUFFER, koch_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    gl.drawArrays(gl.LINES, 0, koch_lines*2);

    gl.flush();
}
