from playwright.async_api import async_playwright, Browser, Response
import asyncio
import sys
import json
import os

async def saving_image(browser, url, har_filename):
    context = await browser.new_context(record_har_mode='full', record_har_path=har_filename)
    page = await context.new_page()

    # visit actual url with playwright
    await page.goto(url)
    # time.sleep(20)
    await context.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python url2har.py <input_folder_path>")
        sys.exit(1)

    input_folder_path = sys.argv[1]

    async def main():
        async with async_playwright() as playwright:
            # launches browser. Adjust arguments as you like
            browser = await playwright.chromium.launch(headless=False)

            for filename in os.listdir(input_folder_path):
                if filename.endswith(".json"):
                    json_filename = os.path.join(input_folder_path, filename)
                    with open(json_filename, 'r') as f:
                        data = json.load(f)
                        links = data['links']

                    subfolder_name = os.path.splitext(filename)[0]
                    subfolder_path = os.path.join("traces", subfolder_name)
                    os.makedirs(subfolder_path, exist_ok=True)

                    for link in links:
                        filename = link.split('/')[-1]
                        if len(filename) > 50: filename = filename[:100]
                        har_filename = os.path.join(subfolder_path, f"{filename}.har")
                        await saving_image(browser, link, har_filename)
            await browser.close()

    asyncio.run(main())
