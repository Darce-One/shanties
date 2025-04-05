#!/usr/bin/env python3
"""
main.py

This script walks through a dataset folder, finds all MIDI files,
and processes each file with the feature extractors.
It adheres to SOLID design principles.
"""

import os
import sys
import argparse
import logging
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
                if instr.instrumentName is not None and "voice" in instr.instrumentName.lower():
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


def main():
    parser = argparse.ArgumentParser(
        description="Walk through a folder with MIDI files and analyze musical features."
    )
    parser.add_argument("dataset", help="Path to dataset folder containing MIDI files.")
    args = parser.parse_args()

    midi_files = find_midi_files(args.dataset)
    if not midi_files:
        print("No MIDI files found in the provided dataset directory.")
        sys.exit(0)

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

    # Process each MIDI file.
    for midi_file in midi_files:
        print("=" * 40)
        print("Processing file:", midi_file)
        features = analyze_midi_file(midi_file, extractors)
        if features is None:
            print("Skipping file due to parse error.\n")
            continue

        print("Extracted Features:")
        for feature_name, value in features.items():
            print(f"{feature_name}: {value}")
        print("\n")


if __name__ == "__main__":
    main()
