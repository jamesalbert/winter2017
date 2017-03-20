#include <omp.h>
#include <algorithm>
#include <cstdlib>
#include <cctype>
#include <cmath>
#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>

/* Global variables, Look at their usage in main() */
int image_height;
int image_width;
int image_maxShades;
int inputImage[1000][1000];
int outputImage[1000][1000];
int chunkSize;
std::vector<int> doneChunks = std::vector<int>(1000, 0);

/* ****************Change and add functions below ***************** */
void processStaticImage(){
  int rank = omp_get_thread_num();
  int num_processes = omp_get_num_threads();
  int x, y, sum, sumx, sumy;
  int GX[3][3], GY[3][3];
  /* 3x3 Sobel masks. */
  GX[0][0] = -1; GX[0][1] = 0; GX[0][2] = 1;
  GX[1][0] = -2; GX[1][1] = 0; GX[1][2] = 2;
  GX[2][0] = -1; GX[2][1] = 0; GX[2][2] = 1;

  GY[0][0] =  1; GY[0][1] =  2; GY[0][2] =  1;
  GY[1][0] =  0; GY[1][1] =  0; GY[1][2] =  0;
  GY[2][0] = -1; GY[2][1] = -2; GY[2][2] = -1;

  //chunkSize is the number of rows to be computed by this process
  int chunkSize = ceil(image_height / num_processes);
  int start_of_chunk = (rank * chunkSize);
  int end_of_chunk = start_of_chunk + chunkSize;
  std::cout << "Thread " << rank << " -> Processing Chunk starting at row " << start_of_chunk << std::endl;
  for( x = start_of_chunk; x < end_of_chunk; x++ ){
     for( y = 0; y < image_width; y++ ){
       sumx = 0;
       sumy = 0;

       if (x==0 || x==image_height || y==0 || y==image_width) {
         sum = 0;
       }
       else if (x == end_of_chunk) {
         sum = outputImage[x-1][y];
       }
       else if (y==image_width) {
         sum = outputImage[x][y-1];
       }
       else{

         for(int i=-1; i<=1; i++)  {
           for(int j=-1; j<=1; j++){
             sumx += (inputImage[x+i][y+j] * GX[i+1][j+1]);
           }
         }

         for(int i=-1; i<=1; i++)  {
           for(int j=-1; j<=1; j++){
             sumy += (inputImage[x+i][y+j] * GY[i+1][j+1]);
           }
         }

         sum = (abs(sumx) + abs(sumy));
         sum = sum >= 255 ? 255 : sum;
         sum = sum <= 0 ? 0 : sum;
       }
       outputImage[x][y] = sum;
     }
  }
}

void processDynamicImage(){
  int rank = omp_get_thread_num();
  int num_processes = omp_get_num_threads();
  int x, y, sum, sumx, sumy;
  int GX[3][3], GY[3][3];
  /* 3x3 Sobel masks. */
  GX[0][0] = -1; GX[0][1] = 0; GX[0][2] = 1;
  GX[1][0] = -2; GX[1][1] = 0; GX[1][2] = 2;
  GX[2][0] = -1; GX[2][1] = 0; GX[2][2] = 1;

  GY[0][0] =  1; GY[0][1] =  2; GY[0][2] =  1;
  GY[1][0] =  0; GY[1][1] =  0; GY[1][2] =  0;
  GY[2][0] = -1; GY[2][1] = -2; GY[2][2] = -1;

  //chunkSize is the number of rows to be computed by this process
  for (int i = 0; i < num_processes; i++) {
    if (doneChunks[i] == 0) {
      doneChunks[i] = 1;
      rank = i;
      break;
    }
  }
  int chunkSize = ceil(image_height / num_processes);
  int start_of_chunk = (rank * chunkSize);
  int end_of_chunk = start_of_chunk + chunkSize;
  std::cout << "Thread " << rank << " -> Processing Chunk starting at row " << start_of_chunk << std::endl;
  for( x = start_of_chunk; x < end_of_chunk; x++ ){
     for( y = 0; y < image_width; y++ ){
       sumx = 0;
       sumy = 0;

       if (x==0 || x==image_height || y==0 || y==image_width) {
         sum = 0;
       }
       else if (x == end_of_chunk) {
         sum = outputImage[x-1][y];
       }
       else if (y==image_width) {
         sum = outputImage[x][y-1];
       }
       else{

         for(int i=-1; i<=1; i++)  {
           for(int j=-1; j<=1; j++){
             sumx += (inputImage[x+i][y+j] * GX[i+1][j+1]);
           }
         }

         for(int i=-1; i<=1; i++)  {
           for(int j=-1; j<=1; j++){
             sumy += (inputImage[x+i][y+j] * GY[i+1][j+1]);
           }
         }

         sum = (abs(sumx) + abs(sumy));
         sum = sum >= 255 ? 255 : sum;
         sum = sum <= 0 ? 0 : sum;
       }
       outputImage[x][y] = sum;
     }
  }
}
void compute_sobel_static() {
  #pragma omp parallel for schedule(static)
    for (int i = 0; i < omp_get_num_threads(); i++) {
      processStaticImage();
    }
}

void compute_sobel_dynamic() {
  #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < omp_get_num_threads(); i++) {
      processDynamicImage();
    }
}
/* **************** Change the function below if you need to ***************** */

int main(int argc, char* argv[])
{
    if(argc != 5)
    {
        std::cout << "ERROR: Incorrect number of arguments. Format is: <Input image filename> <Output image filename> <Chunk size> <a1/a2>" << std::endl;
        return 0;
    }

    std::ifstream file(argv[1]);
    if(!file.is_open())
    {
        std::cout << "ERROR: Could not open file " << argv[1] << std::endl;
        return 0;
    }
    chunkSize  = std::atoi(argv[3]);

    std::cout << "Detect edges in " << argv[1] << " using OpenMP threads\n" << std::endl;

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

    /************ Call functions to process image *********/
    std::string opt = argv[4];
    if( !opt.compare("a1") )
    {
        double dtime_static = omp_get_wtime();
        compute_sobel_static();
        dtime_static = omp_get_wtime() - dtime_static;
        std::cout << "Lab 3 part A1 finished in " << dtime_static << std::endl;
    } else {
        double dtime_dyn = omp_get_wtime();
        compute_sobel_dynamic();
        dtime_dyn = omp_get_wtime() - dtime_dyn;
        std::cout << "Lab 3 part A2 finished in " << dtime_dyn << std::endl;
    }

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
