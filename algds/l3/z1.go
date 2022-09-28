package main

import (
    "fmt"
    "math/rand"
    "os"
)

var ncomp = 0
var nswap = 0

func insort( arr []int, start int, end int){
    for i := start+1; i <= end; i++ {
        tosort := arr[i]
        j := i-1
        for ; j >= start ; j-- {
            ncomp++
            fmt.Fprintln(os.Stderr, "compare", arr[j], tosort)
            if arr[j] > tosort {
                arr[j+1] = arr[j]
                nswap++
                fmt.Fprintln(os.Stderr, "slide forward", arr[j])
            } else {
                break
            }
        }
        arr[j+1] = tosort
        nswap++
        fmt.Fprintln(os.Stderr, "insert", tosort, "at idx", j+1)
    }
}

func medpivot(arr []int, start int, end int, glen int) int{
    if end - start < 5 {
        insort(arr, start, end)
        return (start + end)/2
    }
    for i := start; i <= end; i+= 5 {
        blockend := i+4
        if blockend > end {
            blockend = end
        }
        insort(arr, i, blockend)
        arr[(i+blockend)/2], arr[start+((i-start)/glen)] = arr[start+((i-start)/glen)], arr[(i+blockend)/2]
        nswap++
        fmt.Fprintln(os.Stderr, "swap median to front", arr[start+((i-start)/glen)], "to idx", start+((i-start)/glen))
    }
    return qselect(arr, start, start + ((end-start)/5), ((((end-start)/5)+1)/2)+start, medpivot)
}

func randompivot(arr []int, start int, end int, glen int) int{
    return start + rand.Intn((end-start)+1)
}

func qselect(arr []int, start int, end int, k int, pivfun func([]int, int, int, int) int) int{
    if start == end {
        return start
    }
    pividx := pivfun(arr, start, end, 5)
    pivval := arr[pividx]
    fmt.Fprintln(os.Stderr, "pivot idx", pividx, "val", pivval )
    arr[pividx], arr[end] = arr[end], arr[pividx]
    nswap++
    fmt.Fprintln(os.Stderr, "swap pivot to end", pivval, "to idx", end )
    
    swapslot := start
    for i := start; i < end; i++ {
        ncomp++
        fmt.Fprintln(os.Stderr, "compare with pivot", arr[i], pivval )
        if arr[i] < pivval {
            nswap++
            fmt.Fprintln(os.Stderr, "move to lesser swap idx", i, "and", swapslot)
            arr[i], arr[swapslot] = arr[swapslot], arr[i]
            swapslot++
        }
    }
    firstpividx := swapslot
    for i := swapslot; i < end; i++ {
        ncomp++
        fmt.Fprintln(os.Stderr, "compare to pivot", arr[i], pivval )
        if arr[i] == pivval {
            nswap++
            fmt.Fprintln(os.Stderr, "move to equal swap idx", i, "and", swapslot)
            arr[i], arr[swapslot] = arr[swapslot], arr[i]
            swapslot++
        }
    }
    nswap++
    fmt.Fprintln(os.Stderr, "swap pivot back to idx", swapslot)
    arr[end], arr[swapslot] = arr[swapslot], arr[end]
    if k < firstpividx {
        return qselect(arr, start, firstpividx-1, k, pivfun)
    }
    if k > swapslot {
        return qselect(arr, swapslot+1, end, k, pivfun)
    }
    return k;
    
}

func main(){
    mode := os.Args[1]
    var n int
    var k int
    fmt.Scan(&n)
    fmt.Scan(&k)
    
    input := make([]int, n)
    if mode == "-r" {
        for i := 0; i < n; i++ {
            input[i] = rand.Int()
        }
    } else {
        for i := 0; i < n; i++ {
            input[i] = i+1
        }
        rand.Shuffle(n, func(i,j int){
            input[i], input[j] = input[j], input[i]
        })
    }
    
    var ninput = make([]int, n)
    copy(ninput, input)
    ncomp = 0
    nswap = 0
    fmt.Fprintln(os.Stderr, "input ", ninput)
    fmt.Fprintln(os.Stderr, "k ", k)
    var answer = qselect(ninput, 0, n-1, k-1, randompivot)
    fmt.Fprintln(os.Stderr, "comparisons", ncomp, "moves", nswap)
    for i := 0; i < n; i++ {
        if i == answer {
            fmt.Print("[", ninput[i], "] ")
        } else {
            fmt.Print(ninput[i], " ")
        }
    }
    fmt.Println("")
    
    copy(ninput, input)
    ncomp = 0
    nswap = 0
    fmt.Fprintln(os.Stderr, "input ", ninput)
    fmt.Fprintln(os.Stderr, "k ", k)
    answer = qselect(ninput, 0, n-1, k-1, medpivot)
    fmt.Fprintln(os.Stderr, "comparisons", ncomp, "moves", nswap)
    fmt.Println(input[answer])
    for i := 0; i < n; i++ {
        if i == answer {
            fmt.Print("[", ninput[i], "] ")
        } else {
            fmt.Print(ninput[i], " ")
        }
    }
    fmt.Println("")
}
    
