import argparse
import sys
import math
import numpy

from typing import List
from PIL import Image


PROGRAM_NAME = "imascii"
PROGRAM_DESCRIPTION = "Image to Ascii conversion"

DEFAULT_OUTPUTFILE = "out.txt"
DEFAULT_SCALE = 0.43
DEFAULT_COLUMNS = 80
 
# http://paulbourke.net/dataformats/asciiart/
GRADIENT = "@%#*+=-:. "
GRADIENT_LONG = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."


def get_average_luminance(image: Image) -> float:
    image_array = numpy.array(image)
    width, height = image_array.shape
    return numpy.average(image_array.reshape(width * height))

def imascii(filename: str, columns: int, scale: float, gradient: str) -> List[str]:
    image = Image.open(filename).convert("L")

    image_width = image.size[0]
    image_height = image.size[1]

    tile_width = image_width / columns
    tile_height = tile_width / scale

    rows = int(image_height / tile_height)

    print("INFO:")
    print(f"    Image {filename}, {image_width}x{image_height}")
    print(f"    Tile {tile_width}x{tile_height}")
    print(f"    {columns} cols, {rows} rows")
    print(f"    Scale {scale}")
    print(f"    Gradient {gradient}")

    if columns > image_width or rows > image_height:
        print("ERROR: The image is too small for specified columns")
        exit(1)

    ascii_image = []

    for y in range(rows):
        y1 = int(y * tile_height)
        y2 = int((y + 1) * tile_height)

        if y == rows - 1:
            y2 = image_height
        
        ascii_image.append("")

        for x in range(columns):
            x1 = int(x * tile_width)
            x2 = int((x + 1) * tile_width)

            if x == columns - 1:
                x2 = image_width
            
            cropped_image = image.crop((x1, y1, x2, y2))
            average_luminance = int(get_average_luminance(cropped_image))
            gradient_value = gradient[int((average_luminance * (len(gradient)) - 1) / 255)]

            ascii_image[y] += gradient_value

    return ascii_image
 
def main():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
    parser.add_argument("-i", "--input", dest="input_filename", required=True)
    parser.add_argument("-o", "--output", dest="output_filename", required=False)
    parser.add_argument("-s", "--scale", dest="scale", required=False)
    parser.add_argument("-c", "--columns", dest="columns", required=False)

    args = parser.parse_args()

    input_filename = args.input_filename

    output_filename = DEFAULT_OUTPUTFILE
    if args.output_filename:
        output_filename = args.output_filename
    
    scale = DEFAULT_SCALE
    if args.scale:
        scale = float(args.scale)
    
    columns = DEFAULT_COLUMNS
    if args.columns:
        columns = int(args.columns)

    ascii_image = imascii(input_filename, columns, scale, GRADIENT)

    with open(output_filename, "w") as f:
        for row in ascii_image:
            f.write(row + "\n")

    print(f"{output_filename} Done.")
 
if __name__ == "__main__":
    main()
