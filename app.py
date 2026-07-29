import json
import os
import tempfile

import cv2
import numpy as np
import streamlit as st

from renderer import AnnotationRenderer
from image_generator import ImageGenerator
from pdf_generator import PDFGenerator

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Label Studio Annotation Visualizer",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Label Studio Annotation Visualizer")

st.write(
    "Upload one COCO result.json file and one image."
)

# -------------------------------------------------------
# Upload Files
# -------------------------------------------------------

json_file = st.file_uploader(
    "Upload COCO JSON",
    type=["json"]
)

uploaded_image = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# -------------------------------------------------------
# Main
# -------------------------------------------------------

if json_file is not None and uploaded_image is not None:

    try:

        # -----------------------------------------------
        # Load JSON
        # -----------------------------------------------

        coco = json.load(json_file)

        renderer = AnnotationRenderer(coco)

        image_generator = ImageGenerator()

        pdf_generator = PDFGenerator()

        # -----------------------------------------------
        # Read Uploaded Image
        # -----------------------------------------------

        file_bytes = np.asarray(
            bytearray(uploaded_image.read()),
            dtype=np.uint8
        )

        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        if image is None:

            st.error("Unable to read uploaded image.")

            st.stop()

        # -----------------------------------------------
        # Get Image ID
        # -----------------------------------------------

        if len(coco["images"]) == 0:

            st.error("No images found inside JSON.")

            st.stop()

        image_id = coco["images"][0]["id"]

        # -----------------------------------------------
        # Render
        # -----------------------------------------------

        annotated = renderer.draw(
            image,
            image_id
        )

        # -----------------------------------------------
        # Preview
        # -----------------------------------------------

        st.divider()

        st.subheader("Preview")

        rgb = cv2.cvtColor(
            annotated,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            rgb,
            use_container_width=True
        )

        # -----------------------------------------------
        # Save Annotated Image
        # -----------------------------------------------

        output_name = (
            os.path.splitext(uploaded_image.name)[0]
            + "_annotated.jpg"
        )

        saved_image = image_generator.save_image(
            annotated,
            output_name
        )

        with open(saved_image, "rb") as f:

            st.download_button(
                label="⬇ Download Annotated Image",
                data=f,
                file_name=output_name,
                mime="image/jpeg"
            )

        # -----------------------------------------------
        # Create PDF
        # -----------------------------------------------

        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as tmp:

            pdf_path = tmp.name

        pdf_generator.save_pdf(
            [annotated],
            pdf_path
        )

        with open(pdf_path, "rb") as pdf:

            st.download_button(
                label="📄 Download PDF",
                data=pdf,
                file_name="Annotation_Report.pdf",
                mime="application/pdf"
            )

        os.remove(pdf_path)

        st.success("Annotation completed successfully!")

    except Exception as e:

        st.exception(e)
