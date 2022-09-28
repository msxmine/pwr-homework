f(x) = sqrt(x^2 + 1) - 1
g(x) = x^2 / (sqrt(x^2 + 1) + 1)

for i in -1:-1:-10
    println(f(Float64(8)^i))
    println(g(Float64(8)^i))
end
