module zad1

export mbisekcji

function mbisekcji(f, a::Float64, b::Float64, delta::Float64, epsilon::Float64)
    u = f(a)
    v = f(b)
    e = b - a
    iter = 0
    if u*v > 0
        return (0.0,0.0,0,1)
    else
        while true
            iter += 1
            e /= 2.0
            c = a + e
            w = f(c)
            if abs(e) < delta || abs(w) < epsilon
                return (c,w,iter,0)
            end
            if w*u < 0.0
                b = c
                v = w
            else
                a = c
                u = w
            end
        end
    end
end

end
