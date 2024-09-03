import json
from datetime import datetime, timedelta

def main():
    with open('files/Legendaries.json', 'r') as legendaries:
        legendaries = json.load(legendaries)

    with open('files/LegendariesChangelog.json', 'r') as legendaries_data:
        legendaries_data = json.load(legendaries_data)

    todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    with open(f'data/{todays_date}-cards.json', 'r') as cards_json:
        cards_json = json.load(cards_json)

    legdata = {
        "date": todays_date,
        "changes": [],
    }

    for legendary in legendaries:
        cte = cards_json[legendary['id']]
        if not cte != legendary['exists']:
            print (cte)
            legdata['changes'].append({
                "name": legendary['name'],
                "seasons": [legendary['S1'], legendary['S2'], legendary['S3']],
                "old": legendary['exists'],
                "new": not cte
            })
        legendary['exists'] = not cte

    if len(legdata['changes']) > 0:
        legendaries_data.insert(0, legdata)

    with open('files/Legendaries.json', 'w') as legendaries_file:
        json.dump(legendaries, legendaries_file, indent=2)

    with open('files/LegendariesChangelog.json', 'w') as legendaries_data_file:
        json.dump(legendaries_data, legendaries_data_file, indent=2)

    print ("Done computing legendaries")

if __name__ == "__main__":
    main()