import java.util.ArrayList;

public class Vertex {
    int vertidx;
    ArrayList<Edge> exits = new ArrayList<Edge>();
    int exitidx;
    boolean visited = false;

    public int exit(int idx){
        int cand = exits.get(idx).a;
        if (cand == vertidx){
            cand = exits.get(idx).b;
        }
        return cand;
    }
}
