import json
import os
import tempfile

import cv2
import numpy as np
import streamlit as st

from renderer import AnnotationRenderer
from image_generator import ImageGenerator
from pdf_generator import PDFGenerator

st.set_page_config(
    page_title="Annotation Visualizer",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Label Studio Annotation Visualizer")

st.write(
    "Upload a COCO result.json file and the corresponding images."
)

# --------------------------------------------------------
# Upload Files
# --------------------------------------------------------

json_file = st.file_uploader(
    "Upload COCO JSON",
    type=["json"]
)

uploaded_images = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# --------------------------------------------------------
# Main
# --------------------------------------------------------

if json_file is not None and uploaded_images:

    coco = json.load(json_file)

    renderer = AnnotationRenderer(coco)

    image_generator = ImageGenerator()

    pdf_generator = PDFGenerator()

    image_lookup = {}

    # Build lookup using uploaded filenames
    for img in uploaded_images:

        image_lookup[img.name] = img

    annotated_images = []

    st.divider()

    st.subheader("Preview")

    for image_info in coco["images"]:

        image_name = os.path.basename(
            image_info["file_name"].replace("\\", "/")
        )

        if image_name not in image_lookup:

            st.warning(
                f"Image not uploaded: {image_name}"
            )
            continue

        uploaded_file = image_lookup[image_name]

        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8
        )

        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        annotated = renderer.draw(
            image,
            image_info["id"]
        )

        annotated_images.append(annotated)

        rgb = cv2.cvtColor(
            annotated,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            rgb,
            caption=image_name,
            use_container_width=True
        )

        saved_path = image_generator.save_image(
            annotated,
            image_name
        )

        with open(saved_path, "rb") as f:

            st.download_button(
                label=f"⬇ Download {image_name}",
                data=f,
                file_name=image_name,
                mime="image/jpeg"
            )

    # ----------------------------------------------------
    # PDF
    # ----------------------------------------------------

    if annotated_images:

        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as tmp:

            pdf_path = tmp.name

        pdf_generator.save_pdf(
            annotated_images,
            pdf_path
        )

        with open(pdf_path, "rb") as pdf:

            st.download_button(
                "📄 Download PDF",
                pdf,
                file_name="Annotation_Report.pdf",
                mime="application/pdf"
            )

        os.remove(pdf_path)