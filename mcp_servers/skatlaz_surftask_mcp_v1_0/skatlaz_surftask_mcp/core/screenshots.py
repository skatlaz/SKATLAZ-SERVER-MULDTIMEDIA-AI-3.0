from __future__ import annotations
from pathlib import Path
from .webtools import ensure_url, slugify_url

async def screenshot_url(url: str, out_dir: str | Path = "screenshots", width: int = 1280, height: int = 900) -> str:
    from playwright.async_api import async_playwright
    url = ensure_url(url)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slugify_url(url)}.png"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await page.screenshot(path=str(path), full_page=False)
        await browser.close()
    return str(path)
