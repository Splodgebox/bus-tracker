import requests, re
from bs4 import BeautifulSoup
from bus_tracker.models import BusTime

def get_bee_times(url: str):
    if "no-script=true" not in url:
        url = url + ("&" if "?" in url else "?") + "no-script=true"

    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    out = []
    for row in soup.select('[data-testid="departure-row"]'):
        title = row.select_one('[data-testid="bus-service-details"] h3')
        when  = row.select_one('[data-testid="bus-timings"] h3')
        label = row.select_one('[data-testid="bus-timings"] span')

        if not title or not when:
            continue

        svc = title.get_text(strip=True)
        number, name = (svc.split(":", 1) + [""])[:2]
        number, name = number.strip(), name.strip()

        primary = when.get_text(strip=True).strip()
        low = primary.lower()
        tag = (label.get_text(strip=True).lower() if label else "")

        if "min" in low or "due" in low:
            disp = "0 mins" if "due" in low else primary
            is_timetabled = False
        else:
            disp = primary
            if "live" in tag:
                is_timetabled = False
            elif "timetabled" in tag:
                is_timetabled = True
            else:
                is_timetabled = True

        out.append(BusTime(number, name, disp, is_timetabled))

    return out
