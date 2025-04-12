#!/usr/bin/env python3
"""
shanty_type_classifier.py

This script parses the HTML index of "The Shanty Book, Part I" to extract
the types of shanties, then matches them with MIDI files in the dataset.
It produces a CSV and JSON file with shanty types that can be used for
further analysis.

Usage:
    python shanty_type_classifier.py --html-file <path_to_html> --output-dir <output_directory>
"""

import os
import re
import json
import csv
import argparse
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_html_for_shanty_types(html_file):
    """
    Parse the HTML file to extract shanty names and their types.
    
    Args:
        html_file (str): Path to the HTML file
        
    Returns:
        dict: A dictionary mapping shanty names to their types
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    shanty_types = {}
    current_type = None
    
    # Find all h3 headings which contain shanty type information
    for heading in soup.find_all('h3'):
        text = heading.get_text().strip()
        
        # Check if this is a shanty type heading
        if any(keyword in text.lower() for keyword in ['shanties', 'shanty']):
            # Clean up the type name
            current_type = text.replace(':', '').strip()
            logging.info(f"Found shanty type: {current_type}")
            
            # Get the table that follows this heading
            table = heading.find_next('table')
            if table:
                # Extract shanty names from the table
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if cells and len(cells) >= 1:
                        # Extract the shanty name
                        link = cells[0].find('a')
                        if link:
                            shanty_number = cells[0].get_text().strip().split()[0]
                            shanty_name = link.get_text().strip()
                            shanty_types[shanty_name] = {
                                'type': current_type,
                                'number': shanty_number
                            }
                            logging.info(f"  - {shanty_number}: {shanty_name}")
    
    return shanty_types

def map_shanties_to_midi_files(shanty_types, music_dir):
    """
    Map shanty names to MIDI files in the dataset.
    
    Args:
        shanty_types (dict): Dictionary mapping shanty names to their types
        music_dir (str): Directory containing MIDI files
        
    Returns:
        dict: A dictionary mapping MIDI filenames to shanty types
    """
    midi_to_type = {}
    
    # Get all MIDI files in the directory
    midi_files = [f for f in os.listdir(music_dir) if f.endswith(('.midi', '.mid'))]
    
    # Create a dictionary for fuzzy matching
    fuzzy_map = {}
    for shanty_name, info in shanty_types.items():
        # Convert shanty name to lowercase and remove special characters for matching
        simple_name = re.sub(r'[^\w\s]', '', shanty_name.lower())
        simple_name = re.sub(r'\s+', ' ', simple_name).strip()
        fuzzy_map[simple_name] = {
            'original_name': shanty_name,
            'type': info['type'],
            'number': info['number']
        }
    
    # Match MIDI files to shanty types
    for midi_file in midi_files:
        # Skip music files that don't correspond to shanties (e.g., music01.midi)
        if midi_file.startswith('music') and midi_file[5].isdigit():
            continue
            
        # Get the base name without extension
        base_name = os.path.splitext(midi_file)[0]
        
        # Remove leading numbers (e.g., 01billy -> billy)
        base_name_without_number = re.sub(r'^[0-9]+', '', base_name)
        
        # Try to match with shanty names
        matched = False
        for simple_name, info in fuzzy_map.items():
            # Check if the base name is contained in the simple name or vice versa
            if base_name_without_number in simple_name or simple_name in base_name_without_number:
                midi_to_type[midi_file] = {
                    'shanty_name': info['original_name'],
                    'shanty_type': info['type'],
                    'shanty_number': info['number']
                }
                matched = True
                logging.info(f"Matched {midi_file} to {info['original_name']} ({info['type']})")
                break
        
        if not matched:
            logging.warning(f"Could not match {midi_file} to any shanty in the index")
    
    return midi_to_type

def save_to_json(midi_to_type, output_file):
    """
    Save the MIDI to shanty type mapping to a JSON file.
    
    Args:
        midi_to_type (dict): Dictionary mapping MIDI filenames to shanty types
        output_file (str): Path to the output JSON file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(midi_to_type, f, indent=2)
    logging.info(f"Saved shanty type data to {output_file}")

def save_to_csv(midi_to_type, output_file):
    """
    Save the MIDI to shanty type mapping to a CSV file.
    
    Args:
        midi_to_type (dict): Dictionary mapping MIDI filenames to shanty types
        output_file (str): Path to the output CSV file
    """
    fieldnames = ['midi_file', 'shanty_name', 'shanty_type', 'shanty_number']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for midi_file, info in midi_to_type.items():
            writer.writerow({
                'midi_file': midi_file,
                'shanty_name': info['shanty_name'],
                'shanty_type': info['shanty_type'],
                'shanty_number': info['shanty_number']
            })
    
    logging.info(f"Saved shanty type data to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Parse HTML index to extract shanty types and match with MIDI files."
    )
    parser.add_argument('--html-file', help='Path to the HTML index file', required=True)
    parser.add_argument('--music-dir', help='Directory containing MIDI files', default='data/shanty_book/music')
    parser.add_argument('--output-dir', help='Directory to save output files', default='results')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set up output file paths
    json_output = os.path.join(args.output_dir, 'shanty_types.json')
    csv_output = os.path.join(args.output_dir, 'shanty_types.csv')
    
    # Parse HTML and extract shanty types
    logging.info(f"Parsing HTML file: {args.html_file}")
    shanty_types = parse_html_for_shanty_types(args.html_file)
    
    # Map shanties to MIDI files
    logging.info(f"Mapping shanties to MIDI files in: {args.music_dir}")
    midi_to_type = map_shanties_to_midi_files(shanty_types, args.music_dir)
    
    # Save results
    save_to_json(midi_to_type, json_output)
    save_to_csv(midi_to_type, csv_output)
    
    logging.info("Classification complete!")
    logging.info(f"Results saved to {json_output} and {csv_output}")
    
if __name__ == "__main__":
    main()
