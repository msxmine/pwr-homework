package main

import (
	"container/heap"
)

type Item struct {
	value    [16]int
	priority int
	index int
}

type PriorityQueue struct {
	storage []*Item
	search map[[16]int]int
}

func (pq PriorityQueue) Len() int { return len(pq.storage) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq.storage[i].priority < pq.storage[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq.storage[i], pq.storage[j] = pq.storage[j], pq.storage[i]
	pq.storage[i].index = i
	pq.storage[j].index = j
	pq.search[pq.storage[i].value] = i
	pq.search[pq.storage[j].value] = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(pq.storage)
	item := x.(*Item)
	item.index = n
	pq.search[item.value] = n
	pq.storage = append(pq.storage, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := pq.storage
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	delete(pq.search, item.value)
	pq.storage = old[0 : n-1]
	return item
}

func (pq *PriorityQueue) insertOrBump(newvalue [16]int, newpriority int){
	if val, ok := pq.search[newvalue]; ok {
		if pq.storage[val].priority > newpriority {
			pq.storage[val].priority = newpriority
			heap.Fix(pq, val)
		}
	} else {
		newitem := &Item{
			value: newvalue,
			priority: newpriority,
		}
		heap.Push(pq, newitem)
	}
}

func newPriorityQueue() *PriorityQueue {
	pq := new(PriorityQueue)
	pq.storage = make([]*Item, 0)
	pq.search = make(map[[16]int]int)
	return pq
}
