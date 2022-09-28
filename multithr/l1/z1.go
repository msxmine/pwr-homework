package main

import (
    "fmt"
    "time"
    "math/rand"
    "sync"
    "strconv"
)

type packet struct {
    num int
    path []*node
    cbchan chan int
}

type node struct {
    id int
    entry chan packet
    exits []chan packet
    exitids []int
    handled []int
}

func nodelogic(n *node, wg *sync.WaitGroup){
    defer wg.Done()
    for {
        val, more := <- n.entry
        if !more {
            close(n.exits[0])
            return
        }
        printch <- ("Pakiet " + strconv.Itoa(val.num) + " jest w wierzchołku " + strconv.Itoa(n.id))
        val.cbchan <- 1
        val.path = append(val.path, n)
        n.handled = append(n.handled, val.num)
        time.Sleep(time.Duration(rand.Intn(millislimit))*time.Millisecond)
        exidx := len(n.exitids)
        exidx = rand.Intn(exidx)
        val.cbchan = make(chan int)
        n.exits[exidx] <- val
        <- val.cbchan
    }
}

func sink(ch chan packet, cp chan bool, results *[]packet){
    for i := 0; i < k; i++ {
        gotpack := <- ch
        printch <- ("Pakiet " + strconv.Itoa(gotpack.num) + " został odebrany")
        *results = append(*results, gotpack)
        gotpack.cbchan <- 1
    }
    cp <- true
}

func printer(inp chan string, wg *sync.WaitGroup){
    defer wg.Done()
    for {
        newline, more := <- inp
        if !more {
            return
        }
        fmt.Println(newline)
    }
}

var printch chan string
var n int
var d int
var k int
var millislimit int

func main(){
    rand.Seed(1)
    n = 10
    d = 5
    k = 6
    millislimit = 1000
    
    var psync sync.WaitGroup
    printch = make(chan string)
    psync.Add(1);
    go printer(printch, &psync)
    
    start := make(chan packet)
    lastch := start
    var graph []*node
    var wg sync.WaitGroup
    for i := 0; i < n; i++ {
        var newnode node
        newnode.id = i
        newnode.entry = lastch
        lastch = make(chan packet)
        newnode.exits = append(newnode.exits, lastch)
        newnode.exitids = append(newnode.exitids, i+1)
        graph = append(graph, &newnode)
        wg.Add(1)
        go nodelogic(&newnode, &wg)
    }
    for i := 0; i < d; i++ {
        startidx := rand.Intn(n)
        endidx := startidx
        for endidx == startidx {
            endidx = rand.Intn(n)
        }
        if endidx < startidx {
            startidx, endidx = endidx, startidx
        }
        graph[startidx].exits = append(graph[startidx].exits, graph[endidx].entry)
        graph[startidx].exitids = append(graph[startidx].exitids, endidx)
    }
    for i := 0; i < n-1; i++ {
        fmt.Print(strconv.Itoa(i) + "->")
        for j := 0; j < len(graph[i].exitids); j++ {
            fmt.Print(strconv.Itoa(graph[i].exitids[j]) + ",")
        }
        fmt.Print(" ")
    }
    fmt.Print("\n")
    
    
    
    
    done := make(chan bool)
    var endpack []packet
    go sink(lastch, done, &endpack)
    for i := 0; i < k; i++ {
        var newpack packet
        newpack.num = i
        newpack.cbchan = make(chan int)
        time.Sleep(time.Duration(rand.Intn(millislimit))*time.Millisecond)
        start <- newpack
        <- newpack.cbchan
    }
    <- done
    close(start)
    wg.Wait()
    close(printch)
    psync.Wait()
    
    for i := 0; i < n; i++ {
        fmt.Print("Wierchołek " + strconv.Itoa(i) + " :")
        for _,p := range graph[i].handled {
            fmt.Print(" " + strconv.Itoa(p))
        }
        fmt.Print("\n")
    }
    
    for i := 0; i < k; i++ {
        fmt.Print("Pakiet " + strconv.Itoa(endpack[i].num) + " :")
        for _,p := range endpack[i].path {
            fmt.Print(" " + strconv.Itoa(p.id))
        }
        fmt.Print("\n")
    }
    
}
