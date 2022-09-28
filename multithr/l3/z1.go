package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
    "strconv"
    "os"
)

type routingentry struct {
    dest int
    cost int
    nexthop int
    changed bool
    cbchan chan bool
}

type node struct {
    id int
    entry chan []routingentry
    exits []chan []routingentry
    exitids []int
    table []routingentry
    get chan bool
    getresp chan []routingentry
    set chan []routingentry
    newdata bool
}

func tablemanager(n *node, wg *sync.WaitGroup){
    for {
        select {
            case <-n.get:
                resp := make([]routingentry, 0)
                for i := 0; i < len(n.table); i++ {
                    if n.table[i].changed == true {
                        var newoffer routingentry
                        newoffer.dest = i
                        newoffer.cost = n.table[i].cost
                        newoffer.nexthop = n.id
                        newoffer.changed = true
                        n.table[i].changed = false
                        resp = append(resp, newoffer)
                    }
                }
                if (len(resp) > 0){
                    wg.Done()
                }
                n.newdata = false
                n.getresp <- resp
            case write := <-n.set:
                for _, entry := range write {
                    if entry.cost < n.table[entry.dest].cost {
                        printch <- ("Zmiana: wierzcholek " + strconv.Itoa(n.id) + " trasa do " + strconv.Itoa(entry.dest) + " przez " + strconv.Itoa(entry.nexthop) + " koszt " + strconv.Itoa(entry.cost))
                        n.table[entry.dest].cost = entry.cost
                        n.table[entry.dest].nexthop = entry.nexthop
                        n.table[entry.dest].changed = true
                        if (n.newdata == false){
                            wg.Add(1)
                            n.newdata = true
                        }
                    }
                }
        }
    }
}

func sender(n *node, wg *sync.WaitGroup){
    lastsucc := true
    for {
        if (lastsucc){
            wg.Done()
            lastsucc = false
        }
        select {
            case <- time.After(time.Duration(rand.Intn(5000))*time.Millisecond):
        }
        if (n.newdata){
            lastsucc = true
            wg.Add(1)
            n.get <- true
            offer := <- n.getresp
            if (len(offer) > 0){
                for idx, neighbour := range n.exits {
                    toprint := ("Oferta: z wierzchołka " + strconv.Itoa(n.id) + " do " + strconv.Itoa(n.exitids[idx]) + " : " )
                    for _, line := range offer {
                        toprint += ("\n   dest: " + strconv.Itoa(line.dest)  + " nexthop: " + strconv.Itoa(line.nexthop) + " cost: " + strconv.Itoa(line.cost+1))
                    }
                    printch <- toprint
                    specoffer := append([]routingentry(nil), offer...)
                    specoffer[0].cbchan = make(chan bool)
                    neighbour <- specoffer
                    <- specoffer[0].cbchan
                }
            }
        }
    }
}

func receiver(n *node, wg *sync.WaitGroup){
    for {
        wg.Done()
        var offer []routingentry
        select {
            case offer = <- n.entry:
        }
        wg.Add(1)
        offer[0].cbchan <- true
        for i,_ := range offer {
            offer[i].cost += 1
        }
        n.set <- offer
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

func printer(){
    for {
        newline, more := <- printch
        if !more {
            return
        }
        fmt.Println(newline)
    }
}

var printch chan string

func main(){
    rand.Seed(1)
    n := 5
    d := 4
    
    n, _ = strconv.Atoi(os.Args[1])
    d, _ = strconv.Atoi(os.Args[2])
    
    printch = make(chan string)
    go printer()
    
    var graph []*node
    
    for i := 0; i < n; i++ {
        var newnode node
        newnode.id = i
        newnode.entry = make(chan []routingentry)
        newnode.exits = make([]chan []routingentry, 0)
        newnode.exitids = make([]int, 0)
        newnode.table = make([]routingentry, n)
        newnode.get = make(chan bool)
        newnode.getresp = make(chan []routingentry)
        newnode.set = make(chan []routingentry)
        newnode.newdata = true
        graph = append(graph, &newnode)
    }
    
    for i := 0; i < n-1; i++ {
        graph[i].exits = append(graph[i].exits, graph[i+1].entry)
        graph[i].exitids = append(graph[i].exitids, i+1)
        graph[i+1].exits = append(graph[i+1].exits, graph[i].entry)
        graph[i+1].exitids = append(graph[i+1].exitids, i)
    }
    
    scMax := ((n-1)*(n-2))/2
    if d > scMax {
        fmt.Println("Za dużo krawedzi")
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
                    graph[endNod].exits = append(graph[endNod].exits, graph[stNod].entry)
                    graph[endNod].exitids = append(graph[endNod].exitids, stNod)
                    scDone = 1
                    scAdded++
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
    
    var wg sync.WaitGroup
    wg.Add((3*n))
    
    for i := 0; i < n; i++ {
        for j := 0; j < n; j++ {
            graph[i].table[j].dest = j
            graph[i].table[j].changed = true
            if i == j {
                graph[i].table[j].cost = 0
                graph[i].table[j].nexthop = i
                graph[i].table[j].changed = false
                continue
            }
            _, found := Find(graph[i].exitids, j)
            if found {
                graph[i].table[j].cost = 1
                graph[i].table[j].nexthop = j
                continue
            }
            if j < i {
                graph[i].table[j].nexthop = i-1
                graph[i].table[j].cost = i-j
            } else {
                graph[i].table[j].nexthop = i+1
                graph[i].table[j].cost = j-i
            }
        }
        go tablemanager(graph[i], &wg)
    }
    
    for i := 0; i < n; i++ {
        go receiver(graph[i], &wg)
    }
    
    for i := 0; i < n; i++ {
        go sender(graph[i], &wg)
    }
    
    wg.Wait()
    for i := 0; i < n; i++ {
        for j := 0; j < n; j++ {
            fmt.Println("Wierzcholek", i, "trasa do", j, "koszt", graph[i].table[j].cost, "przez", graph[i].table[j].nexthop)
        }
    }
    
}
