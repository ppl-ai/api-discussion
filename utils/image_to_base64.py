import base64
from PIL import Image
from io import BytesIO

def convert_image_to_base64(input_image_path, output_format="PNG"):
    """
    Convert an image from any format to a base64-encoded string in the specified format.

    :param input_image_path: Path to the input image file.
    :param output_format: Format to convert the image to (default is PNG).
    :return: Base64-encoded string of the converted image.
    """
    # Open the image using Pillow
    with Image.open(input_image_path) as img:
        # Convert the image to the desired output format (PNG by default)
        buffered = BytesIO()
        img.save(buffered, format=output_format)
        img_bytes = buffered.getvalue()
    
    # Encode the image bytes into base64 and return as a UTF-8 string
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    return base64_str
