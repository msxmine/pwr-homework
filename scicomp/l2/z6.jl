function step(prev,c)
    return prev^2.0 + c
end

start = [1.0, 2.0, 1.99999999999999, 1.0, -1.0, 0.75, 0.25]
cee = [-2.0, -2.0, -2.0, -1.0, -1.0, -1.0, -1.0]

for didx in 1:7
    x = start[didx]
    c = cee[didx]
    res = Vector{Float64}()
    append!(res, x)
    for i in 1:40
        x = step(x, c)
        append!(res, x)
    end
    println(res)
end

