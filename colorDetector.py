import cv2
import numpy as np

_cap = None
_colorRanges = {}

def initialize(index=0):
    global _cap
    _cap = cv2.VideoCapture(index)

    if not _cap.isOpened():
        raise Exception(f"Cannot open camera at index {index}")

def setColors(colorDict):
    """
    format:
    {
        "Red": [((lowerHSV), (upperHSV)), ((lowerHSV), (upperHSV))],
        "Green": [((lowerHSV), (upperHSV))]
    }
    """
    global _colorRanges
    _colorRanges = colorDict

def getColorPercentage():
    global _cap, _colorRanges

    if _cap is None:
        raise Exception("Camera not initialized. Call initialize() first.")

    ret, frame = _cap.read()
    if not ret:
        raise Exception("Failed to read frame from camera.")

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width = frame.shape[:2]
    totalPixels = height * width

    results = {}

    for color, ranges in _colorRanges.items():
        combinedMask = None

        for lower, upper in ranges:
            lowerBound = np.array(lower)
            upperBound = np.array(upper)

            mask = cv2.inRange(hsvFrame, lowerBound, upperBound)

            if combinedMask is None:
                combinedMask = mask
            else:
                combinedMask = cv2.bitwise_or(combinedMask, mask)

        colorPixels = cv2.countNonZero(combinedMask)
        percentage = (colorPixels / totalPixels) * 100
        results[color] = percentage

    return results

def close():
    global _cap
    if _cap is not None:
        _cap.release()
        _cap = None