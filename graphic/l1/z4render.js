canvas = document.getElementById("my_canvas");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

gl = canvas.getContext("webgl");
vsSource = `
attribute vec3 aVertexPosition;
uniform mat4 uViewMatrix;
uniform mat4 uProjectionMatrix;
void main(void) {
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(aVertexPosition, 1.);
}
`;

fsSource = `
void main(void) {
 gl_FragColor = vec4(0.0,0.0,0.0,1.0);
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

gl.enableVertexAttribArray(_position);

gl.useProgram(shader);


var ver_buf = gl.createBuffer();
var geo_buf = gl.createBuffer();
var loaded_vert = 0;
var loaded_geom = 0;
function updateBufs(){
gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
loaded_bufs = vertices.length/3;
gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, geo_buf);
gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(geometry), gl.STATIC_DRAW);
loaded_geom = geometry.length;
}
updateBufs();


var pmat = [
 1/(Math.tan(Math.PI/8)*(canvas.width/canvas.height)), 0, 0, 0,
 0, 1/Math.tan(Math.PI/8), 0, 0,
 0, 0, -(100+0.001)/(100-0.001), -1,
 0, 0, -(2*100*0.001)/(100-0.001), 0
];


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

function translateZ(m, dist){
    m[14] += dist;
}
function translateX(m, dist){
    m[12] += dist;
}

gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LEQUAL);
gl.clearColor(0.0,0.0,0.0,0.0);
gl.clearDepth(1.0);

gl.uniformMatrix4fv(_Pmatrix, false, pmat);

function draw(){
    
    var vmat = [
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, -0.1, 0, 1
    ];
    translateZ(vmat, posz);
    translateX(vmat, posx);



    //gl.viewport(0.0, 0.0, canvas.width, canvas.height);
    //gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    gl.uniformMatrix4fv(_Vmatrix, false, vmat);
    gl.bindBuffer(gl.ARRAY_BUFFER, ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, geo_buf);
    gl.drawElements(gl.LINES, loaded_geom, gl.UNSIGNED_SHORT, 0);
    //gl.flush();
};

