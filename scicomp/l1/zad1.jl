#Epsilon maszynowy
macheps = Float16(1.0)
result = macheps
while Float16(1.0) + macheps > Float16(1.0)
    global result = macheps
    global macheps = macheps / Float16(2.0)
end
println(result)
println(eps(Float16))

macheps = Float32(1.0)
result = macheps
while Float32(1.0) + macheps > Float32(1.0)
    global result = macheps
    global macheps = macheps / Float32(2.0)
end
println(result)
println(eps(Float32))

macheps = Float64(1.0)
result = macheps
while Float64(1.0) + macheps > Float64(1.0)
    global result = macheps
    global macheps = macheps / Float64(2.0)
end
println(result)
println(eps(Float64))

#eta > 0
minim = Float16(1.0)
result = minim
while minim > Float16(0.0)
    global result = minim
    global minim = minim / Float16(2.0)
end

println(result)
println(nextfloat(Float16(0.0)))

minim = Float32(1.0)
result = minim
while minim > Float32(0.0)
    global result = minim
    global minim = minim / Float32(2.0)
end

println(result)
println(nextfloat(Float32(0.0)))

minim = Float64(1.0)
result = minim
while minim > Float64(0.0)
    global result = minim
    global minim = minim / Float64(2.0)
end

println(result)
println(nextfloat(Float64(0.0)))

#Floatmin

println(floatmin(Float16))
println(floatmin(Float32))
println(floatmin(Float64))

#Floatmax
start = prevfloat(Float16(2.0))
#Wersja bez prevfloat, uzywajaca znanych nam juz stalych
#start  = Float16(2.0) - eps(Float16)
result = start
while !isinf(start)
    global result = start
    global start = start * Float16(2.0)
end

println(result)
println(floatmax(Float16))

start = prevfloat(Float32(2.0))
result = start
while !isinf(start)
    global result = start
    global start = start * Float32(2.0)
end

println(result)
println(floatmax(Float32))


start = prevfloat(Float64(2.0))
result = start
while !isinf(start)
    global result = start
    global start = start * Float64(2.0)
end

println(result)
println(floatmax(Float64))

