package main

import (
	"math/rand"
)

func idxToCoords(idx int) [2]int {
	return [2]int{idx%4, idx/4}
}

func coordsToIdx(x int, y int) int{
	return x+(y*4)
}

func getNeighbours(value [16]int) [][16]int {
	result := make([][16]int, 0, 4)
	holeidx := 0
	for i := 0; i < 16; i++ {
		if value[i] == 16 {
			holeidx = i
			break
		}
	}
	holeCoords := idxToCoords(holeidx)

	if holeCoords[0] > 0{
		newneighbour := value
		slideidx := coordsToIdx(holeCoords[0]-1, holeCoords[1])
		newneighbour[holeidx], newneighbour[slideidx] = newneighbour[slideidx], newneighbour[holeidx]
		result = append(result, newneighbour)
	}
	if holeCoords[0] < 3{
		newneighbour := value
		slideidx := coordsToIdx(holeCoords[0]+1, holeCoords[1])
		newneighbour[holeidx], newneighbour[slideidx] = newneighbour[slideidx], newneighbour[holeidx]
		result = append(result, newneighbour)
	}
	if holeCoords[1] > 0{
		newneighbour := value
		slideidx := coordsToIdx(holeCoords[0], holeCoords[1]-1)
		newneighbour[holeidx], newneighbour[slideidx] = newneighbour[slideidx], newneighbour[holeidx]
		result = append(result, newneighbour)
	}
	if holeCoords[1] < 3{
		newneighbour := value
		slideidx := coordsToIdx(holeCoords[0], holeCoords[1]+1)
		newneighbour[holeidx], newneighbour[slideidx] = newneighbour[slideidx], newneighbour[holeidx]
		result = append(result, newneighbour)
	}
	return result
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func manhattan(value [16]int) int{
	result := 0
	for i := 0; i < 16; i++ {
		if value[i] != 16 {
			realpos := idxToCoords(i)
			goodpos := idxToCoords(value[i]-1)
			result += abs(realpos[0] - goodpos[0])
			result += abs(realpos[1] - goodpos[1])
		}
	}
	return result
}

func misplaced(value [16]int) int{
	result := 0
	for i := 0; i < 16; i++ {
		if value[i] != 16 {
			if value[i] != i+1 {
				result += 1
			}
		}
	}
	return result
}

func parityCheck(value [16]int) int {
	result := 0
	for i := 0; i < 16; i++ {
		for j := i+1; j < 16; j++ {
			if value[i] > value[j] {
				result += 1
				result %= 2
			}
		}
	}
	return result
}

func startStateGen(moves int ) [16]int {
	state := [16]int{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
	for i := 0; i < moves; i++ {
		neigh := getNeighbours(state)
		idx := rand.Intn(len(neigh))
		state = neigh[idx]
	}
	for state[15] != 16 {
		for i := 0; i < 16; i++ {
			if state[i] == 16 {
				hco := idxToCoords(i)
				if hco[0] < 3 {
					rightidx := coordsToIdx(hco[0]+1, hco[1])
					state[i], state[rightidx] = state[rightidx], state[i]
				} else {
					downidx := coordsToIdx(hco[0], hco[1]+1)
					state[i], state[downidx] = state[downidx], state[i]
				}
				break
			}
		}
	}
	return state
}
