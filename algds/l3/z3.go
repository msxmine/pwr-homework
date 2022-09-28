package main

import (
    "math/rand"
    "os"
    "bufio"
    "strconv"
    "time"
)

var ncomp = 0

func binsearch(arr []int, start int, end int, val int) bool{
    if start != end {
        mid := (start+end)/2
        ncomp++
        if val > arr[mid] {
            return binsearch(arr, mid+1, end, val)
        } else {
            return binsearch(arr, start, mid, val)
        }
    }
    ncomp++
    if arr[start] == val {
        return true
    } else {
        return false
    }
}

func main(){
    tests := 1000000
    f, _ := os.Create("./z3out.txt")
    defer f.Close()
    fil := bufio.NewWriter(f)
    
    for n := 1000; n <= 100000; n += 1000 {
        data := make([]int, n)
        for i := 0; i < n; i++ {
            data[i] = (i+1)*2
        }
        valarr := make([]int, 5)
        compres := make([]int64, 5)
        timeres := make([]int64, 5)
        for m := 0; m < tests; m++ {
            valarr[0] = (1+rand.Intn(100))*2
            valarr[1] = ((n/2)-50+rand.Intn(100))*2
            valarr[2] = (n-rand.Intn(100))*2
            valarr[3] = ((rand.Intn(n)+1)*2)-1
            valarr[4] = (rand.Intn(n)+1)*2
            for vidx := 0; vidx < 5; vidx++ {
                ncomp = 0
                tstart := time.Now()
                binsearch(data, 0, n-1, valarr[vidx])
                exect := time.Since(tstart)
                compres[vidx] += int64(ncomp)
                timeres[vidx] += int64(exect)
            }
        }
        for vidx := 0; vidx < 5; vidx++ {
            fil.WriteString(strconv.Itoa(vidx) + " " + strconv.Itoa(n) + " " + strconv.Itoa(tests) + " " + strconv.FormatInt(compres[vidx], 10) + " " + strconv.FormatInt(timeres[vidx], 10) + "\n")
        }
        fil.Flush()
        
        
    }
}
