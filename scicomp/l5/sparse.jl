module sparse

export MyArrRow
export MyArr
export createEmpty
export swapRows
export multiplyRow
export addRowMultiple
export optimizeRow
export setVal
export getVal

struct MyArrRow
    elements::Vector{Float64}
    offset::Int64
end
Base.deepcopy(m::MyArrRow) = MyArrRow(deepcopy(m.elements), m.offset)

struct MyArr
    rows::Vector{MyArrRow}
    subblocksize::Int64
end
Base.deepcopy(m::MyArr) = MyArr(deepcopy(m.rows), m.subblocksize)

function createEmpty(siz::Int64, bsiz::Int64, lower::Bool)::MyArr
    newrows = Vector{MyArrRow}()
    newarr = MyArr(newrows, bsiz)
    for ridx = 1:siz
        #els = Vector{Float64}()
        els = zeros(Float64, 5*bsiz)
        bidx = div(ridx-1, bsiz)+1
        newofs = max(((bidx-2)*bsiz)-2, 0)
        if lower == true
            newofs = max(ridx-3*bsiz-1, 0)
        end
        nrow = MyArrRow(els, newofs)
        push!(newarr.rows, nrow)
    end
    return newarr
end

function swapRows(arr::MyArr, y1::Int64, y2::Int64)
    arr.rows[y1], arr.rows[y2] = arr.rows[y2], arr.rows[y1]
end

function multiplyRow(arr::MyArr, yidx::Int64, scalar::Float64)
    #arr.rows[yidx].elements *= scalar
    for i = 1:length(arr.rows[yidx].elements)
        arr.rows[yidx].elements[i] *= scalar
    end
    #optimizeRow(arr, yidx)
end

function addRowMultiple(arr::MyArr, ytarget::Int64, ysrc::Int64, scalar::Float64)
    for colidx = arr.rows[ysrc].offset+1:arr.rows[ysrc].offset+length(arr.rows[ysrc].elements)
        cellres = getVal(arr, colidx, ytarget)
        delta = (getVal(arr, colidx, ysrc) * scalar)
        if delta != 0.0
            cellres += delta
            setVal(arr, colidx, ytarget, cellres)
        end
    end
    #optimizeRow(arr, ytarget)
end

function optimizeRow(arr::MyArr, ridx::Int64)
    idx = 0
    while arr.rows[ridx].elements[idx+1] == 0
        idx += 1
    end
    deleteat!(arr.rows[ridx].elements, 1:idx)
    arr.rows[ridx].offset += idx
    idx = length(arr.rows[ridx].elements) + 1
    endp = idx-1
    while arr.rows[ridx].elements[idx-1] == 0
        idx -= 1
    end
    deleteat!(arr.rows[ridx].elements, idx:endp)
end

function setVal(arr::MyArr, x::Int64, y::Int64, val::Float64)
    roffset = arr.rows[y].offset
    rlen = length(arr.rows[y].elements)
    toopt = false
    if x <= roffset
        trailen = ((roffset+1)-x)
        trail = zeros(Float64, trailen)
        append!(arr.rows[y].elements, trail)
        arr.rows[y].elements = circshift(arr.rows[y].elements, (trailen))
        arr.rows[y].offset -= trailen
        toopt = true
    elseif x > (roffset+rlen)
        trail = zeros(Float64, (x-(roffset+rlen)))
        append!(arr.rows[y].elements, trail)
        toopt = true
    end
    arr.rows[y].elements[x-arr.rows[y].offset] = val
    if toopt == true
        optimizeRow(arr, y)
    end
end

function getVal(arr::MyArr, x::Int64, y::Int64)::Float64
    offs = arr.rows[y].offset
    if (x-offs) < 1 || (x-offs) > length(arr.rows[y].elements)
        return 0.0
    else
        return arr.rows[y].elements[x-offs]
    end
end

end
