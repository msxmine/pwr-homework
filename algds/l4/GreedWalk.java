import java.util.*;

public class GreedWalk extends Walker{
    public void walk(ArrayList<Vertex> graf) {
        steps = 0;
        cost = 0.0;
        long starttime = System.nanoTime();
        boolean[] visited = new boolean[graf.size()];
        Integer visitedNum = 1;
        visited[0] = true;
        Integer current = 0;
        memory = graf.size() + 32 + 32 + 64; //visited + visitednum + current + mincost

        while (visitedNum < graf.size()){
            steps++;
            Integer target = current;
            Double mincost = Double.POSITIVE_INFINITY;
            for (int i = 0; i < graf.size(); i++){
                if (i == current){
                    continue;
                }
                if (visited[i] == false){
                    if (graf.get(current).exits.get(i).cost < mincost){
                        mincost = graf.get(current).exits.get(i).cost;
                        target = i;
                    }
                }
            }
            System.err.println("Przechodze do " + String.valueOf(target) + " koszt " + String.valueOf(mincost));
            cost += mincost;
            current = target;
            if (visited[current] == false){
                visitedNum++;
                visited[current] = true;
            }
        }
        time = System.nanoTime() - starttime;
    }
    
}
