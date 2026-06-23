#!/usr/bin/env python3
"""Print the CoreGraphics window id of the QuickTime iPhone-mirror window.
Reads from the window server (no AppleEvents), so it won't hang on a busy app.
Picks the largest on-screen QuickTime window with a portrait aspect ratio.
"""
import sys
import Quartz

opts = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
wins = Quartz.CGWindowListCopyWindowInfo(opts, Quartz.kCGNullWindowID)

best = None
for w in wins:
    owner = w.get("kCGWindowOwnerName", "")
    if owner != "QuickTime Player":
        continue
    b = w.get("kCGWindowBounds", {})
    width = b.get("Width", 0)
    height = b.get("Height", 0)
    if width < 100 or height < 100:
        continue
    area = width * height
    if best is None or area > best[1]:
        best = (w.get("kCGWindowNumber"), area, width, height)

if best is None:
    sys.stderr.write("no QuickTime window found\n")
    sys.exit(1)

# Re-read bounds of the chosen window for x,y,w,h
for w in wins:
    if w.get("kCGWindowNumber") == best[0]:
        b = w.get("kCGWindowBounds", {})
        print(f"{int(b.get('X',0))} {int(b.get('Y',0))} {int(b.get('Width',0))} {int(b.get('Height',0))}")
        break
