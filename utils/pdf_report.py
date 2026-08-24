
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
import datetime
import qrcode
import base64

def generate_pdf_report(mineral, confidence, grade, value_ngn, image_bytes, scan_id):
    """Generate a PDF report and return bytes."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1*inch, height-1*inch, "SPECTRA")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height-1.3*inch, "Mineral Identification Report")
    c.line(1*inch, height-1.4*inch, width-1*inch, height-1.4*inch)

    # Details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height-2*inch, f"Mineral: {mineral}")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-2.4*inch, f"Confidence: {confidence*100:.1f}%")
    c.drawString(1*inch, height-2.7*inch, f"Estimated Grade: {grade*100:.0f}%")
    c.drawString(1*inch, height-3.0*inch, f"Market Value: ₦{value_ngn:,.0f}")
    c.drawString(1*inch, height-3.3*inch, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(1*inch, height-3.6*inch, f"Scan ID: {scan_id}")

    # Image (if provided)
    if image_bytes:
        # Convert to PIL and draw
        from PIL import Image
        import tempfile
        img = Image.open(io.BytesIO(image_bytes))
        # Resize to fit
        max_width = 3*inch
        max_height = 2*inch
        img.thumbnail((max_width, max_height))
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img.save(tmp.name, format="PNG")
            c.drawImage(tmp.name, 1*inch, height-5.3*inch, width=img.width, height=img.height)
            os.unlink(tmp.name)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.5*inch, "Powered by Darkmoor Ltd")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
