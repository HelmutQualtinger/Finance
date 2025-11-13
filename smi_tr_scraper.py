
import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.six-group.com/de/market-data/indices/index-explorer/index-details.CH0000222130CHF9.html#/")
        
        chart_element = await page.wait_for_selector('[data-chart-data-source-url]')
        data_url = await chart_element.get_attribute('data-chart-data-source-url')
        
        full_url = "https://www.six-group.com" + data_url
        
        # Use page context to fetch the data from the new URL
        api_response = await page.request.get(full_url)
        json_data = await api_response.json()
        
        print(json.dumps(json_data))
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
