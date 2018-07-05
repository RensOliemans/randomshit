from bs4 import BeautifulSoup

FILENAME = 'pagina.html'


def convert_score(score):
    numbers = [int(s) for s in score.split(' - ')]
    return min(numbers), max(numbers)


def parse_matches(matches):
    players = dict()
    for match in matches:
        predictions = match.findAll('td')
        grouped = [predictions[i:i+2] for i in range(0, len(predictions), 2)]

        for group in grouped:
            player = group[0].text
            score = convert_score(group[1].text)

            if player not in players:
                players[player] = list()
            players[player].append(score)
    return players


def analyse_players(players):
    print("Unique predictions")
    predicts = [f"{player}: {len(set(players[player]))} - {set(players[player])}" for player in players]
    print(*predicts, sep='\n')

    print("\nMax amount of goals")
    for player in players:
        print(f"{player}: {max(sum(game) for game in players[player])}")

    print("\nAverage amount of goals")
    for player in players:
        print(f"{player}: {max(sum(game) for game in players[player]) / len(players[player]):.2f}")


def main():
    html = open(FILENAME).read()
    soup = BeautifulSoup(html, 'html.parser')

    matches = soup.find_all(attrs={'class': 'compareGame overview played active'})
    players = parse_matches(matches)
    return players


if __name__ == '__main__':
    print(main())
