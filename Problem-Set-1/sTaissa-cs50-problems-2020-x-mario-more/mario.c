#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h;

    do
    {
        h = get_int("Between 1 and 8, how tall is the pyramid?\n");
    }
    while (h < 1 || h > 8);

    for (int i = 1; i <= h; i++)
    {
        for (int p = h - i; p > 0; p--)
        {
            printf(" ");
        }
        for (int q = i; q > 0; q--)
        {
            printf("#");
        }

        printf("  ");

        for (int q = i; q > 0; q--)
        {
            printf("#");
        }

        printf("\n");
    }
}