"""
pdf_generator.py

Creates a PDF from one or more annotated images.
Uses ReportLab for high-quality PDF generation.
"""

import os
import tempfile

import cv2
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class PDFGenerator:

    def __init__(self, title="Annotation Report"):
        self.title = title

    # ---------------------------------------------------------

    def _fit_to_page(self, img_width, img_height, page_width, page_height):
        """
        Calculate image size while preserving aspect ratio.
        """

        margin = 0.5 * inch

        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin) - 30

        scale = min(
            available_width / img_width,
            available_height / img_height
        )

        return (
            img_width * scale,
            img_height * scale
        )

    # ---------------------------------------------------------

    def save_pdf(self, images, output_pdf):
        """
        Parameters
        ----------
        images : list[np.ndarray]
            List of OpenCV images (BGR)

        output_pdf : str
            Output PDF filename
        """

        pdf = canvas.Canvas(
            output_pdf,
            pagesize=A4
        )

        page_width, page_height = A4

        margin = 0.5 * inch

        for index, img in enumerate(images):

            h, w = img.shape[:2]

            draw_w, draw_h = self._fit_to_page(
                w,
                h,
                page_width,
                page_height
            )

            # Convert BGR → RGB
            rgb = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2RGB
            )

            # Save temporarily
            with tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            ) as tmp:

                temp_name = tmp.name

            cv2.imwrite(
                temp_name,
                cv2.cvtColor(
                    rgb,
                    cv2.COLOR_RGB2BGR
                )
            )

            # -----------------------------
            # Title
            # -----------------------------

            pdf.setFont(
                "Helvetica-Bold",
                16
            )

            pdf.drawString(
                margin,
                page_height - margin + 5,
                f"{self.title} - Page {index + 1}"
            )

            # -----------------------------
            # Image
            # -----------------------------

            x = (page_width - draw_w) / 2
            y = (page_height - draw_h) / 2 - 20

            pdf.drawImage(
                temp_name,
                x,
                y,
                width=draw_w,
                height=draw_h
            )

            pdf.showPage()

            os.remove(temp_name)

        pdf.save()