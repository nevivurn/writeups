package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
)

var (
	sbox = []byte{210, 213, 115, 178, 122, 4, 94, 164, 199, 230, 237, 248, 54,
		217, 156, 202, 212, 177, 132, 36, 245, 31, 163, 49, 68, 107,
		91, 251, 134, 242, 59, 46, 37, 124, 185, 25, 41, 184, 221,
		63, 10, 42, 28, 104, 56, 155, 43, 250, 161, 22, 92, 81,
		201, 229, 183, 214, 208, 66, 128, 162, 172, 147, 1, 74, 15,
		151, 227, 247, 114, 47, 53, 203, 170, 228, 226, 239, 44, 119,
		123, 67, 11, 175, 240, 13, 52, 255, 143, 88, 219, 188, 99,
		82, 158, 14, 241, 78, 33, 108, 198, 85, 72, 192, 236, 129,
		131, 220, 96, 71, 98, 75, 127, 3, 120, 243, 109, 23, 48,
		97, 234, 187, 244, 12, 139, 18, 101, 126, 38, 216, 90, 125,
		106, 24, 235, 207, 186, 190, 84, 171, 113, 232, 2, 105, 200,
		70, 137, 152, 165, 19, 166, 154, 112, 142, 180, 167, 57, 153,
		174, 8, 146, 194, 26, 150, 206, 141, 39, 60, 102, 9, 65,
		176, 79, 61, 62, 110, 111, 30, 218, 197, 140, 168, 196, 83,
		223, 144, 55, 58, 157, 173, 133, 191, 145, 27, 103, 40, 246,
		169, 73, 179, 160, 253, 225, 51, 32, 224, 29, 34, 77, 117,
		100, 233, 181, 76, 21, 5, 149, 204, 182, 138, 211, 16, 231,
		0, 238, 254, 252, 6, 195, 89, 69, 136, 87, 209, 118, 222,
		20, 249, 64, 130, 35, 86, 116, 193, 7, 121, 135, 189, 215,
		50, 148, 159, 93, 80, 45, 17, 205, 95}
	p     = []byte{3, 9, 0, 1, 8, 7, 15, 2, 5, 6, 13, 10, 4, 12, 11, 14}
	rsbox = make([]byte, len(sbox))
	rp    = make([]byte, len(p))

	keys = 16777216
)

func enc(key, pt, bufa, bufb []byte) string {
	h := md5.New()
	h.Write(key)
	key = h.Sum(nil)

	copy(bufa, pt)
	for i := 0; i < 16; i++ {
		for i, c := range bufa {
			bufb[rp[i]] = sbox[c^key[i]]
		}
		bufa, bufb = bufb, bufa
	}
	return string(bufa)
}

func dec(key, ct, bufa, bufb []byte) string {
	h := md5.New()
	h.Write(key)
	key = h.Sum(nil)

	copy(bufa, ct)
	for i := 0; i < 16; i++ {
		for i, c := range bufa {
			bufb[p[i]] = rsbox[c] ^ key[p[i]]
		}
		bufa, bufb = bufb, bufa
	}
	return string(bufa)
}

func main() {
	for i, b := range sbox {
		rsbox[b] = byte(i)
	}
	for i, b := range p {
		rp[b] = byte(i)
	}

	allKeys := make([][]byte, keys)
	grid := make([]byte, keys*3)
	for i := 0; i < keys; i++ {
		grid[i*3+2] = byte(i & 0xff)
		grid[i*3+1] = byte((i >> 8) & 0xff)
		grid[i*3+0] = byte((i >> 16) & 0xff)
		allKeys[i] = grid[i*3 : i*3+3]
	}

	plain := []byte("16 bit plaintext")
	cipher, _ := hex.DecodeString("0467a52afa8f15cfb8f0ea40365a6692")
	flag, _ := hex.DecodeString("04b34e5af4a1f5260f6043b8b9abb4f8")

	a := make([]byte, 16)
	b := make([]byte, 16)

	fmt.Println("forward mapping...")
	forward := make(map[string]int, keys)
	for i, key := range allKeys {
		forward[enc(key, plain, a, b)] = i
	}

	fmt.Println("reverse mapping...")
	ans := make([]int, 2)
	for i, key := range allKeys {
		ind, ok := forward[dec(key, cipher, a, b)]
		if ok {
			ans[0], ans[1] = ind, i
			break
		}
	}

	fmt.Println("keys:", ans[0], ans[1])
	fmt.Println(dec(allKeys[ans[0]], []byte(dec(allKeys[ans[1]], flag, a, b)), a, b))
}
