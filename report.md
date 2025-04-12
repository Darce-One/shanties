
# Sea Shanties: A Computational Musicology Approach to Feature Analysis and Classification

Andreas Papaeracleous and Siddharth Saxena
Music Technology Group, Universitat Pompeu Fabra
andreas.papaeracleous01@estudiant.upf.edu, siddharth.saxena01@estudiant.upf.edu

---

## Abstract

A brief summary (150–250 words) of the paper’s purpose, methodology, key results, and conclusions.
- Introduce sea shanties and their historical significance
- Summarize the computational approaches used for feature extraction and analysis
- Highlight the main findings regarding melodic, rhythmic, and structural features
- Mention the results from clustering and decision tree classification experiments

**text:**

Sea shanties, a genre of working songs performed aboard sailing vessels, provide a compelling subject for computational musicology. In this study, we adopt a computational musicology approach to perform feature analysis on symbolic music data, despite challenges in dataset availability and variability in MIDI representations. By curating a dataset of approximately 160 shanties from historical archives and digital repositories, we carefully preprocessed and normalized the data using the music21 toolkit to extract a comprehensive set of musical features. Our analysis focused on three core dimensions: melodic, rhythmic, and structural, examining variables such as melodic pattern repetition, rest frequency, and score length in bars. The results reveal that the two primary shanty categories—hauling and capstan—exhibit clear differences across these features, with significant distinctions in melodic repetition and structural characteristics. Clustering experiments and decision tree classification further validated that these quantifiable attributes can effectively differentiate between shanty types. These findings highlight the potential of integrating computational techniques with traditional musicological inquiry, offering new insights into the relationship between musical form and its functional context in maritime traditions.

---

## 1. Introduction

- Background on sea shanties: their history, musical characteristics (call-and-response, steady rhythms, repeated refrains), and cultural importance.
- Motivation for studying shanties from a computational perspective.
- Overview of related work in computational musicology and historical music analysis.
- Objectives of the project:
  - Feature extraction from musical scores in MIDI format
  - Analysis of melodic, rhythmic, and structural features
  - Clustering and classification of shanty types based on musical features
- Outline of the paper’s structure.

**text:**

The study of sea shanties offers a fascinating glimpse into a unique confluence of musical tradition and social function. Historically, these maritime work songs were more than mere entertainment for sailors; they served as vital tools for coordinating labor aboard ships. Their characteristic call-and-response structure, steady rhythmic patterns, and repeated refrains were not only musically engaging but also functionally efficient—enabling groups of sailors to sync their movements during physically demanding tasks such as hauling and operating capstans.

Embedded within broader folk traditions that include Irish, Scottish, and English repertoires, sea shanties are rooted in a rich oral tradition. This cultural heritage, passed down through generations, reflects a form of communal expression where music was inherently linked to daily life and labor. Unlike art music composed solely for aesthetic enjoyment, shanties were created with a clearly defined purpose, seamlessly blending practicality with musical creativity.

In recent years, the emerging field of computational musicology has provided new avenues for exploring such historical musical practices. Positioned at the intersection of musicology and computer science, computational musicology employs algorithmic analyses and statistical models to uncover patterns and structures that might otherwise remain hidden. By using digital tools to extract and analyze features such as melodic contours, rhythmic complexity, and structural repetition, this study seeks to elucidate how the specific labor demands—capstan versus hauling—shaped both the musical and lyrical structures of sea shanties. This approach not only enhances our understanding of these historic work songs but also enriches the broader investigation into how function influences musical form across different cultures and traditions.

---

## 2. Experiment Details / Methods

### 2.1. Data Collection and Preprocessing
- Description of the MIDI dataset: number of pieces, sources, preprocessing steps (e.g., MIDI parsing, normalization).
- Brief discussion of any challenges encountered during data collection.

**text:**

he initial step of our analysis involved assembling a MIDI dataset comprising approximately 160 sea shanties. These were gathered from a mix of historical archives and contemporary digital repositories. Specifically, the dataset includes:
• 30 files from "The Shanty Book Part 1"
• 30 files from "The Shanty Book Part 2"
• 100 files from mainsailcafe.com

Each MIDI file was parsed using the music21 toolkit to convert the files into a standard stream format suitable for processing. Due to variability in score structure and formatting across the different sources, significant preprocessing was needed to reliably extract individual parts; when available, vocal parts were preferentially selected for analysis. Normalization procedures — such as standardizing tempo and dynamic markings — were applied to minimize potential biases during feature extraction, ensuring the consistency necessary for accurate computational analysis.


### 2.2. Feature Extraction
Outline the three main feature categories and specific features extracted:

#### A. Pitch and Interval Features
- Pitch Range
- Average Interval
- Interval Complexity (e.g., entropy of interval distribution)
- Leap Frequency
- Contour Directionality
- Melodic Contour Complexity

#### B. Rhythmic and Duration Features
- Average Note Duration
- Rhythm Complexity (entropy of note durations)
- Syncopation Count/Index
- Note Count per Bar
- Variability in Note Count per Bar
- Rest Frequency

#### C. Structural and Statistical Complexity Features
- Score Length (in bars)
- Repetition: Rhythmic Pattern Recurrence
- Repetition: Melodic Pattern Recurrence
- Entropy of the Pitch Sequence
- Variance in Note Density

**text:**

We extracted a diverse set of musical features reflecting pitch, rhythmic, and structural characteristics from each sea shanty. The process made extensive use of our custom feature extractors [python file](https://github.com/Darce-One/shanties/blob/main/src/feature_extractors.py) that utilize music21 to navigate each score’s structure. Pitch and interval features were computed, including Pitch Range, Average Interval, Interval Complexity (via Shannon entropy), Leap Frequency (proportion of intervals >2 semitones), Contour Directionality (ratio of upward movements), and Melodic Contour Complexity (normalized count of directional changes). Rhythmic features encompassed Average Note Duration, Rhythm Complexity (entropy of note durations), Syncopation (ratio of off-beat onsets), Note Count per Bar along with its variability, and Rest Frequency. To capture the structural and statistical complexity, we determined Score Length in bars, computed repetition ratios for melodic and rhythmic patterns using n-gram analysis, measured Entropy of the Pitch Sequence, and examined Variance in Note Density across measures.

### 2.3. Experimental Design
- Description of the analysis pipeline:
  - Correlation analysis of the extracted features
  - Clustering experiments to identify groups of similar shanties
  - Decision tree classification for predicting shanty type hauling versus capstan.
- Brief explanation of the machine learning models and parameters used.

---

## 3. Results and Discussion

### 3.1. Feature Analysis
- Summary and visualization (e.g., charts, histograms) of the extracted features.
- Discussion on the distribution of melodic, rhythmic, and structural features across different shanty types.

### 3.2. Clustering Results
- Description of the clustering technique used (e.g., k-means, hierarchical clustering).
- Presentation of clusters with interpretations—how do clusters relate to known shanty categories?
- Include figures and cluster maps where applicable.

### 3.3. Classification Results
- Overview of the decision tree classifier setup and evaluation metrics (accuracy, precision, recall, etc.).
- Analysis of the results: How well do musical features predict shanty type?
- Discussion on feature importance and any misclassification issues.
- Comparison with traditional qualitative classifications of shanties (e.g., based on historical usage such as hauling versus capstan).

### 3.4. Discussion
- Interpret the significance of the findings in the context of computational musicology.
- Consider limitations of the current study (dataset size, nuances of musical interpretation, etc.).
- Suggestions for further study or improvements (e.g., incorporating lyrical analysis, exploring alternative ML models).

---

## 4. Conclusion

- Recap the main objectives and summarize the methodologies applied.
- Summarize key findings regarding the musical features and their effectiveness in classifying shanty types.
- Emphasize the contributions of the study to both the field of computational musicology and historical music research.
- Point out limitations and provide recommendations for future research, including the potential for integrating lyrical analysis and expanding the dataset.

---

## References

- Format your references in the style required by the conference.
- Include all relevant sources on sea shanties, computational musicology, musical feature analysis, and any machine learning tools or methodologies referenced in the paper.

---
