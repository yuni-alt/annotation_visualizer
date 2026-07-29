import cv2

from colors import (
    get_color,
    get_alpha,
    get_border_thickness,
    get_font_scale,
    get_font_thickness,
    get_text_color,
)


class AnnotationRenderer:

    def __init__(self, coco_json):

        self.categories = {
            c["id"]: c["name"]
            for c in coco_json["categories"]
        }

        self.annotations = coco_json["annotations"]

    # ---------------------------------------------------------

    def get_annotations(self, image_id):

        anns = [
            ann
            for ann in self.annotations
            if ann["image_id"] == image_id
        ]

        anns.sort(
            key=lambda x: x["bbox"][2] * x["bbox"][3],
            reverse=True
        )

        return anns

    # ---------------------------------------------------------

    def draw(self, image, image_id):

        img = image.copy()

        overlay = image.copy()

        annotations = self.get_annotations(image_id)

        font = cv2.FONT_HERSHEY_SIMPLEX

        scale = get_font_scale()

        thickness = get_font_thickness()

        img_h, img_w = img.shape[:2]

        occupied = []

        # -------------------------------------------------
        # Draw Filled Boxes
        # -------------------------------------------------

        for ann in annotations:

            x, y, w, h = map(int, ann["bbox"])

            color = get_color(ann["category_id"])

            cv2.rectangle(
                overlay,
                (x, y),
                (x + w, y + h),
                color,
                -1
            )

        img = cv2.addWeighted(
            overlay,
            get_alpha(),
            img,
            1 - get_alpha(),
            0
        )

        # -------------------------------------------------
        # Draw Borders + Labels
        # -------------------------------------------------

        for ann in annotations:

            x, y, w, h = map(int, ann["bbox"])

            category = ann["category_id"]

            label = self.categories.get(
                category,
                str(category)
            )

            color = get_color(category)

            # Border

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                color,
                get_border_thickness()
            )

            (tw, th), _ = cv2.getTextSize(
                label,
                font,
                scale,
                thickness
            )

            # -------------------------------------
            # Preferred Positions
            # -------------------------------------

            candidates = [

                (x, y - 6),

                (x, y + h + th + 8),

                (x + w - tw - 8, y - 6),

                (x + w - tw - 8, y + h + th + 8),

            ]

            chosen = None

            for lx, ly in candidates:

                lx = max(0, min(lx, img_w - tw - 10))

                ly = max(th + 8, min(ly, img_h - 2))

                box = (
                    lx,
                    ly - th - 8,
                    lx + tw + 8,
                    ly
                )

                overlap = False

                for b in occupied:

                    if not (
                        box[2] < b[0] or
                        box[0] > b[2] or
                        box[3] < b[1] or
                        box[1] > b[3]
                    ):
                        overlap = True
                        break

                if not overlap:

                    chosen = box
                    occupied.append(box)
                    break

            # -------------------------------------
            # If everything overlaps,
            # use the first position.
            # -------------------------------------

            if chosen is None:

                lx = x

                ly = max(th + 8, y - 6)

                chosen = (
                    lx,
                    ly - th - 8,
                    lx + tw + 8,
                    ly
                )

            x1, y1, x2, y2 = chosen

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                color,
                -1
            )

            cv2.putText(
                img,
                label,
                (x1 + 4, y2 - 4),
                font,
                scale,
                get_text_color(),
                thickness,
                cv2.LINE_AA
            )

        return img
