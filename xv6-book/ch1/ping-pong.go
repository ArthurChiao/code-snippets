package main

import (
	"fmt"
	"io"
)

// This implementation is incorrect
// Golang does not support fork().

func main() {
	r1, w1 := io.Pipe()
	r2, w2 := io.Pipe()

	// Peer 1
	go func() {
		buf := []byte("a")
		w2.Write(buf)
		fmt.Printf("Ping-pong started, Ping out\n")

		for {
			r1.Read(buf)
			w2.Write(buf)
			fmt.Printf("Ping out\n")
		}
	}()

	// Peer 2
	buf := []byte{}

	for {
		r2.Read(buf)
		w1.Write(buf)
		fmt.Printf("Pong out\n")
	}
}
