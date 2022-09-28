include("sparse.jl")
include("z1.jl")
include("filer.jl")
include("mgen.jl")

function solveProblemMeas(arrsrc::sparse.MyArr, bsrc::Vector{Float64}, computelu::Bool, pivot::Bool)::Tuple{Vector{Float64}, Vector{Float64}}
    arr = deepcopy(arrsrc)
    b = deepcopy(bsrc)
    times = Vector{Float64}()
    if computelu == true
        lower = sparse.createEmpty(length(arr.rows), arr.subblocksize, true)
        permut = blockhelper.getIdPermut(length(arr.rows))
        et = @elapsed blocksys.luDecomp(arr, lower, permut, pivot)
        push!(times, et)
        et = @elapsed blocksys.luCalc(arr, lower, permut, b)
        push!(times, et)
    else
        et = @elapsed blocksys.solveMatrixEq(arr, b, pivot)
        push!(times, et)
    end
    return b, times
end

function verifyResult(res::Vector{Float64})
    errsum = 0.0
    for i = 1:length(res)
        if (abs(res[i] - 1.0) > 0.001)
            error("Wynik bledny bardziej niz 0.1%")
        end
        errsum += abs(res[i] - 1.0)
    end
    errsum /= length(res)
    println("Blad wzgledny ", errsum)
end

function runtest()
    open("testseries3.txt", "w") do plik
        sizestotest = [10000, 100000]
        for n in sizestotest
            myarr = matrixgen.blockmatvar(n, 4, 5.0)
            bsid = vec(blockhelper.createBSideWithOnes(myarr))
            usedmem = @allocated res, tim = solveProblemMeas(myarr, bsid, false, false)
            verifyResult(res)
            println(plik, n, " ", 0, " ", 0, " ", usedmem, " ", tim[1])
            usedmem = @allocated res, tim = solveProblemMeas(myarr, bsid, false, true)
            verifyResult(res)
            println(plik, n, " ", 0, " ", 1, " ", usedmem, " ", tim[1])
            usedmem = @allocated res, tim = solveProblemMeas(myarr, bsid, true, false)
            verifyResult(res)
            println(plik, n, " ", 1, " ", 0, " ", usedmem, " ", tim[1], " ", tim[2])
            usedmem = @allocated res, tim = solveProblemMeas(myarr, bsid, true, true)
            verifyResult(res)
            println(plik, n, " ", 1, " ", 1, " ", usedmem, " ", tim[1], " ", tim[2])
        end
    end
end

runtest()
