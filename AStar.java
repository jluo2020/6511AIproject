import java.io.*;
import java.util.*;
import java.lang.*;
import java.math.*;

public class AStar {
    static class NODE {
        int u;
        double f;
        NODE(){}
        NODE(int a,double b){u=a;f=b;}
    }

    //Necessary variables
    static NODE top=new NODE();
    static int inp1,inp2;
    static double inp3;
    static int n=0,m=0,S,D,pos[]=new int[105],vis[]=new int[105],pre[]=new int[105];
    static double g[][]=new double[105][105],dis[]=new double[105],f[]=new double[105];//f represents the valuation function
    static long StartTime,EndTime;

    //initialization
    public static void Initial() {
        for(int i=0;i<100;i++){
            for(int j=0;j<100;j++){
                g[i][j]=1e12;
            }
        }
        for(int i=0;i<100;i++){
            vis[i]=0;
            dis[i]=1e12;
            f[i]=1e12;
        }
    }

    //Calculate the value of Euclidean distance and valuation function
    public static double cal(int pos1,int pos2) {
        int x1=pos1/10,y1=pos1%10;
        int x2=pos2/10,y2=pos2%10;
        double ret=java.lang.Math.sqrt((double)(x1-x2)*(x1-x2)+(double)(y1-y2)*(y1-y2));
        return ret;
//        return Math.abs(pos1/10-pos2/10)+Math.abs(pos1%10-pos2%10);
    }

    //input data
    public static void Read() {
//        Scanner ip=new Scanner(System.in);
//        String ch=new String("");
//
//        while(ip.hasNext()){
//            n++;
//            ch=ip.next();
//            String[] in=ch.split(",");
//            inp1=Integer.valueOf(in[0]).intValue();
//            inp2=Integer.valueOf(in[1]).intValue();
//            pos[inp1]=inp2;
//            if(n==100) break;
//        }
//        while(ip.hasNext()){
//            m++;
//            ch=ip.next();
//            String[] in=ch.split(",");
//            inp1=Integer.valueOf(in[0]).intValue();
//            inp2=Integer.valueOf(in[1]).intValue();
//            inp3=Double.valueOf(in[2]);
//            if(inp3<g[inp1][inp2]) g[inp1][inp2]=g[inp2][inp1]=inp3;
////            System.out.println(inp1+" "+inp2+" "+inp3);
//            if(m==985) break;
//        }
//
////        System.out.println("S: "+S+" D: "+D);

        //read v.txt
        try {
            BufferedReader br = new BufferedReader(new FileReader("F:\\homeworkcode\\6511javahw1\\v.txt"));
            String str;
            while ((str = br.readLine()) != null) {
                n++;
                String[] in=str.split(",");
                inp1=Integer.valueOf(in[0]).intValue();
                inp2=Integer.valueOf(in[1]).intValue();
                pos[inp1]=inp2;
            }
        } catch (IOException e) {}

        //read e.txt
        try {
            BufferedReader br = new BufferedReader(new FileReader("F:\\homeworkcode\\6511javahw1\\e.txt"));
            String str;
            while ((str = br.readLine()) != null) {
                m++;
                String[] in=str.split(",");
                inp1=Integer.valueOf(in[0]).intValue();
                inp2=Integer.valueOf(in[1]).intValue();
                inp3=Double.valueOf(in[2]);
                if(inp3<g[inp1][inp2]) g[inp1][inp2]=g[inp2][inp1]=inp3;
            }
        } catch (IOException e) {}

        //input start and end point
        Scanner ip=new Scanner(System.in);
        String ch=new String();
        ch=ip.next();
        String[] in=ch.split(",");
        S=Integer.valueOf(in[1]).intValue();
        ch=ip.next();
        in=ch.split(",");
        D=Integer.valueOf(in[1]).intValue();
    }
    //output
    public static void Output(){
        System.out.println("AStar result:"+dis[D]);
        System.out.println("Running Time："+(EndTime-StartTime)+"ms");
        System.out.println("time complexity：nearly O(E log V)");
        System.out.println("space complexity：O(E+V)，E is the edge，V is the point");
    }

    //AStar algorithm
    public static void main(String[] args) {
        Initial();
        Read();

        //start the timer
        StartTime = System.currentTimeMillis();

        //Priority queue
        top.u=S;top.f=cal(pos[S],pos[D]);dis[S]=0;f[S]=cal(pos[S],pos[D]);
        PriorityQueue<NODE>pQ=new PriorityQueue<NODE>(com);pQ.add(top);
        while(!pQ.isEmpty()){
            top=pQ.poll();
            if(vis[top.u]==1) continue;
//            System.out.print("u:"+top.u);
            vis[top.u]=1;
            if(top.u==D) break;
            for(int i=0;i<100;i++){
                if(i!=top.u & dis[i]>dis[top.u]+g[top.u][i]){
                    dis[i]=dis[top.u]+g[top.u][i];
                    f[i]=cal(pos[i],pos[D]);
                    pre[i]=top.u;
                    pQ.add(new NODE(i,f[i]));
                }
            }
        }
        //end the timer
        EndTime = System.currentTimeMillis();

        //output
        Output();
    }

    //comparator
    static Comparator<NODE>com=new Comparator<NODE>() {
        public int compare(NODE o1, NODE o2) {
            if(o1.f>o2.f) return 1;
            else return -1;
        }
    };
}
