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

void GraphicalEngine::drawRectangle(RectangleOptions options) {
  try {
    Image image = generateImageCanvas(options.getCanvasOptions());

    std::list<Drawable> drawList =
        initialiseDrawableList(options.getShapeOptions());

    // TODO - Add Labels Correctly
    drawList.push_back(DrawableRectangle(10, 50, 110, 150));
    drawList.push_back(DrawableText(
        10, 50, precision_to_string(options.getHorizontalLength()) + "cm"));
    image.draw(drawList);

    image.write("rectangle.png");
  } catch (std::exception &error_) {
    std::cout << "Error Creating Rectangle" << error_.what() << "\n";
  }
}

void GraphicalEngine::drawCircle(CircleOptions options) {
  try {
    Image image = generateImageCanvas(options.getCanvasOptions());

    std::list<Drawable> drawList =
        initialiseDrawableList(options.getShapeOptions());

    drawList.push_back(DrawableCircle(50, 50, 80, 80));

    image.draw(drawList);
    image.write("circle.png");
  } catch (std::exception &error_) {
    std::cout << "Error Creating Circle" << error_.what() << "\n";
  }
}

void GraphicalEngine::drawTriangle(TriangleOptions options) {
  try {
    Image image = generateImageCanvas(options.getCanvasOptions());

    std::list<Drawable> drawList =
        initialiseDrawableList(options.getShapeOptions());

    std::list<Coordinate> coordinates{Coordinate(50, 50), Coordinate(50, 10),
                                      Coordinate(90, 50)};

    drawList.push_back(DrawablePolygon(coordinates));
    image.draw(drawList);

    image.write("triangle.png");
  } catch (std::exception &error_) {
    std::cout << "Error Creating Triangle" << error_.what() << "\n";
  }
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

  engine.drawRectangle(rectangleOptions);
  engine.drawCircle(circleOptions);
  engine.drawTriangle(triangleOptions);

  return 0;
}