#ifndef UTILITY_H
#define UTILITY_H
#include <sstream>

using std::string;

template <typename T>
string precision_to_string(const T value, const int n = 2) {
  std::ostringstream output;
  output.precision(n);
  output << std::fixed << value;
  return std::move(output).str();
}

#endif