include("zad1.jl")
include("zad2.jl")
include("zad3.jl")

using .zad1
using .zad2
using .zad3

f1(x) = (MathConstants.e^(1.0-x)) - 1.0
f2(x) = x*(MathConstants.e^(-x))

df1(x) = (-MathConstants.e^(1-x))
df2(x) = (-MathConstants.e^-x)*(x-1)

println(mbisekcji(f1, 0.9, 1.2, 10.0^-5.0, 10.0^-5.0))
println(mstycznych(f1, df1, 0.9, 10.0^-5.0, 10.0^-5.0, 9999))
println(msiecznych(f1, 0.9, 1.2, 10.0^-5.0, 10.0^-5.0, 9999))

println(mbisekcji(f2, -0.2, 0.1, 10.0^-5.0, 10.0^-5.0))
println(mstycznych(f2, df2, 0.1, 10.0^-5.0, 10.0^-5.0, 9999))
println(msiecznych(f2, -0.2, 0.1, 10.0^-5.0, 10.0^-5.0, 9999))

println(mstycznych(f1, df1, 1.5, 10.0^-5.0, 10.0^-5.0, 999))
println(mstycznych(f2, df2, 1.5, 10.0^-5.0, 10.0^-5.0, 999))
println(mstycznych(f2, df2, 1.0, 10.0^-5.0, 10.0^-5.0, 999))
