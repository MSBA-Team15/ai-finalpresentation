# Import & Setup # --------------------------------------------------
import random, time, datetime, names, random_address, fitz
from pypdf import PdfReader, PdfWriter
from PIL import Image
from io import BytesIO
import numpy as np



# Fill Fields # -----------------------------------------------------
reader = PdfReader("financial_statement.pdf")
writer = PdfWriter()

page = reader.pages[0]
writer.add_page(page)
fields = reader.get_fields()

while True:
    random_loc = random_address.real_random_address()
    try: _ = random_loc["city"]; break
    except: continue
        

writer.update_page_form_field_values(
    writer.pages[0], {"Statement Date" : str(datetime.datetime.fromtimestamp( \
                        random.randint(1, int(time.time()))).strftime('%Y-%m-%d')),
                      "Personal Information 1" : names.get_full_name(),
                      "Personal Information 2" : random_loc["address1"],
                      "Personal Information 3" : ", ".join([random_loc["city"],
                        random_loc["state"], random_loc["postalCode"]]),
                      "SSN" : "".join([str(random.randint(0, 9)) for i in range(9)]),
                      "Home Telephone" : "".join([str(random.randint(0, 9)) for i in range(10)])
                      }
)

with open("generated_statement.pdf", "wb") as output_stream:
    writer.write(output_stream)



# Add Smudges # -----------------------------------------------------
doc = fitz.open("generated_statement.pdf")

def random_rect():
    start = random.randint(0, 550), random.randint(0, 600)
    end = random.randint(start[0] + 50, 612), random.randint(start[1] + 50, 792)

    return fitz.Rect(start, end)

for i in range(1, np.random.binomial(5, 0.8)):
    byteImgIO = BytesIO()
    byteImg = Image.open(f"obstructions/{random.randint(1, 3)}.png")
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    obstruction = byteImgIO.read()

    rect = random_rect()
    doc[0].insert_image(rect, stream = obstruction)

doc.save("smudged_statement.pdf")  