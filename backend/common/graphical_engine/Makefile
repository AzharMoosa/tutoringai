CXX=g++
CPPFLAGS=-O2 -Wall
MAGICK_CPPFLAGS = `Magick++-config --cxxflags --cppflags`
MAGICK_LDFLAGS = `Magick++-config --ldflags --libs`

SRCS=graphical_engine.cc
OBJS=$(subst .cc,.o,$(SRCS))

all: graphical_engine

graphical_engine:
	$(CXX) -c graphical_engine.cpp
	$(CXX) $(MAGICK_CPPFLAGS) $(CPPFLAGS) -o graphical_engine graphical_engine.o $(MAGICK_LDFLAGS)

.PHONY: clean

clean:
	$(RM) $(OBJS) *.png graphical_engine
