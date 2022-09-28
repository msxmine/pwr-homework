using LinearAlgebra

function hilb(n::Int)
    return [1 / (i + j - 1) for i in 1:n, j in 1:n]
end

function matcond(n::Int, c::Float64)
    (U,S,V) = svd(rand(n,n))
    return U*diagm(0 => [LinRange(1.0,c,n);])*V'
end

function reserror(result)
    leng = size(result)
    goodres = ones(Float64, leng)
    dif = result - goodres
    return norm(dif)/norm(goodres)
end


#Hilbert n 2 do 30
for n in 2:30
    A = hilb(n)
    xreal = ones(Float64, n)
    b = A * xreal

    x1 = A\b
    x2 = inv(A)*b
    println(n, " ", cond(A), " ", reserror(x1), " ", reserror(x2))
end


#Losowe
randsizes = [5,10,20]
ransc = [1.0, 10.0, 10.0^3.0, 10.0^7.0, 10.0^12.0, 10.0^16.0]

for n in randsizes
    for c in ransc
        A = matcond(n,c)
        xreal = ones(Float64, n)
        b = A * xreal
    
        x1 = A\b
        x2 = inv(A)*b
        println(n, " ", c, " ", reserror(x1), " ", reserror(x2))
    end
end
