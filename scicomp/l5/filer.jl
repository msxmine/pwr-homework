module blockhelper

import Main.sparse
import Main.blocksys

export createBSideWithOnes
export solveProblem
export userepoint
export getIdPermut

function readArrFromFile(filename::String)::sparse.MyArr
    filepath = string("./", filename)
    arrfile = open(filepath)
    arrspec = split(readline(arrfile), " ")
    arrsiz = parse(Int64, arrspec[1])
    blocksiz = parse(Int64, arrspec[2])

    res = sparse.createEmpty(arrsiz,blocksiz, false)
    for ln in eachline(arrfile)
        ldata = split(ln, " ")
        y = parse(Int64, ldata[1])
        x = parse(Int64, ldata[2])
        num = parse(Float64, ldata[3])
        sparse.setVal(res, x, y, num)
    end
    close(arrfile)
    return res
end

function readCoefFromFile(filename::String)::Matrix{Float64}
    filepath = string("./", filename)
    coeffile = open(filepath)
    bsizstr = readline(coeffile)
    bsiz = parse(Int64, bsizstr)
    res = zeros(Float64, (bsiz, 1))
    idx = 1
    for ln in eachline(coeffile)
        res[idx] = parse(Float64, ln)
        idx += 1
    end
    close(coeffile)
    return res
end

function getIdPermut(last::Int64)::Vector{Int64}
    res = Vector{Int64}()
    for i = 1:last
        push!(res, i)
    end
    return res
end

function createBSideWithOnes(arr::sparse.MyArr)::Matrix{Float64}
    res = zeros(Float64, (length(arr.rows),1))
    for linidx = 1:length(arr.rows)
        res[linidx] = sum(arr.rows[linidx].elements)
    end
    return res
end

function createBSideWithRising(arr::sparse.MyArr)::Matrix{Float64}
    res = zeros(Float64, (length(arr.rows),1))
    for linidx = 1:length(arr.rows)
        for cidx = arr.rows[linidx].offset+1:arr.rows[linidx].offset+length(arr.rows[linidx].elements)
            res[linidx] += sparse.getVal(arr, cidx, linidx)*Float64(cidx)
        end
    end
    return res
end

function writeResultToFile(result::Vector{Float64}, filename::String, oneserror)
    resfile = open(string("./", filename), "w")
    if oneserror == true
        errorsum = 0.0
        for i = 1:length(result)
            errorsum += abs(result[i]-1.0)
        end
        errorsum /= length(result)
        write(resfile, string(errorsum, "\n"))
    end
    for i = 1:length(result)
        write(resfile, string(result[i], "\n"))
    end
    close(resfile)
end

function solveProblem(arrsrc::sparse.MyArr, bsrc::Vector{Float64}, computelu::Bool, pivot::Bool)::Vector{Float64}
    arr = deepcopy(arrsrc)
    b = deepcopy(bsrc)
    if computelu == true
        lower = sparse.createEmpty(length(arr.rows), arr.subblocksize, true)
        permut = getIdPermut(length(arr.rows))
        blocksys.luDecomp(arr, lower, permut, pivot)
        blocksys.luCalc(arr, lower, permut, b)
        return b
    else
        blocksys.solveMatrixEq(arr, b, pivot)
        return b
    end
end

#filer.jl MacierzA.txt metoda wyborElementu wynik.txt (stronaB.txt)
# metoda : 0 - Bezposredni Gauss
#          1 - Rozklad LU
# wyborElementu : 0 - Bez zamiany rzedow
#                 1 - Czesciowy wybor
function userepoint()
    myarr = readArrFromFile(ARGS[1])
    method = (parse(Int64, ARGS[2]) == 1)
    piv = (parse(Int64, ARGS[3]) == 1)
    outfil = ARGS[4]
    if length(ARGS) > 4
        bsid = vec(readCoefFromFile(ARGS[5]))
        outerr = false
    else
        bsid = vec(createBSideWithOnes(myarr))
        outerr = true
    end
    resul = solveProblem(myarr, bsid, method, piv)
    writeResultToFile(resul, outfil, outerr)
end

end
