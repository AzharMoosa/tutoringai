#ifndef GRAPHICAL_ENGINE_H
#define GRAPHICAL_ENGINE_H

#include <Magick++.h>

#include <algorithm>
#include <concepts>
#include <iostream>
#include <list>
#include <string>
#include <utility>

#include "graphics_options.hpp"
#include "utility.hpp"

using Magick::Color;
using Magick::Coordinate;
using Magick::Drawable;
using Magick::DrawableCircle;
using Magick::DrawableFillColor;
using Magick::DrawablePolygon;
using Magick::DrawableRectangle;
using Magick::DrawableStrokeColor;
using Magick::DrawableStrokeWidth;
using Magick::DrawableText;
using Magick::DrawableTextAntialias;
using Magick::Geometry;
using Magick::Image;
using Magick::InitializeMagick;
using std::string;

template <typename T>
concept GraphicsOptionsTypes = std::is_same<T, RectangleOptions>::value ||
                               std::is_same<T, TriangleOptions>::value ||
                               std::is_same<T, CircleOptions>::value;

class GraphicalEngine {
 private:
  Image generateImageCanvas(CanvasOptions canvasOptions);

  std::list<Drawable> initialiseDrawableList(ShapeOptions shapeOptions);

  void drawArrowCircle(std::list<Drawable> &drawList, double radius,
                       double centreX, double centreY, double perimX,
                       double perimY, double sf, string unit, bool textAlias,
                       int strokeWidth, string strokeColor,
                       string strokeFillColor);

 public:
  Shape drawShape(RectangleOptions options, std::list<Drawable> &drawList);
  Shape drawShape(CircleOptions options, std::list<Drawable> &drawList);
  Shape drawShape(TriangleOptions options, std::list<Drawable> &drawList);

  template <GraphicsOptionsTypes T>
  void draw(T options, FileType fileType = FileType::PNG) {
    try {
      Image image = generateImageCanvas(options.getCanvasOptions());

      std::list<Drawable> drawList =
          initialiseDrawableList(options.getShapeOptions());

      Shape shape = drawShape(options, drawList);

      image.draw(drawList);
      image.write(shapeMapping[shape] + fileTypeMapping[fileType]);
    } catch (std::exception &error_) {
      std::cout << "Error Creating Shape" << error_.what() << "\n";
    }
  }
};

#endif