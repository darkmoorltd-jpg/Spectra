
import io
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image

def generate_pdf_report(mineral, confidence, grade, value_ngn, image_bytes, scan_id):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Simple text only – no photo, no QR
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height-1*inch, "SPECTRA Mineral Report")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-1.5*inch, f"Mineral: {mineral}")
    c.drawString(1*inch, height-1.8*inch, f"Confidence: {confidence*100:.1f}%")
    c.drawString(1*inch, height-2.1*inch, f"Grade: {grade*100:.0f}%")
    c.drawString(1*inch, height-2.4*inch, f"Value: NGN {value_ngn:,.0f}")
    c.drawString(1*inch, height-2.7*inch, f"Scan ID: {scan_id}")
    c.drawString(1*inch, height-3.0*inch, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
