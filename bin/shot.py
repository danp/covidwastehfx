#!/usr/bin/env python

import sys
from time import sleep
from playwright.sync_api import sync_playwright, expect

def main(args):
    path = args[0]
    with sync_playwright() as p:
        browser = p.firefox.launch()
        context = browser.new_context(device_scale_factor=2)
        page = context.new_page()
        page.goto("https://health-infobase.canada.ca/wastewater/")
        page.get_by_label("Select a province/territory:").select_option("Nova Scotia")
        sleep(1) # ???
        page.get_by_label("Select a municipality:").select_option("Halifax")
        locator = page.locator("#smallmultiples-container")
        divs = locator.locator("div")
        expect(divs).to_have_count(count=3, timeout=10000)
        for idx, div in enumerate(divs.all()):
            p = f"{path}{idx}"
            div.screenshot(path=p)
        browser.close()

if __name__ == "__main__":
    main(args=sys.argv[1:])
