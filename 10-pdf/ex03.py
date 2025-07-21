
from PyPDF2 import PdfMerger
#두개 병합 후 새로운 파일 저장

merger = PdfMerger()
merger.append("./10-pdf/sample.pdf")
merger.append("./10-pdf/sample2.pdf")
merger.write("./10-pdf/merged.pdf")
merger.close()