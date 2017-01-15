#include <iostream>
#include <string>
#include <thread>
#include <vector>


struct Result {
  int line;
  int position;
  int length;
};

std::string search() {
  return "";
}

std::string FindPalindromeStatic(std::vector<std::string> const& lines,
                                 unsigned int numThreads) {
  std::vector<std::thread> threads;
  for (int i = 0; i < numThreads; ++numThreads)
    threads.emplace_back(search);
  return "";
}

int main() {
  std::vector<std::string> lines {"PabbAD", "Quote"};
  FindPalindromeStatic(lines, 3);
}
