from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Function to create a PDF with the title
def create_title_pdf(page_width, page_height, name, signators):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # Set up font
    point = 56
    c.setFont("Helvetica-Bold", point)
    # Draw title in the middle of the page
    text_width = c.stringWidth(name, "Helvetica-Bold", point)
    centerPoint = (page_width - text_width) / 2
    c.drawString(centerPoint, page_height * 0.64, name)

    for i, signator in enumerate(signators): 
        signator = signator.replace(".txt", "").replace("_", " ")
        # Set up font
        point = 18
        c.setFont("Helvetica-Bold", point)
        # Draw title in the middle of the page
        text_width = c.stringWidth(signator, "Helvetica-Bold", point)
        centerPoint = (page_width - text_width) / 2
        c.drawString(centerPoint, page_height * 0.19 + i*20, signator)

    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

# Function to merge the original PDF with the title PDF
def merge_pdfs(original_pdf, name, output_pdf, signators):
    # Read the original PDF
    reader = PdfReader(original_pdf)
    writer = PdfWriter()

    # Get the size of the first page
    first_page = reader.pages[0]
    page_width = first_page.mediabox.width
    page_height = first_page.mediabox.height

    # Create a title PDF
    title_pdf_buffer = create_title_pdf(page_width, page_height, name, signators)
    title_reader = PdfReader(title_pdf_buffer)

    # Merge the title PDF with the original PDF
    for page in range(len(reader.pages)):
        original_page = reader.pages[page]
        title_page = title_reader.pages[0]

        original_page.merge_page(title_page)
        writer.add_page(original_page)

    # Write the result to the output PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)

import os
# Main function
def main():

    original_pdf = "award_template.pdf"  # Path to the input single-page PDF
    signators = os.listdir("signators")
    for name in os.listdir("participants"):
        output_pdf = "awards/" + name[:-4] + ".pdf"  # Path to the output PDF
        formattedName = name.replace(".txt", "").replace("_", " ")
        # Merge the original PDF with the title PDF
        merge_pdfs(original_pdf, formattedName, output_pdf, signators)
        print(f"Output written to {output_pdf}")

if __name__ == "__main__":
    main()

