#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check for invalide usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //Open file
    FILE *image = fopen(argv[1], "r");
    if (image == NULL)
    {
        printf("The image could not be open\n");
        return 1;
    }

    //allocating memory for buffer to read and write
    BYTE *buffer = malloc(512);

    //counter of images
    int i = 0;

    //make sure filename have memory for the 3 digits
    char *filename = malloc(8);

    //create the file for the images
    FILE *img;

    //go across the file
    while (fread(buffer, 512, 1, image) != 0)
    {
        //verify the firts four bytes of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //writing the firts JPEG
            if (i == 0)
            {
                sprintf(filename, "%03i.jpg", 0);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);
            }
            //write the others JPEGs
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);
            }
            i++;
        }
        else
        {
            //check if a JPEG has already been found and continue to write it
            if (i > 0)
            {
                fwrite(buffer, 512, 1, img);
            }
        }
    }

    //free memory allocation and close the files
    free(buffer);
    free(filename);
    fclose(img);
    fclose(image);
}
