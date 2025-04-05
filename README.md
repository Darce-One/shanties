# Sea Shanties - A computational musicology project

---

## A bit about Sea Shanties
Sea shanties are maritime work songs historically sung by sailors to coordinate labor, typically characterized by:
- call-and-response
- steady rhythms, and
- repeated refrains.

### Kinds of Shanties:
- **Capstan Shanty**: Long, Continuous Tasks
- **Halyard / Long-haul shanties**: Coordinated hauling
- **Short-drag shanties**: Quick pulls.

---

## Project Goals:
This project looks to identify certain features in sea shanties that may be relevant in understanding the use of those shanties.

**Clustering & Classification**: Do shanties of different types exhibit distinct melodic/rhythmic/lyrical features?
Can we classify shanty type from these features?

**Musical & Lyrical Comparison**: Do sea shanties that share similar melodic and rhythmic traits (as measured from their musical scores) also exhibit similarities in their lyrics and/or textual themes?

---

## Feature Extraction:

### 1. Pitch and Interval Features

- **Pitch Range:**
  Measure the distance between the highest and lowest pitches.

- **Average Interval:**
  Calculate the mean distance between consecutive pitches.

- **Interval Complexity:**
  Quantify the diversity in intervals — for example, using the entropy of the distribution of intervals.

- **Leap Frequency:**
  Count the proportion of intervals that exceed a step (e.g., intervals larger than a major second) compared to stepwise motion.

- **Contour Directionality:**
  Measure the percentage of upward versus downward movements.

- **Melodic Contour Complexity:**
  Compute metrics such as the number of directional changes or "turns" in the melody to capture the smoothness versus jaggedness of the line.

---

### 2. Rhythmic and Duration Features

- **Average Note Duration:**
  Compute the mean length of notes across the score.

- **Rhythm Complexity:**
  Quantify the diversity in note lengths — for example, using the entropy of the distribution of note durations.

- **Syncopation Count/Index:**
  Count the number of syncopated events or compute a syncopation score based on the degree of off-beat placements.

- **Note Count per Bar:**
  Calculate the number of note onsets per bar, accounting for meter variations.

- **Note Count per Bar Variability:**
  Determine the variance of the note count in each bar, accounting for meter variations.

- **Rest Frequency:**
  Count the ratio of rests to notes, contributing to the overall rhythmic pattern.

---

### 3. Structural and Statistical Complexity Features

- **Score Length in Bars:**
  Simply count the total number of measures in the score.

- **Repetition: Rhythmic Pattern Recurrence:**
  Quantify how often rhythmic patterns repeat throughout the score.

- **Repetition: Melodic Pattern Recurrence:**
  Quantify how often melodic patterns repeat throughout the score.

- **Entropy of the Pitch Sequence:**
  Use information theory (e.g., Shannon entropy) to gauge the unpredictability or variability in the sequence of pitches.

- **Variance in Note Density:**
  Measure changes in note density across the score to detect fluctuations between zones of activity.

---

# Running the scripts:
Set up the virtual environment of your choice, with python version 3.10 installed.
Once activated, run
```bash
pip install -r requirements.txt
```
You can then run the main script on your database of midi files. You do it like so:
```bash
python src/main.py <dataset_folder>
```
