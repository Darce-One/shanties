
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

*Example Placeholder:*
“This paper introduces a computational framework for analyzing the musical and lyrical features of sea shanties, historic maritime work songs. We extract diverse musical features—including pitch, interval, rhythmic, and structural properties—from MIDI representations and employ clustering and decision tree classification techniques to discern differences among shanty subtypes. Our results indicate distinctive musical signatures across capstan and hauling shanties, suggesting that the work associated with shanty tasks have musically relevant features. These findings contribute to the field of computational musicology and provide insights for further interdisciplinary research.”

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

*Example Placeholder:*
“Sea shanties have long been integral to maritime labor, characterized by their call-and-response structure and steady rhythmic patterns. With the advent of computational musicology, detailed analysis of these historical songs offers new perspectives on their musical structure and cultural context. In this paper, we present methodologies for feature extraction and classification to discern the unique musical signatures of various shanty types…”

---

## 2. Experiment Details / Methods

### 2.1. Data Collection and Preprocessing
- Description of the MIDI dataset: number of pieces, sources, preprocessing steps (e.g., MIDI parsing, normalization).
- Brief discussion of any challenges encountered during data collection.

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

Include sample code snippets or command-line instructions if relevant:
```
$ pip install -r requirements.txt
$ python src/main.py <dataset_folder>
```

### 2.3. Experimental Design
- Description of the analysis pipeline:
  - Correlation analysis of the extracted features
  - Clustering experiments to identify groups of similar shanties
  - Decision tree classification for predicting shanty type (hauling versus capstan, with details on sub-types if applicable)
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

*Example Placeholder:*
“Our analysis reveals that features such as melodic contour complexity and syncopation index are strong discriminators between capstan and hauling shanties. Moreover, clustering experiments suggest a natural grouping that corroborates historical classifications, though some pieces remain ambiguous, highlighting the intricate overlap in musical characteristics…”

---

## 4. Conclusion

- Recap the main objectives and summarize the methodologies applied.
- Summarize key findings regarding the musical features and their effectiveness in classifying shanty types.
- Emphasize the contributions of the study to both the field of computational musicology and historical music research.
- Point out limitations and provide recommendations for future research, including the potential for integrating lyrical analysis and expanding the dataset.

*Example Placeholder:*
“In conclusion, our computational analysis of sea shanties demonstrates that robust musical features can be successfully extracted and used to classify shanty subtypes. The integration of clustering and decision tree models provides promising pathways for further inquiry, bridging historical musicology with modern data science techniques…”

---

## References

- Format your references in the style required by the conference.
- Include all relevant sources on sea shanties, computational musicology, musical feature analysis, and any machine learning tools or methodologies referenced in the paper.

---

*Notes for the Authors:*
- Replace placeholder text with your detailed descriptions and experimental data.
- Ensure that any figures, tables, or code excerpts mentioned are included as appendices or embedded in the relevant sections.
- Follow the formatting guidelines of the conference (e.g., font size, margins, citation style).
