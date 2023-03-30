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
                                   ShapeOptions& shapeOptions, double width,
                                   double height)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->height = height;
  this->width = width;
}
double RectangleOptions::getHeight() { return height; }
double RectangleOptions::getWidth() { return width; }

std::pair<double, double> RectangleOptions::getScaledRectangleLengths() {
  double imageWidth = getCanvasOptions().getWidth();
  double imageHeight = getCanvasOptions().getHeight();

  double heightScaleFactor = (imageHeight / pow(height, 1.3));
  double widthScaleFactor = (imageWidth / pow(width, 1.3));
  double rectangleHeight = height * heightScaleFactor;
  double rectangleWidth = width * widthScaleFactor;

  return {rectangleWidth, rectangleHeight};
}

std::pair<double, double> RectangleOptions::getRectangleCentrePoint() {
  double imageWidth = getCanvasOptions().getWidth();
  double imageHeight = getCanvasOptions().getHeight();

  return {imageWidth / 2, imageHeight / 2};
}

std::pair<double, double> RectangleOptions::getRectangleUpperLeft() {
  auto centrePoint = getRectangleCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first - (rectangleHeight / 2),
          centrePoint.second - (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleLowerRight() {
  auto centrePoint = getRectangleCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first + (rectangleHeight / 2),
          centrePoint.second + (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleUpperRight() {
  auto centrePoint = getRectangleCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first + (rectangleHeight / 2),
          centrePoint.second - (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleLowerLeft() {
  auto centrePoint = getRectangleCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first - (rectangleHeight / 2),
          centrePoint.second + (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleTextWidth() {
  auto upperRight = getRectangleUpperRight();
  auto upperLeft = getRectangleUpperLeft();

  return {(upperLeft.first + upperRight.first) / 2 - 20, upperLeft.second - 5};
}

std::pair<double, double> RectangleOptions::getRectangleTextHeight() {
  auto upperLeft = getRectangleUpperLeft();
  auto lowerLeft = getRectangleLowerLeft();

  return {lowerLeft.first + 5, (lowerLeft.second + upperLeft.second) / 2};
}

TriangleOptions::TriangleOptions(CanvasOptions& canvasOptions,
                                 ShapeOptions& shapeOptions, double sideA,
                                 double sideB, double sideC)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->sideA = sideA;
  this->sideB = sideB;
  this->sideC = sideC;
}

double TriangleOptions::getSideA() { return sideA; }
double TriangleOptions::getSideB() { return sideB; }
double TriangleOptions::getSideC() { return sideC; }

CircleOptions::CircleOptions(CanvasOptions& canvasOptions,
                             ShapeOptions& shapeOptions, double radius)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->radius = radius;
}

double CircleOptions::getRadius() { return radius; }