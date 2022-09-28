import java.util.ArrayList;

public class RoundRobinExplorer {
    public long explore(ArrayList<Vertex> graf, int start){
        int explored = 0;
        long timesteps = 0;

        int curnode = start;

        while (explored < graf.size()){
            timesteps++;
            if (!graf.get(curnode).visited){
                graf.get(curnode).visited = true;
                explored++;
            }
            int exitsize = graf.get(curnode).exits.size();
            int next = graf.get(curnode).exitidx % exitsize;
            graf.get(curnode).exitidx = next + 1;
            curnode = graf.get(curnode).exit(next);
        }
        return timesteps;
    }
}
