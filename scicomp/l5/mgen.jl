module matrixgen

using LinearAlgebra
import Main.sparse

export blockmat
export blockmatvar

function matcond(n::Int, c::Float64)::Matrix{Float64}
    (U,S,V) = svd(rand(n,n))
    return U*diagm(0 => [LinRange(1.0,c,n);])*V'
end

function blockmat(n::Int, l::Int, ck::Float64, outputfile::String)
    nb = div(n,l)
    open(outputfile, "w") do f
        println(f, n, " ", l)
        for k in 1:nb
            Ak = matcond(l, ck)
            for i in 1:l, j in 1:l
                println(f, (k-1)*l+i, " ", (k-1)*l+j, " ", Ak[i,j])
            end
            if k < nb
                for i in 1:l
                    println(f, (k-1)*l+i, " ", k*l+i, " ", 0.3*rand())
                end
            end
            if k > 1
                for i in 1:l
                    println(f, (k-1)*l+i, " ", (k-1)*l-1, " ", 0.3*rand())
                    println(f, (k-1)*l+i, " ", (k-1)*l, " ", 0.3*rand())
                end
            end
        end
    end
end

function blockmatvar(n::Int, l::Int, ck::Float64)::sparse.MyArr
    res = sparse.createEmpty(n, l, false)
    nb = div(n,l)

    for k in 1:nb
        Ak = matcond(l, ck)
        for i in 1:l, j in 1:l
            sparse.setVal(res, (k-1)*l+j, (k-1)*l+i, Ak[i,j])
        end
        if k < nb
            for i in 1:l
                sparse.setVal(res, k*l+i, (k-1)*l+i, 0.3*rand())
            end
        end
        if k > 1
            for i in 1:l
                sparse.setVal(res, (k-1)*l-1, (k-1)*l+i, 0.3*rand())
                sparse.setVal(res, (k-1)*l, (k-1)*l+i, 0.3*rand())
            end
        end
    end

    return res
end

end
