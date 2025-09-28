import json
import re
from pathlib import Path
from typing import Dict, Any, List, Iterator

# --- Configuration ---
# Use pathlib for robust path handling relative to the script's location
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
INPUT_FILES = [
    ROOT_DIR / "hexagram_interpretations.md",
    ROOT_DIR / "docs" / "state_cards.md",
]
OUTPUT_DIR = ROOT_DIR / "assets" / "data" / "cards"

def parse_markdown_file(filepath: Path) -> Iterator[Dict[str, Any]]:
    """
    Parses a markdown file to extract JSON data blocks and yields them one by one.

    Args:
        filepath: The path to the markdown file.

    Yields:
        A dictionary representing the parsed JSON of a card.
    """
    print(f"Parsing source file: {filepath.name}...")
    try:
        content = filepath.read_text(encoding="utf-8")
        # Find all ```json ... ``` blocks
        json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)

        for block in json_blocks:
            try:
                yield json.loads(block)
            except json.JSONDecodeError as e:
                print(f"  [Warning] Skipping invalid JSON block in {filepath.name}: {e}")
                print(f"  > Block content: {block[:100]}...")
    except FileNotFoundError:
        print(f"  [Error] Source file not found: {filepath}")
    except Exception as e:
        print(f"  [Error] An unexpected error occurred while parsing {filepath}: {e}")


def generate_card_files(cards: List[Dict[str, Any]], base_output_path: Path):
    """
    Generates individual .json files for each card in the appropriate subdirectory.

    Args:
        cards: A list of card data dictionaries.
        base_output_path: The root directory for all generated card files.
    """
    generated_count = 0
    for card in cards:
        card_type = card.get("type")
        card_id = card.get("id")

        if not card_type or not card_id:
            print(f"  [Warning] Skipping card with missing 'type' or 'id': {card}")
            continue

        # Determine the correct subdirectory based on the card type
        if card_type in ["stem", "branch", "celestial"]:
            # State cards have a nested structure with specific pluralization
            folder_map = {
                "stem": "stems",
                "branch": "branches",
                "celestial": "celestial",
            }
            subfolder_name = folder_map.get(card_type, f"{card_type}s")
            output_path = base_output_path / "state" / subfolder_name
        else:
            # Other cards are directly in a folder named by their type
            output_path = base_output_path / card_type

        # Create the directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Write the JSON file
        file_path = output_path / f"{card_id}.json"
        try:
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(card, f, ensure_ascii=False, indent=2)
            # print(f"  Generated: {file_path}")
            generated_count += 1
        except Exception as e:
            print(f"  [Error] Failed to write file {file_path}: {e}")

    return generated_count


def main():
    """
    Main function to orchestrate the card data generation process.
    """
    print("--- Starting Card Data Generation ---")

    all_cards = []
    for file_path in INPUT_FILES:
        all_cards.extend(parse_markdown_file(file_path))

    if not all_cards:
        print("\nNo card data found in any source file. Exiting.")
        return

    print(f"\nFound a total of {len(all_cards)} card definitions. Generating files...")

    # Ensure the base output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    count = generate_card_files(all_cards, OUTPUT_DIR)

    print(f"\n--- Card Data Generation Complete ---")
    print(f"Successfully generated {count} out of {len(all_cards)} card data files.")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()