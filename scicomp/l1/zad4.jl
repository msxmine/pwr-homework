x = Float64(1.0)

while (x * (Float64(1.0)/x)) == Float64(1.0)
    global x = nextfloat(x)
end
println(bitstring(x))
println(x)
println((x * (Float64(1.0)/x)))

#Mozna to zrobic lepiej http://www-math.mit.edu/~edelman/homepage/papers/ieee.pdf
#Jednak obecne komputery rozwiącują brute-force dla Float64 w mniej niż minutę

