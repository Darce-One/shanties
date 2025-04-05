#!/usr/bin/env python3
"""
Feature Extractors for Sea Shanties Analysis Project

Each feature extractor implements a common interface: extract(score).
The score is a music21 stream (or score) and the extract method
computes a normalized feature (between 0 and 1) for that score.
"""

from abc import ABC, abstractmethod
import math
import statistics
import music21


# ============================================================
# Base FeatureExtractor class
# ============================================================
class FeatureExtractor(ABC):
    """
    Abstract base class for a feature extractor.

    Child classes must implement the extract() method.
    """

    @abstractmethod
    def extract(self, score):
        """
        Extract the feature from the music21 stream (score).

        Args:
            score (music21.stream.Score): A music score.

        Returns:
            float: The computed feature.
        """
        raise NotImplementedError("Subclasses must implement this method")


# ============================================================
# Pitch and Interval Features
# ============================================================


class PitchRangeExtractor(FeatureExtractor):
    """
    Computes the pitch range as the difference between the highest and lowest pitches.
    Returns the range in MIDI numbers.
    """

    def extract(self, score):
        pitch_values = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitch_values.append(n.pitch.midi)
        if not pitch_values:
            return 0.0
        range_val = max(pitch_values) - min(pitch_values)
        return range_val


class AverageIntervalExtractor(FeatureExtractor):
    """
    Calculates the average absolute interval (in semitones) between consecutive notes.
    """

    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitches.append(n.pitch.midi)
        if len(pitches) < 2:
            return 0.0
        intervals = [abs(b - a) for a, b in zip(pitches[:-1], pitches[1:])]
        avg_interval = statistics.mean(intervals)
        return avg_interval


class IntervalComplexityExtractor(FeatureExtractor):
    """
    Quantifies the diversity of intervals using Shannon entropy (in bits).
    """

    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitches.append(n.pitch.midi)
        if len(pitches) < 2:
            return 0.0
        intervals = [abs(b - a) for a, b in zip(pitches[:-1], pitches[1:])]
        if not intervals:
            return 0.0
        # Frequency distribution of intervals
        unique_intervals = {}
        for iv in intervals:
            unique_intervals[iv] = unique_intervals.get(iv, 0) + 1
        total = len(intervals)
        entropy = 0.0
        for count in unique_intervals.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy


class LeapFrequencyExtractor(FeatureExtractor):
    """
    Computes the leap frequency: the proportion of intervals that are larger than a step (defined here as >2 semitones).
    This feature is inherently a ratio between 0 and 1.
    """

    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitches.append(n.pitch.midi)
        if len(pitches) < 2:
            return 0.0
        leaps = [1 for a, b in zip(pitches[:-1], pitches[1:]) if abs(b - a) > 2]
        frequency = sum(leaps) / (len(pitches) - 1)
        return frequency


class ContourDirectionalityExtractor(FeatureExtractor):
    """
    Measures directional movement by returning the ratio of upward intervals.
    This ratio is inherently between 0 and 1.
    """

    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitches.append(n.pitch.midi)
        if len(pitches) < 2:
            return 0.0
        upward = 0
        total = 0
        for a, b in zip(pitches[:-1], pitches[1:]):
            if b != a:
                total += 1
                if b > a:
                    upward += 1
        ratio = upward / total if total > 0 else 0.0
        return ratio


class MelodicContourComplexityExtractor(FeatureExtractor):
    """
    Computes the complexity of the melodic contour by counting the number of directional changes.
    The value is normalized by the total number of intervals minus one (the maximum possible number of changes).
    """

    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, "pitch"):
                pitches.append(n.pitch.midi)
        if len(pitches) < 3:
            return 0.0
        # Determine direction: +1 for upward, -1 for downward, 0 for no change
        directions = []
        for a, b in zip(pitches[:-1], pitches[1:]):
            if b > a:
                directions.append(1)
            elif b < a:
                directions.append(-1)
            else:
                directions.append(0)
        # Count directional changes (ignoring no-change segments)
        filtered = [d for d in directions if d != 0]
        changes = 0
        for a, b in zip(filtered[:-1], filtered[1:]):
            if a != b:
                changes += 1
        # Normalize changes by the maximum possible changes (total intervals - 1)
        total_intervals = len(pitches) - 1
        if total_intervals <= 0:
            return 0.0

        normalized_changes = changes / total_intervals
        return normalized_changes


# ============================================================
# Rhythmic and Duration Features
# ============================================================


class AverageNoteDurationExtractor(FeatureExtractor):
    """
    Computes the average note duration (using quarterLength values)
    and returns it in quarter length units.
    """

    def extract(self, score):
        durations = []
        for n in score.recurse().notes:
            durations.append(n.quarterLength)
        if not durations:
            return 0.0
        avg_duration = statistics.mean(durations)
        return avg_duration


class RhythmComplexityExtractor(FeatureExtractor):
    """
    Measures the complexity of rhythms by computing the entropy of note durations (in bits).
    """

    def extract(self, score):
        durations = [n.quarterLength for n in score.recurse().notes]
        if not durations:
            return 0.0
        unique_durations = {}
        for d in durations:
            unique_durations[d] = unique_durations.get(d, 0) + 1
        total = len(durations)
        entropy = 0.0
        for count in unique_durations.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy


class SyncopationExtractor(FeatureExtractor):
    """
    Computes a simple syncopation score by counting note onsets that are off the beat.
    Here we assume the downbeats occur at integer offsets (for example, in 4/4 time).
    Returns the ratio of syncopated note onsets to total note onsets.
    """

    def extract(self, score):
        note_count = 0
        syncopated = 0
        for n in score.recurse().notes:
            offset = n.offset
            note_count += 1
            if not math.isclose(offset % 1, 0.0, abs_tol=1e-5):
                syncopated += 1
        if note_count == 0:
            return 0.0
        ratio = syncopated / note_count
        return ratio


class NoteCountPerBarExtractor(FeatureExtractor):
    """
    Calculates the average number of note onsets per measure.
    """

    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        note_counts = []
        for m in measures:
            count = len(list(m.flatten().notes))
            note_counts.append(count)
        if not note_counts:
            return 0.0
        avg_notes = statistics.mean(note_counts)
        return avg_notes


class NoteCountPerBarVariabilityExtractor(FeatureExtractor):
    """
    Computes the variance of the note counts per measure across the score.
    Returns the raw variance.
    """

    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        note_counts = [
            len(list(m.flatten().notes)) for m in measures if m.flatten().notes
        ]
        if len(note_counts) < 2:
            return 0.0
        var_notes = statistics.variance(note_counts)
        return var_notes


class RestFrequencyExtractor(FeatureExtractor):
    """
    Computes the frequency of rests relative to notes.
    Returns the ratio of the number of rests to the total count of rests and notes.
    """

    def extract(self, score):
        note_count = 0
        rest_count = 0
        for elem in score.recurse().notesAndRests:
            if isinstance(elem, music21.note.Note):
                note_count += 1
            elif isinstance(elem, music21.note.Rest):
                rest_count += 1
        total = note_count + rest_count
        if total == 0:
            return 0.0
        freq = rest_count / total
        return freq


# ============================================================
# Structural and Statistical Complexity Features
# ============================================================


class ScoreLengthInBarsExtractor(FeatureExtractor):
    """
    Counts the total number of measures (bars) in the score.
    Returns the raw count of bars.
    """

    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        bar_count = len(measures)
        return bar_count


class MelodicPatternRepetitionExtractor(FeatureExtractor):
    """
    A simplified extractor for melodic pattern repetition.
    This implementation converts the melody into a string of pitch numbers (separated by spaces)
    and counts how often n-grams (with n=3) are repeated. It returns a ratio of repetition,
    which is inherently between 0 and 1.
    """

    def extract(self, score):
        pitches = [
            str(n.pitch.midi) for n in score.recurse().notes if hasattr(n, "pitch")
        ]
        n = 3
        if len(pitches) < n:
            return 0.0
        ngrams = [" ".join(pitches[i : i + n]) for i in range(len(pitches) - n + 1)]
        unique = set(ngrams)
        total = len(ngrams)
        repetition = 1 - (len(unique) / total)
        return repetition


class RhythmicPatternRepetitionExtractor(FeatureExtractor):
    """
    A simple extractor to measure rhythmic pattern repetition.
    It extracts a sequence of note durations, creates n-grams (n=3),
    and returns a repetition ratio (between 0 and 1).
    """

    def extract(self, score):
        durations = [str(n.quarterLength) for n in score.recurse().notes]
        n = 3
        if len(durations) < n:
            return 0.0
        ngrams = [" ".join(durations[i : i + n]) for i in range(len(durations) - n + 1)]
        unique = set(ngrams)
        total = len(ngrams)
        repetition = 1 - (len(unique) / total)
        return repetition


class EntropyOfPitchSequenceExtractor(FeatureExtractor):
    """
    Uses Shannon entropy to measure unpredictability in the sequence of pitches (in bits).
    """

    def extract(self, score):
        pitches = [n.pitch.midi for n in score.recurse().notes if hasattr(n, "pitch")]
        if not pitches:
            return 0.0
        unique = {}
        for p in pitches:
            unique[p] = unique.get(p, 0) + 1
        total = len(pitches)
        entropy = 0.0
        for count in unique.values():
            p_val = count / total
            entropy -= p_val * math.log2(p_val)
        return entropy


class VarianceInNoteDensityExtractor(FeatureExtractor):
    """
    Measures changes in note density (number of note onsets) across measures
    by returning the variance of note counts per measure.
    """

    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        counts = []
        for m in measures:
            counts.append(len(list(m.flatten().notes)))
        if len(counts) < 2:
            return 0.0
        var_value = statistics.variance(counts)
        return var_value


# ============================================================
# Example usage
# ============================================================
def extract_all_features(score, extractors):
    """
    Given a music21 score and a list of extractor instances,
    returns a dictionary of feature names and their values.

    Args:
        score (music21.stream.Score): The musical score.
        extractors (list of FeatureExtractor): A list of feature extractors.

    Returns:
        dict: Mapping from extractor class name to extracted value.
    """
    features = {}
    for extractor in extractors:
        feature_value = extractor.extract(score)
        features[extractor.__class__.__name__] = feature_value
    return features


if __name__ == "__main__":
    import sys
    import music21

    if len(sys.argv) < 2:
        print("Usage: python feature_extractors.py <path_to_midi_file>")
        sys.exit(1)
    midi_path = sys.argv[1]
    score = music21.converter.parse(midi_path)

    # Print the score structure (for debugging)
    score.show("text")
    print("\n")

    # Check if the score has parts.
    if hasattr(score, "parts") and score.parts:
        voice_part = None
        for part in score.parts:
            instruments = part.getInstruments(returnDefault=True)
            for instr in instruments:
                if (
                    isinstance(instr, music21.instrument.Vocalist)
                    or "voice" in instr.instrumentName.lower()
                ):
                    voice_part = part
                    break
            if voice_part:
                break
        if voice_part:
            score_for_analysis = voice_part
        else:
            score_for_analysis = score.parts[0]
    else:
        score_for_analysis = score

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
    features = extract_all_features(score_for_analysis, extractors)
    for feature_name, value in features.items():
        print(f"{feature_name}: {value}")
