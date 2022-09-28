start = Float64(1.0)
prev = start
for i in 1:3
    global start = nextfloat(start)
    println(start)
    println(start-prev)
    println(bitstring(start))
    global prev = start
end

start = Float64(2.0)
prev = start
for i in 1:3
    global start = prevfloat(start)
    println(start)
    println(prev-start)
    println(bitstring(start))
    global prev = start
end

println(xor(reinterpret(UInt64, Float64(1.0)), reinterpret(UInt64,prevfloat(Float64(2.0)))))
println((2 ^ 52) - 1)


#
start = Float64(0.5)
prev = start
for i in 1:3
    global start = nextfloat(start)
    println(start)
    println(start-prev)
    println(bitstring(start))
    global prev = start
end

start = Float64(1.0)
prev = start
for i in 1:3
    global start = prevfloat(start)
    println(start)
    println(prev-start)
    println(bitstring(start))
    global prev = start
end

println(xor(reinterpret(UInt64, Float64(0.5)), reinterpret(UInt64,prevfloat(Float64(1.0)))))
println((2 ^ 52) - 1)
println(xor(reinterpret(UInt64, Float64(2.0)), reinterpret(UInt64,prevfloat(Float64(4.0)))))
println((2 ^ 52) - 1)
