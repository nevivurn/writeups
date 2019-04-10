import java.util.Random;

public class Rnd {
	public static void main(String[] args) {
		long ts = 1554422400;

		for (int i = 0; i < 2*24*60*60; i++) {
			long cur = ts-i;
			Random r = new Random(cur);

			String key  = String.format("%016x", ((long)(r.nextDouble()*10000000000L)));
			String ivec  = String.format("%016x", ((long)(r.nextDouble()*10000000000L)));
			System.out.printf("%d %s %s\n", cur, key, ivec);
		}
	}
}
