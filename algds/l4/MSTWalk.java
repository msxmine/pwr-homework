import java.util.ArrayList;

public class MSTWalk extends Walker{

    private ArrayList<Vertex> gr;
    private ArrayList<Vertex> mst;
    private boolean[] visited;
    Integer current;

    private void preorder(Integer addr){
        visited[addr] = true;
        if (addr != 0){
            System.err.println("Przechodze do " + String.valueOf(addr) + " koszt " + String.valueOf(gr.get(current).exits.get(addr).cost));
            cost += gr.get(current).exits.get(addr).cost;
            steps++;
        }
        current = addr;
        for (int i = 0; i < mst.get(addr).exits.size(); i++){
            Edge exit = mst.get(addr).exits.get(i);
            Integer target = exit.target;
            if (target.equals(addr)){
                target = exit.from;
            }
            if (visited[target] == false){
                preorder(target);
            }
        }
    }

    public void walk(ArrayList<Vertex> graf) {
        steps = 0;
        cost = 0.0;
        gr = graf;
        long starttime = System.nanoTime();
        //MST solver = new Kruskal();
        MST solver = new Prim();
        mst = solver.calc(graf);
        visited = new boolean[graf.size()];
        current = 0;
        memory = (graf.size() * 545) + 64; //pqueue - size*192 mst - size*256 dist+prev - size*96 + visited + current

        preorder(current);


        time = System.nanoTime() - starttime;


        
    }

    
}
