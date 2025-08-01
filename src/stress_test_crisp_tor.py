import asyncio
from playwright.async_api import async_playwright
import random

# Tor SOCKS ports (must match the torrc configuration)
TOR_PORTS = [9050]  # 9051

async def run_instance(playwright, tor_port):
    browser = await playwright.chromium.launch(
        headless=False,
        proxy={
            "server": f"socks5://127.0.0.1:{tor_port}",
        },
        args=[
            '--disable-blink-features=AutomationControlled',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        ]
    )

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        # viewport={"width": 1280, "height": 720},
        java_script_enabled=True,
        bypass_csp=True
    )

    await context.add_init_script("""
        delete navigator.__proto__.webdriver;
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    page = await context.new_page()

    try:
        try:
            await page.goto("http://checkip.amazonaws.com", timeout=120_000)
            ip_address = await page.inner_text("body")
            print(f"Instance on port {tor_port} connected successfully | IP: {ip_address.strip()}")

            await page.goto(
                "file:///run/media/rukia/EXT4E/Default/Workspace/Stealth/index.html",
                wait_until="networkidle",
                timeout=120_000
            )
            await page.wait_for_timeout(30_000)

            await page.get_by_role("textbox", name="Escreva sua mensagem...").click()
            await page.wait_for_timeout(1000)

            await page.get_by_role("textbox", name="Escreva sua mensagem...").fill("")
            await page.wait_for_timeout(2000)

            await page.keyboard.press("Enter")
            await page.wait_for_timeout(30_000)
        except Exception as nav_error:
            print(f"Navigation error on port {tor_port}: {str(nav_error)}")
            raise

    except Exception as launch_error:
        print(f"Failed to launch browser on port {tor_port}: {str(launch_error)}")
    finally:
        try:
            await context.close()
            await browser.close()
        except:
            pass

async def main():
    async with async_playwright() as playwright:
        port = random.choice(TOR_PORTS)
        print(f"Running with Tor port: {port}")
        tasks = [run_instance(playwright, port) for _ in range(1)]
        await asyncio.gather(*tasks)
    print("exit(1)")

if __name__ == '__main__':
    asyncio.run(main())

    # :~$ sudo systemctl start tor
    # :~$ sudo systemctl status tor
    # :~$ sudo systemctl restart tor
    # :~$ sudo netstat -tulnp | grep tor
    #
    #
    # :~$ sudo nano /etc/tor/torrc
    # :~$ which obfs4proxy || sudo apt install obfs4proxy
    # :~$ curl --socks5 localhost:9050 -X POST http://checkip.amazonaws.com
    #
    # Get REAL bridge addresses from official sources:
        # Method 1: Via website (recommended)
        # Visit https://bridges.torproject.org/ and select "obfs4" bridges

        # Method 2: Via email
        # Send empty email to bridges@torproject.org (responds instantly)

    #  curl -s https://bridges.torproject.org/bridges?transport=obfs4 | grep -E 'Bridge obfs4' | head -2
    # which obfs4proxy  # Should show /usr/bin/obfs4proxy
    # torsocks curl --socks5-hostname localhost:9050 https://check.torproject.org
    #
    #
    # sudo pkill -9 tor
    # sudo systemctl stop tor
    # sudo rm -rf /var/lib/tor/*
    #

    # 185.220.101.153
