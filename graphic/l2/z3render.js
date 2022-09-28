var bricktexture;
var bgtexture;
var paddletexture;
var balltexture;

//Znajdz referencje do canvas i dopasuj rozmiar do ekranu oraz zinicjalizuj context opengl
var canvas = document.getElementById("my_canvas");
canvas.width = window.innerWidth - 100;
canvas.height = window.innerHeight - 100;
var gl = canvas.getContext("webgl", {alpha: false});

async function loadAssets(){
    //Załaduj tekstury
    function loadTexture(url){
        const texture = gl.createTexture();
        const image = new Image();
        let aret = new Promise(resolve => {
            image.onload = function(){
                //Po załadowaniu do pamięci, zbinduj do GL
                gl.bindTexture(gl.TEXTURE_2D, texture);
                gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
                gl.generateMipmap(gl.TEXTURE_2D);
                resolve(texture);
            }
            image.src = url;
        });
        return aret;
    }

    bricktexture = await loadTexture("bricks.png");
    bgtexture = await loadTexture("ice.png");
    paddletexture = await loadTexture("iron_block.png");
    balltexture = await loadTexture("snowball.png");
}


//Vertex shader wykonuje projekcje współrzednych i przekazuje (interpolowane) koordynaty tekstur do pixel shadera
vsSource = `
attribute mediump vec3 aVertexPosition;
attribute mediump vec3 aTextureCoord;
uniform mediump mat4 uViewMatrix;
uniform mediump mat4 uProjectionMatrix;
varying mediump vec3 vTextureCoord;
void main(void) {
 gl_Position = uProjectionMatrix * uViewMatrix * vec4(aVertexPosition, 1.);
 gl_PointSize = 1.0;
 vTextureCoord = aTextureCoord;
}
`;
//Pixel shader ustawia kolor z tekstury
fsSource = `
varying mediump vec3 vTextureCoord;
uniform sampler2D uSamplers[4];

mediump vec4 getTexColor(int tidx, vec2 uv) {
 if (0 == tidx) {
  return texture2D(uSamplers[0], uv);
 }
 if (1 == tidx) {
  return texture2D(uSamplers[1], uv);
 }
 if (2 == tidx) {
  return texture2D(uSamplers[2], uv);
 }
 if (3 == tidx) {
  return texture2D(uSamplers[3], uv);
 }
 return vec4(0);
}

void main(void) {
 gl_FragColor = getTexColor(int(vTextureCoord[2] + 0.1), vec2(vTextureCoord[0], vTextureCoord[1]));
}`;
//Kompilacja shaderow
var vert_shader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vert_shader, vsSource);
gl.compileShader(vert_shader);
console.log(gl.getShaderInfoLog(vert_shader))
var frag_shader = gl.createShader(gl.FRAGMENT_SHADER);
gl.shaderSource(frag_shader, fsSource);
gl.compileShader(frag_shader);
console.log(gl.getShaderInfoLog(frag_shader))
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
var _Tcoords = gl.getAttribLocation(shader, "aTextureCoord");
var _Tsamplers = gl.getUniformLocation(shader, "uSamplers");

//Ozacz atrybut pozycji jako aktywny
gl.enableVertexAttribArray(_position);
gl.enableVertexAttribArray(_Tcoords);
//Oznacz shader jako aktywny
gl.useProgram(shader);



//Tablice koordynatow wierzchołków i tekstur
bgvertices = [
-1,-1,0, 1,1,0, -1,1,0, -1,-1,0, 1,-1,0, 1,1,0, //Tło
-1,1,0, 1,1,0, -1,1,0.1, -1,1,0.1, 1,1,0, 1,1,0.1, //Sufit
1,-1,0, -1,-1,0, 1,-1,0.1, 1,-1,0.1, -1,-1,0, -1,-1,0.1 //Podłoga
]
bgtextures = [
0,0,0, 2,2,0, 0,2,0, 0,0,0, 2,0,0, 2,2,0,
0,0,1, 10,0,1, 0,1,1, 0,1,1, 10,0,1, 10,1,1,
0,0,1, 10,0,1, 0,1,1, 0,1,1, 10,0,1, 10,1,1
]
paddletextures = [
0,0,0, 1,0,0, 1,1,0, 1,1,0, 0,1,0, 0,0,0,
0,0,0, 1,0,0, 1,1,0, 1,1,0, 0,1,0, 0,0,0
]
balltextures = [
0.5,1,0, 0,0.5,0, 0.5,0,0, 0.5,0,0, 1,0.5,0, 0.5,1,0
]

function recalcDynamicVertex(){
paddlevertices = [
-1, -(paddle_height/2)+p1paddle_pos, 0, -1, (paddle_height/2)+p1paddle_pos, 0, -1, (paddle_height/2)+p1paddle_pos, 0.1, -1, (paddle_height/2)+p1paddle_pos, 0.1, -1, -(paddle_height/2)+p1paddle_pos, 0.1, -1, -(paddle_height/2)+p1paddle_pos, 0,
1 , -(paddle_height/2)+p2paddle_pos, 0, 1 , (paddle_height/2)+p2paddle_pos, 0, 1 , (paddle_height/2)+p2paddle_pos, 0.1, 1 , (paddle_height/2)+p2paddle_pos, 0.1, 1 , -(paddle_height/2)+p2paddle_pos, 0.1, 1 , -(paddle_height/2)+p2paddle_pos, 0
]

ballvertices = [
0+ballx, 0.05+bally, 0.01, -0.05+ballx, 0+bally, 0.01, 0+ballx, -0.05+bally, 0.01, 0+ballx, -0.05+bally, 0.01, 0.05+ballx, 0+bally, 0.01, 0+ballx, 0.05+bally, 0.01
]
}
recalcDynamicVertex()

//Zaladuj wspolrzedne do buforow
var bg_ver_buf = gl.createBuffer();
var bg_tex_buf = gl.createBuffer();
var paddle_ver_buf = gl.createBuffer();
var paddle_tex_buf = gl.createBuffer();
var ball_ver_buf = gl.createBuffer();
var ball_tex_buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, bg_ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(bgvertices), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, bg_tex_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(bgtextures), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, ball_tex_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(balltextures), gl.STATIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, paddle_tex_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(paddletextures), gl.STATIC_DRAW);

function reloadDynamicBuffers(){
gl.bindBuffer(gl.ARRAY_BUFFER, ball_ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(ballvertices), gl.DYNAMIC_DRAW);
gl.bindBuffer(gl.ARRAY_BUFFER, paddle_ver_buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(paddlevertices), gl.DYNAMIC_DRAW);
}
reloadDynamicBuffers()

//Rzut perspektywy
var pmat = [
 1/(Math.tan(Math.PI/4)*(canvas.width/canvas.height)), 0, 0, 0,
 0, 1/Math.tan(Math.PI/4), 0, 0,
 0, 0, -(100+0.001)/(100-0.001), -1,
 0, 0, -(2*100*0.001)/(100-0.001), 0
];
gl.uniformMatrix4fv(_Pmatrix, false, pmat);

//Kamera odsunięta w Z
var vmat = [
1, 0, 0, 0,
0, 1, 0, 0,
0, 0, 1, 0,
0, 0, -1.2, 1
];
gl.uniformMatrix4fv(_Vmatrix, false, vmat);

//Liczenie przezroczystości
gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
gl.enable(gl.BLEND);

//Rysuj Z blizsze ekranu na wierzchu
gl.enable(gl.DEPTH_TEST);
gl.depthFunc(gl.LEQUAL);

function render(){
    //Wyczysc ekran
    gl.clearColor(0.0,0.0,0.0,0.0);
    gl.clearDepth(1.0);

    //Tło
    //Podłącz bufer z koordynatami
    gl.bindBuffer(gl.ARRAY_BUFFER, bg_ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    //Podłącz bufor z koordynatami textur
    gl.bindBuffer(gl.ARRAY_BUFFER, bg_tex_buf);
    gl.vertexAttribPointer(_Tcoords, 3, gl.FLOAT, false, 4*3,0);
    //Połącz textury z właściwymi slotami
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, bgtexture);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, bricktexture);
    gl.uniform1iv(_Tsamplers, new Int32Array([0,1]));
    //Rysuj
    gl.drawArrays(gl.TRIANGLES, 0, 18);

    //Paletki
    gl.bindBuffer(gl.ARRAY_BUFFER, paddle_ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    gl.bindBuffer(gl.ARRAY_BUFFER, paddle_tex_buf);
    gl.vertexAttribPointer(_Tcoords, 3, gl.FLOAT, false, 4*3,0);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, paddletexture);
    gl.uniform1iv(_Tsamplers, new Int32Array([0]));
    gl.drawArrays(gl.TRIANGLES, 0, 12);

    //Piłka
    gl.bindBuffer(gl.ARRAY_BUFFER, ball_ver_buf);
    gl.vertexAttribPointer(_position, 3, gl.FLOAT, false, 4*3,0);
    gl.bindBuffer(gl.ARRAY_BUFFER, ball_tex_buf);
    gl.vertexAttribPointer(_Tcoords, 3, gl.FLOAT, false, 4*3,0);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, balltexture);
    gl.uniform1iv(_Tsamplers, new Int32Array([0]));
    gl.drawArrays(gl.TRIANGLES, 0, 6);

    gl.flush();
}




    
