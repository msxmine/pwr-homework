package main

import (
    "math/rand"
    "os"
    "bufio"
    "strconv"
    "time"
)

var ncomp = 0
var nswap = 0
var gfactor = 5

func insort( arr []int, start int, end int){
    for i := start+1; i <= end; i++ {
        tosort := arr[i]
        j := i-1
        for ; j >= start ; j-- {
            ncomp++
            if arr[j] > tosort {
                arr[j+1] = arr[j]
                nswap++
            } else {
                break
            }
        }
        arr[j+1] = tosort
        nswap++
    }
}

func medpivot(arr []int, start int, end int, glen int) int{
    if end - start < glen {
        insort(arr, start, end)
        return (start + end)/2
    }
    for i := start; i <= end; i+= glen {
        blockend := i+glen-1
        if blockend > end {
            blockend = end
        }
        insort(arr, i, blockend)
        arr[(i+blockend)/2], arr[start+((i-start)/glen)] = arr[start+((i-start)/glen)], arr[(i+blockend)/2]
        nswap++
    }
    return qselect(arr, start, start + ((end-start)/glen), ((((end-start)/glen)+1)/2)+start, medpivot)
}

func randompivot(arr []int, start int, end int, glen int) int{
    return start + rand.Intn((end-start)+1)
}

func qselect(arr []int, start int, end int, k int, pivfun func([]int, int, int, int) int) int{
    if start == end {
        return start
    }
    pividx := pivfun(arr, start, end, gfactor)
    pivval := arr[pividx]
    arr[pividx], arr[end] = arr[end], arr[pividx]
    nswap++
    
    swapslot := start
    for i := start; i < end; i++ {
        ncomp++
        if arr[i] < pivval {
            nswap++
            arr[i], arr[swapslot] = arr[swapslot], arr[i]
            swapslot++
        }
    }
    firstpividx := swapslot
    for i := swapslot; i < end; i++ {
        ncomp++
        if arr[i] == pivval {
            nswap++
            arr[i], arr[swapslot] = arr[swapslot], arr[i]
            swapslot++
        }
    }
    nswap++
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
    f, _ := os.Create("./z2out.txt")
    defer f.Close()
    fil := bufio.NewWriter(f)
    for n:= 100; n <= 10000; n+=100 {
        for m := 0; m < 100; m++ {
            karr := make([]int, 3)
            karr[0] = 30
            karr[1] = n/2
            karr[2] = n-30
            
            randdata := make([]int, n)
            rangedata := make([]int, n)
            input := make([]int, n)
            for i := 0; i < n; i++ {
                randdata[i] = rand.Int()
            }
            for i := 0; i < n; i++ {
                rangedata[i] = i+1
            }
            rand.Shuffle(n, func(i,j int){
                rangedata[i], rangedata[j] = rangedata[j], rangedata[i]
            })
            for kidx := 0; kidx < 3; kidx++ {
                for groups := 5; groups <= 25; groups += 2 {
                    gfactor = groups
                    k := karr[kidx]
                    ncomp = 0
                    nswap = 0
                    copy(input, randdata)
                    tstart := time.Now()
                    qselect(input, 0, n-1, k-1, medpivot)
                    exect := time.Since(tstart)
                    fil.WriteString("randdata " + strconv.Itoa(groups) + " " +strconv.Itoa(n) + " " + strconv.Itoa(kidx) + " " + strconv.Itoa(m) + " " + strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + "\n")
                    ncomp = 0
                    nswap = 0
                    copy(input, rangedata)
                    tstart = time.Now()
                    qselect(input, 0, n-1, k-1, medpivot)
                    exect = time.Since(tstart)
                    fil.WriteString("rangedata " + strconv.Itoa(groups) + " " +strconv.Itoa(n) + " " + strconv.Itoa(kidx) + " " + strconv.Itoa(m) + " " + strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + "\n")
                }
            }
            
        }
        fil.Flush()
    }
}
    
