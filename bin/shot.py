#!/usr/bin/env python

import sys
from time import sleep
from playwright.sync_api import sync_playwright, expect

def main(args):
    date = args[0]
    post_path = args[1]
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
        expect(divs).not_to_have_count(count=0, timeout=10000)
        levels = []
        for idx, div in enumerate(divs.all()):
            place = div.locator("p.h3").text_content()
            place = place.removeprefix("Halifax ")
            level = div.locator("span.badge").text_content()
            levels.append((place, level))
            base = f"{post_path}.image-{idx}"
            div.screenshot(path=base)
            with open(f"{base}.alt", "w") as f:
                f.write(f"Chart for {place} as of {date} showing the level of COVID-19 in wastewater as {level}.")

        with open(f"{post_path}", "w") as f:
            f.write(f"COVID wastewater charts for the Halifax area as of {date}\n\n")
            for level in levels:
                f.write(f"{level[0]}: {level[1]}\n")

if __name__ == "__main__":
    main(args=sys.argv[1:])
