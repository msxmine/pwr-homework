import java.util.*;

abstract class Walker {
    public Integer steps;
    public Double cost;
    public Integer memory;
    public Long time;

    abstract public void walk(ArrayList<Vertex> graf);
}
