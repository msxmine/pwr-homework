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
    ttl int
    systemwg *sync.WaitGroup
}

type node struct {
    id int
    entry chan *packet
    exits []chan *packet
    exitids []int
    handled []int
    traps int
    hunterchan chan int
}

func nodelogic(n *node, wg *sync.WaitGroup){
    defer wg.Done()
    for {
        var val *packet
        var more bool
        select {
            case <- n.hunterchan:
                n.traps++
                continue
            case val, more = <- n.entry:
        }
        if !more {
            close(n.exits[0])
            return
        }
        printch <- ("Pakiet " + strconv.Itoa(val.num) + " jest w wierzchołku " + strconv.Itoa(n.id))
        val.cbchan <- 1
        val.path = append(val.path, n)
        n.handled = append(n.handled, val.num)
        if n.traps > 0 {
            n.traps--
            printch <- ("Pakiet " + strconv.Itoa(val.num) + " wpadł w pułapke w wierzchołku " + strconv.Itoa(n.id))
            val.systemwg.Done()
            continue
        }
        val.ttl -= 1
        if val.ttl > 0 {
            time.Sleep(time.Duration(rand.Intn(millislimit))*time.Millisecond)
            sendcomplete := 0
            for sendcomplete != 1 {
                exidx := len(n.exitids)
                exidx = rand.Intn(exidx)
                val.cbchan = make(chan int)
                //Zapobiegaj deadlockowi gdy np. 1 wysyła do 2 a 2 wysyła do 1
                select {
                    case n.exits[exidx] <- val:
                        <- val.cbchan
                        sendcomplete = 1
                    default:
                        time.Sleep(time.Duration(1*time.Millisecond))
                }
            }
        } else {
            printch <- ("Pakiet " + strconv.Itoa(val.num) + " umarł w wierzchołku " + strconv.Itoa(n.id))
            val.systemwg.Done()
        }
    }
}

func sink(ch chan *packet){
    for {
        gotpack, more := <- ch
        if !more {
            return
        }
        printch <- ("Pakiet " + strconv.Itoa(gotpack.num) + " został odebrany")
        gotpack.cbchan <- 1
        gotpack.systemwg.Done()
    }
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

func hunter(graph []*node, endch chan int){
    for {
        select {
            case <- endch:
                endch <- 1
                return
            default:
        }
        time.Sleep(time.Duration(rand.Intn(millislimit))*time.Millisecond*20)
        idx := rand.Intn(n)
        graph[idx].hunterchan <- 1
    }
}

func Find(slice []int, val int) (int,bool) {
    for i, item := range slice {
        if item == val {
            return i, true
        }
    }
    return -1, false
}

var printch chan string
var n int
var d int
var k int
var b int
var h int
var millislimit int

func main(){
    rand.Seed(1)
    n = 10
    d = 5
    k = 6
    b = 7
    h = 50
    millislimit = 1000
    
    var psync sync.WaitGroup
    printch = make(chan string)
    psync.Add(1);
    go printer(printch, &psync)
    
    start := make(chan *packet)
    lastch := start
    var graph []*node
    var wg sync.WaitGroup
    for i := 0; i < n; i++ {
        var newnode node
        newnode.id = i
        newnode.traps = 0
        newnode.hunterchan = make(chan int, 1)
        newnode.entry = lastch
        lastch = make(chan *packet)
        newnode.exits = append(newnode.exits, lastch)
        newnode.exitids = append(newnode.exitids, i+1)
        graph = append(graph, &newnode)
        wg.Add(1)
        go nodelogic(&newnode, &wg)
    }
    scMax := ((n-1)*(n-2))/2
    if d > scMax {
        fmt.Println("Za dużo skrótów. Ograniczam...")
        d = scMax
    }
    scAdded := 0
    for scAdded < d {
        scIdx := -1
        scTarget := rand.Intn(scMax-scAdded)
        scDone := 0
        for stNod := 0; stNod < n-1 && scDone == 0; stNod++ {
            for endNod := stNod+1; endNod < n && scDone == 0; endNod++ {
                _, found := Find(graph[stNod].exitids, endNod)
                if !found {
                    scIdx++
                }
                if (scIdx == scTarget) {
                    graph[stNod].exits = append(graph[stNod].exits, graph[endNod].entry)
                    graph[stNod].exitids = append(graph[stNod].exitids, endNod)
                    scDone = 1
                    scAdded++
                }
            }
        }
    }
    
    bjMax := (n*(n-1))/2
    if b > bjMax {
        fmt.Println("Za dużo ścieżek powrotnych. Ograniczam...")
        b = bjMax
    }
    bjAdded := 0
    for bjAdded < b {
        bjIdx := -1
        bjTarget := rand.Intn(bjMax-bjAdded)
        bjDone := 0
        for stNod := n-1; stNod > 0 && bjDone == 0; stNod-- {
            for endNod := stNod-1; endNod >= 0 && bjDone == 0; endNod-- {
                _, found := Find(graph[stNod].exitids, endNod)
                if !found {
                    bjIdx++
                }
                if (bjIdx == bjTarget) {
                    graph[stNod].exits = append(graph[stNod].exits, graph[endNod].entry)
                    graph[stNod].exitids = append(graph[stNod].exitids, endNod)
                    bjDone = 1
                    bjAdded++
                }
            }
        }
    }
    

    for i := 0; i < n; i++ {
        fmt.Print(strconv.Itoa(i) + "->")
        for j := 0; j < len(graph[i].exitids); j++ {
            fmt.Print(strconv.Itoa(graph[i].exitids[j]) + ",")
        }
        fmt.Print(" ")
    }
    fmt.Print("\n")
    
    
    
    var mainwg sync.WaitGroup
    go sink(lastch)
    
    hunterendch := make(chan int)
    go hunter(graph, hunterendch)
    
    
    packets := make([]packet, k)
    for i := 0; i < k; i++ {
        var newpack packet
        packets[i] = newpack
        packets[i].num = i
        packets[i].ttl = h
        mainwg.Add(1)
        packets[i].systemwg = &mainwg
        packets[i].cbchan = make(chan int)
        time.Sleep(time.Duration(rand.Intn(millislimit))*time.Millisecond)
        start <- &(packets[i])
        <- packets[i].cbchan
    }
    mainwg.Wait()
    hunterendch <- 1
    <- hunterendch
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
        fmt.Print("Pakiet " + strconv.Itoa(packets[i].num) + " :")
        for _,p := range packets[i].path {
            fmt.Print(" " + strconv.Itoa(p.id))
        }
        fmt.Print("\n")
    }
    
}
