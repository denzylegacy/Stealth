import asyncio
from playwright.async_api import async_playwright
import random
import requests

# Mullvad SOCKS5 proxy configuration
MULLVAD_PROXY = {
    "server": "socks5://10.64.0.1:1080",  # For WireGuard protocol
    # "server": "socks5://10.8.0.1:1080",  # For OpenVPN protocol
}

def get_mullvad_servers():
    """Fetch all Mullvad WireGuard SOCKS5 endpoints"""
    response = requests.get("https://api.mullvad.net/www/relays/wireguard/")
    data = response.json()

    servers = []
    servers = list({server['socks_name'] for server in data if 'socks_name' in server})
    return servers

MULLVAD_SERVERS = get_mullvad_servers()
print(f"Available Mullvad SOCKS5 servers: {len(MULLVAD_SERVERS)}")

async def run_instance(playwright):
    proxy_server = random.choice(MULLVAD_SERVERS)
    proxy_config = {
        "server": f"socks5://{proxy_server}:1080",
    }

    browser = await playwright.chromium.launch(
        headless=False,
        proxy=proxy_config,
        args=[
            '--disable-blink-features=AutomationControlled',
            f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 115)}.0.0.0 Safari/537.36'
        ]
    )

    context = await browser.new_context(
        user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90, 115)}.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 768},
        java_script_enabled=True,
        bypass_csp=True
    )

    await context.add_init_script("""
        delete navigator.__proto__.webdriver;
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    """)

    page = await context.new_page()

    try:
        await page.goto("https://am.i.mullvad.net", timeout=120_000)
        ip_info = await page.inner_text("body")
        print(f"Connected via {proxy_server} | {ip_info.strip()}")

        await page.goto("file:///run/media/rukia/EXT4E/Default/Workspace/Stealth/index.html", wait_until="networkidle")
        await page.wait_for_timeout(5_000)

        await page.get_by_role("textbox", name="Escreva sua mensagem...").fill("*")
        await page.wait_for_timeout(2000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(30_000)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await context.close()
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run_instance(playwright)
    print("Process completed")


if __name__ == '__main__':
    asyncio.run(main())
