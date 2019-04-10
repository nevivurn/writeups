package main

import (
	"bufio"
	"bytes"
	"encoding/base64"
	"fmt"
	"image"
	"image/draw"
	_ "image/jpeg"
	"io"
	"math"
	"net"
)

func main() {
	c, err := net.Dial("tcp", "p1.tjctf.org:8005")
	if err != nil {
		panic(err)
	}
	defer c.Close()

	in := bufio.NewScanner(c)

	// Skip first line
	in.Scan()

	for i := 0; i < 100; i++ {
		in.Scan()
		fmt.Println(in.Text())

		in.Scan()
		data := in.Bytes()

		rd := base64.NewDecoder(base64.StdEncoding, bytes.NewReader(data))
		ans, err := solve(rd)
		if err != nil {
			panic(err)
		}

		fmt.Fprintln(c, ans)
		in.Scan()
		fmt.Println(in.Text())
		in.Scan()
	}

	in.Scan()
	fmt.Println(in.Text())

	if err := in.Err(); err != nil {
		panic(err)
	}
}

func toRGB(img image.Image) *image.RGBA {
	if rgb, ok := img.(*image.RGBA); ok {
		return rgb
	}

	rgb := image.NewRGBA(img.Bounds())
	draw.Draw(rgb, img.Bounds(), img, img.Bounds().Min, draw.Src)
	return rgb
}

func dist(a, b image.Point) int {
	dx, dy := a.X-b.X, a.Y-b.Y
	dx *= dx
	dy *= dy
	return int(math.Sqrt(float64(dx + dy)))
}

func solve(r io.Reader) (int, error) {
	// Read image
	img, _, err := image.Decode(r)
	if err != nil {
		return 0, err
	}

	// Convert to RGB
	rgb := toRGB(img)

	// Init grid
	w, h := rgb.Bounds().Dx(), rgb.Bounds().Dy()
	grid := make([][]int, w)
	for x := 0; x < w; x++ {
		grid[x] = make([]int, h)
	}

	var cnt int
	for x := 0; x < w; x++ {
		// up-down
		cnt = 0
		for y := 0; y < h; y++ {
			grid[x][y] = cnt

			if rgb.RGBAAt(x, y).R < 128 {
				cnt++
			} else {
				cnt = 0
			}
		}

		// down-up
		cnt = 0
		for y := h - 1; y >= 0; y-- {
			if grid[x][y] > cnt {
				grid[x][y] = cnt
			}

			if rgb.RGBAAt(x, y).R < 128 {
				cnt++
			} else {
				cnt = 0
			}
		}
	}
	for y := 0; y < h; y++ {
		// left-right
		cnt = 0
		for x := 0; x < w; x++ {
			if grid[x][y] > cnt {
				grid[x][y] = cnt
			}

			if rgb.RGBAAt(x, y).R < 128 {
				cnt++
			} else {
				cnt = 0
			}
		}

		// right-left
		cnt = 0
		for x := w - 1; x >= 0; x-- {
			if grid[x][y] > cnt {
				grid[x][y] = cnt
			}

			if rgb.RGBAAt(x, y).R < 128 {
				cnt++
			} else {
				cnt = 0
			}
		}
	}

	// Detect circles
	var circles []image.Point
	for x := 1; x < w-1; x++ {
		for y := 1; y < h-1; y++ {
			cur := grid[x][y]
			if cur > grid[x+1][y] && cur > grid[x-1][y] &&
				cur > grid[x][y+1] && cur > grid[x][y-1] {
				circles = append(circles, image.Point{x, y})
			}
		}
	}

	// n^2 loop for minimum distance
	mindist := w + h
	for i, a := range circles {
		for _, b := range circles[i+1:] {
			if d := dist(a, b); d < mindist {
				mindist = d
			}
		}
	}

	return mindist, nil
}
