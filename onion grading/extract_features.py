import cv2
import numpy as np


def extract_features(image_path):
    """
    Extract visual features from an onion image.

    Features:
    1. Object area
    2. Object perimeter
    3. Circularity
    4. Average hue
    5. Average saturation
    6. Average brightness
    7. Brightness standard deviation
    8. Dark spot count
    9. Dark spot ratio
    10. Edge density
    """

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Could not read image.")

    # Resize while preserving a consistent input size
    img = cv2.resize(img, (400, 400))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --------------------------------------------------
    # OBJECT SEGMENTATION
    # --------------------------------------------------

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, mask = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Sometimes onion is darker than background
    if np.mean(mask) > 220:
        mask = cv2.bitwise_not(mask)

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:

        largest = max(
            contours,
            key=cv2.contourArea
        )

        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(
            largest,
            True
        )

        if perimeter > 0:
            circularity = (
                4 * np.pi * area
            ) / (perimeter ** 2)

        else:
            circularity = 0

    else:

        area = 0
        perimeter = 0
        circularity = 0

    # --------------------------------------------------
    # COLOUR FEATURES
    # --------------------------------------------------

    avg_hue = float(
        np.mean(hsv[:, :, 0])
    )

    avg_saturation = float(
        np.mean(hsv[:, :, 1])
    )

    avg_brightness = float(
        np.mean(hsv[:, :, 2])
    )

    brightness_std = float(
        np.std(hsv[:, :, 2])
    )

    # --------------------------------------------------
    # DARK SPOTS / DAMAGE
    # --------------------------------------------------

    dark_mask = cv2.inRange(
        hsv,
        np.array([0, 0, 0]),
        np.array([180, 255, 75])
    )

    dark_contours, _ = cv2.findContours(
        dark_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    spot_count = 0

    for contour in dark_contours:

        contour_area = cv2.contourArea(
            contour
        )

        if 5 < contour_area < 2000:
            spot_count += 1

    total_pixels = gray.shape[0] * gray.shape[1]

    dark_spot_ratio = (
        np.sum(dark_mask > 0)
        / total_pixels
    )

    # --------------------------------------------------
    # EDGE DENSITY
    # --------------------------------------------------

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_density = (
        np.sum(edges > 0)
        / total_pixels
    )

    # --------------------------------------------------
    # RETURN FEATURES
    # --------------------------------------------------

    return [
        float(area),
        float(perimeter),
        float(circularity),
        avg_hue,
        avg_saturation,
        avg_brightness,
        brightness_std,
        float(spot_count),
        float(dark_spot_ratio),
        float(edge_density)
    ]