package main

import (
	"container/heap"
	"fmt"
	"math/rand"
	"time"
	"os"
)

type stateData struct {
	distanceTo int
	previous [16]int
}

func maino(){
	heur := manhattan
	if os.Args[1] == "badheur" {
		heur = misplaced
	}
	rand.Seed(time.Now().UnixNano())
	//startstate := [16]int{1,2,4,8,9,7,16,5,13,3,6,11,10,15,14,12}
	//startstate := [16]int{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
	//for ok := true; ok; ok = (parityCheck(startstate) == 1){
	//	rand.Shuffle(len(startstate), func(i,j int){startstate[i], startstate[j] = startstate[j], startstate[i]})
	//}
	startstate := startStateGen(50);

	pq := newPriorityQueue()
	heap.Init(pq)
	pq.insertOrBump(startstate, heur(startstate))
	nodedata := make(map[[16]int]stateData)
	nodedata[startstate] = stateData{0, [16]int{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}}

	ended := false
	states := 1

	for (pq.Len() > 0 && !ended) {
		examinedNode := heap.Pop(pq).(*Item).value
		examinedDetails := nodedata[examinedNode]
		succesors := getNeighbours(examinedNode)
		for nidx := 0; nidx < len(succesors); nidx++ {
			neighval := succesors[nidx]
			neighrealcost := examinedDetails.distanceTo + 1
			neighheurestic := heur(neighval)
			//fmt.Println(neighrealcost, neighheurestic)
			if neighheurestic == 0 {
				ended = true
			}
			newroutebetter := true
			states += 1
			if states > 1000000 {
				fmt.Println("-1 -1")
				return
			}
			if details, ok := nodedata[neighval]; ok {
				states -= 1
				if neighrealcost > details.distanceTo {
					newroutebetter = false
				}
			}
			if newroutebetter {
				nodedata[neighval] = stateData{neighrealcost, examinedNode}
				pq.insertOrBump(neighval, neighrealcost+neighheurestic)
			}
		}
	}


	curnod := [16]int{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
	fmt.Println(states, nodedata[curnod].distanceTo)
	for curnod != startstate {
		//fmt.Println(curnod, nodedata[curnod].distanceTo)
		curnod = nodedata[curnod].previous
	}
	//fmt.Println(startstate, nodedata[startstate].distanceTo)

}

func main(){
	for i := 0; i < 10000; i++ {
		maino()
	}
}