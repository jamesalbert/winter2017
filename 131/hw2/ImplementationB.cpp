#include "mpi.h"
#include <algorithm>
#include <functional>
#include <cstdlib>
#include <ctime>
#include <cctype>
#include <cmath>
#include <fstream>
#include <vector>
#include <string>
#include <iostream>
const static int ARRAY_SIZE = 130000;
using Lines = char[ARRAY_SIZE][16];

// To remove punctuations
struct letter_only: std::ctype<char>
{
    letter_only(): std::ctype<char>(get_table()) {}

    static std::ctype_base::mask const* get_table()
    {
        static std::vector<std::ctype_base::mask>
            rc(std::ctype<char>::table_size,std::ctype_base::space);

        std::fill(&rc['A'], &rc['z'+1], std::ctype_base::alpha);
        return &rc[0];
    }
};

void DoOutput(std::string word, int result)
{
    std::cout << "Word Frequency: " << word << " -> " << result << std::endl;
}

// ***************** Add your functions here *********************

int *GetFreq(Lines lines, int wordCount, std::string word, int rank) {
  int *freq = new int[1];
  *freq = 0;
  int i;
  for (i = 0; i < wordCount; i++) {
    std::string line = lines[i];
    if (!line.compare(word)) {
      ++(*freq);
    }
  }
  return freq;
}

int main(int argc, char* argv[])
{
    int *frequency = new int[1];
    int rank;
    int num_processes;
    int *to_return = NULL;
    double start_time, end_time;
    MPI_Datatype MPI_STR;

    // Setup MPI
    MPI_Init( &argc, &argv );
    MPI_Comm_rank( MPI_COMM_WORLD, &rank);
    MPI_Comm_size( MPI_COMM_WORLD, &num_processes);
    MPI_Type_contiguous(16, MPI_CHAR, &MPI_STR);
    MPI_Type_commit(&MPI_STR);

    // Three arguments: <input file> <search word> <part B1 or part B2 to execute>
    if(argc != 4)
    {
        if(rank == 0)
        {
            std::cout << "ERROR: Incorrect number of arguments. Format is: <filename> <word> <b1/b2>" << std::endl;
        }
        MPI_Finalize();
        return 0;
    }
    std::string word = argv[2];

    Lines lines;
    int* totalWords = new int[1];
    // Read the input file and put words into char array(lines)
    if (rank == 0) {
      std::ifstream file;
      file.imbue(std::locale(std::locale(), new letter_only()));
      file.open(argv[1]);
      std::string workString;
      int i = 0;
      while(file >> workString){
        memset(lines[i], '\0', 16);
        memcpy(lines[i++], workString.c_str(), workString.length());
      }
      *totalWords = i;
    }

  // ***************** Add code as per your requirement below *****************

  std::string mode = argv[3];
  Lines partialLines;
  start_time=MPI_Wtime();
  MPI_Bcast(totalWords, 1, MPI_INT, 0, MPI_COMM_WORLD);
  int partialLineCount = ceil(*totalWords/num_processes);
  MPI_Scatter(lines, partialLineCount, MPI_STR, partialLines, partialLineCount, MPI_STR, 0, MPI_COMM_WORLD);

  if( mode == "b1" )
  {
    int *freq = new int[1];
    freq = GetFreq(partialLines, partialLineCount, word, rank);
    MPI_Reduce(freq, frequency, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
  } else {
    int *freq = new int[1];
    int *prevFreq = new int[1];
    freq = GetFreq(partialLines, partialLineCount, word, rank);
    if (rank != 0) {
      MPI_Recv(prevFreq, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      *frequency += *prevFreq + *freq;
    }
    if (rank == num_processes - 1) {
      MPI_Send(frequency, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    } else {
      MPI_Send(frequency, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
    }
    if (rank == 0) {
      MPI_Recv(prevFreq, 1, MPI_INT, num_processes - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      *frequency += *prevFreq + *freq;
    }
  }

    if(rank == 0)
    {
        // Output the search word's frequency here
        DoOutput(word, *frequency);

    end_time=MPI_Wtime();
        std::cout << "Time: " << ((double)end_time-start_time) << std::endl;
    }

    MPI_Finalize();

    return 0;
}
