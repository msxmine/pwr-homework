module wielNew

export ilorazyRoznicowe
export warNewton
export naturalna
export rysujNnfx

using Plots

function ilorazyRoznicoweRekursywne(x::Vector{Float64}, f::Vector{Float64})
    n = length(x)
    if n == 1
        return [f[1]]
    end
    shorter = ilorazyRoznicowe(x[1:n-1], f[1:n-1])
    offset = ilorazyRoznicowe(x[2:n], f[2:n])
    myval = (offset[n-1] - shorter[n-1])/(x[n]-x[1])
    mystack = vcat(shorter, [myval])
    return mystack
end

function ilorazyRoznicowe(x::Vector{Float64}, f::Vector{Float64})
    n = length(x)
    calcs = Vector{Float64}(undef,0)
    results = Vector{Float64}(undef,0)

    for delta in 0:n-1
        for start in 1:n-delta
            endstop = start+delta
            if start == endstop
                append!(calcs, f[start])
                if start == 1
                    append!(results, f[start])
                end
            else
                curlast = length(calcs)
                addr = curlast-(n-delta)
                vall = (calcs[addr+1]-calcs[addr])/(x[endstop] - x[start])
                append!(calcs, vall)
                if start == 1
                    append!(results, vall)
                end
            end
        end
    end

    return results
end

function warNewton(x::Vector{Float64}, fx::Vector{Float64}, t::Float64)
    n = length(x)
    wynik = fx[n]
    for i in n-1:-1:1
        wynik = fx[i] + ((t-x[i])*wynik)
    end
    return wynik
end

function naturalna(x::Vector{Float64}, fx::Vector{Float64})
    n = length(x)
    result = zeros(n)
    result[1] = fx[n]
    for i in n-1:-1:1
        shifted = copy(result[1:n-1])
        result *= (-x[i])
        result[2:n] += shifted
        result[1] += fx[i]
    end
    return result
end

function rysujNnfx(f, a::Float64, b::Float64, n::Int)
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
    w(x) = warNewton(keypoints, ilorazy, x)

    plot(f, a, b, label = "Funkcja")
    xlabel!(string("N=",n))
    plot!(w, label = "Wielomian")
end

end
