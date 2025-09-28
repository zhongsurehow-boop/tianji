# -*- coding: utf-8 -*-
"""
Card Data Generation Script for 《天机变》.

This script automates the process of converting human-readable card definitions
from Markdown files into structured, machine-readable JSON data files that the
game engine can consume.

Key Functions:
- Parses specified Markdown files (`hexagram_interpretations.md`, etc.).
- Extracts all `json` code blocks.
- Validates each card's JSON data against the official `card_logic_schema.md`.
- Generates individual `.json` files for each valid card into the
  `assets/data/cards/` directory, organized by card type.
- Provides detailed error reporting for both JSON syntax and schema violations.

This script is the cornerstone of the "data-driven design" philosophy of the project,
ensuring that all game logic originates from a single, version-controlled source of truth.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Iterator, Optional, Set, Tuple

# --- 1. Configuration & Constants ---

# Get the script's directory and project root for robust pathing.
SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent
DEFAULT_SCHEMA_PATH = ROOT_DIR / "card_logic_schema.md"

# Define input source files and the base output directory.
INPUT_FILES = [
    ROOT_DIR / "hexagram_interpretations.md",
    # Add other source files here if they are created, e.g., for expansions.
    # ROOT_DIR / "docs" / "state_cards.md", # This file was mentioned in the original script but doesn't exist.
]
OUTPUT_DIR = ROOT_DIR / "assets" / "data" / "cards"

# Define card types that are classified as "state" cards.
STATE_CARD_TYPES = {"stem", "branch", "celestial"}


# --- 2. Schema Loading & Validation ---

class CardSchema:
    """A container for the game's logic schema, parsed from Markdown."""

    def __init__(self, schema_path: Path):
        """
        Loads and parses the schema definitions from the provided Markdown file.

        Args:
            schema_path: The path to the `card_logic_schema.md` file.
        """
        self.path = schema_path
        self.actions: Set[str] = set()
        self._load()

    def _load(self):
        """Parses the schema file to extract valid action names."""
        print(f"Loading schema from: {self.path.name}")
        try:
            content = self.path.read_text(encoding="utf-8")
            # Regex to find the 'Action' table and extract the action names.
            # It looks for a markdown table header, then captures the first
            # column of each subsequent row.
            action_table_match = re.search(
                r"## 4\. 动作 \(Action\).*?\| 类型.*?\|(.*?)^---", content, re.S | re.M
            )
            if not action_table_match:
                print("  [Error] Could not find the Action table in the schema file.", file=sys.stderr)
                return

            table_content = action_table_match.group(1)
            # Extracts all action names (e.g., `GAIN_RESOURCE`) from the table rows.
            self.actions = {
                action.strip()
                for action in re.findall(r"\|\s*`([A-Z_]+)`", table_content)
            }
            print(f"  Successfully loaded {len(self.actions)} valid actions from schema.")

        except FileNotFoundError:
            print(f"  [Error] Schema file not found at: {self.path}", file=sys.stderr)
        except Exception as e:
            print(f"  [Error] Failed to parse schema file: {e}", file=sys.stderr)

    def validate(self, card_data: Dict[str, Any]) -> List[str]:
        """
        Validates a single card's data against the loaded schema.

        This function serves as the "Card Data Linter" required by AGENTS.md.

        Args:
            card_data: The dictionary of card data to validate.

        Returns:
            A list of error strings. An empty list means the card is valid.
        """
        errors = []
        card_id = card_data.get("id", "UNKNOWN")

        # Rule 1: Check for mandatory top-level keys.
        required_keys = {"id", "name", "type"}
        for key in required_keys:
            if key not in card_data:
                errors.append(f"Missing required top-level key: '{key}'")

        # Rule 2: Recursively find and validate all action objects.
        self._validate_actions_recursively(card_data, card_id, errors)

        return errors

    def _validate_actions_recursively(
        self, data: Any, card_id: str, errors: List[str], path: str = ""
    ):
        """Helper to traverse the data and validate 'actions' arrays."""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if key == "actions" and isinstance(value, list):
                    for i, action_obj in enumerate(value):
                        action_path = f"{new_path}[{i}]"
                        if not isinstance(action_obj, dict):
                            errors.append(f"Action at '{action_path}' is not a dictionary.")
                            continue
                        action_name = action_obj.get("action")
                        if not action_name:
                            errors.append(f"Action at '{action_path}' is missing the 'action' key.")
                        elif action_name not in self.actions:
                            errors.append(
                                f"Action '{action_name}' at '{action_path}' is not a valid action "
                                f"defined in {self.path.name}."
                            )
                else:
                    self._validate_actions_recursively(value, card_id, errors, new_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._validate_actions_recursively(item, card_id, errors, f"{path}[{i}]")


# --- 3. Markdown Parsing & Data Extraction ---

def find_json_blocks(content: str) -> Iterator[Tuple[str, int]]:
    """
    Finds all ```json ... ``` blocks in a string and yields them with their line numbers.

    Args:
        content: The string content of the file.

    Yields:
        A tuple containing the JSON string and its starting line number.
    """
    # Using re.finditer to get match objects which contain position info.
    for match in re.finditer(r"```json\n(.*?)\n```", content, re.DOTALL):
        json_block = match.group(1)
        # Calculate the line number of the start of the block.
        line_number = content.count("\n", 0, match.start()) + 1
        yield json_block, line_number


def parse_markdown_file(filepath: Path) -> Iterator[Tuple[Dict[str, Any], str, int]]:
    """
    Parses a markdown file to extract JSON data blocks.

    Args:
        filepath: The path to the markdown file.

    Yields:
        A tuple of (parsed_json, filename, line_number).
    """
    print(f"\nParsing source file: {filepath.name}...")
    try:
        content = filepath.read_text(encoding="utf-8")
        for block, line_num in find_json_blocks(content):
            try:
                yield json.loads(block), filepath.name, line_num
            except json.JSONDecodeError as e:
                print(
                    f"  [Warning] Skipping invalid JSON block in {filepath.name} "
                    f"near line {line_num}: {e}",
                    file=sys.stderr,
                )
                print(f"  > Block content: {block[:120]}...", file=sys.stderr)
    except FileNotFoundError:
        print(f"  [Error] Source file not found: {filepath}", file=sys.stderr)
    except Exception as e:
        print(f"  [Error] An unexpected error occurred while parsing {filepath}: {e}", file=sys.stderr)


# --- 4. File Generation ---

def generate_card_files(cards: List[Dict[str, Any]], base_output_path: Path):
    """
    Generates individual .json files for each card in the appropriate subdirectory.

    Args:
        cards: A list of validated card data dictionaries.
        base_output_path: The root directory for all generated card files.
    """
    generated_count = 0
    print(f"\nGenerating {len(cards)} valid card files...")

    for card in cards:
        card_type = card["type"]
        card_id = card["id"]

        # Determine the correct subdirectory based on the card type.
        if card_type in STATE_CARD_TYPES:
            # Pluralization for state cards is specific.
            subfolder_name = "celestial" if card_type == "celestial" else f"{card_type}s"
            output_path = base_output_path / "state" / subfolder_name
        else:
            # Other cards are directly in a folder named by their type.
            output_path = base_output_path / card_type

        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / f"{card_id}.json"

        try:
            with file_path.open("w", encoding="utf-8") as f:
                # Use indent=2 for readability, ensure_ascii=False for Chinese chars.
                json.dump(card, f, ensure_ascii=False, indent=2)
            generated_count += 1
        except IOError as e:
            print(f"  [Error] Failed to write file {file_path}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  [Error] An unexpected error occurred writing {file_path}: {e}", file=sys.stderr)

    print(f"  Successfully generated {generated_count} files.")


# --- 5. Main Execution ---

def main():
    """Main function to orchestrate the card data generation process."""
    print("--- Starting Card Data Generation (v2.0) ---")

    # 1. Load the schema first, as it's required for validation.
    schema = CardSchema(DEFAULT_SCHEMA_PATH)
    if not schema.actions:
        print("\nCould not load schema definitions. Aborting.", file=sys.stderr)
        sys.exit(1)

    # 2. Parse all source files to get raw card data.
    all_parsed_cards = []
    for file_path in INPUT_FILES:
        if not file_path.exists():
            print(f"\n[Warning] Input file not found, skipping: {file_path}", file=sys.stderr)
            continue
        all_parsed_cards.extend(parse_markdown_file(file_path))

    if not all_parsed_cards:
        print("\nNo card data found in any source file. Exiting.", file=sys.stderr)
        return

    # 3. Validate cards and collect valid ones.
    valid_cards = []
    total_cards = len(all_parsed_cards)
    print(f"\nFound {total_cards} card definitions. Validating against schema...")

    for card_data, filename, line_num in all_parsed_cards:
        card_id = card_data.get("id", "UNKNOWN")
        errors = schema.validate(card_data)
        if errors:
            print(
                f"  [Validation Error] Card '{card_id}' from {filename} (line {line_num}) is invalid:",
                file=sys.stderr,
            )
            for error in errors:
                print(f"    - {error}", file=sys.stderr)
        else:
            valid_cards.append(card_data)

    print(f"  Validation complete. {len(valid_cards)} / {total_cards} cards are valid.")

    # 4. Generate files for the valid cards.
    if valid_cards:
        generate_card_files(valid_cards, OUTPUT_DIR)
    else:
        print("\nNo valid cards to generate.")

    # 5. Final summary.
    print("\n--- Card Data Generation Complete ---")
    print(f"Output directory: {OUTPUT_DIR}")
    if len(valid_cards) < total_cards:
        print(f"Warning: {total_cards - len(valid_cards)} cards failed validation and were not generated.")
        sys.exit(1) # Exit with an error code if some cards failed validation


if __name__ == "__main__":
    main()