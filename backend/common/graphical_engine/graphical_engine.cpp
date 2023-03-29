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

void GraphicalEngine::drawArrowCircle(
    std::list<Drawable> &drawList, double radius, double centreX,
    double centreY, double perimX, double perimY, double sf, string unit = "cm",
    bool textAlias = true, int strokeWidth = 1, string strokeColor = "green",
    string strokeFillColor = "green") {
  drawList.push_back(DrawableTextAntialias(textAlias));
  drawList.push_back(DrawableStrokeWidth(strokeWidth));
  drawList.push_back(DrawableText((centreX + perimX) / 2 - 20, centreY - 5,
                                  precision_to_string(radius) + unit));
  drawList.push_back(DrawableStrokeColor(strokeColor));
  drawList.push_back(DrawableFillColor(strokeFillColor));
  drawList.push_back(
      DrawableRectangle(centreX, centreY, perimX + (25 * sf), centreY + 5));
  std::list<Coordinate> coordinates{
      Coordinate(perimX + (25 * sf), centreY + 10),
      Coordinate(perimX + (25 * sf), centreY - 5),
      Coordinate(perimX + (25 * (sf + 1)), centreY + 2)};
  drawList.push_back(DrawablePolygon(coordinates));
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
  int imageWidth = options.getCanvasOptions().getWidth();
  int imageHeight = options.getCanvasOptions().getHeight();
  double radius = options.getRadius();

  // Define Origin Of Circle
  double centreX = 0.5 * imageWidth;
  double centreY = 0.5 * imageHeight;
  double scaleFactor = 10;
  double perimX = centreX + 0.3 * imageWidth;
  double perimY = centreY + 0.3 * imageHeight;

  // Creates Drawable Circle At Centre Of Canvas
  drawList.push_back(DrawableCircle(centreX, centreY, perimX, perimY));

  // Draw Arrow Specifying Radius of Circle
  drawArrowCircle(drawList, radius, centreX, centreY, perimX, perimY,
                  (imageWidth / 200.0) - 1);

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

  CircleOptions circleOptions = CircleOptions(canvasOptions, shapeOptions, 1);

  TriangleOptions triangleOptions =
      TriangleOptions(canvasOptions, shapeOptions, 1, 2, 3);

  // engine.draw(rectangleOptions);
  engine.draw(circleOptions);
  // engine.draw(triangleOptions);

  return 0;
}