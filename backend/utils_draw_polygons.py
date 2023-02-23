import json
from typing import Any, List, Tuple
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw
from rdp import rdp


def polygons_to_mask(
        polygons: List[List[Tuple[int, int]]],
        width: int = 600,
        height: int = 600,
) -> np.ndarray:
    mask = np.zeros((width, height))
    for idx, polygon in enumerate(reversed(polygons)):  # Latest annot likely worse annot
        if polygon.__len__() > 4:
            img = Image.new("L", (width, height), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=1, fill=0, width=3)
            mask += (idx + 1) * np.array(img)  # Add binary mask (0=background, (idx+1)=field)
            mask = np.clip(mask, a_min=0, a_max=(idx + 1))  # type: ignore
    return mask


def transform(values: List[Any]) -> List[List[Tuple[int, int]]]:
    boundaries = []
    for value in values:
        x = value["shape_attributes"]["all_points_x"]
        x += [x[-1]]
        y = value["shape_attributes"]["all_points_y"]
        y += [y[-1]]
        boundaries.append(list(zip(x, y)))
    return boundaries


def load_annotations(path: str, key) -> List[List[Tuple[int, int]]]:
    with open(path, "r") as f:
        annotations = json.load(f)
    annotation = annotations[key]
    # gibt nur die x und y werte jedes polygons in einer Liste zurück
    return transform(annotation["regions"])

def mask_to_polygons(
        mask: np.ndarray,
) :
    """Transform a mask back to a polygon boundary."""
    polygons = []
    polygons2 = []
    # jede Maske wird durchgegangen weil es können Mehrer Felder in einem Bild sein
    for v in sorted(set(np.unique(mask)) - {0}):
        # Extract polygon
        # Geht auf die Maske die gerade in der For schleife ist
        contours, _ = cv2.findContours(
            np.asarray(mask == v, dtype=np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        points = []
        for point in sorted(contours, key=lambda x: -len(x))[0]:  # If multiple (shouldn't be); use largest
            points.append([int(point[0][0]), int(point[0][1])])


        polygon2 = list([list(e) for e in rdp(points)])
        polygon = list([tuple(e) for e in rdp(points)])

        # Stellt sicher das der Anfang und das ende gleich sind
        if polygon[0] != polygon[-1]:
            polygon.append(polygon[0])
        polygons.append(polygon)

        if polygon2[0] != polygon2[-1]:
            polygon2.append(polygon2[0])
        polygons2.append(polygon2)

    return polygons, polygons2



def rgb_to_hex(rgb):
    return "%02x%02x%02x" % rgb

def find_min_max(polygon):
    max_x = 0
    min_x = sys.maxsize
    max_y = 0
    min_y = sys.maxsize

    for x, y in polygon:
        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

        if x < min_x:
            min_x = x

        if y < min_y:
            min_y = y
    return min_x, min_y, max_x, max_y


def crop_image(name, color, count):
    f = open(f"predictions/{name}.json", "r")
    fields = json.load(f)
    polygons = []
    for shape in fields:
        print(shape)
        if(shape[0] == color):
            polygons = shape[1][0]
            print("gefunden")
            break

    print(polygons)


    min_x, min_y, max_x, max_y = find_min_max(polygons)

    img = cv2.imread("uploads/"+name+".png")

    #print(""+min_x+""+max_y+""+max_y)
    img = img[min_y:max_y, min_x:max_x]
    # height = max_x - min_x
    # width = max_y-min_y
    # if height > width:
    #     img = img[min_y:min_y+height, min_x:max_x]
    # else:
    #     img = img[min_y:max_y, min_x:min_x+width]

    #img = cv2.resize(img, (100, 100))
    cv2.imwrite("uploads/c"+count+"_"+name+".png", img)


def polygons_to_mask_fill(
        polygons: List[List[Tuple[int, int]]],
        width: int = 600,
        height: int = 600,
) -> np.ndarray:
    mask = np.zeros((width, height))
    for idx, polygon in enumerate(reversed(polygons)):  # Latest annot likely worse annot
        if polygon.__len__() > 4:
            img = Image.new("L", (width, height), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=0, fill=1, width=3)
            mask += (idx + 1) * np.array(img)  # Add binary mask (0=background, (idx+1)=field)
            mask = np.clip(mask, a_min=0, a_max=(idx + 1))  # type: ignore
    return mask

def polygons_to_mask_thick(
        polygons: List[List[Tuple[int, int]]],
        width: int = 600,
        height: int = 600,
) -> np.ndarray:
    mask = np.zeros((width, height))
    for idx, polygon in enumerate(reversed(polygons)):  # Latest annot likely worse annot
        if polygon.__len__() > 4:
            img = Image.new("L", (width, height), 0)
            ImageDraw.Draw(img).polygon(polygon, outline=1, fill=0, width=10)
            mask += (idx + 1) * np.array(img)  # Add binary mask (0=background, (idx+1)=field)
            mask = np.clip(mask, a_min=0, a_max=(idx + 1))  # type: ignore
    return mask


def create_image_for_classification(name, color, count):

    print("Farbe:")
    print("Farbe hex:" + color)

    color_rgb = hex_to_rgb(color)

    img_with_poly = cv2.imread("predictions/filled_" + name+".png")
    img_org = cv2.imread("predictions/" + name+".png")
    mask = cv2.inRange(img_with_poly, np.array([color_rgb[2], color_rgb[1], color_rgb[0]]), np.array([color_rgb[2], color_rgb[1], color_rgb[0]]))

    polygons = mask_to_polygons(mask)

    min_x, min_y, max_x, max_y = find_min_max(polygons[0][0])
    mask = mask // 255

    red_channel = mask * img_org[:, :, 0]
    green_channel = mask * img_org[:, :, 1]
    blue_channel = mask * img_org[:, :, 2]

    merged = cv2.merge([red_channel, green_channel, blue_channel])

    height = max_x - min_x
    width = max_y-min_y
    if height > width:
        merged = merged[min_y:min_y+height, min_x:max_x]
    else:
        merged = merged[min_y:max_y, min_x:min_x+width]
    merged = cv2.resize(merged, (100, 100))
    print(name)
    print(count)
    cv2.imwrite("output/crop_" + name  +".png", merged)

def hex_to_rgb(hex):
    return list(int(hex[i:i+2], 16) for i in (0, 2, 4))