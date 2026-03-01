import colorDetector

colorDetector.initialize(0)

colorDetector.setColors({
    "Red": [
        ((0, 100, 100), (10, 255, 255)),
        ((160, 100, 100), (179, 255, 255))
    ],
    "Green": [
        ((35, 100, 100), (85, 255, 255))
    ],
    "Blue": [
        ((90, 100, 100), (130, 255, 255))
    ]
})

try:
    while True:
        percentages = colorDetector.getColorPercentage()
        print(" | ".join(f"{c}: {p:.2f}%" for c, p in percentages.items()))

except KeyboardInterrupt:
    pass

finally:
    colorDetector.close()