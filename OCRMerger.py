# Use this After the invisible ink python script.
# Have the path to folder to the jpeg ready and path to the insvisible ink pdf ready, And make sure they have the same name
# After you run this, all files in the folder will pop out a placeholder pdf which is a pdf version of the image, AND
# the final output which will match the same name with the suffix "_merged"
import os
import fitz  # PyMuPDF
from PIL import Image

# Directories for the JPEG images and PDF files
jpeg_directory_path = r'C:\Users\User\Documents\musts\armand\sampletest'
pdf_directory_path = r'C:\Users\User\Documents\musts\armand\sampletest'

for filename in os.listdir(jpeg_directory_path):
    if filename.lower().endswith('.jpg'):  # Check if the file is a JPEG image
        base_name = os.path.splitext(filename)[0]

        # Paths for the files
        jpeg_path = os.path.join(jpeg_directory_path, filename)
        text_pdf_path = os.path.join(pdf_directory_path, base_name + '.pdf')  # PDF with invisible text
        merged_pdf_path = os.path.join(jpeg_directory_path, base_name + '_merged.pdf')
        
        if not os.path.exists(text_pdf_path):
            print(f"Text PDF for {filename} not found in {pdf_directory_path}. Skipping...")
            continue

        # Convert JPEG to PDF
        img = Image.open(jpeg_path)
        img_pdf_path = jpeg_path.replace('.jpg', '_placeholder.pdf')
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(img_pdf_path, 'PDF', resolution=100.0)
        img.close()

        # Open the newly created PDF with the image
        img_doc = fitz.open(img_pdf_path)

        # Open the PDF with the invisible text
        text_doc = fitz.open(text_pdf_path)

        # Create a new PDF to store the merged content
        merged_doc = fitz.open()

        # Assume each PDF has the same number of pages
        for page_num in range(img_doc.page_count):
            img_page = img_doc.load_page(page_num)  # page with image
            text_page = text_doc.load_page(page_num)  # page with text

            # New page in the merged document
            merged_page = merged_doc.new_page(width=img_page.rect.width, height=img_page.rect.height)

            # First, insert the image page
            merged_page.show_pdf_page(merged_page.rect, img_doc, page_num)

            # Then overlay the text page
            merged_page.show_pdf_page(merged_page.rect, text_doc, page_num)

        # Save the merged PDF
        merged_doc.save(merged_pdf_path)
        merged_doc.close()
        img_doc.close()
        text_doc.close()

        print(f"Merged PDF created successfully for {filename}")

print("Processing complete for all files.")
