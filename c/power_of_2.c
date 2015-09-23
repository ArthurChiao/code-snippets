bool is_power_of_2(uint32_t x)
{
    return x & (x-1);
}

/**
 * find number N where (N >= x) and N is power of 2
 *
 * @from cJSON project
 *
 * @param n - n should be larger than 0x0
 */
uint32_t pow2gt (uint32_t x)
{
    --x;
    x|=x>>1;
    x|=x>>2;
    x|=x>>4;
    x|=x>>8;
    x|=x>>16;
    return x+1;
}

/**
 * find number N where (N =< x) and N is power of 2
 *
 * @param n - n should be smaller than 0xFFFFFFFF
 */
uint32_t pow2lt(uint32_t n)
{
    return pow2gt(++n) >> 1;
}
