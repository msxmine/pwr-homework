canvas = document.getElementById("your_canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

gl = canvas.getContext("webgl");
vsSource = `
attribute vec3 aVertexPosition;
attribute vec4 color;
varying vec4 vColor;
uniform mat4 uViewMatrix;
uniform mat4 uProjectionMatrix;
void main(void) {
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(aVertexPosition, 1.);
 vColor = color;
}
`;

fsSource = `
varying mediump vec4 vColor;
void main(void) {
 gl_FragColor = vColor;
}`;

var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
var frag_shader = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader, fsSource);
gl.compileShader(frag_shader);

var shader = gl.createProgram();
gl.attachShader(shader, vert_shader);
gl.attachShader(shader, frag_shader);
gl.linkProgram(shader);


var _Pmatrix = gl.getUniformLocation(shader, "uProjectionMatrix");
var _Vmatrix = gl.getUniformLocation(shader, "uViewMatrix");

var _position = gl.getAttribLocation(shader, "aVertexPosition");
var _color = gl.getAttribLocation(shader, "color");

gl.enableVertexAttribArray(_position);
gl.enableVertexAttribArray(_color);

gl.useProgram(shader);


var ver_buf = gl.createBuffer();
var loaded_bufs = 0;
function updateBufs(){
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(traces), gl.STATIC_DRAW);
loaded_bufs = traces.length/7;
}
updateBufs();


var pmat = [
 0.5/Math.tan(Math.PI/8), 0, 0, 0,
 0, 0.5*(canvas.width/canvas.height)/Math.tan(Math.PI/8), 0, 0,
 0, 0, -1, -1,
 0, 0, 0, 0
];

var drag = false;
var old_x, old_y;
var dX = 0, dY = 0;
var THETA = 0;
var PHI = 0;

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

canvas.addEventListener("mousedown", mouseDown, false);
canvas.addEventListener("mouseup", mouseUp, false);
canvas.addEventListener("mouseout", mouseUp, false);
canvas.addEventListener("mousemove", mouseMove, false);

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

var time_prev = 0;
var draw = function(time){

    var deltat = time - time_prev;
    time_prev = time;
    
    
    var vmat = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, -1, 0,
    0, 0, -5, 1
    ];

    rotateY(vmat, THETA);
    rotateX(vmat, PHI);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.clearColor(0.0,0.0,0.0,0.0);
    gl.clearDepth(1.0);


    gl.viewport(0.0, 0.0, canvas.width, canvas.height);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.uniformMatrix4fv(_Pmatrix, false, pmat);
    gl.uniformMatrix4fv(_Vmatrix, false, vmat);
    gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*7,0);
    gl.vertexAttribPointer(_color, 4, gl.FLOAT, false, 4*7, 4*3);
    gl.drawArrays(gl.LINES, 0, loaded_bufs);
    gl.flush();

    window.requestAnimationFrame(draw);
};
draw(0);

