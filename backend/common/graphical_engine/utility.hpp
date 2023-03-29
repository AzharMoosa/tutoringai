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

enum FileType { PNG, JPEG };
static const string fileTypeMapping[] = {".png", ".jpeg"};

enum Shape { Rectangle, Triangle, Circle };
static const string shapeMapping[] = {"rectangle", "triangle", "circle"};

#endif