"""Capture screenshots of the frontend using Playwright.
Requirements: playwright (Python) and browsers installed via `playwright install`.

Usage:
  python capture_screenshots.py --url http://localhost:8080/terrestrial.html --out screenshots

Outputs two files (initial.png and after.png) in the output directory when possible.
"""
import os
import time
import argparse

from playwright.sync_api import sync_playwright


def capture(url, outdir):
    os.makedirs(outdir, exist_ok=True)
    initial_path = os.path.join(outdir, 'initial.png')
    after_path = os.path.join(outdir, 'after.png')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(url, wait_until='networkidle')
        time.sleep(0.8)
        page.screenshot(path=initial_path, full_page=True)
        # try to interact (click a send button if it exists) to show a different state
        try:
            page.click('#sendButton', timeout=1500)
            time.sleep(0.6)
            page.screenshot(path=after_path, full_page=True)
        except Exception:
            # fallback: try to focus input and type a tiny string then screenshot
            try:
                page.fill('input, textarea', 'demo')
                time.sleep(0.3)
                page.screenshot(path=after_path, full_page=True)
            except Exception:
                # only initial screenshot available
                after_path = None
        browser.close()
    out_files = [initial_path]
    if after_path:
        out_files.append(after_path)
    return out_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost:8080/terrestrial.html', help='Frontend URL to capture')
    parser.add_argument('--out', default='screenshots', help='Output folder')
    args = parser.parse_args()
    files = capture(args.url, args.out)
    for f in files:
        print(f)
