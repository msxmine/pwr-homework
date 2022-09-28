import java.util.Scanner;

public class z1 {
    public static void main(String[] args) {
        PQueue que = new PQueue();

        Scanner clin = new Scanner(System.in);
        int m = clin.nextInt();
        clin.nextLine();

        for (int i = 0; i < m; i++){
            String command = clin.nextLine();
            if (command.startsWith("insert ")){
                String[] strparams = command.substring(7).split("\\s+");
                Integer x = Integer.parseInt(strparams[0]);
                Integer p = Integer.parseInt(strparams[1]);
                que.Insert(x, p);
            }

            if (command.startsWith("empty")){
                if (que.size <= 0){
                    System.out.println("1");
                }
                else{
                    System.out.println("0");
                }
            }

            if (command.startsWith("top")){
                QElement t = que.Top();
                if (t == null){
                    System.out.println("");
                }
                else{
                    System.out.println(t.value);
                }
            }

            if (command.startsWith("pop")){
                QElement t = que.Top();
                if (t == null){
                    System.out.println("");
                }
                else{
                    que.Pop();
                    System.out.println(t.value);
                }
            }

            if (command.startsWith("priority ")){
                String[] strparams = command.substring(9).split("\\s+");
                Integer x = Integer.parseInt(strparams[0]);
                Integer p = Integer.parseInt(strparams[1]);
                que.Decrease(x, p);
            }

            if (command.startsWith("print")){
                for (int j = 0 ; j < que.size; j++){
                    System.out.print("(" + que.arr.get(j).value.toString() + "," + que.arr.get(j).priority.toString() + "),");
                }
                System.out.println("");
            }
        }
    }
} 
