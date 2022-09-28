import java.util.*;

public class Vertex {
    public Integer prev = null;
    public ArrayList<Edge> exits = new ArrayList<Edge>();
    public Double distance = Double.POSITIVE_INFINITY;
}