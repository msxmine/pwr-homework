import java.util.*;

public class z4 {
    public static void main(String[] args) {
        Scanner clin = new Scanner(System.in).useLocale(Locale.ENGLISH);
        ArrayList<Vertex> lis = new ArrayList<Vertex>();

        int n = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < n; i++){
            Vertex nvert = new Vertex();
            for (int j = 0; j < n; j++){
                nvert.exits.add(null);
            }
            lis.add(nvert);
        }

        int m = (n*(n-1))/2;

        for (int i = 0; i < m; i++){
            int u = clin.nextInt();
            int v = clin.nextInt();
            Double w = clin.nextDouble();
            clin.nextLine();
            Edge tmpedge = new Edge();
            tmpedge.from = u;
            tmpedge.target = v;
            tmpedge.cost = w;
            lis.get(u).exits.set(v, tmpedge);
            lis.get(v).exits.set(u, tmpedge);
        }

        Walker w1 = new RandWalk();
        Walker w2 = new GreedWalk();
        Walker w3 = new MSTWalk();

        w1.walk(lis);
        System.out.println(String.valueOf(w1.steps) + " " + String.valueOf(w1.cost) + " " + String.valueOf(w1.memory) + " " + String.valueOf(w1.time));

        w2.walk(lis);
        System.out.println(String.valueOf(w2.steps) + " " + String.valueOf(w2.cost) + " " + String.valueOf(w2.memory) + " " + String.valueOf(w2.time));

        w3.walk(lis);
        System.out.println(String.valueOf(w3.steps) + " " + String.valueOf(w3.cost) + " " + String.valueOf(w3.memory) + " " + String.valueOf(w3.time));
    }
}