from playwright.async_api import async_playwright, Browser, Response
import asyncio
import sys
import json
import os
import time

async def saving_image(browser, url, har_filename, wait_to_close):
    context = await browser.new_context(record_har_mode='full', record_har_path=har_filename)
    page = await context.new_page()

    # visit actual url with playwright
    await page.goto(url)
    time.sleep(wait_to_close)
    await context.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python url2har.py <input_folder_path> <output_folder_path>")
        sys.exit(1)

    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    wait_to_close = 0
    if len(sys.argv) > 3: wait_to_close = int(sys.argv[3])

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
                        w8 = wait_to_close
                        if 'wait' in data:
                            w8 = max(wait_to_close, data['wait'])
                        repeats = 1
                        if 'repeats' in data:
                            repeats = data['repeats']
                    for link in links:
                        # filename = link.split('/')[0]
                        # if len(filename) > 50: filename = filename[:50
                        link_short = link[:min(50, len(link))].replace('/', '_').replace('?', '_')
                        for rep in range(repeats):
                            _suff = ""
                            if rep > 1:
                                _suff = f'_rep{rep}'
                            har_filename = f"{output_folder_path}/{filename}/{link_short}{_suff}.har"
                            await saving_image(browser, link, har_filename, w8)
            await browser.close()

    asyncio.run(main())
