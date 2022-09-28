module zad2

export mstycznych

function mstycznych(f,pf,x0::Float64, delta::Float64, epsilon::Float64, maxit::Int)
    v = f(x0)
    if abs(v) < epsilon
        return (x0,v,0,0)
    end
    for i = 1:maxit
        x1 = x0 - (v/pf(x0))
        if abs(x1) == Inf
            return (x1,0.0,i,2)
        end
        v = f(x1)
        if abs(x1-x0) < delta || abs(v) < epsilon
            return (x1,v,i,0)
        end
        x0 = x1
    end
    return (x0,v,maxit,1)
end

end
