import java.util.ArrayList;

public class DFSExplorer {
    public long explore(ArrayList<Vertex> graf, int start){
        int explored = 0;
        long timesteps = 0;

        int lastnode = start;
        int curnode = start;
        boolean entering = true;

        while (explored < graf.size()){
            timesteps++;
            if (entering){
                if (graf.get(curnode).visited){
                    curnode = lastnode;
                    entering = false;
                    continue;
                }
                graf.get(curnode).visited = true;
                explored++;
                graf.get(curnode).exitidx = lastnode;
            }
            boolean hooked = false;
            for (int i = 0; i < graf.get(curnode).exits.size(); i++){
                if (!graf.get(curnode).exits.get(i).explored){
                    graf.get(curnode).exits.get(i).explored = true;
                    lastnode = curnode;
                    entering = true;
                    curnode = graf.get(curnode).exit(i);
                    hooked = true;
                    break;
                }
            }
            if (hooked){
                continue;
            }
            entering = false;
            curnode = graf.get(curnode).exitidx;

        }

        return timesteps;
    }
}