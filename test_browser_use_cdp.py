"""Test browser_use BrowserSession with our Chrome CDP connection."""
import asyncio
import os

# Set env to avoid LiteLLM DNS hangs during import
os.environ["LITELLM_MODE"] = "LOCAL"

async def main():
    print("Creating BrowserSession with CDP URL...")
    from browser_use.browser.session import BrowserSession

    # Connect to our already-running Chrome CDP
    browser = BrowserSession(
        cdp_url="http://127.0.0.1:9222",
        headless=False,  # We already have a visible window
    )

    print("Getting browser info...")
    info = await browser.get_info()
    print(f"Browser info: {info}")

    print("\nCreating new page...")
    page = await browser.new_page()
    print(f"Page created: {page}")

    print("\nNavigating to example.com...")
    await page.goto("https://example.com")
    title = await page.title()
    content = await page.content()
    print(f"Title: {title}")
    print(f"Content length: {len(content)} chars")
    print(f"Content preview: {content[:300]}")

    print("\nSUCCESS! BrowserSession + CDP works!")

    # Clean up
    await page.close()

if __name__ == "__main__":
    asyncio.run(main())
