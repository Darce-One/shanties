#!/usr/bin/env python3
"""
Feature Extractors for Sea Shanties Analysis Project

Each feature extractor implements a common interface: extract(score).
The score is a music21 stream (or score) and the extract method
computes a normalized feature (between 0 and 1) for that score.
"""

from abc import ABC, abstractmethod
import math
import numpy as np
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
            float: A normalized feature value between 0 and 1.
        """
        raise NotImplementedError("Subclasses must implement this method")


# ============================================================
# Pitch and Interval Features
# ============================================================

class PitchRangeExtractor(FeatureExtractor):
    """
    Computes the pitch range as the difference between the highest and lowest pitches.
    The result is normalized by dividing the observed range by two octaves (24).
    """
    def extract(self, score):
        # List to hold MIDI pitch numbers
        pitch_values = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
                pitch_values.append(n.pitch.midi)

        if not pitch_values:
            return 0.0
        range_val = max(pitch_values) - min(pitch_values)
        # Normalize by dividing by 2 octaves (24)
        normalized_range = range_val / 24.0
        return min(max(normalized_range, 0.0), 1.0)


class AverageIntervalExtractor(FeatureExtractor):
    """
    Calculates the average absolute interval between consecutive notes.
    The value is normalized by assuming the maximum interval is 127.
    """
    def extract(self, score):
        # Extract note MIDI numbers in order
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
                pitches.append(n.pitch.midi)

        if len(pitches) < 2:
            return 0.0

        intervals = [abs(b - a) for a, b in zip(pitches[:-1], pitches[1:])]
        avg_interval = statistics.mean(intervals)
        normalized_avg = avg_interval / 127.0
        return min(max(normalized_avg, 0.0), 1.0)


class IntervalComplexityExtractor(FeatureExtractor):
    """
    Quantifies the diversity of intervals using Shannon entropy.
    The extraction calculates the distribution (frequency) of interval sizes
    and normalizes the entropy by the maximum possible value (log2(number of unique intervals)).
    """
    def extract(self, score):
        # Extract note MIDI numbers in order
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
                pitches.append(n.pitch.midi)

        if len(pitches) < 2:
            return 0.0

        intervals = [abs(b - a) for a, b in zip(pitches[:-1], pitches[1:])]
        if not intervals:
            return 0.0

        # Calculate frequency distribution
        unique_intervals = {}
        for iv in intervals:
            unique_intervals[iv] = unique_intervals.get(iv, 0) + 1
        total = len(intervals)

        entropy = 0.0
        for count in unique_intervals.values():
            p = count / total
            entropy -= p * math.log2(p)

        # Normalize entropy by maximum possible entropy (log2(n_unique))
        max_entropy = math.log2(len(unique_intervals)) if unique_intervals else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        return min(max(normalized_entropy, 0.0), 1.0)


class LeapFrequencyExtractor(FeatureExtractor):
    """
    Computes the leap frequency: the proportion of intervals that are larger than a step (defined here as >2 semitones).
    """
    def extract(self, score):
        # Extract note MIDI numbers in order
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
                pitches.append(n.pitch.midi)

        if len(pitches) < 2:
            return 0.0

        leaps = [1 for a, b in zip(pitches[:-1], pitches[1:]) if abs(b - a) > 2]
        frequency = sum(leaps) / (len(pitches) - 1)
        return min(max(frequency, 0.0), 1.0)


class ContourDirectionalityExtractor(FeatureExtractor):
    """
    Measures the directional movement: it returns the ratio of upward movements.
    (i.e. the number of intervals where pitch goes up divided by total intervals).
    """
    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
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
        return min(max(ratio, 0.0), 1.0)


class MelodicContourComplexityExtractor(FeatureExtractor):
    """
    Computes the complexity of the melodic contour by counting the number of directional changes.
    The value is normalized by the total number of intervals minus one (the maximum possible number of changes).
    """
    def extract(self, score):
        pitches = []
        for n in score.recurse().notes:
            if hasattr(n, 'pitch'):
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
        changes = 0
        filtered = [d for d in directions if d != 0]
        for a, b in zip(filtered[:-1], filtered[1:]):
            if a != b:
                changes += 1

        max_possible = len(filtered) - 1 if len(filtered) > 1 else 1
        normalized_complexity = changes / max_possible
        return min(max(normalized_complexity, 0.0), 1.0)


# ============================================================
# Rhythmic and Duration Features
# ============================================================

class AverageNoteDurationExtractor(FeatureExtractor):
    """
    Computes the average note duration (using quarterLength values).
    The average is normalized relative to the maximum note duration found in the score.
    """
    def extract(self, score):
        durations = []
        for n in score.recurse().notes:
            durations.append(n.quarterLength)

        if not durations:
            return 0.0
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        normalized_duration = avg_duration / max_duration if max_duration > 0 else 0.0
        return min(max(normalized_duration, 0.0), 1.0)


class RhythmComplexityExtractor(FeatureExtractor):
    """
    Measures the complexity of rhythms by computing the entropy of note durations.
    The entropy is normalized by the maximum entropy for the observed number of unique durations.
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

        max_entropy = math.log2(len(unique_durations)) if len(unique_durations) > 0 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        return min(max(normalized_entropy, 0.0), 1.0)


class SyncopationExtractor(FeatureExtractor):
    """
    Computes a simple syncopation score by counting note onsets that are off the beat.
    Here we assume the downbeats occur at integer offsets (for example, in 4/4 time).
    The syncopation score is the ratio of syncopated note onsets to total note onsets.
    """
    def extract(self, score):
        note_count = 0
        syncopated = 0
        for n in score.recurse().notes:
            offset = n.offset
            note_count += 1
            # If the offset is not an integer, consider it off the beat.
            if not math.isclose(offset % 1, 0.0, abs_tol=1e-5):
                syncopated += 1
        if note_count == 0:
            return 0.0
        ratio = syncopated / note_count
        return min(max(ratio, 0.0), 1.0)


class NoteCountPerBarExtractor(FeatureExtractor):
    """
    Calculates the average number of note onsets per measure.
    For normalization, we assume an expected upper bound on note count per bar (for instance, 20).
    """
    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        note_counts = []
        for m in measures:
            count = len(list(m.flat.notes))
            note_counts.append(count)
        if not note_counts:
            return 0.0
        avg_notes = statistics.mean(note_counts)
        # Normalize using an upper bound (e.g., 20 notes per bar)
        normalized = avg_notes / 20.0
        return min(max(normalized, 0.0), 1.0)


class NoteCountPerBarVariabilityExtractor(FeatureExtractor):
    """
    Computes the variance of the note counts per bar across the score.
    Normalization is achieved by assuming a maximum variance (this may be tuned).
    """
    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        note_counts = [len(list(m.flat.notes)) for m in measures if m.flat.notes]
        if len(note_counts) < 2:
            return 0.0
        var_notes = statistics.variance(note_counts)
        # For normalization we assume a max variance (e.g., 20)
        normalized = var_notes / 20.0
        return min(max(normalized, 0.0), 1.0)


class RestFrequencyExtractor(FeatureExtractor):
    """
    Computes the frequency of rests relative to notes.
    The feature is calculated as the ratio of the number of rests to the total of rests and notes.
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
        return min(max(freq, 0.0), 1.0)


# ============================================================
# Structural and Statistical Complexity Features
# ============================================================

class ScoreLengthInBarsExtractor(FeatureExtractor):
    """
    Counts the total number of measures (bars) in the score.
    Normalization is application-dependent. Here we assume an upper bound of 200 bars.
    """
    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        bar_count = len(measures)
        normalized = bar_count / 200.0
        return min(max(normalized, 0.0), 1.0)


# Placeholder for pattern repetition extractors.
# For melodic or rhythmic repetition, more advanced algorithms (e.g., pattern matching)
# would be necessary. Below is a simple implementation based on n-gram repetition.

class MelodicPatternRepetitionExtractor(FeatureExtractor):
    """
    A very simplified extractor for melodic pattern repetition.
    This implementation converts the melody into a string of pitch numbers (separated by spaces)
    and counts how often n-grams (with n=3) are repeated. The score is normalized by the total possible n-grams.
    """
    def extract(self, score):
        pitches = [str(n.pitch.midi) for n in score.recurse().notes if hasattr(n, 'pitch')]
        n = 3
        if len(pitches) < n:
            return 0.0
        ngrams = [" ".join(pitches[i:i+n]) for i in range(len(pitches)-n+1)]
        unique = set(ngrams)
        total = len(ngrams)
        # Pattern repetition is measured as 1 - (unique patterns / total patterns)
        repetition = 1 - (len(unique) / total)
        return min(max(repetition, 0.0), 1.0)


class RhythmicPatternRepetitionExtractor(FeatureExtractor):
    """
    A simple extractor to measure rhythmic pattern repetition.
    It extracts a sequence of note durations, creates n-grams (n=3),
    and computes a repetition ratio.
    """
    def extract(self, score):
        durations = [str(n.quarterLength) for n in score.recurse().notes]
        n = 3
        if len(durations) < n:
            return 0.0
        ngrams = [" ".join(durations[i:i+n]) for i in range(len(durations)-n+1)]
        unique = set(ngrams)
        total = len(ngrams)
        repetition = 1 - (len(unique) / total)
        return min(max(repetition, 0.0), 1.0)


class EntropyOfPitchSequenceExtractor(FeatureExtractor):
    """
    Uses Shannon entropy to measure unpredictability in the sequence of pitches.
    This is similar to the interval complexity but computed directly over pitch occurrences.
    """
    def extract(self, score):
        pitches = [n.pitch.midi for n in score.recurse().notes if hasattr(n, 'pitch')]
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

        max_entropy = math.log2(len(unique)) if len(unique) > 0 else 1
        normalized = entropy / max_entropy if max_entropy > 0 else 0.0
        return min(max(normalized, 0.0), 1.0)


class VarianceInNoteDensityExtractor(FeatureExtractor):
    """
    Measures changes in note density across the measure.
    This extractor computes the number of note onsets per measure,
    then returns the normalized variance in note counts across all measures.
    """
    def extract(self, score):
        measures = score.getElementsByClass(music21.stream.Measure)
        counts = []
        for m in measures:
            counts.append(len(list(m.flat.notes)))
        if len(counts) < 2:
            return 0.0
        var_value = statistics.variance(counts)
        # Normalize (assume a max expected variance of 10)
        normalized = var_value / 10.0
        return min(max(normalized, 0.0), 1.0)



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
        # The extractor's class name is used as a key
        feature_value = extractor.extract(score)
        features[extractor.__class__.__name__] = feature_value
    return features


if __name__ == "__main__":
    # Example: load a MIDI file and get features.
    import sys
    if len(sys.argv) < 2:
        print("Usage: python feature_extractors.py <path_to_midi_file>")
        sys.exit(1)

    midi_path = sys.argv[1]
    score = music21.converter.parse(midi_path)

    # List of extractors to run.
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

    features = extract_all_features(score, extractors)

    for feature_name, value in features.items():
        print(f"{feature_name}: {value:.3f}")
