//Plik definiujący funkcje grafiki żółwia
posx = 0
posy = 0
rot = 0
penstate = true
color = "#000000"
minX = -1
maxX = 1
minY = -1
maxY = 1

sf = document.getElementById("surface")
ctx = sf.getContext("2d")
//Skalowanie między koordynatami a pikselami
function applyScale(len){
  chei = ctx.canvas.height
  cwid = ctx.canvas.width
  vhei = (maxY - minY)
  vwid = (maxX - minX)
  yScale = chei / vhei
  xScale = cwid / vwid
  minScale = Math.min(yScale, xScale)
  return minScale*len
}
//Zamiana dla wartości absolutnych
function convertXCoord(xcoord){
  return applyScale(xcoord - ((minX + maxX)/2)) + (ctx.canvas.width/2)
}
function convertYCoord(ycoord){
  return -applyScale(ycoord - ((minY + maxY)/2)) + (ctx.canvas.height/2)
}

function clear(){
    ctx.clearRect(0,0, ctx.canvas.width, ctx.canvas.height)
    ctx.beginPath()
    posx = 0
    posy = 0
    rot = 0
    penstate = true
    color = "#000000"
    ctx.strokeStyle = color
    ctx.moveTo(convertXCoord(posx),convertYCoord(posy))
}
clear()

function forward(distance){
  ctx.beginPath()
  ctx.moveTo(convertXCoord(posx), convertYCoord(posy))
  posx = posx + distance*Math.sin(rot)
  posy = posy + distance*Math.cos(rot)
  if (penstate){
  	ctx.lineTo(convertXCoord(posx), convertYCoord(posy))
  }
  else{
    ctx.moveTo(convertXCoord(posx), convertYCoord(posy))
  }
  ctx.stroke()
}

function backward(distance){
  forward(-distance)
}

function right(deg){
  rot = rot + (Math.PI * deg/180)
}

function left(deg){
  right(-deg)
}

function penup(){
  penstate = false
}

function pendown(){
  penstate = true
}

function setcolor(clr){
  color = clr
  ctx.strokeStyle = color
}

function goto(x, y){
  ctx.beginPath()
  ctx.moveTo(convertXCoord(posx), convertYCoord(posy))
  posx = x
  posy = y
  if (penstate){
  	ctx.lineTo(convertXCoord(posx), convertYCoord(posy))
  }
  else{
    ctx.moveTo(convertXCoord(posx), convertYCoord(posy))
  }
  ctx.stroke()
}

function setrot(rotation){
  rot = (Math.PI * rotation/180)
}

