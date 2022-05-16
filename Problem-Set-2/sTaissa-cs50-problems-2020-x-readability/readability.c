#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //reading the text and declaring variables
    string t = get_string("Texto: ");
    int n = strlen(t);
    float letters = 0, words = 0, sentences = 0;

    //counting letters, words and sentences
    for (int i = 0; i < n; i++)
    {
        if (isalpha(t[i]))
        {
            letters++;
        }
        else if (isspace(t[i]) || i == n - 1)
        {
            words++;
        }
        if (t[i] == '.' || t[i] == '!' || t[i] == '?')
        {
            sentences++;
        }
    }

    //apply the Coleman-Liau index
    float grade = 0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8;

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", round(grade));
    }
}