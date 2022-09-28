import java.util.*;

public class z5 {
    public static void main(String[] args) {
        ArrayList<Vertex> graf = new ArrayList<Vertex>();
        Random rand = new Random();

        Scanner clin = new Scanner(System.in).useLocale(Locale.ENGLISH);
        int n = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < n; i++){
            graf.add(new Vertex());
            graf.get(i).vertidx = i;
        }

        int m = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < m; i++){
            int u = clin.nextInt();
            int v = clin.nextInt();
            clin.nextLine();
            Edge tmp = new Edge();
            tmp.a = u;
            tmp.b = v;
            graf.get(u).exits.add(tmp);
            graf.get(v).exits.add(tmp);
        }

        int start = clin.nextInt();
        clin.nextLine();

        if (args[1].equals("dfs")){
            DFSExplorer ex = new DFSExplorer();
            double result = ex.explore(graf, start);
            System.out.println(result);
        }

        if (args[1].equals("rw")){
            double result = 0.0;
            for (int i = 0; i < 10; i++){
                for (int idx = 0; idx < n; idx++){
                    graf.get(idx).visited = false;
                }
                RandomExplorer ex = new RandomExplorer();
                result += ex.explore(graf, start);
            }
            System.out.println(result/10.0);
        }

        if (args[1].equals("rr")){
            double result = 0.0;
            for (int i = 0; i < 10; i++){
                for (int idx = 0; idx < n; idx++){
                    graf.get(idx).visited = false;
                    graf.get(idx).exitidx = rand.nextInt(n);
                }
                RoundRobinExplorer ex = new RoundRobinExplorer();
                result += ex.explore(graf, start);
            }
            System.out.println(result/10.0);
        }

    }
}
