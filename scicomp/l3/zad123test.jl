include("zad1.jl")
include("zad2.jl")
include("zad3.jl")

using .zad1
using .zad2
using .zad3

f1(x) = (1.0 ./ (1.0 .+ exp(-x))) - 0.5
g1(x) = sin(x)
h1(x) = x^3.0

println(mbisekcji(f1,-0.5,0.6,0.0001,0.0001))
println(mbisekcji(g1,-0.5,0.6,0.0001,0.0001))
println(mbisekcji(h1,-0.5,0.6,0.0001,0.0001))
println(mbisekcji(h1,0.5,1.6,0.0001,0.0001))

f2(x) = (MathConstants.e^x)-1.0
pf2(x) = (MathConstants.e^x)
g2(x) = (0.5*x)^2.0 + sin(x)
pg2(x) = (0.5*x) + cos(x)
h2(x) = x^3.0 + x^2.0 + x
ph2(x) = 3.0*(x^2.0) + 2.0*x + 1.0

println(mstycznych(f2,pf2,2.0,0.0001,0.0001,99))
println(mstycznych(f2,pf2,90.0,0.0001,0.0001,99))
println(mstycznych(f2,pf2,90.0,0.0001,0.0001,50))
println(mstycznych(g2,pg2,0.1,0.0001,0.0001,99))
println(mstycznych(h2,ph2,0.1,0.0001,0.0001,99))

println(msiecznych(f2, 0.1, 0.3, 0.0001, 0.0001, 99))
println(msiecznych(f2, -0.1, 0.1, 0.0001, 0.0001, 99))
println(msiecznych(f2, 3.0, 2.0, 0.0001, 0.0001, 50))
println(msiecznych(f2, 3.0, 2.0, 0.0001, 0.0001, 99))
println(msiecznych(g2, 0.1, 1.0, 0.0001, 0.0001, 10))
println(msiecznych(h2, 0.1, -1.0, 0.0001, 0.0001, 10))
