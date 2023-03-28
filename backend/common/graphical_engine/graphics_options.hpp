#ifndef GRAPHICS_OPTIONS_H
#define GRAPHICS_OPTIONS_H

#include <iostream>
#include <string>
using std::string;

class CanvasOptions {
 private:
  int imageWidth;
  int imageHeight;
  string backgroundColor;

 public:
  CanvasOptions(int imageWidth, int imageHeight, string backgroundColor);

  int getWidth();
  int getHeight();
  string getBackgroundColor();
};

class ShapeOptions {
 private:
  string strokeColor;
  int strokeWidth;
  string fillColor;

 public:
  ShapeOptions(string strokeColor, int strokeWidth, string fillColor);

  string getStrokeColor();
  int getStrokeWidth();
  string getFillColor();
};

class GraphicsOptions {
 private:
  CanvasOptions& canvasOptions;
  ShapeOptions& shapeOptions;

 public:
  GraphicsOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions);

  CanvasOptions getCanvasOptions();

  ShapeOptions getShapeOptions();
};

class RectangleOptions : public GraphicsOptions {
 private:
  int verticalLength;
  int horizontalLength;

 public:
  RectangleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                   int verticalLength, int horizontalLength);

  int getVerticalLength();
  int getHorizontalLength();
};

#endif