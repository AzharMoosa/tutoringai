#include <Magick++.h>

#include <iostream>
#include <list>
#include <string>

class GraphicalEngine {
 public:
  void drawRectangle(std::string strokeColor, int strokeWidth,
                     std::string fillColor, int verticalLength,
                     int horizontalLength, int imageWidth, int imageHeight,
                     std::string backgroundColor) {
    try {
      // Create Image
      Magick::Image image(Magick::Geometry(200, 200), Magick::Color("white"));

      // Construct drawing list
      std::list<Magick::Drawable> drawList;

      // Add some drawing options to drawing list
      drawList.push_back(
          Magick::DrawableStrokeColor("black"));               // Outline color
      drawList.push_back(Magick::DrawableStrokeWidth(2));      // Stroke width
      drawList.push_back(Magick::DrawableFillColor("white"));  // Fill color

      // Add a Rectangle to drawing list
      drawList.push_back(Magick::DrawableRectangle(10, 50, 110, 150));
      drawList.push_back(Magick::DrawableText(10, 50, "1cm"));

      // Draw everything using completed drawing list
      image.draw(drawList);

      // Display the result
      image.write("a.png");
    } catch (std::exception &error_) {
      std::cout << "Error Creating Rectangle" << error_.what() << "\n";
    }
  }
};

int main(int argc, char **argv) {
  Magick::InitializeMagick(*argv);
  GraphicalEngine engine = GraphicalEngine();

  engine.drawRectangle("black", 2, "white", 2, 2, 200, 200, "white");

  return 0;
}