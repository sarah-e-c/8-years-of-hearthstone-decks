from bs4 import BeautifulSoup
import requests
import time
import csv

MAX_PAGES_TO_SCRAPE = 30000 #'pages' refers to sets of 25 decks
tot_jumps = 0 # set to 0 if starting from scratch

pages_scraped = 0 # edit if continuing -- will print last value

# loop control
tot_jumps_on_page = 0
page_scraped = False

#
base_home_url = 'https://www.hearthpwn.com/decks'
base_url = 'https://www.hearthpwn.com'

with open('deck_data.csv', 'a', newline='') as deck_data:
    writer = csv.writer(deck_data)

    #run first time
    writer.writerow(['Title', 
                        'Class',
                        'Expansion',
                        'MinionCount',
                        'SpellCount',
                        'DustCost',
                        'DeckType',
                        'DeckArchetype',
                        'LastUpdated',
                        'Creator',
                        'DeckCode',
                        'Rating',
                        'Cards',
                        'CardQuantities',
                        'CardCosts',
                        'Link'])

    try:
        while pages_scraped < MAX_PAGES_TO_SCRAPE:
            if pages_scraped == 0:
                home_url = base_home_url + '?sort=datemodified'
            else: 
                home_url = base_home_url + '?page=' + str(pages_scraped + 1) + '&sort=datemodified'
            page_scraped = False
            tot_jumps_on_page = 0
            home_source = requests.get(home_url).text
            home_soup = BeautifulSoup(home_source, 'lxml')
            next_href_list = home_soup.find_all('td',class_='col-name')


            while (page_scraped == False):
                home = True
                link = home_url
                try:
                    next_href = next_href_list[tot_jumps_on_page].div.span.a['href']#.find('span', class_='tip').div#.find('a')['href']
                    link = base_url + next_href
                    print(link)
                    source = requests.get(link).text
                    soup = BeautifulSoup(source, 'lxml')
                except: 
                    page_scraped = True
                    break      

                # to find
                title = soup.title.text
                try:
                    minion_count = int(soup.find('li', class_='t-deck-card-count-minions').text.split(' ')[0])
                except:
                    minion_count = 0
                try:
                    spell_count = int(soup.find('li', class_='t-deck-card-count-spells').text.split(' ')[0])
                except:
                    spell_count = 0
                
                try:
                    dust_cost = int(soup.find('span', class_ ='craft-cost').text)
                except:
                    dust_cost = 0
                
                try: 
                    deck_type = soup.find_all('span', class_='deck-type')[0].text
                except:
                    deck_type = 'other'
                try:
                    deck_archetype = soup.find_all('span', class_='deck-type')[1].text.split('\n')[1]
                except: 'other'

                last_updated = soup.find('abbr', class_='tip standard-date standard-datetime').text
                creator = soup.find('li', class_='name').text
                deck_code = soup.find('button', class_='copy-button button')['data-clipboard-text']
                rating = soup.find('div', class_="b-rating b-rating-a rating-form up-down group").find_all('div')[1].text #rating is different if its positive

                try:
                    class_ = soup.find('section', class_='deck-actions').find('span')['class'][1].split('-')[1]
                except:
                    class_ = 'None'
                expansion = soup.find('span', class_="deck-build").text


                card_list_final = []
                card_quantities = []
                card_costs = []

                #card names and quantities
                card_list = soup.find('div', class_='details t-deck-details').find_all('td', class_='col-name')
                for card in card_list:
                    try:
                        card_components = card.text.split('>')
                        card_1 = card_components[0].split('\n')
                        card_list_final.append(card_1[3])
                        card_quantities.append(int(card_1[6].split(' ')[1]))
                    except:
                        card_components = None
                    #print(card_components)

                #card costs
                card_costs_list = soup.find_all('td', class_='col-cost')
                for card in card_costs_list:
                    try:
                        card_costs.append(int(card.text))
                    except:
                        card_costs.append(None)

                list_to_append = [title, class_, expansion, minion_count, spell_count, dust_cost, deck_type, deck_archetype, last_updated, 
                                creator, deck_code, rating, str(card_list_final), str(card_quantities), str(card_costs), link]
                writer.writerow(list_to_append)

                #loop control
                tot_jumps_on_page += 1
                tot_jumps += 1
                time.sleep(1) #sleeping for a bit, can be a bit faster, but be respectful!

            pages_scraped += 1
            print('page scraped!')
            print('Total pages scraped: ', pages_scraped)

    except Exception as e:
        print('Scrape failed because of:')
        print(e)
        print('Total decks scraped: ', tot_jumps)
        print('Total pages scraped: ', pages_scraped - 1)

