#ifndef GRAPHICS_OPTIONS_H
#define GRAPHICS_OPTIONS_H

#include <cmath>
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
  double verticalLength;
  double horizontalLength;

 public:
  RectangleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                   double verticalLength, double horizontalLength);

  double getVerticalLength();
  double getHorizontalLength();
};

class TriangleOptions : public GraphicsOptions {
 private:
  double lengthOne;
  double lengthTwo;
  double lengthThree;

 public:
  TriangleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                  double lengthOne, double lengthTwo, double lengthThree);

  double getLengthOne();
  double getLengthTwo();
  double getLengthThree();
};

class CircleOptions : public GraphicsOptions {
 private:
  double radius;

 public:
  CircleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                double radius);

  double getRadius();
};

#endif