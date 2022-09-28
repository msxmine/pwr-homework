module zad3

export msiecznych

function msiecznych(f, x0::Float64, x1::Float64, delta::Float64, epsilon::Float64, maxit::Int)
    a = x0
    b = x1
    fa = f(a)
    fb = f(b)
    for k = 1:maxit
        if abs(fa) > abs(fb)
            a,b = b,a
            fa,fb = fb,fa
        end
        s = (b-a)/(fb-fa)
        a = b
        fa = fb
        b = b - (fb*s)
        fb = f(b)
        if abs(b-a) < delta || abs(fb) < epsilon
            return (b,fb,k,0)
        end
    end
    return (b,fb,maxit,1)
end

end
