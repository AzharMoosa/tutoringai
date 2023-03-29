#include "graphical_engine.hpp"

Image GraphicalEngine::generateImageCanvas(CanvasOptions canvasOptions) {
  int imageWidth = canvasOptions.getWidth();
  int imageHeight = canvasOptions.getHeight();
  string backgroundColor = canvasOptions.getBackgroundColor();
  return Image(Geometry(imageWidth, imageHeight), Color(backgroundColor));
}

std::list<Drawable> GraphicalEngine::initialiseDrawableList(
    ShapeOptions shapeOptions) {
  std::list<Drawable> drawList;

  drawList.push_back(DrawableStrokeColor(shapeOptions.getStrokeColor()));
  drawList.push_back(DrawableStrokeWidth(shapeOptions.getStrokeWidth()));
  drawList.push_back(DrawableFillColor(shapeOptions.getFillColor()));

  return drawList;
}

Shape GraphicalEngine::drawShape(RectangleOptions options,
                                 std::list<Drawable> &drawList) {
  drawList.push_back(DrawableRectangle(10, 50, 110, 150));
  drawList.push_back(DrawableText(
      10, 50, precision_to_string(options.getHorizontalLength()) + "cm"));

  return Shape::Rectangle;
}

Shape GraphicalEngine::drawShape(CircleOptions options,
                                 std::list<Drawable> &drawList) {
  drawList.push_back(DrawableCircle(50, 50, 80, 80));

  return Shape::Circle;
}

Shape GraphicalEngine::drawShape(TriangleOptions options,
                                 std::list<Drawable> &drawList) {
  std::list<Coordinate> coordinates{Coordinate(50, 50), Coordinate(50, 10),
                                    Coordinate(90, 50)};

  drawList.push_back(DrawablePolygon(coordinates));

  return Shape::Triangle;
}

int main(int argc, char **argv) {
  InitializeMagick(*argv);
  GraphicalEngine engine = GraphicalEngine();
  CanvasOptions canvasOptions = CanvasOptions(200, 200, "white");
  ShapeOptions shapeOptions = ShapeOptions("black", 2, "white");

  RectangleOptions rectangleOptions =
      RectangleOptions(canvasOptions, shapeOptions, 2, 2);

  CircleOptions circleOptions = CircleOptions(canvasOptions, shapeOptions, 3);

  TriangleOptions triangleOptions =
      TriangleOptions(canvasOptions, shapeOptions, 1, 2, 3);

  engine.draw(rectangleOptions);
  engine.draw(circleOptions);
  engine.draw(triangleOptions);

  return 0;
}