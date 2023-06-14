import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def add_text_if_found(input_path, output_path, search_text, new_text, x_offset, y_offset):
    # Open the existing PDF file
    with open(input_path, "rb") as file:
        pdf = PdfReader(file)
        num_pages = len(pdf.pages)

        # Create a new PDF writer
        writer = PdfWriter()

        # Iterate over each page of the PDF
        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            width = page.mediabox.width
            height = page.mediabox.height

            # Create a canvas to draw on the page
            c = canvas.Canvas("temp.pdf", pagesize=(width, height))
            c.setFont("Helvetica", 12)  # Set the font and size of the text

            # Search for the text in the page content
            content = page.extract_text()

            if search_text in content:
                x, y = get_text_position(content, search_text, x_offset, y_offset)
                if x is not None and y is not None:
                    c.drawString(x, y, new_text)  # Draw the new text next to the search text

            c.save()

            # Merge the original page with the modified page
            modified_page = PdfReader("temp.pdf").pages[0]
            modified_page.merge_page(page)
            writer.add_page(modified_page)

    # Write the modified PDF to the output file
    with open(output_path, "wb") as file:
        writer.write(file)

    # Remove the temporary file
    if os.path.exists("temp.pdf"):
        os.remove("temp.pdf")

def get_text_position(content, search_text, x_offset, y_offset):
    lines = content.split('\n')
    for line in lines:
        if search_text in line:
            x = line.find(search_text) * 5 + len(search_text) * 5 + x_offset  # Adjust the multipliers and offset for position
            y = lines.index(line) * 12 + y_offset  # Adjust the multiplier and offset for vertical position
            return x, y
    return None, None

# Usage:
input_path = "timesheet_blank.pdf"
output_path = "pramod.pdf"
search_text = "Joyce"  # Text to search for in the PDF
new_text = "Additional Text"  # Text to add if "Joyce" is found
x_offset = 50  # Horizontal offset for the new text position
y_offset = 10  # Vertical offset for the new text position

add_text_if_found(input_path, output_path, search_text, new_text, x_offset, y_offset)
