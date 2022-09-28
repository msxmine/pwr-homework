f(x) = sin(x) + cos(3.0 * x)
fder(x) = cos(x) - (3.0 * sin(3.0*x))

for i in 0:54
    h = 2.0^(-i)
    approx = (f(1.0 + h) - f(1.0))/h
    error = abs(approx - fder(1.0))
    print(approx, ",")
    print(1.0 + h, ",")
    println(error)
end
