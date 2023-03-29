CXX=clang++
CPPFLAGS=-O2 -Wall
MAGICK_CPPFLAGS = `Magick++-config --cxxflags --cppflags`
MAGICK_LDFLAGS = `Magick++-config --ldflags --libs`

SRCS=$(wildcard *.cpp)
OBJS=$(subst .cpp,.o,$(SRCS))

all: graphical_engine

graphical_engine:
	$(CXX) -c $(SRCS) -std=c++20
	$(CXX) $(MAGICK_CPPFLAGS) $(CPPFLAGS) -o graphical_engine $(OBJS) $(MAGICK_LDFLAGS)

.PHONY: clean

clean:
	$(RM) $(OBJS) *.png graphical_engine
