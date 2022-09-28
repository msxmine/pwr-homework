import java.util.*;

public class PQueue {

    public ArrayList<QElement> arr;
    public HashMap<Integer,Set<QElement>> map;
    public Integer size;

    private Integer parent(Integer i){ return (i-1)/2; }
    private Integer left(Integer i){ return (2*i + 1); }
    private Integer right(Integer i){ return (2*i + 2); }

    public PQueue(){
        arr = new ArrayList<QElement>();
        map = new HashMap<Integer,Set<QElement>>();
        size = 0;
    }

    private void swap(Integer i, Integer j){
        QElement temp = arr.get(i);
        QElement temp2 = arr.get(j);
        arr.set(i, temp2);
        arr.set(j, temp);
        temp2.idx = i;
        temp.idx = j;
    }

    public void Insert(Integer x, Double p){
        Integer i = size;
        size++;
        arr.add(null);
        QElement inserted = new QElement(x, p);
        arr.set(i, inserted);
        inserted.idx = i;
        map.computeIfAbsent(inserted.value, k -> new HashSet<QElement>()).add(inserted);

        while (i > 0){
            if (arr.get(i).priority < arr.get(parent(i)).priority){
                swap(i, parent(i));
                i = parent(i);
            } else {
                break;
            }
        }

    }

    public void Pop(){
        if (size == 0){
            return;
        }
        map.computeIfAbsent(arr.get(0).value, k -> new HashSet<QElement>()).remove(arr.get(0));
        arr.set(0, arr.get(size-1));
        arr.get(0).idx = 0;
        size--;
        if (size == 0){
            return;
        }
        Integer i = 0;
        while (left(i) < size){
            if (right(i) >= size || arr.get(left(i)).priority < arr.get(right(i)).priority){
                if (arr.get(i).priority > arr.get(left(i)).priority){
                    swap(i, left(i));
                    i = left(i);
                }
                else {
                    break;
                }
            }
            else{
                if (arr.get(i).priority > arr.get(right(i)).priority){
                    swap(i, right(i));
                    i = right(i);
                }
                else{
                    break;
                }
            }
        }

    }

    public void Decrease(Integer val, Double newprio){
        Iterator<QElement> affected = map.computeIfAbsent(val, k -> new HashSet<QElement>()).iterator();
        while (affected.hasNext()){
            QElement obj = affected.next();
            if (newprio < obj.priority){
                obj.priority = newprio;
                Integer cur = obj.idx;
                while (cur > 0){
                    if (arr.get(cur).priority < arr.get(parent(cur)).priority){
                        swap(cur, parent(cur));
                        cur = parent(cur);
                    }
                    else{
                        break;
                    }
                }
            }
        }
    }

    public QElement Top(){
        if (size == 0){
            return null;
        }
        return arr.get(0);
    }


}