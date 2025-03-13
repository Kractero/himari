from urllib.request import urlopen, Request
import xml.etree.ElementTree as ET
from time import sleep
from datetime import datetime
from json import dumps

top100names = []

for i in range(5):
    start = 1 + i * 20

    with urlopen(Request(f"https://www.nationstates.net/cgi-bin/api.cgi?q=censusranks&scale=86&start={start}", headers={'User-Agent': 'Kractero using Ledger'})) as response:
        response_bytes = response.read()
        response_text = response_bytes.decode('utf-8')

        root = ET.fromstring(response_text)

        for nation in root.findall('.//NATION'):
            name = nation.find('NAME').text
            top100names.append(name)

        ratelimit_remaining = int(response.headers.get('RateLimit-Remaining'))
        ratelimit_reset = int(response.headers.get('RateLimit-Reset'))

        if ratelimit_remaining > 0:
            sleep((ratelimit_reset / ratelimit_remaining))
        else:
            sleep(ratelimit_reset)

top100data = []

for name in top100names:
    with urlopen(Request(f"https://www.nationstates.net/cgi-bin/api.cgi?nationname={name}&q=cards+deck+info", headers={'User-Agent': 'Kractero using Ledger'})) as response:
        response_bytes = response.read()
        response_text = response_bytes.decode('utf-8')

        root = ET.fromstring(response_text)
        nation = name.lower().replace('_', ' ').title()

        deck = { "Nation": nation }

        category_counts = {}
        season_counts = {}
        category_season_counts = {}
        legendary_value = 0

        cards = root.findall('.//CARD')
        if cards is not None:
            for card in cards:
                category = card.find('CATEGORY').text.lower()
                category = ' '.join(word.capitalize() for word in category.split(' '))
                category = '-'.join(word.capitalize() for word in category.split('-'))

                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1

                season = card.find('SEASON').text
                season_key = f"S{season}"
                if season_key in season_counts:
                    season_counts[season_key] += 1
                else:
                    season_counts[season_key] = 1

                key = f"S{season} {category}"
                if key in category_season_counts:
                    category_season_counts[key] += 1
                else:
                    category_season_counts[key] = 1

                if category == 'Legendary':
                    legendary_value += float(card.find('MARKET_VALUE').text)

            junk_value = (
                (category_counts.get('Legendary', 0) * 1 +
                category_counts.get('Epic', 0) * 0.5 +
                category_counts.get('Common', 0) * 0.01 +
                category_counts.get('Uncommon', 0) * 0.05 +
                category_counts.get('Ultra-Rare', 0) * 0.2)
            )
            deck['Junk Value'] = round(junk_value, 2)

        deck_info = root.find('.//INFO')
        if deck_info is not None:
            deck['Bank'] = float(deck_info.find('BANK').text)
            deck['Deck Value'] = float(deck_info.find('DECK_VALUE').text)
            deck['Card Count'] = int(deck_info.find('NUM_CARDS').text)
            deck['Deck Capacity'] = int(deck_info.find('DECK_CAPACITY_RAW').text)

        deck['Legendary Value Raw'] = round(legendary_value, 2)
        deck['Legendary Value'] = min(100.0, round(legendary_value / float(deck_info.find('DECK_VALUE').text) * 100, 2))
        deck.update(category_counts)
        deck.update(season_counts)
        deck.update(category_season_counts)

        if deck['Card Count'] > deck['Deck Capacity']:
            deck['Deck Capacity'] = deck['Deck Capacity'] * 2

        top100data.append(deck)

        ratelimit_remaining = int(response.headers.get('RateLimit-Remaining'))
        ratelimit_reset = int(response.headers.get('RateLimit-Reset'))

        if ratelimit_remaining > 0:
            sleep((ratelimit_reset / ratelimit_remaining))
        else:
            sleep(ratelimit_reset)

current_date = datetime.now().strftime('%Y-%m-%d')
with open(f'data/{current_date}.json', 'w') as file:
    file.write(dumps(top100data, indent=2))

with open('files/leaderboard.txt', 'r') as file:
    existing_dates = file.read()

new_content = f"{existing_dates.strip()}\n{current_date}"

with open('files/leaderboard.txt', 'w') as file:
    file.write(new_content)
