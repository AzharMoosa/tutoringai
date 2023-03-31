#include "graphics_options.hpp"

CanvasOptions::CanvasOptions(int imageWidth, int imageHeight,
                             string backgroundColor) {
  this->imageWidth = imageWidth;
  this->imageHeight = imageHeight;
  this->backgroundColor = backgroundColor;
}

int CanvasOptions::getWidth() { return imageWidth; }
int CanvasOptions::getHeight() { return imageHeight; }
std::pair<double, double> CanvasOptions::getCentrePoint() {
  return {imageWidth / 2, imageHeight / 2};
}

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

std::pair<double, double> RectangleOptions::getRectangleUpperLeft() {
  auto centrePoint = getCanvasOptions().getCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first - (rectangleHeight / 2),
          centrePoint.second - (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleLowerRight() {
  auto centrePoint = getCanvasOptions().getCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first + (rectangleHeight / 2),
          centrePoint.second + (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleUpperRight() {
  auto centrePoint = getCanvasOptions().getCentrePoint();
  auto scaledRectangleLengths = getScaledRectangleLengths();
  double rectangleWidth = scaledRectangleLengths.first;
  double rectangleHeight = scaledRectangleLengths.second;

  return {centrePoint.first + (rectangleHeight / 2),
          centrePoint.second - (rectangleWidth / 2)};
}

std::pair<double, double> RectangleOptions::getRectangleLowerLeft() {
  auto centrePoint = getCanvasOptions().getCentrePoint();
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

double TriangleOptions::getAngleA(double a, double b, double c) {
  return acos((pow(b, 2.0) + pow(c, 2.0) - pow(a, 2.0)) / (2 * b * c));
}
double TriangleOptions::getAngleB(double a, double b, double c) {
  return acos((pow(a, 2.0) + pow(c, 2.0) - pow(b, 2.0)) / (2 * a * c));
}
double TriangleOptions::getAngleC(double a, double b, double c) {
  return acos((pow(a, 2.0) + pow(b, 2.0) - pow(c, 2.0)) / (2 * a * b));
}

TriangleType TriangleOptions::getTriangleType() {
  if (sideA == sideB && sideB == sideC) {
    return TriangleType::Equilateral;
  } else if (sideA == sideB || sideA == sideC || sideB == sideC) {
    return TriangleType::Isosceles;
  } else {
    return TriangleType::Scalene;
  }
}

std::list<Coordinate> TriangleOptions::getCoordinatesEquilateral() {
  double imageHeight = getCanvasOptions().getHeight();
  double imageWidth = getCanvasOptions().getWidth();
  auto centrePoint = getCanvasOptions().getCentrePoint();

  double s = imageHeight * 0.8;

  std::pair<double, double> coordinateA{centrePoint.first,
                                        centrePoint.second - (sqrt(3) / 6) * s};

  std::pair<double, double> coordinateB{centrePoint.first + (s / 2),
                                        centrePoint.second + (sqrt(3) / 6) * s};

  std::pair<double, double> coordinateC{centrePoint.first - (s / 2),
                                        centrePoint.second + (sqrt(3) / 6) * s};

  return std::list<Coordinate>{
      Coordinate(coordinateA.first, coordinateA.second),
      Coordinate(coordinateB.first, coordinateB.second),
      Coordinate(coordinateC.first, coordinateC.second)};
}

std::list<Coordinate> TriangleOptions::getCoordinatesScalene() {
  double imageHeight = getCanvasOptions().getHeight();
  double imageWidth = getCanvasOptions().getWidth();
  auto centrePoint = getCanvasOptions().getCentrePoint();

  double a = imageHeight * 0.9;
  double b = imageHeight * 0.8;
  double c = imageHeight * 0.7;

  double angleA = getAngleA(a, b, c);
  double angleB = getAngleB(a, b, c);
  double angleC = getAngleC(a, b, c);

  std::pair<double, double> coordinateA{
      centrePoint.first - (c / 2) * cos(angleA),
      centrePoint.second - (c / 2) * sin(angleA)};

  std::pair<double, double> coordinateB{
      centrePoint.first + (a / 2) * cos(angleB),
      centrePoint.second - (a / 2) * sin(angleB)};

  std::pair<double, double> coordinateC{
      centrePoint.first - (b / 2) * cos(angleC),
      centrePoint.second + (b / 2) * sin(angleC)};

  return std::list<Coordinate>{
      Coordinate(coordinateA.first, coordinateA.second),
      Coordinate(coordinateB.first, coordinateB.second),
      Coordinate(coordinateC.first, coordinateC.second)};
}

std::list<Coordinate> TriangleOptions::getCoordinatesIsosceles() {
  double imageHeight = getCanvasOptions().getHeight();
  double imageWidth = getCanvasOptions().getWidth();
  auto centrePoint = getCanvasOptions().getCentrePoint();

  double h = imageHeight * 0.8;
  double b = imageWidth / 2;

  std::pair<double, double> coordinateA{centrePoint.first,
                                        centrePoint.second - h / 2};

  std::pair<double, double> coordinateB{centrePoint.first - (b / 2), h};

  std::pair<double, double> coordinateC{centrePoint.first + (b / 2), h};

  return std::list<Coordinate>{
      Coordinate(coordinateA.first, coordinateA.second),
      Coordinate(coordinateB.first, coordinateB.second),
      Coordinate(coordinateC.first, coordinateC.second)};
}

std::list<Coordinate> TriangleOptions::getCoordinates() {
  TriangleType triangleType = getTriangleType();

  switch (triangleType) {
    case TriangleType::Equilateral:
      return getCoordinatesEquilateral();
    case TriangleType::Scalene:
      return getCoordinatesScalene();
    case TriangleType::Isosceles:
      return getCoordinatesIsosceles();
    default:
      throw std::invalid_argument("Triangle Type Not Found");
  }
}

CircleOptions::CircleOptions(CanvasOptions& canvasOptions,
                             ShapeOptions& shapeOptions, double radius)
    : GraphicsOptions(canvasOptions, shapeOptions) {
  this->radius = radius;
}

double CircleOptions::getRadius() { return radius; }