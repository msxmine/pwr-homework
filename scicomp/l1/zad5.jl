x = Vector{Float64}([2.718281828, -3.141592654, 1.414213562, 0.5772156649, 0.3010299957])
y = Vector{Float64}([1486.2497, 878366.9879, -22.37492, 4773714.647, 0.000185049])

result = Float64(0.0)
for i in 1:5
    global result = result + (x[i]*y[i])
end
println(result)

result = Float64(0.0)
for i in 5:-1:1
    global result = result + (x[i]*y[i])
end
println(result)

negresult = Float64(0.0)
posresult = Float64(0.0)
temp = Vector{Float64}([0.0,0.0,0.0,0.0,0.0])
for i in 1:5
    temp[i] = x[i]*y[i]
end
sort!(temp, by=abs, rev=true)
for i in 1:5
    if temp[i] > Float64(0.0)
        global posresult = posresult + temp[i]
    else
        global negresult = negresult + temp[i]
    end
end
result = negresult + posresult
println(result)

negresult = Float64(0.0)
posresult = Float64(0.0)
temp = Vector{Float64}([0.0,0.0,0.0,0.0,0.0])
for i in 1:5
    temp[i] = x[i]*y[i]
end
sort!(temp, by=abs)
for i in 1:5
    if temp[i] > Float64(0.0)
        global posresult = posresult + temp[i]
    else
        global negresult = negresult + temp[i]
    end
end
result = negresult + posresult
println(result)


##F32

x = Vector{Float32}([2.718281828, -3.141592654, 1.414213562, 0.5772156649, 0.3010299957])
y = Vector{Float32}([1486.2497, 878366.9879, -22.37492, 4773714.647, 0.000185049])

result = Float32(0.0)
for i in 1:5
    global result = result + (x[i]*y[i])
end
println(result)

result = Float32(0.0)
for i in 5:-1:1
    global result = result + (x[i]*y[i])
end
println(result)

negresult = Float32(0.0)
posresult = Float32(0.0)
temp = Vector{Float32}([0.0,0.0,0.0,0.0,0.0])
for i in 1:5
    temp[i] = x[i]*y[i]
end
sort!(temp, by=abs, rev=true)
for i in 1:5
    if temp[i] > Float32(0.0)
        global posresult = posresult + temp[i]
    else
        global negresult = negresult + temp[i]
    end
end
result = negresult + posresult
println(result)

negresult = Float32(0.0)
posresult = Float32(0.0)
temp = Vector{Float32}([0.0,0.0,0.0,0.0,0.0])
for i in 1:5
    temp[i] = x[i]*y[i]
end
sort!(temp, by=abs)
for i in 1:5
    if temp[i] > Float32(0.0)
        global posresult = posresult + temp[i]
    else
        global negresult = negresult + temp[i]
    end
end
result = negresult + posresult
println(result)
