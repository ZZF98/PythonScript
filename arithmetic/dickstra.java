import java.util.*;

class Node {
    String name;
    int val;
    Map<String, Node> map;

    public Node(String name, int val) {
        this.name = name;
        this.val = val;
    }

    public Node(String name) {
        this.name = name;
        this.val = val;
    }

    public Node() {

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getVal() {
        return val;
    }

    public void setVal(int val) {
        this.val = val;
    }

    public Map<String, Node> getMap() {
        return map;
    }

    public void setMap(Map<String, Node> map) {
        this.map = map;
    }

    public static void main(String[] args) {
        Node A = new Node("A");

        //构建A
        Map<String, Node> map = new HashMap<>();
        map.put("B", new Node("B", 10));
        map.put("D", new Node("D", 20));
        map.put("C", new Node("C", 10));
        A.setMap(map);
        //构建B
        Node B = A.getMap().get("B");
        map = new HashMap<>();
        map.put("F", new Node("F", 5));
        map.put("E", new Node("E", 20));
        B.setMap(map);
        //构建C
        Node C = A.getMap().get("C");
        map = new HashMap<>();
        map.put("F", new Node("F", 20));
        C.setMap(map);
        //构建D
        Node D = A.getMap().get("D");
        map = new HashMap<>();
        map.put("E", new Node("E", 30));
        map.put("G", new Node("G", 100));
        D.setMap(map);

        //构建BE
        Node BE = A.getMap().get("B").getMap().get("E");
        map = new HashMap<>();
        map.put("G", new Node("G", 50));
        BE.setMap(map);
        Node BF = A.getMap().get("B").getMap().get("F");
        map = new HashMap<>();
        map.put("G", new Node("G", 20));
        BF.setMap(map);

        //构建CF
        Node CF = A.getMap().get("C").getMap().get("F");
        map = new HashMap<>();
        map.put("G", new Node("G", 20));
        CF.setMap(map);

        //构建CF
        Node DE = A.getMap().get("D").getMap().get("E");
        map = new HashMap<>();
        map.put("G", new Node("G", 30));
        DE.setMap(map);


        //记录存值
        Map<String, Integer> DateMap = new HashMap<>();
        //队列
        List<Node> list = new ArrayList<>();
        //获取A节点下的所有节点
        getListNode(list, A);
        //记录A节点下的值（可能A-F就是最短路径）
        int count = list.size();
        //只要列表不为空
        while (list.size() > 0) {
            //每次减一
            --count;
            Node node = list.get(0);
            //获取这个这个节点的子节点
            List<Node> chiNode = new ArrayList<>();
            getListNode(chiNode, node);
            //只记录A到子节点值
            if (DateMap.get("A" + node.getName()) == null && count >= 0) {
                DateMap.put("A" + node.getName(), node.getVal());
            }
            if (!chiNode.isEmpty()) {
                for (Node n : chiNode) {
                    if (DateMap.get("A" + n.getName()) != null) {
                        if (DateMap.get("A" + n.getName()) > (DateMap.get("A" + node.getName()) + n.getVal())) {
                            DateMap.put("A" + n.getName(), (DateMap.get("A" + node.getName()) + n.getVal()));
                        }
                    } else {
                        //添加值
                        DateMap.put("A" + n.getName(), node.getVal() + n.getVal());
                        DateMap.put(node.getName() + n.getName(), n.getVal());
                    }
                }
            }
            //获取这个节点下的子节点
            getListNode(list, node);
            //删除
            list.remove(0);
        }
        System.out.println(DateMap.get("AG"));
    }

    public static void getListNode(List<Node> list, Node node) {
        Map<String, Integer> map = new HashMap<>();
        if (node.getMap() != null) {
            //获取这个节点的所有子节点
            for (String name : node.getMap().keySet()) {
                map.put(name, node.getMap().get(name).getVal());
            }
            //排序
            List<Map.Entry<String, Integer>> arrayList = new ArrayList<>(map.entrySet());
            Collections.sort(arrayList, new Comparator<Map.Entry<String, Integer>>() {
                @Override
                public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                    return o1.getValue().compareTo(o2.getValue());
                }
            });
            //添加节点到末尾
            for (Map.Entry<String, Integer> entry : arrayList) {
                list.add(node.getMap().get(entry.getKey()));
            }
        }
    }
}

