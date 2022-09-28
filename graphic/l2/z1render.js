//Znajdz referencje do canvas i dopasuj rozmiar do ekranu oraz zinicjalizuj context opengl
canvas = document.getElementById("my_canvas");
canvas.width = window.innerWidth - 100;
canvas.height = window.innerHeight - 100;
gl = canvas.getContext("webgl");

//Vertex shader wykonuje projekcje współrzednych
vsSource = `
attribute mediump vec3 aVertexPosition;
uniform mediump mat4 uViewMatrix;
uniform mediump mat4 uProjectionMatrix;
void main(void) {
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(aVertexPosition, 1.);
 gl_PointSize = 1.0;
}
`;
//Pixel shader ustawia kolor
fsSource = `
uniform mediump vec4 uColor;
void main(void) {
 gl_FragColor = uColor;
}`;
//Kompilacja
var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
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
var _color = gl.getUniformLocation(shader, "uColor")

//Ozacz atrybut pozycjijako aktywny
gl.enableVertexAttribArray(_position);
//Oznacz shader jako aktywny
gl.useProgram(shader);

vertices = [
-1,0,0, //Punkt
-0.8,0,0, -0.7,0.1,0, -0.8,0.2,0, //Line_STRIP
-0.5,0,0, -0.4,0.1,0, -0.5,0.2,0, //Line_LOOP
-0.2,0,0, -0.1,0.1,0, -0.2,0.2,0, -0.1,0.3,0, //LINES
0.2,0,0, 0.1,0,0, 0.15,0.1,0, 0.15,0.2,0, //triangle Line_STRIP
0.5,0,0, 0.4,0,0, 0.45,0.1,0, 0.45,0.2,0, //triangle fan
0.7,0,0, 0.8,0,0, 0.75,0.1,0, 0.75,0.2,0, 0.8,0.3,0, 0.7,0.3,0 //triangles
]

colors = [[0, 0, 0, 1], [1, 0, 0, 1],[0, 1, 0, 1],[0, 0, 1, 1],[1, 0, 1, 1],[0, 1, 1, 1],[1, 1, 0, 1]]

//Zaladuj wspolrzedne do buforow
var ver_buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);


//Rzut prostokatny
var pmat = [
 1/(canvas.width/canvas.height), 0, 0, 0,
 0, 1, 0, 0,
 0, 0, 0.001, 0,
 0, 0, 0, 1 ];
gl.uniformMatrix4fv(_Pmatrix, false, pmat);

//Kamera odsunięta w Z
var vmat = [
1, 0, 0, 0,
0, 1, 0, 0,
0, 0, 1, 0,
0, 0, -2, 1
];
gl.uniformMatrix4fv(_Vmatrix, false, vmat);

//Rysuj Z blizsze ekranu na wierzchu
gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LEQUAL);
//Wyczysc ekran
gl.clearColor(0.0,0.0,0.0,0.0);
gl.clearDepth(1.0);

//Podłącz bufer z koordynatami
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
//(Ustaw kolor, załaduj koorynaty z bufora i rysuj)
gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
gl.uniform4fv(_color, colors[0]);
gl.drawArrays(gl.POINTS, 0, 1);
gl.uniform4fv(_color, colors[1]);
gl.drawArrays(gl.LINE_STRIP, 1, 3);
gl.uniform4fv(_color, colors[2]);
gl.drawArrays(gl.LINE_LOOP, 4, 3);
gl.uniform4fv(_color, colors[3]);
gl.drawArrays(gl.LINES, 7, 4);
gl.uniform4fv(_color, colors[4]);
gl.drawArrays(gl.TRIANGLE_STRIP, 11, 4);
gl.uniform4fv(_color, colors[5]);
gl.drawArrays(gl.TRIANGLE_FAN, 15, 4);
gl.uniform4fv(_color, colors[6]);
gl.drawArrays(gl.TRIANGLES, 19, 6);

gl.flush();


for (i = 0; i < gl.getProgramParameter(shader, gl.ACTIVE_ATTRIBUTES); i++) {
    console.log(gl.getActiveAttrib(shader, i).name);
}
for (i = 0; i < gl.getProgramParameter(shader, gl.ACTIVE_UNIFORMS); i++) {
    console.log(gl.getActiveUniform(shader, i).name);
}
    
