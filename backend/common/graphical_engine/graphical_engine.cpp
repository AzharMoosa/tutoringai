#include "graphical_engine.hpp"

class GraphicalEngine {
 private:
  Image generateImageCanvas(CanvasOptions canvasOptions) {
    int imageWidth = canvasOptions.getWidth();
    int imageHeight = canvasOptions.getHeight();
    string backgroundColor = canvasOptions.getBackgroundColor();
    return Image(Geometry(imageWidth, imageHeight), Color(backgroundColor));
  }

 public:
  void drawRectangle(RectangleOptions options) {
    try {
      Image image = generateImageCanvas(options.getCanvasOptions());

      std::list<Drawable> drawList;

      drawList.push_back(
          DrawableStrokeColor(options.getShapeOptions().getStrokeColor()));
      drawList.push_back(
          DrawableStrokeWidth(options.getShapeOptions().getStrokeWidth()));
      drawList.push_back(
          DrawableFillColor(options.getShapeOptions().getFillColor()));

      // TODO - Add Labels Correctly
      drawList.push_back(DrawableRectangle(10, 50, 110, 150));
      drawList.push_back(DrawableText(
          10, 50, std::to_string(options.getHorizontalLength()) + "cm"));

      image.draw(drawList);

      image.write("rectangle.png");
    } catch (std::exception &error_) {
      std::cout << "Error Creating Rectangle" << error_.what() << "\n";
    }
  }
};

int main(int argc, char **argv) {
  InitializeMagick(*argv);
  GraphicalEngine engine = GraphicalEngine();
  CanvasOptions canvasOptions = CanvasOptions(200, 200, "white");
  ShapeOptions shapeOptions = ShapeOptions("black", 2, "white");

  RectangleOptions rectangleOptions =
      RectangleOptions(canvasOptions, shapeOptions, 2, 2);

  engine.drawRectangle(rectangleOptions);

  return 0;
}