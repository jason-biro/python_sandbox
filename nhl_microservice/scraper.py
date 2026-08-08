import asyncio
from typing import List
import httpx
from bs4 import BeautifulSoup

from database import AsyncSessionLocal
from models import NHLTeamStat

def _parse_html_page(html_content: str) -> List[dict]:
    """Pure structural manipulation block isolating BeautifulSoup out of I/O cycles."""
    soup = BeautifulSoup(html_content, "html.parser")
    teams_data = []
    rows = soup.select("tr.team")

    for row in rows:
        try:
            teams_data.append({
                "team_name": row.select_one(".name").text.strip(),
                "year": int(row.select_one(".year").text.strip()),
                "wins": int(row.select_one(".wins").text.strip()),
                "losses": int(row.select_one(".losses").text.strip()),
                "win_percentage": float(row.select_one(".pct").text.strip())
            })
        except (AttributeError, ValueError):
            continue
    return teams_data

async def run_background_ingestion(pages: int) -> None:
    """
    Asynchronous runner executed entirely out-of-band on a background task loop.
    Protects API responsiveness against slow target network bounds.
    """
    print(f"[*] Background Queue: Initiating collection for {pages} target frames.")

    async with httpx.AsyncClient(follow_redirects=True) as client:
        #Build tasks concurrently
        tasks = []
        for p in range(1, pages + 1):
            url = f"https://scrapethissite.com/pages/forms/?page_num={p}"
            tasks.append(client.get(url, timeout=15.0))

        # Concurrent network I/O execution.
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Safely open a scraped unit of work session context.
        async with AsyncSessionLocal() as session:
            async with session.begin():
                for index, response in enumerate(responses, start=1):
                    if isinstance(response, Exception) or response.status_code != 200:
                        print(f"[!] Target handling failure encountered on pipeline index {index}: {response}")
                        continue

                    parsed_records = _parse_html_page(response.text)
                    for item_data in parsed_records:
                        print(f"[+] Background Queue: Ingesting record for team '{item_data['team_name']}' from page {index}.")
                        session.add(NHLTeamStat(**item_data))

                # Database transaction automatically commits here when leaving context block.

    print(f"[+] Background Queue: Successfully processed background job batch sequence for {pages} records.")
