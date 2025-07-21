

from PyPDF2 import PdfReader

reader = PdfReader(r"C:\Users\ghgh2\OneDrive\바탕 화면\github\10-pdf\sample.pdf")
print(reader.pages[0].extract_text())

