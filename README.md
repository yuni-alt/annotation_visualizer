# 🖼️ Label Studio Annotation Visualizer

A Streamlit application that visualizes **COCO-format annotations exported from Label Studio**.

The application allows you to upload:

- A COCO `result.json`
- The corresponding image

It generates:

- ✅ Annotated image preview
- ✅ Downloadable annotated image
- ✅ Downloadable PDF report

---

# Features

- 📤 Upload COCO `result.json`
- 🖼 Upload a single image
- 🎨 Label Studio-style annotation visualization
- 🟩 Colored bounding boxes
- 🏷 Colored labels
- 🌈 Semi-transparent annotation regions
- 📄 Export annotations as PDF
- 💾 Download annotated image
- ☁ Deployable on Streamlit Community Cloud

---

# Project Structure

```
annotation_visualizer/
│
├── app.py
├── renderer.py
├── colors.py
├── image_generator.py
├── pdf_generator.py
├── requirements.txt
├── README.md
└── output/
```

---

# Requirements

- Python 3.10+
- Streamlit
- OpenCV
- NumPy
- Pillow
- ReportLab

All dependencies are listed in `requirements.txt`.

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/annotation_visualizer.git
```

Go to the project directory

```bash
cd annotation_visualizer
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

Start the Streamlit app

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# Usage

## Step 1

Upload the exported COCO JSON file.

Example:

```
result.json
```

## Step 2

Upload the corresponding image.

Supported formats:

- JPG
- JPEG
- PNG

## Step 3

The application will automatically

- Render all annotations
- Display a preview
- Generate an annotated image
- Generate a PDF report

## Step 4

Download

- Annotated Image
- PDF Report

---

# Supported Annotation Format

This application supports **COCO Detection** format exported from Label Studio.

Example:

```json
{
  "images": [],
  "annotations": [],
  "categories": []
}
```

Bounding boxes (`bbox`) are visualized.

---

# Output

The application generates

### Annotated Image

- Colored bounding boxes
- Category labels
- Semi-transparent annotation regions

### PDF Report

- Annotated image
- Ready for sharing or documentation

---

# Technologies Used

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow
- ReportLab

---

# Notes

- Designed for **one JSON file and one image** at a time.
- The uploaded image filename does not need to match the filename stored in the COCO JSON.
- Optimized for Label Studio COCO exports.

---

# Future Improvements

Potential enhancements include:

- Multiple image support
- Polygon annotation support
- Segmentation masks
- ZIP export
- Custom color themes
- Statistics dashboard
- Annotation summary
- Dark mode optimization

---

# License

This project is released under the MIT License.

---

# Author

Developed as a visualization tool for Label Studio COCO annotations using Streamlit.
