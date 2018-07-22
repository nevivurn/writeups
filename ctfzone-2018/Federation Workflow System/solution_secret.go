package main

import (
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"net"
)

const (
	//host = "localhost:7331"
	host   = "crypto-04.v7frkwrfyhsjtbpfcppnu.ctfz.one:7331"
	length = 48
	//charset = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_-"
	charset = "0123456789abcdef"
)

func genPad(n int) (string, int) {
	n %= 16

	pre := "../"
	post := "totp.secret: "

	if n%2 == 1 {
		pre = "../files/" + pre
	}

	for (16-(len(pre)+len(post))%16)%16 != n {
		pre += "./"
	}
	return pre + "totp.secret", len(pre) + len("totp.secret: ")
}

func getData(n int) ([]byte, []byte) {
	pad, padlen := genPad(n)

	c, err := net.Dial("tcp", host)
	if err != nil {
		panic(err)
	}
	defer c.Close()

	c.Write([]byte("file " + pad + "</msg>"))
	b, _ := ioutil.ReadAll(c)
	b = b[:len(b)-6]

	out := make([]byte, base64.StdEncoding.DecodedLen(len(b)))
	n, err = base64.StdEncoding.Decode(out, b)
	if err != nil {
		panic(err)
	}
	out = out[padlen/16*16 : n]

	return out, []byte(pad + ": ")
}

func send(b []byte) []byte {
	c, err := net.Dial("tcp", host)
	if err != nil {
		panic(err)
	}
	defer c.Close()

	c.Write([]byte("file " + string(b) + "</msg>"))
	b, _ = ioutil.ReadAll(c)
	b = b[:len(b)-6]

	out := make([]byte, base64.StdEncoding.DecodedLen(len(b)))
	_, err = base64.StdEncoding.Decode(out, b)
	if err != nil {
		panic(err)
	}

	return out[:16]
}

func cmp(a, b []byte) bool {
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func main() {
	//for i := 1; i <= 16; i++ {
	//	fmt.Println("len:", i, len(getData(i)))
	//}

	var plain []byte
	for len(plain) < length {
		data, pad := getData((len(plain) + 1) % 16)
		pad = append(pad, plain...)
		pad = append(pad, 'a')
		pad = pad[(len(pad)/16-1)*16:]

		fmt.Println(plain)

		blockInd := len(plain) / 16
		data = data[blockInd*16 : blockInd*16+16]

		for _, i := range charset {
			fmt.Println("trying ", i)
			pad[15] = byte(i)
			get := send(pad)
			if cmp(data, get) {
				fmt.Println("FOUND:", i)
				plain = append(plain, byte(i))
				break
			}
		}
	}

	fmt.Println(plain)
	fmt.Println(string(plain))
}
