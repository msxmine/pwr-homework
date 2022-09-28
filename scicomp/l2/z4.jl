using Polynomials

myrtseq = collect(Int128, 1:20)
P = fromroots(Polynomial{Float64},myrtseq)
calcres = roots(P)

function p(x, rts)
    result = 1.0
    for i in 1:20
        result = result * (x - rts[i])
    end
    return result
end

for i in 1:20
    println(abs(P(calcres[i])), " ,", abs(p(calcres[i], myrtseq)), " ,", abs(calcres[i]-i))
end

#b
println("Zmiana")
P[19] = -210.0 - (2.0^(-23.0))
calcres = roots(P)

for i in 1:20
    println(abs(P(Float64(i))), " ,", abs(calcres[i]-i), " ,", calcres[i])
end
