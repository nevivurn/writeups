
import java.util.*;
public class Checker{
    public static String wow(String b, int s){
        String r = "";
        for(int x=s; x<b.length()+s; x++){
            r+=b.charAt(x%b.length());
        }
        return r;
    }
    public static String woah(String b){
        String r = "";
        for(int x=0; x<b.length(); x++){
            if(b.charAt(x)=='0')
                r+='1';
            else
                r+='0';
        }
        return r;
    }
    public static String lol(int a){
        String s = Integer.toBinaryString(a);
        while(s.length()<8){
            s = "0" + s;
        }
        return s;
    }
    public static String encode(String plain){
        String b = "";
        Stack<Integer> t = new Stack<Integer>();
        for(int x=0; x<plain.length(); x++){
            int i = (int)plain.charAt(x);
            t.push(i);
        }
        for(int x=0; x<plain.length(); x++){
            b += lol(t.pop());
        }
        b = woah(b);
        b = wow(b,9);
        System.out.println(b);
        return b;
    }
    public static boolean check(String flag, String encoded){
        if(encode(flag).equals(encoded))
            return true;
        return false;
    }
    public static void main(String[] args){
        String flag = "redacted";
        String encoded = "10011001001110011001110100011001001010010011100110011101000101010001110100001001001100110001011100111001001010110001011100000101";
        System.out.println(check(flag,encoded));
    }
}
