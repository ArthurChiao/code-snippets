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

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <assert.h>
#include <time.h>

#include "gradient.h"

static uint8_t* generate_random_image(int width, int height)
{
    uint8_t *image = (uint8_t *)malloc(width * height);
    if (!image) {
        printf("malloc memory for image failed\n");
        return NULL;
    }

    int i, j;
    for (j = 0; j < height; j++) {
        for (i = 0; i < width; i++) {
            image[j * width + i] = random() % 256;
            //printf("%3d ", image[j * width + i]);
        }
        //printf("\n");
    }

    return image;
}

int main(int argc, char **argv)
{
    if (argc != 3) {
        printf("Usage: ./gradient <width> <height>\n");
        exit(1);
    }

    int width  = atoi(argv[1]);
    int height = atoi(argv[2]);
    assert(width > 0 && width <= 4096);
    assert(height > 0 && height <= 4096);
    printf("simulated image size: %dx%d\n", width, height);

    uint8_t *image = generate_random_image(width, height);
    if (!image) {
        printf("generate image failed\n");
        goto failed;
    }

    int *gradient = (int *)malloc(width * height * sizeof(int));
    if (!gradient) {
        printf("malloc gradient array failed\n");
        goto failed;
    }

    calc_gradients_whole_pic(gradient, image, width, height);

    free(image);
    image = NULL;

    free(gradient);
    gradient = NULL;

failed:
    if (image) {
        free(image);
    }
    if (gradient) {
        free(gradient);
    }

    return -1;
}
