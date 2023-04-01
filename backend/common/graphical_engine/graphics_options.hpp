#ifndef GRAPHICS_OPTIONS_H
#define GRAPHICS_OPTIONS_H

#include <Magick++.h>

#include <cmath>
#include <iostream>
#include <list>
#include <string>

#include "utility.hpp"

#define CM_TO_PIXEL(x) (x * 37.7952755906)

using Magick::Coordinate;
using std::string;
class CanvasOptions {
 private:
  /**
   * The image width, height, and background color of the canvas.
   */
  int imageWidth, imageHeight;
  string backgroundColor;

 public:
  /// Defines the options for the canvas in which shapes are drawn on.
  /// @brief Constructor.
  /// @param imageWidth The width of the canvas.
  /// @param imageHeight The height of the canvas.
  /// @param backgroundColor The background color of the canvas.
  CanvasOptions(int imageWidth, int imageHeight, string backgroundColor);

  /// @brief Gets the width of the canvas.
  /// @return The width of the canvas.
  int getWidth();

  /// @brief Gets the height of the canvas.
  /// @return The height of the canvas.
  int getHeight();

  std::pair<double, double> getCentrePoint();

  /// @brief Gets the background color of the canvas.
  /// @return The background color of the canvas.
  string getBackgroundColor();
};

class ShapeOptions {
 private:
  /**
   * The strokeColor, strokeWidth, and fillColor of the shape.
   */
  string strokeColor, fillColor;
  int strokeWidth;

 public:
  /// Defines the visual options of the shape that is drawn onto a canvas.
  /// @brief Constructor
  /// @param strokeColor The outline color of the shape.
  /// @param strokeWidth The width of the shape outline.
  /// @param fillColor The color of the shape.
  ShapeOptions(string strokeColor, int strokeWidth, string fillColor);

  /// @brief Gets the outline color of the shape.
  /// @return The color of the outline as a string.
  string getStrokeColor();

  /// @brief Gets the width of the shape outline.
  /// @return The width of the outline.
  int getStrokeWidth();

  /// @brief Gets the color of the shape.
  /// @return The color that the shape will be filled in with.
  string getFillColor();
};

class GraphicsOptions {
 private:
  /**
   * The canvas and shape options used when generating the graphical output.
   */
  CanvasOptions& canvasOptions;
  ShapeOptions& shapeOptions;

 public:
  /// Defines the canvas and shape options of the image.
  /// @brief Constructor
  /// @param canvasOptions
  /// @param shapeOptions
  GraphicsOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions);

  /// @brief Gets the canvas options.
  /// @return The canvas options specified.
  CanvasOptions getCanvasOptions();

  /// @brief Gets the shape options.
  /// @return The shape options specified.
  ShapeOptions getShapeOptions();
};

class RectangleOptions : public GraphicsOptions {
 private:
  /**
   * The vertical and horizontal length of the rectangles.
   */
  double height, width;

 public:
  /// Creates the options required to generate a rectangle with the specified
  /// vertical and horizontal lengths.
  /// @brief Constructor
  /// @param canvasOptions The canvas options in which the rectangle is drawn
  /// on.
  /// @param shapeOptions The shape options of the rectangle that is being
  /// drawn.
  /// @param width The width of the rectangle.
  /// @param height The height of the rectangle.
  RectangleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                   double width, double height);

  /// @brief Gets the height of the rectangle.
  /// @return The height of the rectangle.
  double getHeight();

  /// @brief Gets the width of the rectangle.
  /// @return The width of the rectangle.
  double getWidth();

  std::pair<double, double> getScaledRectangleLengths();

  std::pair<double, double> getRectangleUpperLeft();

  std::pair<double, double> getRectangleLowerRight();

  std::pair<double, double> getRectangleUpperRight();

  std::pair<double, double> getRectangleLowerLeft();

  std::pair<double, double> getRectangleTextWidth();

  std::pair<double, double> getRectangleTextHeight();
};

enum TriangleType { Equilateral, Scalene, Isosceles };

class TriangleTextCoordinate {
 private:
  double x, y;
  string label;

 public:
  TriangleTextCoordinate(double x, double y, string label) {
    this->x = x;
    this->y = y;
    this->label = label;
  }

  std::pair<double, double> getCoordinate() {
    return std::pair{this->x, this->y};
  }

  string getLabel() { return this->label; }
};

class TriangleOptions : public GraphicsOptions {
 private:
  /**
   * Defines the side lengths of the triangle.
   */
  double sideA, sideB, sideC;

  std::vector<std::pair<double, double>> getCoordinatesEquilateral();

  std::vector<std::pair<double, double>> getCoordinatesScalene();

  std::vector<std::pair<double, double>> getCoordinatesIsosceles();

  std::list<TriangleTextCoordinate> getTextCoordinatesIsosceles();

  std::list<TriangleTextCoordinate> getTextCoordinatesEquilateral();

  std::list<TriangleTextCoordinate> getTextCoordinatesScalene();

 public:
  /// Creates the options required to generate a triangle of side lengths A,
  /// B, C.
  /// @brief Constructor
  /// @param canvasOptions The canvas options in which the triangle is drawn
  /// on.
  /// @param shapeOptions The shape options of the triangle that is being
  /// drawn.
  /// @param sideA The length of triangle side a.
  /// @param sideB The length of triangle side b.
  /// @param sideC The length of triangle side c.
  TriangleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                  double sideA, double sideB, double sideC);

  /// @brief Gets the length of a.
  /// @return The side length a.
  double getSideA();

  /// @brief Gets the length of b.
  /// @return The side length b.
  double getSideB();

  /// @brief Gets the length of c.
  /// @return The side length c.
  double getSideC();

  double getAngleA(double a, double b, double c);

  double getAngleB(double a, double b, double c);

  double getAngleC(double a, double b, double c);

  TriangleType getTriangleType();

  std::vector<std::pair<double, double>> getCoordinates();

  std::list<TriangleTextCoordinate> getTextCoordinates();

  std::list<Coordinate> getCoordinateList();
};

class CircleOptions : public GraphicsOptions {
 private:
  /**
   * The radius of the circle.
   */
  double radius;

 public:
  /// Creates the options required to generate a circle with a specified radius.
  /// @brief Constructor
  /// @param canvasOptions The canvas options in which the circle is drawn on.
  /// @param shapeOptions The shape options of the circle that is being drawn.
  /// @param radius The radius of the circle.
  CircleOptions(CanvasOptions& canvasOptions, ShapeOptions& shapeOptions,
                double radius);

  /// @brief Gets the radius of the circle.
  /// @return The radius of the circle.
  double getRadius();
};

#endif