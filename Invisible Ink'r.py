# This Script will take the output txt file given by Microsfot Azure and use its info to build the invsible ink pdf
# It requires also for the original image to be in the same folder, to know the dimensions the pdf you want to make
# Both the txt and the image need to have the same name, the output will be a pdf of the same name


import os
import re
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

def parse_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    text_entries = []
    current_text = None

    for line in lines:
        text_match = re.search(r'Text: (.+)', line)
        bbox_match = re.search(r'Bounding Box: \[(.+)\]', line)

        if text_match:
            current_text = text_match.group(1).strip()
        elif bbox_match and current_text is not None:
            bbox = [float(n) for n in bbox_match.group(1).split(',')]
            text_entries.append((current_text, bbox))
            current_text = None

    return text_entries

# Directory containing the JPEG images and text files
directory_path = r"C:\Users\User\Documents\musts\armand\sampletest"

for filename in os.listdir(directory_path):
    if filename.lower().endswith('.jpg'):  # Check if the file is a JPEG image
        image_path = os.path.join(directory_path, filename)
        base_name = os.path.splitext(filename)[0]

        # Corresponding text file path
        text_file_path = os.path.join(directory_path, base_name + '.txt')
        if not os.path.exists(text_file_path):
            print(f"Text file for {filename} not found. Skipping...")
            continue

        text_entries = parse_text_file(text_file_path)

        # Load the image
        image = Image.open(image_path)
        image_width, image_height = image.size

        # Set PDF properties
        pdf_width = 595  # A4 width in points
        pdf_height = 842  # A4 height in points
        scale_x = pdf_width / image_width
        scale_y = pdf_height / image_height

        # Output PDF path
        pdf_path = os.path.join(directory_path, base_name + '.pdf')
        c = canvas.Canvas(pdf_path, pagesize=(pdf_width, pdf_height))

        # Set color to fully transparent
        transparent_color = Color(0, 0, 0, alpha=0)

        for text, bbox in text_entries:
            x1, y1, x3, y3 = bbox[0], bbox[1], bbox[4], bbox[5]
            bbox_width = x3 - x1
            bbox_height = y3 - y1

            # Calculate scaled bounding box dimensions
            scaled_bbox_width = bbox_width * scale_x
            scaled_bbox_height = bbox_height * scale_y

            # Estimate font size (adjust the factor as needed)
            font_size = scaled_bbox_height * 0.75

            # Set font size and transparent color
            c.setFont("Helvetica", font_size)
            c.setFillColor(transparent_color)

            # Calculate text position
            x = x1 * scale_x
            y = pdf_height - y1 * scale_y - font_size  # Adjust y for font size

            c.drawString(x, y, text)

        c.save()
        print(f"PDF generated for {filename}")
