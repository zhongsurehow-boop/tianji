import os
import json
import re

def parse_markdown(filepath):
    """
    Parses the markdown file to extract structured card data.
    It looks for JSON code blocks within the markdown.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    card_data_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)

    cards = []
    for block in card_data_blocks:
        try:
            card = json.loads(block)
            cards.append(card)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic block: {block}")

    return cards

def generate_json_files(cards, base_path='assets/data/cards'):
    """
    Generates JSON files for each card in the appropriate directory.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for card in cards:
        card_type = card.get('type')
        card_id = card.get('id')

        if not card_type or not card_id:
            print(f"Skipping card with missing type or id: {card}")
            continue

        # Determine the correct subdirectory
        if card_type in ['stem', 'branch', 'celestial']:
            type_folder = {
                'stem': 'stems',
                'branch': 'branches',
                'celestial': 'celestial'
            }[card_type]
            dir_path = os.path.join(base_path, 'state', type_folder)
        else:
            dir_path = os.path.join(base_path, card_type)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        filepath = os.path.join(dir_path, f"{card_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(card, f, ensure_ascii=False, indent=2)
        print(f"Generated: {filepath}")

def main():
    """
    Main function to run the script.
    """
    print("Starting card data generation...")
    cards = parse_markdown('hexagram_interpretations.md')
    if cards:
        generate_json_files(cards)
        print(f"\nSuccessfully generated {len(cards)} card data files.")
    else:
        print("No card data found in the markdown file.")

if __name__ == '__main__':
    main()