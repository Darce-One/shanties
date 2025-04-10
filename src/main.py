#!/usr/bin/env python3
"""
main.py

This script walks through a dataset folder, finds all MIDI files,
processes each file with the feature extractors, and saves the results
to JSON and CSV files for further analysis.
It adheres to SOLID design principles.
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime

import music21

from feature_extractors import (
    AverageIntervalExtractor,
    AverageNoteDurationExtractor,
    ContourDirectionalityExtractor,
    EntropyOfPitchSequenceExtractor,
    IntervalComplexityExtractor,
    LeapFrequencyExtractor,
    MelodicContourComplexityExtractor,
    MelodicPatternRepetitionExtractor,
    NoteCountPerBarExtractor,
    NoteCountPerBarVariabilityExtractor,
    PitchRangeExtractor,
    RestFrequencyExtractor,
    RhythmComplexityExtractor,
    RhythmicPatternRepetitionExtractor,
    ScoreLengthInBarsExtractor,
    SyncopationExtractor,
    VarianceInNoteDensityExtractor,
    extract_all_features,
)


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


def save_to_json(analysis_results, output_path):
    """
    Saves the analysis results to a JSON file.

    Args:
        analysis_results (list): List of dictionaries with filename and features.
        output_path (str): Path to save the JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
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

    # Create fieldnames with filename and directory first, then all feature names alphabetically
    fieldnames = ["filename", "directory"] + sorted(list(all_feature_names))

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for result in analysis_results:
            if result["features"] is None:
                continue

            row = {"filename": result["filename"], "directory": result["directory"]}
            row.update(result["features"])
            writer.writerow(row)

    print(
        f"CSV data saved to {output_path} with {len(all_feature_names)} features from {successful_analyses} files"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Walk through a folder with MIDI files and analyze musical features."
    )
    parser.add_argument("dataset", help="Path to dataset folder containing MIDI files.")
    parser.add_argument(
        "--output-dir",
        help="Directory to save output files. Defaults to 'results'.",
        default="results",
    )
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_output = os.path.join(
        args.output_dir, f"sea_shanties_analysis_{timestamp}.json"
    )
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

        result = {"filename": filename, "directory": rel_dir, "features": features}

        all_results.append(result)

        if features is None:
            print("Skipping file due to parse error.\n")
            continue

        # print("Extracted Features:")
        # for feature_name, value in features.items():
        #     print(f"{feature_name}: {value}")
        # print("\n")

    # Save results to files
    save_to_json(all_results, json_output)
    save_to_csv(all_results, csv_output)

    print(f"Analysis complete. Processed {len(midi_files)} files.")
    print(f"Results saved to {json_output} and {csv_output}")


if __name__ == "__main__":
    main()
