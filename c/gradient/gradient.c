/**
 * Copyright (c) 2015, Yanan Zhao
 * All rights reserved.
 *
 * Authors: Yanan Zhao <ya_nanzhao@hotmail.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 *   * Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 *
 *   * Neither the name of gradient nor the names of its
 *     contributors may be used to endorse or promote products derived from
 *     this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <assert.h>
#include <time.h>

static int _calc_gradient_one_pixel(int gx, int gy)
{
    int g;

    if (gx == 0) {
        return 0xFF; /* magic number */
    }
    else {
        g = gy / gx;
    }

    return g;
}

static void _calc_single_line(int *gradient, uint8_t *image,
        int width, int height, int y)
{
    int U[3]; // up row
    int M[3]; // current/middle row
    int D[3]; // bottom/down row

    int off_up_row     = (y - 1) * width;
    int off_curr_row   = y * width;
    int off_bottom_row = (y + 1) * width;

    U[1] = image[off_up_row    ];
    U[2] = image[off_up_row + 1];

    M[1] = image[off_curr_row    ];
    M[2] = image[off_curr_row + 1];

    D[1] = image[off_bottom_row    ];
    D[2] = image[off_bottom_row + 1];

    int gx, gy;
    int off_gradient = y * width; // intra mode array stride
    for (int x = 1; x < width - 1; x++) {
        U[0] = U[1];
        U[1] = U[2];
        U[2] = image[off_up_row + (x + 1)];

        M[0] = M[1];
        M[1] = M[2];
        M[2] = image[off_curr_row + (x + 1)];

        D[0] = D[1];
        D[1] = D[2];
        D[2] = image[off_bottom_row + (x + 1)];

        gy = (U[0] + 2 * U[1] + U[2]) - (D[0] + 2 * D[1] + D[2]);
        gx = (U[2] + 2 * M[2] + D[2]) - (U[0] + 2 * M[0] + D[0]);

        gradient[off_gradient + x] = _calc_gradient_one_pixel(gx, gy);
    }
}

static void _calc_mutiple_lines(int *gradient, uint8_t *image,
        int width, int height, int num_lines, int y)
{
#define EST_MODE_LINES (4)
    int buf[EST_MODE_LINES + 2][3]; /* 6 rows * 3 columns */
    int offset[6] = {(y-1)*width, (y)*width, (y+1)*width,
        (y+2)*width, (y+3)*width, (y+4)*width};

    // 3x3 matrix for gradient calculation
    int *U; // up row
    int *M; // current/middle row
    int *D; // bottom/down row

    for (int i = 0; i < num_lines + 2; i++) {
        buf[i][1] = image[offset[i] + 0];
        buf[i][2] = image[offset[i] + 1];
    }

    int gx, gy;
    for (int x = 1; x < width - 1; x++) {
        for (int i = 0; i < num_lines + 2; i++) { //update left/middle/right pixel
            buf[i][0] = buf[i][1];
            buf[i][1] = buf[i][2];
            buf[i][2] = image[offset[i] + (x + 1)];
        }

        for (int i = 0; i < num_lines; i++) {
            U = buf[i + 0]; // upper row
            M = buf[i + 1]; // current/middle row
            D = buf[i + 2]; // bottom/down row
            gy = (U[0] + 2 * U[1] + U[2]) - (D[0] + 2 * D[1] + D[2]);
            gy = (U[2] + 2 * M[2] + D[2]) - (U[0] + 2 * M[0] + D[0]);

            gradient[(y+i)*width + x] = _calc_gradient_one_pixel(gx, gy);
        }
    }
}

//--------------------------------------------------------------------------
//                  Calculate Gradient for Whole Image
//--------------------------------------------------------------------------
/**
 * calculate gradients for whole picture by definition
 * one PIXEL each loop
 */
static void _calc_gradients_pix_by_pix(int *gradient, uint8_t *image,
        int width, int height)
{
    uint8_t *U;
    uint8_t *M;
    uint8_t *D;

    int gy, gx;
    int i, j;
    for (j = 1; j < height - 1; j++) {
        U = image + (j - 1) * width + 1;
        M = image + (j + 0) * width + 1;
        D = image + (j + 1) * width + 1;

        for (i = 1; i < width - 1; i++) {
            gy = (U[-1] + 2 * U[0] + U[1]) - (D[-1] + 2 * D[0] + D[1]); 
            gx = (U[1] + 2 * M[1] + D[1]) - (U[-1] + 2 * M[-1] + D[-1]); 
            gradient[j * width + i] = _calc_gradient_one_pixel(gx, gy);

            U++;
            M++;
            D++;
        }
    }
}

/**
 * calculate gradients for whole picture, optimized
 * one LINE of PIXELs each loop
 */
static void _calc_gradients_line_by_line(int *gradient, uint8_t *image,
        int width, int height)
{
    for (int y = 1; y < height - 1; y++) {
        _calc_single_line(gradient, image, width, height, y);
    }
}

/**
 * calculate gradients for whole picture, optimized
 * multiple LINEs of PIXELs each loop
 */
static void _calc_gradients_by_mutiple_lines(int *gradient, uint8_t *image,
        int width, int height)
{
    int y;
    int num_lines = 1;
    for (y = 1; y < height - 1 - num_lines; y += num_lines) {
        _calc_mutiple_lines(gradient, image, width, height, num_lines, y);
    }
    for (; y < height - 1; y++) {
        _calc_single_line(gradient, image, width, height, y);
    }
}

void calc_gradients_whole_pic(int *gradient, uint8_t *image,
        int width, int height)
{
    assert(gradient != NULL);
    assert(image != NULL);

    clock_t start;

#define BENCH_INIT(repetitions) \
    start = clock(); \
    for (int i = 0; i < repetitions; i++) {

#define BENCH_FINISH(method) \
    } \
    printf("\n[%s] elapsed time: %.4f\n", method, \
            (double)(clock() - start) / CLOCKS_PER_SEC);

    int repetitions = 50;
    printf("benchmarking ... repetitions %d\n", repetitions);

    BENCH_INIT(repetitions);
    _calc_gradients_pix_by_pix(gradient, image, width, height);
    BENCH_FINISH("OnePixelEachLoop");

    BENCH_INIT(repetitions);
    _calc_gradients_line_by_line(gradient, image, width, height);
    BENCH_FINISH("OneLineEachLoop");

    BENCH_INIT(repetitions);
    _calc_gradients_by_mutiple_lines(gradient, image, width, height);
    BENCH_FINISH("MultipleLinesEachLoop");

#undef BENCH_INIT
#undef BENCH_FINISH
    /* printf("\nGradient Image:\n"); */
    /* int i, j; */
    /* for (j = 0; j < height; j++) { */
    /*     for (i = 0; i < width; i++) { */
    /*         printf("%3d ", gradient[j * width + i]); */
    /*     } */
    /*     printf("\n"); */
    /* } */

}
