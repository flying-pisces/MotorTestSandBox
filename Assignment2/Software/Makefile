# Makefile for Pendulum Control System
# Assignment 2: Rope Transmission System

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = pendulum_control
SOURCE = pendulum_control.cpp
OUTPUT_DIR = ../Output

# Default target
all: $(TARGET)

# Build the main executable
$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE) -lm

# Create output directory if it doesn't exist
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Run the program
run: $(TARGET) $(OUTPUT_DIR)
	./$(TARGET)

# Clean build files
clean:
	rm -f $(TARGET)
	rm -f $(OUTPUT_DIR)/pendulum_cycle_log.csv

# Debug build
debug: CXXFLAGS += -g -DDEBUG
debug: $(TARGET)

# Install dependencies (if needed)
install:
	@echo "No external dependencies required"

# Help
help:
	@echo "Available targets:"
	@echo "  all     - Build the pendulum control program"
	@echo "  run     - Build and run the program"
	@echo "  clean   - Remove build files and logs"
	@echo "  debug   - Build with debug symbols"
	@echo "  help    - Show this help message"

.PHONY: all run clean debug install help