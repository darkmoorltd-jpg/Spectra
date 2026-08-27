
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import datetime
import qrcode
import base64
from PIL import Image
import os

def generate_pdf_report(mineral, confidence, grade, value_ngn, image_bytes, scan_id):
    """Generate a professional PDF report with photo, QR code, and details."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1*inch, height-1*inch, "SPECTRA")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-1.3*inch, "Mineral Identification Report")
    c.line(1*inch, height-1.5*inch, width-1*inch, height-1.5*inch)

    # Mineral Details
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, height-2*inch, f"Mineral: {mineral}")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-2.4*inch, f"Confidence: {confidence*100:.1f}%")
    c.drawString(1*inch, height-2.7*inch, f"Estimated Grade: {grade*100:.0f}%")
    c.drawString(1*inch, height-3.0*inch, f"Market Value: ₦{value_ngn:,.0f}")
    c.drawString(1*inch, height-3.3*inch, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(1*inch, height-3.6*inch, f"Scan ID: {scan_id}")

    # Mineral Photo (if provided)
    if image_bytes:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            # Save to temp file for reportlab
            tmp_path = f"/tmp/mineral_{scan_id}.jpg"
            img.save(tmp_path, format="JPEG")
            # Draw image on right side of details
            c.drawImage(tmp_path, width-3.2*inch, height-3.5*inch, width=2.5*inch, height=2.5*inch, preserveAspectRatio=True)
            os.remove(tmp_path)
        except Exception as e:
            print(f"Could not add photo to PDF: {e}")

    # QR Code
    qr_data = f"SPECTRA_VERIFY:{scan_id}:{mineral}:{confidence:.4f}:{grade:.4f}:{value_ngn:.2f}"
    qr = qrcode.QRCode(version=1, box_size=3, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_tmp = f"/tmp/qr_{scan_id}.png"
    qr_img.save(qr_tmp)
    c.drawImage(qr_tmp, 1*inch, height-5.8*inch, width=1.2*inch, height=1.2*inch)
    os.remove(qr_tmp)

    c.setFont("Helvetica", 8)
    c.drawString(1*inch, height-6.2*inch, "Verify this report by scanning the QR code.")

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.5*inch, "Powered by Darkmoor Ltd")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
