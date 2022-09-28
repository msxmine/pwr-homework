include("z1234.jl")
using .wielNew
using Plots

function wartoscWielNatu(wielomian, punkt)
    faclen = length(wielomian)
    result = 0.0
    for i in 0:faclen-1
        result += wielomian[i+1]*(punkt^i)
    end
    return result
end

function drawByNatu(f, a::Float64, b::Float64, n::Int)
    h = (b-a)/n
    keypoints = Vector{Float64}(undef,0)
    for k in 0:n
        append!(keypoints, a+(k*h))
    end
    fvals = Vector{Float64}(undef,0)
    for k in 1:n+1
        append!(fvals, f(keypoints[k]))
    end
    ilorazy = ilorazyRoznicowe(keypoints, fvals)
    wcooef = naturalna(keypoints, ilorazy)
    w(x) = wartoscWielNatu(wcooef, x)
    plot!(w, label = "Wielomian (Postac naturalna)")
end

h(x) = x
h2(x) = x^2
h21(x) = x^21
s(x) = sin(x)

functions = [h, h2, h21, s]
for fun in functions
    rysujNnfx(fun, -10.0, 10.0, 10)
    drawByNatu(fun, -10.0, 10.0, 10)
    savefig(string("test", fun, ".png"))
end
