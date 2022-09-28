include("z1234.jl")
using .wielNew
using Plots

prza(x) = MathConstants.e^x
for n in [5,10,15]
    rysujNnfx(prza, 0.0, 1.0, n)
    savefig(string("z5a_n", n, ".png"))
end

przb(x) = (x^2.0)*(sin(x))
for n in [5,10,15]
    rysujNnfx(przb, -1.0, 1.0, n)
    savefig(string("z5b_n", n, ".png"))
end

przc(x) = abs(x)
for n in [5,10,15]
    rysujNnfx(przc, -1.0, 1.0, n)
    savefig(string("z6a_n", n, ".png"))
end

przd(x) = 1.0/(1+(x^2.0))
for n in [5,10,15]
    rysujNnfx(przd, -5.0, 5.0, n)
    savefig(string("z6b_n", n, ".png"))
end
