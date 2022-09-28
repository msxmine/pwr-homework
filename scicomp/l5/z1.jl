module blocksys

import Main.sparse

export solveMatrixEq
export luDecomp
export luCalc

function calcTrianglBlock(arr::sparse.MyArr, b::Vector{Float64})
    for cline = length(arr.rows):-1:1
        multiplier = sparse.getVal(arr, cline, cline)
        sparse.multiplyRow(arr, cline, 1.0/multiplier)
        b[cline] /= multiplier
        for cidx = cline+1:min(cline+(3*arr.subblocksize), length(arr.rows))
            submulti = sparse.getVal(arr, cidx, cline)
            if submulti != 0.0
                sparse.addRowMultiple(arr, cline, cidx, -submulti)
                sparse.setVal(arr, cidx, cline, 0.0)
                b[cline] -= (submulti*b[cidx])
            end
        end
    end
end

function calcTrianglBlockRev(arr::sparse.MyArr, b::Vector{Float64})
    for cline = 1:length(arr.rows)
        for cidx = cline-1:-1:max(cline-(3*arr.subblocksize), 1)
            submulti = sparse.getVal(arr, cidx, cline)
            if submulti != 0.0
                sparse.addRowMultiple(arr, cline, cidx, -submulti)
                sparse.setVal(arr, cidx, cline, 0.0)
                b[cline] -= (submulti*b[cidx])
            end
        end
    end
end

function solveBlock(arr::sparse.MyArr, b::Vector{Float64}, startrow::Int64, endrow::Int64, endsolv::Int64, elglowny::Bool)
    for solvingline = startrow:endsolv
        bestcandidx = solvingline
        bestcandval = abs(sparse.getVal(arr, solvingline, bestcandidx))
        if elglowny == true
            for newcand = solvingline:endrow
                candval = abs(sparse.getVal(arr, solvingline, newcand))
                if candval > bestcandval
                    bestcandval = candval
                    bestcandidx = newcand
                end
            end
        end
        sparse.swapRows(arr, bestcandidx, solvingline)
        b[bestcandidx], b[solvingline] = b[solvingline], b[bestcandidx]

        for lower = solvingline+1:endrow
            linefact = (sparse.getVal(arr, solvingline, lower)/sparse.getVal(arr, solvingline, solvingline))
            sparse.addRowMultiple(arr, lower, solvingline, -linefact)
            sparse.setVal(arr, solvingline, lower, 0.0)
            b[lower] -= b[solvingline] * linefact
        end
    end
end

function solveMatrixEq(arr::sparse.MyArr, b::Vector{Float64}, elglowny::Bool)
    curstart = -1
    while curstart <= length(arr.rows)
        start = max(1,curstart)
        curendp = (curstart + (arr.subblocksize-1))
        endp = min(length(arr.rows), curendp+2)
        endsolv = min(length(arr.rows), curendp)
        solveBlock(arr, b, start, endp, endsolv, elglowny)
    curstart += arr.subblocksize
    end
    calcTrianglBlock(arr, b)
end

function luDecompBlock(arr::sparse.MyArr, larr::sparse.MyArr, permut::Vector{Int64}, startrow::Int64, endrow::Int64, endsolv::Int64, elglowny::Bool)
    for solvingline = startrow:endsolv
        bestcandidx = solvingline
        bestcandval = abs(sparse.getVal(arr, solvingline, bestcandidx))
        if elglowny == true
            for newcand = solvingline:endrow
                candval = abs(sparse.getVal(arr, solvingline, newcand))
                if candval > bestcandval
                    bestcandval = candval
                    bestcandidx = newcand
                end
            end
        end
        sparse.swapRows(arr, bestcandidx, solvingline)
        sparse.swapRows(larr, bestcandidx, solvingline)
        permut[bestcandidx], permut[solvingline] = permut[solvingline], permut[bestcandidx]
        sparse.setVal(larr, solvingline, solvingline, 1.0)

        for lower = solvingline+1:endrow
            linefact = (sparse.getVal(arr, solvingline, lower)/sparse.getVal(arr, solvingline, solvingline))
            sparse.setVal(larr, solvingline, lower, linefact)
            sparse.addRowMultiple(arr, lower, solvingline, -linefact)
            sparse.setVal(arr, solvingline, lower, 0.0)
        end
    end
end

function luDecomp(arr::sparse.MyArr, larr::sparse.MyArr, permut::Vector{Int64}, elglowny::Bool)
    curstart = -1
    while curstart <= length(arr.rows)
        start = max(1,curstart)
        curendp = (curstart + (arr.subblocksize-1))
        endp = min(length(arr.rows), curendp+2)
        endsolv = min(length(arr.rows), curendp)
        luDecompBlock(arr, larr, permut, start, endp, endsolv, elglowny)
    curstart += arr.subblocksize
    end
end

function luCalc(upper::sparse.MyArr, lower::sparse.MyArr, permut::Vector{Int64}, b::Vector{Float64})
    bcp = copy(b)
    for i = 1:length(permut)
        b[i] = bcp[permut[i]]
    end
    calcTrianglBlockRev(lower, b)
    calcTrianglBlock(upper, b)
end

end
