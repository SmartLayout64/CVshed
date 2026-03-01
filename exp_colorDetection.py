import cv2
import numpy as np

def getColorPercentage(mask, totalPixels):
    colorPixels = cv2.countNonZero(mask)
    return (colorPixels / totalPixels) * 100

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width = frame.shape[:2]
        totalPixels = height * width

        # HSV color ranges
        colorRanges = {
            "Red1": ((0, 100, 100), (10, 255, 255)),
            "Red2": ((160, 100, 100), (179, 255, 255)),
            "Green": ((35, 100, 100), (85, 255, 255)),
            "Blue": ((90, 100, 100), (130, 255, 255)),
            "Yellow": ((20, 100, 100), (30, 255, 255)),
            "Purple": ((130, 50, 50), (160, 255, 255)),
            "Orange": ((10, 100, 100), (20, 255, 255)),
        }

        masks = {}

        for color, (lower, upper) in colorRanges.items():
            lowerBound = np.array(lower)
            upperBound = np.array(upper)
            masks[color] = cv2.inRange(hsvFrame, lowerBound, upperBound)

        redMask = cv2.bitwise_or(masks["Red1"], masks["Red2"])
        masks["Red"] = redMask
        del masks["Red1"]
        del masks["Red2"]

        yOffset = 30
        for color, mask in masks.items():
            percentage = getColorPercentage(mask, totalPixels)
            text = f"{color}: {percentage:.2f}%"
            cv2.putText(frame, text, (10, yOffset),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)
            yOffset += 25

        cv2.imshow("Color Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()