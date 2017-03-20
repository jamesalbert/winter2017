#include <algorithm>
#include <assert.h>
#include <cstdlib>
#include <cctype>
#include <cmath>
#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>
#include <mutex>
#include <thread>

/* Global variables, Look at their usage in main() */
int image_height;
int image_width;
int image_maxShades;
int inputImage[1000][1000];
int outputImage[1000][1000];
int num_threads;
int chunkSize;
int currentChunk;
int maxChunk;
std::mutex mtx;

int gen_x_grad(int x, int y) {
    return inputImage[y-1][x-1] +
           2*inputImage[y][x-1] +
           inputImage[y+1][x-1] -
           inputImage[y-1][x+1] -
           2*inputImage[y][x+1] -
           inputImage[y+1][x+1];
}

int gen_y_grad(int x, int y) {
    return inputImage[y-1][x-1] +
           2*inputImage[y-1][x] +
           inputImage[y-1][x+1] -
           inputImage[y+1][x-1] -
           2*inputImage[y+1][x] -
           inputImage[y+1][x+1];
}

void sobelify(int start) {
  int i, j, gx, gy, sum;
  while (currentChunk < image_height) {
    printf("%d < %d\n", currentChunk, image_height);
    mtx.lock();
    currentChunk = start + chunkSize;
    mtx.unlock();
    for (i = start; i < start + chunkSize - 1; i += 3) {
      for (j = 1; j < image_width - 1; j += 3) {
        gx = gen_x_grad(j, i);
        gy = gen_y_grad(j, i);
        sum = abs(gx) + abs(gy);
        sum = sum > 255 ? 255 : sum;
        sum = sum < 0 ? 0 : sum;
        outputImage[i][j] = outputImage[i][j+1] = outputImage[i][j+2] =
        outputImage[i+1][j] = outputImage[i+1][j+1] = outputImage[i+1][j+2] =
        outputImage[i+2][j] = outputImage[i+2][j+1] = outputImage[i+2][j+2] = sum;
      }
    }
    start = currentChunk;
  }
}

/* ****************Change and add functions below ***************** */
void dispatch_threads() {
  int i;
  std::vector<std::thread> threads;
  for (i = 0; i < num_threads; i++) {
    printf("%d\n", chunkSize * i);
    threads.insert(threads.begin(), std::thread(sobelify, (chunkSize * i) + 1));
  }
  for(std::vector<std::thread>::iterator it = threads.begin(); it != threads.end(); ++it) {
    it->join();
  }
}

/* ****************Need not to change the function below ***************** */

int main(int argc, char* argv[])
{
    if(argc != 5)
    {
        std::cout << "ERROR: Incorrect number of arguments. Format is: <Input image filename> <Output image filename> <Threads#> <Chunk size>" << std::endl;
        return 0;
    }

    std::ifstream file(argv[1]);
    if(!file.is_open())
    {
        std::cout << "ERROR: Could not open file " << argv[1] << std::endl;
        return 0;
    }
    num_threads = std::atoi(argv[3]);
    chunkSize  = std::atoi(argv[4]);

    std::cout << "Detect edges in " << argv[1] << " using " << num_threads << " threads\n" << std::endl;

    /* ******Reading image into 2-D array below******** */

    std::string workString;
    /* Remove comments '#' and check image format */
    while(std::getline(file,workString))
    {
        if( workString.at(0) != '#' ){
            if( workString.at(1) != '2' ){
                std::cout << "Input image is not a valid PGM image" << std::endl;
                return 0;
            } else {
                break;
            }
        } else {
            continue;
        }
    }
    /* Check image size */
    while(std::getline(file,workString))
    {
        if( workString.at(0) != '#' ){
            std::stringstream stream(workString);
            int n;
            stream >> n;
            image_width = n;
            stream >> n;
            image_height = n;
            break;
        } else {
            continue;
        }
    }

    /* maxChunk is total number of chunks to process */
    maxChunk = ceil((float)image_height/chunkSize);

    /* Check image max shades */
    while(std::getline(file,workString))
    {
        if( workString.at(0) != '#' ){
            std::stringstream stream(workString);
            stream >> image_maxShades;
            break;
        } else {
            continue;
        }
    }
    /* Fill input image matrix */
    int pixel_val;
    for( int i = 0; i < image_height; i++ )
    {
        if( std::getline(file,workString) && workString.at(0) != '#' ){
            std::stringstream stream(workString);
            for( int j = 0; j < image_width; j++ ){
                if( !stream )
                    break;
                stream >> pixel_val;
                inputImage[i][j] = pixel_val;
            }
        } else {
            continue;
        }
    }

    /************ Function that creates threads and manage dynamic allocation of chunks *********/
    dispatch_threads();

    /* ********Start writing output to your file************ */
    std::ofstream ofile(argv[2]);
    if( ofile.is_open() )
    {
        ofile << "P2" << "\n" << image_width << " " << image_height << "\n" << image_maxShades << "\n";
        for( int i = 0; i < image_height; i++ )
        {
            for( int j = 0; j < image_width; j++ ){
                ofile << outputImage[i][j] << " ";
            }
            ofile << "\n";
        }
    } else {
        std::cout << "ERROR: Could not open output file " << argv[2] << std::endl;
        return 0;
    }
    return 0;
}
