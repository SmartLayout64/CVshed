import colorDetector
import os

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def getColorName(hidx, sidx, vidx):
    if vidx == 0:
        return "Black"
    if sidx == 0:
        if vidx == 2:
            return "White"
        return "Gray"
    names = [
        "Red", "Red-Orange", "Orange", "Yellow-Orange",
        "Yellow", "Yellow-Green", "Green", "Green",
        "Teal", "Cyan", "Sky Blue", "Blue",
        "Blue", "Blue-Violet", "Violet", "Magenta",
        "Pink", "Red",
    ]
    return names[hidx]

LOGO = '''────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████──██████──██████──██████████████──██████──██████──██████████████──████████████───
─██░░░░░░░░░░██──██░░██──██░░██──██░░░░░░░░░░██──██░░██──██░░██──██░░░░░░░░░░██──██░░░░░░░░████─
─██░░██████████──██░░██──██░░██──██░░██████████──██░░██──██░░██──██░░██████████──██░░████░░░░██─
─██░░██──────────██░░██──██░░██──██░░██──────────██░░██──██░░██──██░░██──────────██░░██──██░░██─
─██░░██──────────██░░██──██░░██──██░░██████████──██░░██████░░██──██░░██████████──██░░██──██░░██─
─██░░██──────────██░░██──██░░██──██░░░░░░░░░░██──██░░░░░░░░░░██──██░░░░░░░░░░██──██░░██──██░░██─
─██░░██──────────██░░██──██░░██──██████████░░██──██░░██████░░██──██░░██████████──██░░██──██░░██─
─██░░██──────────██░░░░██░░░░██──────────██░░██──██░░██──██░░██──██░░██──────────██░░██──██░░██─
─██░░██████████──████░░░░░░████──██████████░░██──██░░██──██░░██──██░░██████████──██░░████░░░░██─
─██░░░░░░░░░░██────████░░████────██░░░░░░░░░░██──██░░██──██░░██──██░░░░░░░░░░██──██░░░░░░░░████─
─██████████████──────██████──────██████████████──██████──██████──██████████████──████████████───
────────────────────────────────────────────────────────────────────────────────────────────────'''

def tickUI(percentages, bucketMeta, maxColorRows):
    ranked = sorted(
        [(name, p) for name, p in percentages.items() if p > 0],
        key=lambda x: x[1],
        reverse=True
    )

    lines = []
    lines.append(LOGO)
    lines.append("")
    lines.append(f"  {'%':<10} {'Color':<16} {'HSV'}")
    lines.append("  " + "-" * 43)

    for i in range(maxColorRows):
        if i < len(ranked):
            name, p = ranked[i]
            generic, hMid, sMid, vMid = bucketMeta[name]
            lines.append(f"  [{p:5.1f}%]   {generic:<16} ({hMid}, {sMid}, {vMid})")
        else:
            lines.append("")

    lines.append("")
    lines.append("  Press Ctrl+C to quit.")

    output = "\033[H"
    for line in lines:
        output += "\033[2K" + line + "\n"

    print(output, end="", flush=True)


# --- Setup ---
colorDetector.initialize(0)

hBuckets = 18
sBuckets = 3
vBuckets = 3
colors = {}
bucketMeta = {}

for h in range(hBuckets):
    for s in range(sBuckets):
        for v in range(vBuckets):
            name = f"H{h}_S{s}_V{v}"
            hMin = int(h * (180 / hBuckets))
            hMax = int((h + 1) * (180 / hBuckets)) - 1
            sMin = int(s * (256 / sBuckets))
            sMax = int((s + 1) * (256 / sBuckets)) - 1
            vMin = int(v * (256 / vBuckets))
            vMax = int((v + 1) * (256 / vBuckets)) - 1
            colors[name] = [((hMin, sMin, vMin), (hMax, sMax, vMax))]
            hMid = (hMin + hMax) // 2
            sMid = (sMin + sMax) // 2
            vMid = (vMin + vMax) // 2
            generic = getColorName(h, s, v)
            bucketMeta[name] = (generic, hMid, sMid, vMid)

colorDetector.setColors(colors)

maxColorRows = 20

print("\033[?25l", end="", flush=True)
clearTerminal()

try:
    while True:
        percentages = colorDetector.getColorPercentage()
        tickUI(percentages, bucketMeta, maxColorRows)
except KeyboardInterrupt:
    pass
finally:
    print("\033[?25h", end="", flush=True)
    colorDetector.close()