
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
import datetime
import tempfile
import os
from PIL import Image

def generate_pdf_report(mineral, confidence, grade, value_ngn, image_bytes, scan_id):
    """Generate a PDF report with photo, QR code, and details. Returns bytes."""
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

    # Mineral Photo (if provided) using temp file
    if image_bytes:
        tmp_photo = None
        try:
            img = Image.open(io.BytesIO(image_bytes))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            tmp_photo = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(tmp_photo.name, format="JPEG")
            c.drawImage(tmp_photo.name, width-3.2*inch, height-3.5*inch, width=2.5*inch, height=2.5*inch)
        except Exception as e:
            print(f"Could not add photo to PDF: {e}")
        finally:
            if tmp_photo and os.path.exists(tmp_photo.name):
                os.unlink(tmp_photo.name)

    # QR Code using temp file
    tmp_qr = None
    try:
        import qrcode
        qr_data = f"SPECTRA_VERIFY:{scan_id}:{mineral}:{confidence:.4f}:{grade:.4f}:{value_ngn:.2f}"
        qr = qrcode.QRCode(version=1, box_size=3, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        tmp_qr = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        qr_img.save(tmp_qr.name)
        c.drawImage(tmp_qr.name, 1*inch, height-5.8*inch, width=1.2*inch, height=1.2*inch)
        c.setFont("Helvetica", 8)
        c.drawString(1*inch, height-6.2*inch, "Verify this report by scanning the QR code.")
    except Exception as e:
        print(f"QR code generation failed: {e}")
    finally:
        if tmp_qr and os.path.exists(tmp_qr.name):
            os.unlink(tmp_qr.name)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.5*inch, "Powered by Darkmoor Ltd")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
