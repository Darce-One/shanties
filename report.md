# Sea Shanties: A Computational Musicology Approach to Feature Analysis and Classification

Andreas Papaeracleous and Siddharth Saxena
Music Technology Group, Universitat Pompeu Fabra
andreas.papaeracleous01@estudiant.upf.edu, siddharth.saxena01@estudiant.upf.edu

---

## Abstract

Sea shanties, historically integral to maritime labor, possess a dual role as both practical tools for communication and coordinated work and as vibrant expressions of folk musical traditions. This study employs computational musicology to explore how specific labor functions—namely hauling and capstan operations—influenced the musical and lyrical structures of sea shanties. By assembling a curated MIDI dataset of 160 shanties and extracting a diverse array of features across pitch, rhythm, and structure using the music21 toolkit and custom Python extractors, we mapped the musical signatures of these work songs. Our analysis proceeded through feature correlation assessments, dimensionality reduction via PCA, and classification experiments employing five machine learning models. The results reveal that features such as melodic repetition, rest frequency, and score length robustly differentiate between shanty types, a finding supported by both statistical analyses and machine learning interpretations. These outcomes underscore the impact of functional demands on musical form, bridging historical ethnomusicology with modern computational methodologies.

---

## 1. Introduction

The study of sea shanties offers a fascinating glimpse into a unique confluence of musical tradition and social function. Historically, these maritime work songs were more than mere entertainment for sailors; they served as vital tools for coordinating labor aboard ships. Their characteristic call-and-response structure, steady rhythmic patterns, and repeated refrains were not only musically engaging but also functionally efficient—enabling groups of sailors to sync their movements during physically demanding tasks such as hauling and operating capstans.

Embedded within broader folk traditions that include Irish, Scottish, and English repertoires, sea shanties are rooted in a rich oral tradition. This cultural heritage, passed down through generations, reflects a form of communal expression where music was inherently linked to daily life and labor. Unlike art music composed solely for aesthetic enjoyment, shanties were created with a clearly defined purpose, seamlessly blending practicality with musical creativity.

In recent years, the emerging field of computational musicology has provided new avenues for exploring such historical musical practices. Positioned at the intersection of musicology and computer science, computational musicology employs algorithmic analyses and statistical models to uncover patterns and structures that might otherwise remain hidden. By using digital tools to extract and analyze features such as melodic contours, rhythmic complexity, and structural repetition, this study seeks to elucidate how the specific labor demands—capstan versus hauling—shaped both the musical and lyrical structures of sea shanties. This approach not only enhances our understanding of these historic work songs but also enriches the broader investigation into how function influences musical form across different cultures and traditions.

---

## 2. Experiment Details / Methods

### 2.1. Data Collection and Preprocessing

The analysis began by assembling a MIDI dataset of about 160 sea shanties from historical archives and digital repositories. This dataset includes 30 files each from The Shanty Book Part 1 and Part 2, plus 100 files from mainsailcafe.com. Each MIDI file was parsed with the music21 toolkit, converting them into a standardized stream format focused exclusively on the vocal parts to ensure consistency during feature extraction.

For data labeling, we used annotations from The Shanty Book Part 1 and Part 2 to differentiate shanties by function (hauling vs. capstan). These detailed descriptions allowed us to categorize most pieces confidently, though some shanties exhibit characteristics of both styles, introducing potential ambiguities. Overall, the book annotations served as our ground truth.

Although preprocessing addressed general challenges, additional effort was needed to manage variability in MIDI formatting. Most MIDI files were well-behaved; however, for shanties from Part 2, we employed Optical Music Recognition (OMR) using MuseScore's API to extract the data, followed by manual checks. Aside from one shanty with significant formatting issues (which was discarded), the extracted data met our quality standards. We also corrected minor issues, such as missing channels and outlier tempo values, ensuring a robust and consistent dataset for feature extraction.

### 2.2. Feature Extraction

We extracted musical features representing three distinct dimensions—pitch and interval, rhythmic and duration, and structural/statistical complexity. Initially defined in detail here, subsequent references (e.g., “melodic repetition” or “score length”) assume these definitions:

A. Pitch and Interval Features
• Pitch Range
• Average Interval
• Interval Complexity (using Shannon entropy of the interval distribution)
• Leap Frequency (proportion of intervals >2 semitones)
• Contour Directionality (ratio of upward movements)
• Melodic Contour Complexity (normalized count of directional changes)

B. Rhythmic and Duration Features
• Average Note Duration
• Rhythm Complexity (entropy of note durations)
• Syncopation Count/Index (ratio of off-beat onsets)
• Note Count per Bar and its Variability
• Rest Frequency

C. Structural and Statistical Complexity Features
• Score Length (in bars)
• Repetition (melodic and rhythmic pattern recurrence via n-gram analysis)
• Entropy of the Pitch Sequence
• Variance in Note Density

Custom Python extractors (see https://github.com/Darce-One/shanties/blob/main/src/feature_extractors.py) processed each score to generate these features.

### 2.3. Experimental Design

Our analysis followed a three-step pipeline:

1. Feature Correlation Analysis
After extraction, we assessed inter-feature relationships using visualizations (e.g., boxplots grouping features by shanty type) and a Pearson correlation matrix. For example, features such as note_count_per_bar_variability and variance_in_note_density, or average_interval and leap_frequency, showed strong correlations (|r| > 0.7). These insights guided our selection of independent, informative features.

2. Clustering Experiments
Standardizing the feature set allowed us to reduce dimensionality via Principal Component Analysis (PCA), projecting the data onto two principal components. The resulting scatterplot displayed natural grouping trends among shanties that, while not perfectly separated, loosely correspond with known types (hauling versus capstan).

3. Classification via Machine Learning
We compared five classifiers (Decision Tree, Random Forest, Gradient Boosting, SVM, and Logistic Regression) to predict shanty type. Following feature selection and hyperparameter tuning via cross-validation, model performance was evaluated through metrics such as accuracy, precision, recall, and F1-score. Visual tools (e.g., confusion matrices and feature importance rankings) highlighted melodic repetition, rest frequency, and score length—in addition to other features—as key predictors. Finally, the best-performing model was applied to classify a further set of 100 unassigned shanties.
---

## 3. Results and Discussion

### 3.1. Feature Analysis

Visualizations (including boxplots and histograms) of the extracted features confirmed significant differences between shanty types. For instance, WINDLASS CAPSTAN shanties showed a 22.5% higher average of melodic repetition compared to HALLIARD shanties, while rest frequency was 24.1% higher and score length was 35.3% lower in HALLIARD pieces. The overall feature distributions (refer to Figure: feature_distributions.png) and the correlation matrix (Figure: feature_correlation_matrix.png) provided clarity on how melodic, rhythmic, and structural characteristics vary with shanty function.

### 3.2. Clustering Results

The PCA scatterplot (see Figure: cluster_visualization.png) highlighted natural clusters that align with historical groupings. While some overlap exists between clusters, the grouping based on the core features (as earlier defined) strongly suggests that shanties with similar rhythmic and melodic properties tend to cluster together. Complementary pairwise scatterplots reinforced this observation, supporting the notion that musical function (hauling versus capstan) has a quantifiable musical signature.

### 3.3. Classification Results

Comparative analysis of the five classifiers (see Figure: model_accuracy_comparison.png and confusion matrices in Figure: all_confusion_matrices.png) revealed a higher recall for WINDLASS CAPSTAN shanties over HALLIARD shanties. The pruned decision tree (visualized in Figure: decision_tree_visualization.png), although less accurate (43.8%), provided critical interpretative value by highlighting feature importance (see Figure: feature_importance_for_shanty_type_classification.png). Ensemble models, reaching up to 68.8% accuracy, confirmed that the set of features—including melodic repetition, rest frequency, and score length—robustly discriminates between shanty types.


### 3.4. Discussion

Our analysis has revealed an intriguing interplay between the features identified through traditional statistical methods such as ANOVA and those highlighted by our classification models. The ANOVA analysis produced a top three list of features — melody pattern recognition, rest frequency, and score length in bars — as being most significant. In contrast, our classification models found that score length in bars, note count per bar, and entropy of the pitch sequence were the most influential in segregating shanty types. The consistency of score length in bars as a key predictor in both approaches reinforces its importance, while the differences in the remaining features suggest that the underlying musical structure has multifaceted aspects that are captured differently by statistical and machine learning methods.

Moreover, we applied our trained classification models to a set of 100 new, unclassified shanties. These new predictions were, on average, supported by high confidence scores (exceeding 60%), indicating that the selected feature set and trained classifiers are capable of making robust determinations on unseen data. However, it is important to acknowledge an inherent complexity in the classification problem: some shanties exhibit characteristics of both capstan and hauling types. This inherent overlap suggests that, for certain pieces, a strict binary classification might be overly simplistic or even inappropriate.

Ultimately, our aim was not to produce a definitive classification of each shanty, but rather to identify and understand the musical features that influence the work functions performed by sailors. The discrepancies between features highlighted by ANOVA and those driving classification results underscore the complexity in translating musical scores into quantifiable attributes and remind us that a single work can defy strict categorization. This analysis provides a data-driven foundation from which future studies may further explore the multifaceted relationship between musical structure and maritime labor.

---

## 4. Conclusion

**text:**

The investigation has provided compelling evidence that functional demands inherent in maritime labor have left quantifiable imprints on the musical structure of sea shanties. Our multi-step analysis—from feature extraction and statistical correlation to clustering and machine learning classification—demonstrated that attributes like score length, melodic repetition, and rest frequency are pivotal in distinguishing between hauling and capstan shanties. Notably, while ensemble classifiers achieved accuracies approaching 68.8%, some shanties exhibited hybrid characteristics that challenge straightforward binary classification, suggesting the need for more nuanced categorization approaches in future research.

These findings illuminate the intricate interplay between musical form and its utilitarian purpose, reinforcing the notion that work songs are not merely artistic expressions but are deeply embedded in the practical and social fabric of cultural heritage. As a foundation for further exploration, future studies may consider integrating additional contextual factors, employing multi-label classification strategies, or extending the analytical framework to other folk traditions. Ultimately, the fusion of computational techniques with traditional musicological inquiry opens new avenues for understanding the multifaceted relationships between musical expression and human activity.

---

## References

- Format your references in the style required by the conference.
- Include all relevant sources on sea shanties, computational musicology, musical feature analysis, and any machine learning tools or methodologies referenced in the paper.

---
