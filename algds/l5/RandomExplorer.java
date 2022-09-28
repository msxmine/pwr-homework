import java.util.ArrayList;
import java.util.Random;

public class RandomExplorer {
    public long explore(ArrayList<Vertex> graf, int start){
        int explored = 0;
        long timesteps = 0;
        Random rand = new Random();

        int curnode = start;

        while (explored < graf.size()){
            timesteps++;
            if (!graf.get(curnode).visited){
                graf.get(curnode).visited = true;
                explored++;
            }
            curnode = graf.get(curnode).exit(rand.nextInt(graf.get(curnode).exits.size()));
        }
        return timesteps;
    }
}
