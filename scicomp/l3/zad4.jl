include("zad1.jl")
include("zad2.jl")
include("zad3.jl")

using .zad1
using .zad2
using .zad3

f(x) = ( sin(x) - ((0.5*x)^2.0)  )
pf(x) = ( cos(x) - (0.5*x) )

println(mbisekcji(f,1.5,2.0,(0.5*(10.0^-5.0)),(0.5*(10.0^-5.0))))
println(mstycznych(f,pf,1.5,(0.5*(10.0^-5.0)),(0.5*(10.0^-5.0)),9999))
println(msiecznych(f,1.0,2.0,(0.5*(10.0^-5.0)),(0.5*(10.0^-5.0)),9999))

