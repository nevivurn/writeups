package main

import (
	"fmt"
	"image"
	_ "image/png"
	"os"
)

func main() {
	f, err := os.Open("galaxy.png")
	if err != nil {
		panic(err)
	}
	img, _, err := image.Decode(f)
	f.Close()
	if err != nil {
		panic(err)
	}

	for y := 0; y < img.Bounds().Dy(); y++ {
		for x := 0; x < img.Bounds().Dx(); x++ {
			r, g, b, _ := img.At(x, y).RGBA()
			fmt.Print(r & 1)
			fmt.Print(g & 1)
			fmt.Print(b & 1)
		}
	}
}
