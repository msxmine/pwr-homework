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

func quicksort(arr []int, smart bool){
    size := len(arr)
    if size > 1 {
        if smart {
            pividx := qselect(arr, 0, size-1, size/2, medpivot)
            nswap++
            arr[pividx], arr[size-1] = arr[size-1], arr[pividx]
        }
        pivval := arr[size-1]
        swapslot := 0
        for i := 0; i < size-1; i++ {
            ncomp++
            if arr[i] > pivval {
                nswap++
                arr[swapslot], arr[i] = arr[i], arr[swapslot]
                swapslot++
            }
        }
        nswap++
        arr[swapslot], arr[size-1] = arr[size-1], arr[swapslot]
        quicksort(arr[:swapslot], smart)
        quicksort(arr[swapslot+1:], smart)
    }
}

func dpqsort(arr []int, smart bool){
    size := len(arr)
    if size > 1 {
        if smart {
            pfidx := qselect(arr, 0, size-1, size/3, medpivot)
            psidx := qselect(arr, 0, size-1, 2*(size/3), medpivot)
            nswap += 2
            arr[0], arr[pfidx] = arr[pfidx], arr[0]
            arr[size-1], arr[psidx] = arr[psidx], arr[size-1]
        }
        ncomp++
        if arr[size-1] > arr[0] {
            nswap++
            arr[0], arr[size-1] = arr[size-1], arr[0]
        }
        pnum := 0
        qnum := 0
        for i := 1 ; i < (size-1-qnum); i++ {
            if qnum > pnum {
                ncomp++
                if arr[size-1] > arr[i] {
                    nswap++
                    arr[i], arr[size-2-qnum] = arr[size-2-qnum], arr[i]
                    qnum++
                    continue
                }
                ncomp++
                if arr[i] > arr[0] {
                    nswap++
                    arr[i], arr[1+pnum] = arr[1+pnum], arr[i]
                    pnum++
                    i++
                    continue
                }
            } else {
                ncomp++
                if arr[i] > arr[0] {
                    nswap++
                    arr[i], arr[1+pnum] = arr[1+pnum], arr[i]
                    pnum++
                    i++
                    continue
                }
                ncomp++
                if arr[size-1] > arr[i] {
                    nswap++
                    arr[i], arr[size-2-qnum] = arr[size-2-qnum], arr[i]
                    qnum++
                    continue
                }
            }
        }
        nswap += 2
        arr[0], arr[pnum] = arr[pnum], arr[0]
        arr[size-1], arr[size-1-qnum] = arr[size-1-qnum], arr[size-1]
        dpqsort(arr[:pnum], smart)
        dpqsort(arr[pnum+1:size-1-qnum], smart)
        dpqsort(arr[size-qnum:size], smart)
    }
}

func main(){
    f, _ := os.Create("./z4outrand.txt")
    defer f.Close()
    fil := bufio.NewWriter(f)
    
    for n:= 100; n <= 10000; n+=100 {
        for m := 0; m < 100; m++ {
            randdata := make([]int, n)

            input := make([]int, n)
            for i := 0; i < n; i++ {
                randdata[i] = rand.Int()
            }

            ncomp = 0
            nswap = 0
            copy(input, randdata)
            tstart := time.Now()
            quicksort(input, false)
            exect := time.Since(tstart)
            fil.WriteString(strconv.Itoa(n) + " " +strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + " quicksort\n")
            
            ncomp = 0
            nswap = 0
            copy(input, randdata)
            tstart = time.Now()
            dpqsort(input, false)
            exect = time.Since(tstart)
            fil.WriteString(strconv.Itoa(n) + " " +strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + " dpqsort\n")
            
            ncomp = 0
            nswap = 0
            copy(input, randdata)
            tstart = time.Now()
            quicksort(input, true)
            exect = time.Since(tstart)
            fil.WriteString(strconv.Itoa(n) + " " +strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + " quicksortselect\n")
            
            ncomp = 0
            nswap = 0
            copy(input, randdata)
            tstart = time.Now()
            dpqsort(input, true)
            exect = time.Since(tstart)
            fil.WriteString(strconv.Itoa(n) + " " +strconv.Itoa(ncomp) + " " + strconv.Itoa(nswap) + " " + strconv.FormatInt(int64(exect), 10) + " dpqsortselect\n")

            
        }
        fil.Flush()
    }
}
    
