import pandas as pd

# quick data cleaner to drop duplicates and remove title redundancy

unclean_data_path = 'deck_data.csv'
clean_data_path = 'deck_data_clean.csv'

df = pd.read_csv(unclean_data_path, low_memory=False)
df = df.drop_duplicates()

# removing '- Hearthstone Decks' from ends of titles
def drop_last_split(deck_title):
    if '-' in deck_title:
        *deck_list, _ = deck_title.split(' -')
        deck_name = ''
        for str in deck_list:
            deck_name = deck_name + str
        return deck_name
    else:
        return deck_title


df['Title'] = df['Title'].apply(drop_last_split)

df.to_csv(clean_data_path, index=False)