import java.util.*;
import java.util.stream.*;

public class z1test {
    public static void main(String[] args) {
        PQueue[] que = new PQueue[1000];
        Random rand = new Random();
        List<List<Integer>> res = new ArrayList<List<Integer>>();
        boolean failed = false;

        for (int i = 0; i < 1000; i++){
            res.add(new ArrayList<Integer>(1000));
            que[i] = new PQueue();
        }


        for (int i = 0; i < 1000; i++){
            long insertstart = System.nanoTime();
            for (int j = 0; j < 1000; j++){
                que[j].Insert(rand.nextInt(500), rand.nextInt(500));
            }
            long insertstop = System.nanoTime();

            long popstart = System.nanoTime();
            for (int j = 0; j < 1000; j++){
                que[j].Pop();
            }
            long popstop = System.nanoTime();

            for (int j = 0; j < 1000; j++){
                que[j].Insert(rand.nextInt(500), rand.nextInt(500));
            }

            System.out.println(String.valueOf(i) + " " + String.valueOf(insertstop-insertstart) + " " + String.valueOf(popstop-popstart));
        }

        for (int i = 0; i < 1000; i++){
            for (int j = 0; j < 100; j++){
                que[i].Decrease(rand.nextInt(500), rand.nextInt(500));
            }
        }

        for (int i = 0; i < 1000; i++){
            for (int j = 0; j < 1000; j++){
                res.get(i).add(que[i].Top().priority);
                que[i].Pop();
            }
            if (!res.get(i).stream().sorted().collect(Collectors.toList()).equals(res.get(i))){
                failed = true;
                System.err.println("nieudany test");
            }
        }
    }
}