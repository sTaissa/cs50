#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float av = 0.0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //get the average of the 3 colors
            av = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0; //remember float numbers need to be divided by float numbers

            //change the image color to new average
            image[i][j].rgbtBlue = (int) round(av);
            image[i][j].rgbtGreen = (int) round(av);
            image[i][j].rgbtRed = (int) round(av);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int k = width - 1;//remember the last element is always the width of array - 1
        for (int j = 0; j < width / 2; j++)
        {
            //change the positions of the first with the last in the line
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = tmp;
            k--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //make a copy of original image for calculations
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    //go across the image
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float sumR = 0.0, sumG = 0.0, sumB = 0.0, avC = 0.0;

            //go across the pixels around
            for (int hh = -1; hh < 2; hh++)//-1=anterior, 0=linha/coluna atual, 1=proxima linha/coluna
            {
                for (int ww = -1; ww < 2; ww++)
                {
                    if ((h + hh >= 0 && h + hh < height) && (w + ww >= 0 && w + ww < width))
                    {
                        //get the sum of each color around the pixel
                        sumR += copy[h + hh][w + ww].rgbtRed;
                        sumG += copy[h + hh][w + ww].rgbtGreen;
                        sumB += copy[h + hh][w + ww].rgbtBlue;
                        //increment the value to divide in the average futurally
                        avC ++;
                    }
                }
            }

            //change the pixel with the new value of each color
            image[h][w].rgbtRed = round(sumR / avC);
            image[h][w].rgbtGreen = round(sumG / avC);
            image[h][w].rgbtBlue = round(sumB / avC);
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //make a copy of original image for calculations
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    //create the kernels
    int gx [3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy [3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    //go across the image
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //initialize the calculate variables
            int gxr = 0, gxg = 0, gxb = 0;
            int gyr = 0, gyg = 0, gyb = 0;

            //go across the pixels around
            for (int hh = - 1; hh < 2; hh++)
            {
                for (int ww = - 1; ww < 2; ww++)
                {
                    int a = hh + h;
                    int b = ww + w;

                    if (a >= 0 && a < height && b >= 0 && b < width)
                    {
                        //get the multiplication of pixel per kernel
                        gxr += (gx[hh + 1][ww + 1] * copy[a][b].rgbtRed);
                        gxg += (gx[hh + 1][ww + 1] * copy[a][b].rgbtGreen);
                        gxb += (gx[hh + 1][ww + 1] * copy[a][b].rgbtBlue);

                        gyr += (gy[hh + 1][ww + 1] * copy[a][b].rgbtRed);
                        gyg += (gy[hh + 1][ww + 1] * copy[a][b].rgbtGreen);
                        gyb += (gy[hh + 1][ww + 1] * copy[a][b].rgbtBlue);
                    }
                }
            }

            //sobel algorithm
            int gr = gxr * gxr + gyr * gyr;
            int gg = gxg * gxg + gyg * gyg;
            int gb = gxb * gxb + gyb * gyb;

            //make sure it is int and a lower number
            gr = round(sqrt(gr));
            gg = round(sqrt(gg));
            gb = round(sqrt(gb));

            //make sure it is into 255
            if (gr >= 255)
            {
                gr = 255;
            }
            if (gg >= 255)
            {
                gg = 255;
            }
            if (gb >= 255)
            {
                gb = 255;
            }


            image[h][w].rgbtRed = gr;
            image[h][w].rgbtGreen = gg;
            image[h][w].rgbtBlue = gb;

        }
    }
    return;
}
