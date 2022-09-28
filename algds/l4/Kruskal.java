import java.util.*;

public class Kruskal implements MST{
    class subset {
        int parent;
        int rank;
    }

    int find(subset[] subsets, int i){
        if (subsets[i].parent != i){
            subsets[i].parent = find(subsets, subsets[i].parent);
        }
        return subsets[i].parent;
    }

    void union(subset[] subsets, int x, int y){
        int xroot = find(subsets, x);
        int yroot = find(subsets, y);

        if(subsets[xroot].rank == subsets[yroot].rank){
            subsets[xroot].parent = yroot;
            subsets[yroot].rank++;
        } else {
            if (subsets[xroot].rank < subsets[yroot].rank){
                subsets[xroot].parent = yroot;
            } else {
                subsets[yroot].parent = xroot;
            }
        }
    }

    public ArrayList<Vertex> calc(ArrayList<Vertex> in){
        ArrayList<Vertex> out = new ArrayList<Vertex>();
        ArrayList<Edge> alledges = new ArrayList<Edge>();
        subset[] subsets = new subset[in.size()];
        PQueue kol = new PQueue();

        for (int i = 0; i < in.size(); i++){
            subset newset = new subset();
            newset.parent = i;
            newset.rank = 0;
            subsets[i] = newset;

            out.add(new Vertex());

            for (int j = 0; j < in.get(i).exits.size(); j++){
                if (in.get(i).exits.get(j) != null){
                    Edge newedge = new Edge();
                    newedge.from = i;
                    newedge.target = in.get(i).exits.get(j).target;
                    if (newedge.target == i){
                        newedge.target = in.get(i).exits.get(j).from;
                    }
                    newedge.cost = in.get(i).exits.get(j).cost;
                    Integer neidx = alledges.size();
                    alledges.add(newedge);
                    kol.Insert(neidx, newedge.cost);
                }
            }
        }

        while (kol.size > 0){
            Edge tmpedge = alledges.get(kol.Top().value);
            kol.Pop();

            if (find(subsets, tmpedge.from) != find(subsets, tmpedge.target)){
                out.get(tmpedge.from).exits.add(tmpedge);
                out.get(tmpedge.target).exits.add(tmpedge);
                union(subsets, tmpedge.from, tmpedge.target);
            }
        }

        return out;


    }
}
