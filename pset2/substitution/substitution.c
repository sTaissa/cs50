#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

//get the key
int main(int argc, string argv[])
{
    //check if a key was entered
    if (argc == 2)
    {
        //check if the key is the right size
        if (strlen(argv[1]) == 26)
        {
            bool c = true, d = true;

            for (int i = 0; i < 26; i++)
            {
                //check if the key has numbers
                if (!isalpha(argv[1][i]))
                {
                    c = false;
                }
                //check if the key has repeated characters
                for (int j = 0; j < 26; j++)
                {
                    if (argv[1][i] == argv[1][j] && i != j)
                    {
                        d = false;
                    }
                }
            }

            if (c == true && d == true)
            {
                //as the key is valid, prompt the plaintext
                string text = get_string("plaintext: ");

                //transform it into a ciphertext, paying attention to preserve case
                for (int i = 0, n = strlen(text); i < n; i++)
                {
                    int t = 0;

                    if (isupper(text[i]))
                    {
                        t = text[i] - 65;
                        if (islower(argv[1][t]))
                        {
                            argv[1][t] = toupper(argv[1][t]);
                        }
                        text[i] = argv[1][t];
                    }
                    else if (islower(text[i]))
                    {
                        t = text[i] - 97;
                        if (isupper(argv[1][t]))
                        {
                            argv[1][t] = tolower(argv[1][t]);
                        }
                        text[i] = argv[1][t];
                    }
                }
                printf("ciphertext: %s\n", text);
                return 0;
            }
            else if (c == false)
            {
                printf("Key must only contain alphabetic characters.\n");
                return 1;
            }
            else
            {
                printf("Key must not coutain repeated characters.\n");
                return 1;
            }
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }
}