# emoji_helper.py
import argparse
import time
from PIL import Image
import pyautogui
import sys

# ─ configure these to match your screen ──────────────────────────────
ex1, ey1 = 307, 167  # top-left corner of the emoji region
ex2, ey2 = 327, 186  # bottom-right corner of the emoji region
EMOJI_REGION = (ex1, ey1, ex2 - ex1, ey2 - ey1)
# e.g. EMOJI_REGION = (500, 150, 40, 40)  # (left, top, width, height)
# ─────────────────────────────────────────────────────────────────────

def capture(state: str):
    """Screenshot the emoji region and save as emoji_<state>.png"""
    img = pyautogui.screenshot(region=EMOJI_REGION)
    fn = f"emoji_{state}.png"
    img.save(fn)
    print(f"Saved {fn}. Now rerun in the other state.")

def analyze():
    """Load the two reference images and find a differing pixel."""
    try:
        img_h = Image.open("emoji_happy.png")
        img_s = Image.open("emoji_sad.png")
    except FileNotFoundError:
        print("Missing emoji_happy.png or emoji_sad.png – run capture first.", file=sys.stderr)
        sys.exit(1)

    w, h = img_h.size
    for y in range(h):
        for x in range(w):
            if img_h.getpixel((x, y)) != img_s.getpixel((x, y)):
                ph = img_h.getpixel((x, y))
                ps = img_s.getpixel((x, y))
                print(f"diff at ({x}, {y}): happy={ph} sad={ps}")
                return  # stop at first diff

    print("No differences found – maybe your captures are the same?")

def detect():
    """Screenshot region, test the magic pixel, and print 'happy' or 'sad'."""
    # load the diff info from a small JSON or hard-code it:
    MAGIC = {
        "x": 7, "y": 5,
        "happy": (255, 255, 0),
        "sad":   (0, 0, 0)
    }
    im = pyautogui.screenshot(region=EMOJI_REGION)
    px = im.getpixel((MAGIC["x"], MAGIC["y"]))
    state = "sad" if px == MAGIC["sad"] else "happy"
    print(state)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["capture","analyze","detect"], required=True)
    parser.add_argument("--state", choices=["happy","sad"], help="only with --mode capture")
    args = parser.parse_args()

    if args.mode == "capture":
        if not args.state:
            parser.error("--state happy|sad is required for capture")
        capture(args.state)
    elif args.mode == "analyze":
        analyze()
    elif args.mode == "detect":
        detect()
