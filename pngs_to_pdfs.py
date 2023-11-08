from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import os

# Function to combine PNG files into a single PDF, scaling them to fit the page size
def pngs_to_pdf(png_files, output_pdf, page_size=letter):
    c = canvas.Canvas(output_pdf, pagesize=page_size)
    page_width, page_height = page_size

    for png_file in png_files:
        img = Image.open(png_file)
        img_width, img_height = img.size
        aspect = img_width / float(img_height)

        # Calculate dimensions to maintain aspect ratio
        if (page_width / float(page_height)) >= aspect:
            # Fit to page height
            img_height = page_height
            img_width = aspect * img_height
        else:
            # Fit to page width
            img_width = page_width
            img_height = img_width / aspect

        # Center the image on the page
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2

        c.drawImage(png_file, x, y, width=img_width, height=img_height)
        c.showPage()

    c.save()

# Main script
if __name__ == "__main__":
    png_files = [f for f in os.listdir('./output') if f.endswith('.png')]
    png_files.sort()  # Sort the files by name
    output_pdf = "combined_document.pdf"
    pngs_to_pdf(png_files, output_pdf)
    print(f"Combined PDF created as '{output_pdf}'.")
