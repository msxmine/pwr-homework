include("zad1.jl")

using .zad1

f(x) = (3*x) - (MathConstants.e^x)

println(mbisekcji(f,1.0,3.0,10.0^-4.0,10.0^-4.0))
println(mbisekcji(f,-3.0,1.0,10.0^-4.0,10.0^-4.0))
