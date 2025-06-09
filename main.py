import pyautogui
import time
import random

pyautogui.FAILSAFE = True  # drag to any corner to abort

# ───────── CONFIGURE THESE TO YOUR SCREEN ───────────────
ex1, ey1 = 307, 167  # top-left corner of the emoji region
ex2, ey2 = 327, 186  # bottom-right corner of the emoji region
EMOJI_REGION = (ex1, ey1, ex2 - ex1, ey2 - ey1)

# Pixel‐within that region whose color flips between happy/sad:
MAGIC = {
    "x": 7, "y": 5,               # coords *within* the emoji screenshot
    "happy": (255, 255, 0),      # RGB when game is live
    "sad":   (0, 0, 0)           # RGB when you’ve hit a mine
}
# ─────────────────────────────────────────────────────────

def detect():
    """
    Screenshot the emoji region and return 'happy' or 'sad'
    based on that one magic pixel.
    """
    im = pyautogui.screenshot(region=EMOJI_REGION)
    px = im.getpixel((MAGIC["x"], MAGIC["y"]))
    return "sad" if px == MAGIC["sad"] else "happy"

def click_emoji():
    """
    Click in the center of the emoji region to restart the game.
    """
    left, top, w, h = EMOJI_REGION
    cx = left + w // 2
    cy = top  + h // 2
    pyautogui.click(cx, cy)

def random_grid_click_no_repeat(
    x1: int, y1: int,
    x2: int, y2: int,
    cols: int, rows: int,
    duration: float = 10.0,
    min_interval: float = 0.05,
    max_interval: float = 0.2
):
    """
    Clicks each of the cols×rows cells exactly once (in random order),
    checks the emoji after each click, and restarts the game automatically
    if it goes sad.
    """
    cell_w = (x2 - x1) / cols
    cell_h = (y2 - y1) / rows

    clicked = set()
    total_cells = cols * rows
    end_time = time.time() + duration

    while time.time() < end_time:
        # 1) pick a random cell we haven't clicked yet
        if len(clicked) >= total_cells:
            print("All cells clicked once—waiting for sad emoji to restart…")
            # Give the game time to reset
            time.sleep(0.5)
        else:
            cx = random.randint(0, cols - 1)
            cy = random.randint(0, rows - 1)
            if (cx, cy) in clicked:
                continue
            clicked.add((cx, cy))
            px = int(x1 + (cx + 0.5) * cell_w)
            py = int(y1 + (cy + 0.5) * cell_h)
            pyautogui.click(px, py)
            print(f"Clicked cell {(cx, cy)} ({len(clicked)}/{total_cells})")

        # 2) check emoji state
        state = detect()
        print(state)
        if state == "sad":
            print("💥 Hit a mine! Restarting game…")
            click_emoji()
            clicked.clear()            # start fresh
            # allow board to redraw
            # time.sleep(0.5)

        # 3) small pause between actions
        # time.sleep(random.uniform(min_interval, max_interval))

    print("Duration elapsed—stopping.")

if __name__ == "__main__":
    # your measured board bounds
    x1, y1 = 246, 201
    x2, y2 = 391, 344

    # run for 60 seconds (or change as you like)
    random_grid_click_no_repeat(
        x1, y1, x2, y2,
        cols=9, rows=9,
        duration=5000,
        min_interval=0.05,
        max_interval=0.2
    )
