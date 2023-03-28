#include "graphics_options.hpp"

CanvasOptions::CanvasOptions(int imageWidth, int imageHeight,
                             string backgroundColor) {
  this->imageWidth = imageWidth;
  this->imageHeight = imageHeight;
  this->backgroundColor = backgroundColor;
}

int CanvasOptions::getWidth() { return imageWidth; }
int CanvasOptions::getHeight() { return imageHeight; }
string CanvasOptions::getBackgroundColor() { return backgroundColor; }

ShapeOptions::ShapeOptions(string strokeColor, int strokeWidth,
                           string fillColor) {
  this->strokeColor = strokeColor;
  this->strokeWidth = strokeWidth;
  this->fillColor = fillColor;
}

string ShapeOptions::getStrokeColor() { return strokeColor; }
int ShapeOptions::getStrokeWidth() { return strokeWidth; }
string ShapeOptions::getFillColor() { return fillColor; }

GraphicsOptions::GraphicsOptions(CanvasOptions& cOptions,
                                 ShapeOptions& sOptions)
    : canvasOptions(cOptions), shapeOptions(sOptions) {
  this->canvasOptions = cOptions;
  this->shapeOptions = sOptions;
}

CanvasOptions GraphicsOptions::getCanvasOptions() { return canvasOptions; }

ShapeOptions GraphicsOptions::getShapeOptions() { return shapeOptions; }

RectangleOptions::RectangleOptions(CanvasOptions& canvasOptions,
                                   ShapeOptions& shapeOptions,
                                   double verticalLength,
                                   double horizontalLength)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->verticalLength = verticalLength;
  this->horizontalLength = horizontalLength;
}
double RectangleOptions::getVerticalLength() { return verticalLength; }
double RectangleOptions::getHorizontalLength() { return horizontalLength; }

TriangleOptions::TriangleOptions(CanvasOptions& canvasOptions,
                                 ShapeOptions& shapeOptions, double lengthOne,
                                 double lengthTwo, double lengthThree)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->lengthOne = lengthOne;
  this->lengthTwo = lengthTwo;
  this->lengthThree = lengthThree;
}

double TriangleOptions::getLengthOne() { return lengthOne; }
double TriangleOptions::getLengthTwo() { return lengthTwo; }
double TriangleOptions::getLengthThree() { return lengthThree; }

CircleOptions::CircleOptions(CanvasOptions& canvasOptions,
                             ShapeOptions& shapeOptions, double radius)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->radius = radius;
}

double CircleOptions::getRadius() { return radius; }