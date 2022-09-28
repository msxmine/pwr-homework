import java.util.*;

public class RandWalk extends Walker{
    public void walk(ArrayList<Vertex> graf){
        steps = 0;
        cost = 0.0;
        Random rand = new Random();
        long starttime = System.nanoTime();
        boolean[] visited = new boolean[graf.size()];
        Integer visitedNum = 1;
        visited[0] = true;
        Integer current = 0;
        memory = graf.size() + 32 + 32; //visited + visitednum + current

        while (visitedNum < graf.size()){
            steps++;
            Integer target = rand.nextInt(graf.size()-1);
            if (target >= current){
                target++;
            }
            System.err.println("Przechodze do " + String.valueOf(target) + " koszt " + String.valueOf(graf.get(current).exits.get(target).cost));
            cost += graf.get(current).exits.get(target).cost;
            current = target;
            if (visited[current] == false){
                visitedNum++;
                visited[current] = true;
            }
        }
        time = System.nanoTime() - starttime;

    }
}