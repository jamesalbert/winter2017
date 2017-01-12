#include <iostream>
#include <string>
#include <thread>
#include <vector>

std::string search() {
  return "";
}

std::string FindPalindromeStatic(std::vector<std::string> const& lines, unsigned int numThreads) {
  std::vector<std::thread> threads;
  for (int i = 0; i < numThreads; ++numThreads)
    threads.emplace_back(search);
  return "";
}

int main() {
  std::vector<std::string> lines {"PabbAD", "Quote"};
  FindPalindromeStatic(lines, 3);
}
