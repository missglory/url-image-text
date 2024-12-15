from playwright.async_api import async_playwright, Browser, Response
import asyncio
import sys
import json
import time

async def saving_image(browser, url, har_filename):
    context = await browser.new_context(record_har_mode='full', record_har_path=har_filename)
    page = await context.new_page()

    # visit actual url with playwright
    await page.goto(url)
    # time.sleep(20)
    await context.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python soqs.py <result_json_filename>")
        sys.exit(1)

    result_json_filename = sys.argv[1]

    with open(result_json_filename, 'r') as f:
        data = json.load(f)
        links = data['links']

    async def main():
        async with async_playwright() as playwright:
            # launches browser. Adjust arguments as you like
            browser = await playwright.chromium.launch(headless=False)

            for link in links:
                filename = link.split('/')[-1]
                if len(filename) > 50: filename = filename[100:]
                har_filename = f"traces/{filename}.har"
                await saving_image(browser, link, har_filename)
            await browser.close()

    asyncio.run(main())
