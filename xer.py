import base64
import random
import time
import requests
from seleniumbase import SB


def rsleep(a=1, b=3):
    """Randomized sleep helper."""
    time.sleep(random.uniform(a, b))


def get_geo_data():
    """Fetch geolocation data from IP-API."""
    try:
        data = requests.get("http://ip-api.com/json/", timeout=5).json()
        return {
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "timezone": data.get("timezone"),
            "lang": data.get("countryCode", "").lower(),
        }
    except Exception:
        return {"lat": None, "lon": None, "timezone": "UTC", "lang": "en"}


def decode_username(encoded_name: str) -> str:
    """Decode Base64 username."""
    return base64.b64decode(encoded_name).decode("utf-8")


def click_if_present(driver, selector, timeout=4):
    """Click an element if it exists."""
    if driver.is_element_present(selector):
        driver.cdp.click(selector, timeout=timeout)
        rsleep(1, 2)


def open_stream(driver, url, timezone, geoloc):
    """Open stream and handle initial popups."""
    driver.activate_cdp_mode(url, tzone=timezone, geoloc=geoloc)
    rsleep(2, 4)

    click_if_present(driver, 'button:contains("Accept")')
    rsleep(2, 4)

    rsleep(10, 14)
    click_if_present(driver, 'button:contains("Start Watching")')
    click_if_present(driver, 'button:contains("Accept")')


def main():
    geo = get_geo_data()
    geoloc = (geo["lat"], geo["lon"])
    timezone = geo["timezone"]

    encoded_name = "YnJ1dGFsbGVz"
    username = decode_username(encoded_name)

    stream_url = f"https://www.twitch.tv/{username}"
    proxy = False

    while True:
        with SB(
            uc=True,
            locale="en",
            ad_block=True,
            chromium_arg="--disable-webgl",
            proxy=proxy
        ) as driver:

            session_duration = random.randint(450, 800)

            open_stream(driver, stream_url, timezone, geoloc)

            if driver.is_element_present("#live-channel-stream-information"):
                # Secondary viewer instance
                secondary = driver.get_new_driver(undetectable=True)
                open_stream(secondary, stream_url, timezone, geoloc)

                rsleep(8, 12)
                rsleep(session_duration - random.randint(5, 20), session_duration)

            else:
                break


if __name__ == "__main__":
    main()
