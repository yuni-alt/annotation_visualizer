"""
image_generator.py

Saves annotated OpenCV images.
"""

import os
import cv2


class ImageGenerator:

    def __init__(self, output_folder="output"):
        """
        Parameters
        ----------
        output_folder : str
            Folder where images will be saved.
        """

        self.output_folder = output_folder

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    # ---------------------------------------------------------

    def save_image(
        self,
        image,
        filename,
        quality=100
    ):
        """
        Save an OpenCV image.

        Parameters
        ----------
        image : numpy.ndarray
            Annotated OpenCV image.

        filename : str
            Example:
            image1.jpg
            page_001.png

        quality : int
            JPEG quality (1-100)

        Returns
        -------
        str
            Saved file path.
        """

        output_path = os.path.join(
            self.output_folder,
            filename
        )

        extension = os.path.splitext(filename)[1].lower()

        if extension in [".jpg", ".jpeg"]:

            cv2.imwrite(
                output_path,
                image,
                [
                    cv2.IMWRITE_JPEG_QUALITY,
                    quality
                ]
            )

        elif extension == ".png":

            cv2.imwrite(
                output_path,
                image,
                [
                    cv2.IMWRITE_PNG_COMPRESSION,
                    0
                ]
            )

        else:

            raise ValueError(
                "Supported formats: JPG, JPEG, PNG"
            )

        return output_path

    # ---------------------------------------------------------

    def save_images(
        self,
        images,
        filenames
    ):
        """
        Save multiple images.

        Parameters
        ----------
        images : list
            List of OpenCV images.

        filenames : list
            Matching filenames.

        Returns
        -------
        list
            Saved file paths.
        """

        if len(images) != len(filenames):

            raise ValueError(
                "images and filenames must have the same length."
            )

        paths = []

        for image, filename in zip(images, filenames):

            path = self.save_image(
                image,
                filename
            )

            paths.append(path)

        return paths