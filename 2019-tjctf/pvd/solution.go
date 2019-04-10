package main

import (
	"bytes"
	"fmt"
	"image"
	"image/color"
	_ "image/png"
	"os"
)

var (
	indices = []int{0, 8, 16, 32, 64, 128, 256}
	sizes   = []uint{3, 3, 4, 5, 6, 7}
)

func test() {
	p := image.Point{0, 0}
	w, h := 5, 4
	for i := 0; i < w*h; i++ {
		fmt.Println(p)
		p = next(p, w, h)
	}
}

func main() {
	f, err := os.Open("phase2plans.png")
	if err != nil {
		panic(err)
	}

	img, _, err := image.Decode(f)
	f.Close()
	if err != nil {
		panic(err)
	}

	w, h := img.Bounds().Dx(), img.Bounds().Dy()
	p := image.Point{0, 0}

	var out bytes.Buffer
	for i := 0; i < w*h; i++ {
		pn := next(p, w, h)
		g1 := int(img.At(p.X, p.Y).(color.Gray).Y)
		g2 := int(img.At(pn.X, pn.Y).(color.Gray).Y)
		p = next(pn, w, h)

		value, size := extract(g1, g2)
		for size > 0 {
			size--
			if value&(1<<size) == 1<<size {
				out.WriteByte(1)
			} else {
				out.WriteByte(0)
			}
		}
	}

	for i := 0; i < out.Len(); i += 8 {
		var b byte
		for j := 0; j < 8; j++ {
			o, _ := out.ReadByte()
			b = b<<1 | o
		}
		fmt.Printf("%c", b)
	}
}

func next(p image.Point, w, h int) image.Point {
	if p.Y%2 == 0 {
		p.X++
	} else {
		p.X--
	}

	if p.X == -1 {
		p.X++
		p.Y++
	} else if p.X == w {
		p.X--
		p.Y++
	}
	return p
}

func convert(a, b, m, d int) (int, int) {
	f, c := m/2, (m+1)/2
	if d%2 == 0 {
		return a - f, b + c
	}
	return a - c, b + f
}

func extract(a, b int) (int, uint) {
	diff := a - b
	if diff < 0 {
		diff = -diff
	}

	k := 0
	for diff >= indices[k+1] {
		k++
	}
	ap, bp := convert(a, b, indices[k+1]-diff-1, diff)

	if ap >= 256 || ap < 0 || bp >= 256 || bp < 0 {
		return 0, 0
	}

	return (diff - indices[k]) & (1<<sizes[k] - 1), sizes[k]
}
