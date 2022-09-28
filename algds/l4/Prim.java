import java.util.ArrayList;

public class Prim implements MST{

    public ArrayList<Vertex> calc(ArrayList<Vertex> in){
        //ArrayList<Vertex> lis = new ArrayList<Vertex>();
        ArrayList<Vertex> lis = in;
        ArrayList<Vertex> out = new ArrayList<Vertex>();

        for (int i = 0; i < in.size(); i++){
            //Vertex newvert = new Vertex();
            //for (int j = 0; j < in.get(i).exits.size(); j++){
            //    Edge newedge = new Edge();
            //    newedge.target = in.get(i).exits.get(j).target;
            //    newedge.cost = in.get(i).exits.get(j).cost;
            //    newvert.exits.add(newedge);
            //}
            //lis.add(newvert);
            out.add(null);
        }
        PQueue kol = new PQueue();

        out.set(0, new Vertex());
        lis.get(0).distance = 0.0;

        for (int i = 0; i < lis.get(0).exits.size(); i++){
            Edge cand = lis.get(0).exits.get(i);
            if (cand != null){
                Integer target = cand.target;
                if (target == 0){
                    target = cand.from;
                }
                if (target != 0){
                    kol.Insert(target, cand.cost);
                    lis.get(target).distance = cand.cost;
                    lis.get(target).prev = 0;
                }
            }
        }

        while (kol.size > 0){
            QElement top = kol.Top();
            kol.Pop();

            Edge newedge = new Edge();
            newedge.cost = top.priority;
            newedge.target = top.value;
            

            Vertex added = lis.get(newedge.target);
            newedge.from = added.prev;
            out.get(added.prev).exits.add(newedge);
            out.set(newedge.target, new Vertex());
            out.get(newedge.target).exits.add(newedge);
            added.distance = 0.0;
            for (int i = 0; i < added.exits.size(); i++){
                Edge cand = added.exits.get(i);
                if (cand != null){
                    Integer target = cand.target;
                    if (target == newedge.target){
                        target = cand.from;
                    }

                    if (lis.get(target).distance > cand.cost){
                        if (lis.get(target).distance == Double.POSITIVE_INFINITY){
                            kol.Insert(target, cand.cost);
                        }
                        else{
                            kol.Decrease(target, cand.cost);
                        }
                        lis.get(target).prev = newedge.target;
                        lis.get(target).distance = cand.cost;
                    }
                }
            }
        }

        return out;

        
    }
} 
