#!/usr/bin/env python3
"""
main.py

This script walks through a dataset folder, finds all MIDI files,
processes each file with the feature extractors, and classifies them by shanty type.
It saves the results to JSON and CSV files for further analysis.
It adheres to SOLID design principles.
"""

import os
import sys
import json
import csv
import argparse
import logging
from datetime import datetime
import music21
from feature_extractors import (
    PitchRangeExtractor,
    AverageIntervalExtractor,
    IntervalComplexityExtractor,
    LeapFrequencyExtractor,
    ContourDirectionalityExtractor,
    MelodicContourComplexityExtractor,
    AverageNoteDurationExtractor,
    RhythmComplexityExtractor,
    SyncopationExtractor,
    NoteCountPerBarExtractor,
    NoteCountPerBarVariabilityExtractor,
    RestFrequencyExtractor,
    ScoreLengthInBarsExtractor,
    MelodicPatternRepetitionExtractor,
    RhythmicPatternRepetitionExtractor,
    EntropyOfPitchSequenceExtractor,
    VarianceInNoteDensityExtractor,
    extract_all_features,
)
from bs4 import BeautifulSoup
import re


def find_midi_files(dataset_dir):
    """
    Recursively finds all MIDI files in the provided dataset directory.

    Returns:
        list of str: Paths of all found MIDI (.mid or .midi) files.
    """
    midi_files = []
    for root, _, files in os.walk(dataset_dir):
        for fname in files:
            if fname.lower().endswith((".mid", ".midi")):
                midi_files.append(os.path.join(root, fname))
    return midi_files


def select_score_for_analysis(score):
    """
    Given a music21 score, chooses the best score for analyzing melodic features.
    If voice parts are present, return the first recognized voice part.
    Otherwise, return the entire score or the first part.

    Args:
        score (music21.stream.Score): The parsed music score.

    Returns:
        music21.stream.Score or Part: The portion of the score to analyze.
    """
    if hasattr(score, "parts") and score.parts:
        voice_part = None
        # Loop over parts to look for a vocalist or voice indication.
        for part in score.parts:
            instruments = part.getInstruments(returnDefault=True)
            for instr in instruments:
                # Check if instrumentName exists and is a string
                if (
                    instr.instrumentName is not None
                    and "voice" in instr.instrumentName.lower()
                ):
                    voice_part = part
                    break
                # You can also check for Vocalist type explicitly
                elif isinstance(instr, music21.instrument.Vocalist):
                    voice_part = part
                    break
            if voice_part:
                break
        if voice_part:
            return voice_part
        else:
            return score.parts[0]
    return score


def analyze_midi_file(midi_path, extractors):
    """
    Parses the MIDI file and extracts musical features using the provided extractors.

    Args:
        midi_path (str): Path to a MIDI file.
        extractors (list): List of instantiated feature extractors.

    Returns:
        dict or None: Dictionary of feature names and values or None if error occurred.
    """

    try:
        score = music21.converter.parse(midi_path)
    except Exception as e:
        logging.error("Failed to parse MIDI file %s: %s", midi_path, e)
        return None

    score_for_analysis = select_score_for_analysis(score)
    features = extract_all_features(score_for_analysis, extractors)
    return features


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
            # Clean up the type name - remove "SHANTIES", "SHANTY", "&" and ":" and trim
            current_type = text.replace(':', '').strip()
            current_type = re.sub(r'(?i)SHANTIES|SHANTY', '', current_type).strip()
            current_type = re.sub(r'\s*&\s*', ' ', current_type).strip()
            
            # Remove any trailing or leading whitespace or punctuation
            current_type = current_type.strip('., ')
            
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


def map_shanties_to_midi_files(shanty_types, midi_files):
    """
    Map shanty names to MIDI files in the dataset.
    
    Args:
        shanty_types (dict): Dictionary mapping shanty names to their types
        midi_files (list): List of MIDI file paths
        
    Returns:
        dict: A dictionary mapping MIDI filenames to shanty types
    """
    midi_to_type = {}
    
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
    for midi_path in midi_files:
        midi_file = os.path.basename(midi_path)
        
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
                midi_to_type[midi_path] = {
                    'shanty_name': info['original_name'],
                    'shanty_type': info['type'],
                    'shanty_number': info['number']
                }
                matched = True
                logging.info(f"Matched {midi_file} to {info['original_name']} ({info['type']})")
                break
        
        if not matched:
            logging.warning(f"Could not match {midi_file} to any shanty in the index")
            # Still add the file to the dictionary, but with unknown type
            midi_to_type[midi_path] = {
                'shanty_name': 'Unknown',
                'shanty_type': 'Unknown',
                'shanty_number': 'N/A'
            }
    
    return midi_to_type


def save_to_json(analysis_results, output_path):
    """
    Saves the analysis results to a JSON file.

    Args:
        analysis_results (list): List of dictionaries with filename and features.
        output_path (str): Path to save the JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2)
    print(f"JSON data saved to {output_path}")


def save_to_csv(analysis_results, output_path):
    """
    Saves the analysis results to a CSV file.

    Args:
        analysis_results (list): List of dictionaries with filename and features.
        output_path (str): Path to save the CSV file.
    """
    if not analysis_results:
        print("No data to save to CSV.")
        return

    # Collect all unique feature names across all results
    all_feature_names = set()
    successful_analyses = 0
    
    for result in analysis_results:
        if result["features"]:
            all_feature_names.update(result["features"].keys())
            successful_analyses += 1
    
    if successful_analyses == 0:
        print("No successful feature extractions found. Cannot create CSV.")
        return
    
    # Create fieldnames with filename, directory, shanty type info first, then all feature names alphabetically
    fieldnames = ["filename", "directory", "shanty_name", "shanty_type", "shanty_number"] + sorted(list(all_feature_names))

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in analysis_results:
            if result["features"] is None:
                continue
                
            row = {
                "filename": result["filename"],
                "directory": result["directory"],
                "shanty_name": result.get("shanty_name", "Unknown"),
                "shanty_type": result.get("shanty_type", "Unknown"),
                "shanty_number": result.get("shanty_number", "N/A")
            }
            # Add the features to the row
            row.update(result["features"])
            writer.writerow(row)
    
    print(f"CSV data saved to {output_path} with {len(all_feature_names)} features from {successful_analyses} files")


def convert_to_snake_case(name):
    """
    Convert a CamelCase string to snake_case and remove 'Extractor' suffix.
    
    Args:
        name (str): The name to convert
        
    Returns:
        str: The converted name
    """
    # Remove 'Extractor' suffix if present
    if name.endswith('Extractor'):
        name = name[:-9]  # Remove 'Extractor'
    
    # Convert CamelCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def main():
    parser = argparse.ArgumentParser(
        description="Walk through a folder with MIDI files, analyze musical features, and classify shanties by type."
    )
    parser.add_argument("dataset", help="Path to dataset folder containing MIDI files.")
    parser.add_argument("--html-file", help="Path to the shanty book HTML file for classification.", required=True)
    parser.add_argument("--output-dir", 
                      help="Directory to save output files. Defaults to 'results'.",
                      default="results")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_output = os.path.join(args.output_dir, f"sea_shanties_analysis_{timestamp}.json")
    csv_output = os.path.join(args.output_dir, f"sea_shanties_analysis_{timestamp}.csv")

    midi_files = find_midi_files(args.dataset)
    if not midi_files:
        print("No MIDI files found in the provided dataset directory.")
        sys.exit(0)

    print(f"Found {len(midi_files)} MIDI files for analysis.")

    # Create the list of extractors. This list is open for extension (Open/Closed Principle)
    # without modifying the analysis functions.
    extractors = [
        PitchRangeExtractor(),
        AverageIntervalExtractor(),
        IntervalComplexityExtractor(),
        LeapFrequencyExtractor(),
        ContourDirectionalityExtractor(),
        MelodicContourComplexityExtractor(),
        AverageNoteDurationExtractor(),
        RhythmComplexityExtractor(),
        SyncopationExtractor(),
        NoteCountPerBarExtractor(),
        NoteCountPerBarVariabilityExtractor(),
        RestFrequencyExtractor(),
        ScoreLengthInBarsExtractor(),
        MelodicPatternRepetitionExtractor(),
        RhythmicPatternRepetitionExtractor(),
        EntropyOfPitchSequenceExtractor(),
        VarianceInNoteDensityExtractor(),
    ]

    # Parse HTML and extract shanty types
    print(f"Parsing HTML file: {args.html_file}")
    shanty_types = parse_html_for_shanty_types(args.html_file)
    
    # Map shanties to MIDI files
    print(f"Classifying shanties by type...")
    midi_to_type_map = map_shanties_to_midi_files(shanty_types, midi_files)

    # Store all analysis results
    all_results = []

    # Process each MIDI file.
    for midi_file in midi_files:
        print("=" * 40)
        print("Processing file:", midi_file)
        
        features = analyze_midi_file(midi_file, extractors)
        
        # Get the relative directory path
        rel_dir = os.path.dirname(os.path.relpath(midi_file, args.dataset))
        filename = os.path.basename(midi_file)
        
        # Get shanty type information
        shanty_info = midi_to_type_map.get(midi_file, {
            'shanty_name': 'Unknown',
            'shanty_type': 'Unknown',
            'shanty_number': 'N/A'
        })
        
        # Convert feature names to snake_case and remove 'Extractor' suffix
        converted_features = None
        if features:
            converted_features = {
                convert_to_snake_case(name): value 
                for name, value in features.items()
            }
        
        result = {
            "filename": filename,
            "directory": rel_dir,
            "shanty_name": shanty_info['shanty_name'],
            "shanty_type": shanty_info['shanty_type'],
            "shanty_number": shanty_info['shanty_number'],
            "features": converted_features
        }
        
        all_results.append(result)
        
        if features is None:
            print("Skipping file due to parse error.\n")
            continue

        # # Still print for console feedback
        # print("Extracted Features:")
        # if converted_features:
        #     for feature_name, value in converted_features.items():
        #         print(f"{feature_name}: {value}")
        # print(f"Shanty Type: {shanty_info['shanty_type']}")
        # print(f"Shanty Name: {shanty_info['shanty_name']}")
        # print("\n")

    # Save results to files
    save_to_json(all_results, json_output)
    save_to_csv(all_results, csv_output)
    
    print(f"Analysis complete. Processed {len(midi_files)} files.")
    print(f"Results saved to {json_output} and {csv_output}")


if __name__ == "__main__":
    main()