function nextit(r, prev)
    return prev + r*prev*(1.0 - prev)
end

function nextitfl(r, prev)
    return Float32(Float32(prev) + Float32(Float32(r)*Float32(prev)*Float32(1.0f0 - Float32(prev))))
end

function recsol(n)
    return -(2.0/3.0)*(cos((2.0^n)*acos(197.0/200.0))-1.0)
end

start = 0.01
r = 3.0

current = start

for i in 1:40
    global current = nextit(r, current)
    println(i , " ", current)
end

println("Zmienione")

current = 0.722

for i in 11:40
    global current = nextit(r, current)
    println(i, " ", current)
end

println("Symboliczne")
for i in 1:40
    println(i, " ", recsol(i))
end

#F32

startfl = 0.01f0
rfl = 3.0f0

currentfl = startfl

for i in 1:40
    global currentfl = nextitfl(rfl, currentfl)
    println(i , " ", currentfl)
end

println("Zmienione")

currentfl = 0.722f0

for i in 11:40
    global currentfl = nextitfl(rfl, currentfl)
    println(i, " ", currentfl)
end

