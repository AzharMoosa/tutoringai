#ifndef GRAPHICAL_ENGINE_H
#define GRAPHICAL_ENGINE_H

#include <Magick++.h>

#include <iostream>
#include <list>
#include <string>

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
using Magick::Geometry;
using Magick::Image;
using Magick::InitializeMagick;
using std::string;

class GraphicalEngine {
 private:
  Image generateImageCanvas(CanvasOptions canvasOptions);

  std::list<Drawable> initialiseDrawableList(ShapeOptions shapeOptions);

 public:
  void drawRectangle(RectangleOptions options);
  void drawCircle(CircleOptions options);
  void drawTriangle(TriangleOptions options);
};

#endif