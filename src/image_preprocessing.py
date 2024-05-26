import cv2
import xml.etree.ElementTree as ET


def process_image(image_path, output_xml_path, mask_name):
    """
    Process an image by performing the following steps:
    1. Read the image from the given `image_path`.
    2. Convert the image to grayscale.
    3. Apply thresholding to separate the object from the background.
    4. Find contours in the thresholded image.
    5. Select the largest contour as the bounding box.
    6. Create an XML annotation file at the specified `output_xml_path` with the bounding box and other information.

    Parameters:
    - `image_path` (str): The path to the input image file.
    - `output_xml_path` (str): The path to the output XML annotation file.
    - `mask_name` (str): The name of the mask.

    Returns:
    None
    """
    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding to separate the object from the background
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box for the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    bounding_box = [(x, y, x + w, y + h)]

    # Create XML annotation file
    create_xml(image_path, bounding_box, output_xml_path, mask_name)


def create_xml(image_path, bounding_boxes, output_path, mask_name):
    """
    Creates an XML annotation file for the given image and bounding boxes.

    Parameters:
        image_path (str): The path to the input image file.
        bounding_boxes (List[Tuple[int, int, int, int]]): A list of tuples representing the bounding boxes. Each tuple contains the coordinates of the top-left and bottom-right corners of the box.
        output_path (str): The path to the output XML annotation file.
        mask_name (str): The name of the mask.

    Returns:
        None
    """
    # Create the root element
    annotation = ET.Element("annotation")

    # Extract filename and folder from image_path
    filename = image_path.split("/")[-1]
    folder = image_path.split("/")[-2]

    # Create and append elements
    ET.SubElement(annotation, "folder").text = folder
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = image_path

    # Read the image to get dimensions
    image = cv2.imread(image_path)

    # Add source element
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    # Add size element
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(image.shape[1])
    ET.SubElement(size, "height").text = str(image.shape[0])
    ET.SubElement(size, "depth").text = str(image.shape[2])

    # Add segmented element
    ET.SubElement(annotation, "segmented").text = "0"

    # Add object elements
    for box in bounding_boxes:
        obj = ET.SubElement(annotation, "object")
        ET.SubElement(obj, "name").text = mask_name
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = "0"
        ET.SubElement(obj, "difficult").text = "0"
        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(box[0])
        ET.SubElement(bndbox, "ymin").text = str(box[1])
        ET.SubElement(bndbox, "xmax").text = str(box[2])
        ET.SubElement(bndbox, "ymax").text = str(box[3])

    # Create the tree and write to file
    tree = ET.ElementTree(annotation)
    tree.write(output_path)


if __name__ == "__main__":
    # Example usage
    image_path = "Tensorflow/workspace/images/collectedimages/biskuit-selamat/biskuit-selamat01.jpg"
    mask_name = "biskuit-selamat"
    output_xml_path = image_path.split(".")[0] + ".xml"
    process_image(image_path, output_xml_path, mask_name)
