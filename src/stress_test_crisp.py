import asyncio
from playwright.async_api import async_playwright


async def run_instance(playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    await context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = await context.new_page()

    await page.goto("file:///run/media/rukia/EXT4E/Default/Workspace/Stealth/index.html")

    await page.wait_for_timeout(10_000)

    await page.screenshot(path="screenshot.png")

    await page.get_by_role("textbox", name="Escreva sua mensagem...").click()
    await page.wait_for_timeout(1000)

    # await page.screenshot(path="screenshot2.png")

    await page.get_by_role("textbox", name="Escreva sua mensagem...").fill("*")
    await page.wait_for_timeout(2000)

    await page.keyboard.press("Enter")

    await page.wait_for_timeout(30_000)

    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        tasks = [run_instance(playwright) for _ in range(1)]
        await asyncio.gather(*tasks)
    print("ended!")


if __name__ == '__main__':
    asyncio.run(main())
