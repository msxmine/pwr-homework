import java.util.*;

public class z2 {
    public static void main(String[] args) {
        PQueue que = new PQueue();
        ArrayList<Vertex> lis = new ArrayList<Vertex>();

        Scanner clin = new Scanner(System.in).useLocale(Locale.ENGLISH);
        int n = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < n; i++){
            Vertex tmp = new Vertex();
            lis.add(tmp);
            que.Insert(i, tmp.distance);
        }

        int m = clin.nextInt();
        clin.nextLine();
        for (int i = 0; i < m; i++){
            int u = clin.nextInt();
            int v = clin.nextInt();
            Double w = clin.nextDouble();
            clin.nextLine();
            Edge tmp = new Edge();
            tmp.target = v;
            tmp.cost = w;
            lis.get(u).exits.add(tmp);
        }

        int start = clin.nextInt();
        clin.nextLine();

        lis.get(start).distance = 0.0;
        que.Decrease(start, 0.0);


        long djikstrastart = System.nanoTime();
        while (que.size > 0){
            QElement idx = que.Top();
            que.Pop();
            Vertex cur = lis.get(idx.value);
            for (int i = 0; i < cur.exits.size(); i++){
                Edge curexit = cur.exits.get(i);
                Double newdist = idx.priority + curexit.cost;
                if (newdist < lis.get(curexit.target).distance){
                    lis.get(curexit.target).distance = newdist;
                    lis.get(curexit.target).prev = idx.value;
                    que.Decrease(curexit.target, newdist);
                }
            }
        }
        long djikstraend = System.nanoTime();

        for (int i = 0; i < n; i++){
            System.out.println(String.valueOf(i) + " " + lis.get(i).distance.toString());
            Vertex cur = lis.get(i);
            while (cur.prev != null){
                System.err.print(" <-(" + String.valueOf(cur.distance - lis.get(cur.prev).distance) + ")- " + String.valueOf(cur.prev));
                cur = lis.get(cur.prev);
            }
            System.err.println("");
        }
        System.err.println( String.valueOf( (double)(djikstraend-djikstrastart) / 1000000.0 ) );




    }
} 
