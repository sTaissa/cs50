// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26*26;

//number of words in dictionary
unsigned int dic_size = 0;

//bool if loades or not
bool loaded;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int wsize = strlen(word);
    char w[wsize];

    //convert the word to a copy lowercase to compare
    for (int i = 0; i <= wsize; i++)
    {
        w[i] = tolower(word[i]);
    }

    //hash the word
    int index = hash(w);

     //compare strings
    if (table[index] != NULL) //if there is word in this index
    {
        if (strcmp(w, table[index]->word) == 0)
        {
            return true;
        }
        else
        {
            node *p = table[index];
            while (p->next != NULL)
            {
                p = p->next;

                if (strcmp(w, p->word) == 0)
                {
                    return true;
                }
            }
            return false;
        }
    }
    else
    {
        return false;
    }
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0, num1 = 0, num2 = 0;
    num1 = (word[0] - 97) * 26; //get the first character in int ASCII
    if (strlen(word) > 1)
    {
        num2 = word[1] - 97;// get the second
    }
    hash = num1 + num2;

    return hash;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //null the table
    for (int i = 0; i <= N; i++)
    {
        table[i] = NULL;
    }

    //open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        loaded = false;
        return false;
    }

    //read the words
    node *n;
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        //create a new node
        n = malloc(sizeof(node));
        if (n != NULL)
        {
            //copy the dictionary word to that node
            strcpy(n->word, word);
            n->next = NULL;

            //put into the hash table
            int index = hash(n->word);
            if (table[index] == NULL)
            {
                table[index] = n;
                dic_size++;
            }
            else //create a linked list
            {
                n->next = table[index];
                table[index] = n;
                dic_size++;
            }
        }
        else
        {
            loaded = false;
            return false;
        }
    }

    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded == true)
    {
        return dic_size;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *tmp, *c = table[i];
            while (c->next != NULL)
            {
                tmp = c;
                c = c->next;
                free(tmp);
            }
            free(c);
        }
    }
    return true;
}
