#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    string n = get_string("Numero: ");
    int sum = 0;
    int size = strlen(n);

    //convert ASCII values to real numbers
    for (int i = 0; i < size; i++)
    {
        n[i] -= '0';
    }

    //verify if it is a card size
    if (size != 13 && size != 15 && size != 16)
    {
        printf("INVALID\n");
    }
    else
    {
        //Luhn's algorithm
        for (int i = size - 2; i >= 0; i -= 2)
        {
            int v = n[i] * 2;

            //if the product has two digits, divide them to sum
            if (v > 9)
            {
                while (v > 0)
                {
                    int digit = v % 10;
                    sum += digit;
                    v /= 10;
                }
            }
            else
            {
                sum += v;
            }
        }

        for (int i = size - 1; i >= 0; i -= 2)
        {
            sum += n[i];
        }

        if (sum % 10 == 0)
        {
            //check which card is
            if (n[0] == 3 && (n[1] == 4 || n[1] == 7))
            {
                printf("AMEX\n");
            }
            else if (n[0] == 5 && (n[1] == 1 || n[1] == 2 || n[1] == 3 || n[1] == 4 || n[1] == 5))
            {
                printf("MASTERCARD\n");
            }
            else if (n[0] == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
}