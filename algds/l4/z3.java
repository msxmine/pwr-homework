import java.util.*;

public class z3 {
    public static void main(String[] args) {
        MST solver = new Kruskal();

        if (args.length > 0){
            if (args[0].equals("-p")){
                solver = new Prim();
            }
            if (args[0].equals("-k")){
                solver = new Kruskal();
            }
        }

        ArrayList<Vertex> lis = new ArrayList<Vertex>();

        Scanner clin = new Scanner(System.in).useLocale(Locale.ENGLISH);
        int n = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < n; i++){
            lis.add(new Vertex());
        }

        int m = clin.nextInt();
        clin.nextLine();
        for (int i = 0; i < m; i++){
            int u = clin.nextInt();
            int v = clin.nextInt();
            Double w = clin.nextDouble();
            clin.nextLine();

            Edge t1 = new Edge();
            Edge t2 = new Edge();

            t1.from = u;
            t2.target = u;
            t1.target = v;
            t2.from = v;
            t1.cost = w;
            t2.cost = w;

            lis.get(u).exits.add(t1);
            lis.get(v).exits.add(t2);
        }

        ArrayList<Vertex> span = solver.calc(lis);

        Double total = 0.0;

        System.out.println("results:");

        for (int i = 0; i < span.size(); i++){
            Vertex tmpv = span.get(i);
            for (int j = 0; j < tmpv.exits.size(); j++){
                Edge tmpe = tmpv.exits.get(j);
                total += tmpe.cost;
                int startv = i;
                int endv = tmpe.target;
                if (startv > endv){
                    int stmp = startv;
                    startv = endv;
                    endv = stmp;
                }
                System.out.println(String.valueOf(startv) + " " + String.valueOf(endv) + " " + String.valueOf(tmpe.cost));
            }
        }
        System.out.println(String.valueOf(total));


    }
}
