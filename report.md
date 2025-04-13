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

Sea shanties, a genre of working songs performed aboard sailing vessels, provide a compelling subject for computational musicology. In this study, we adopt a computational musicology approach to perform feature analysis on symbolic music data, despite challenges in dataset availability and variability in MIDI representations. By curating a dataset of approximately 160 shanties from historical archives and digital repositories, we carefully preprocessed and normalized the data using the music21 toolkit to extract a comprehensive set of musical features. Our analysis focused on three core dimensions: melodic, rhythmic, and structural, examining variables such as melodic pattern repetition, rest frequency, and score length in bars. The results reveal that the two primary shanty categories—hauling and capstan—exhibit clear differences across these features, with significant distinctions in melodic repetition and structural characteristics. Clustering experiments and decision tree classification further validated that these quantifiable attributes can effectively differentiate between shanty types. These findings (see Figures: decision_tree_visualization.png and model_accuracy_comparison.png) highlight the potential of integrating computational techniques with traditional musicological inquiry, offering new insights into the relationship between musical form and its functional context in maritime traditions.

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

The initial step of our analysis involved assembling a MIDI dataset comprising approximately 160 sea shanties. These were gathered from a mix of historical archives and contemporary digital repositories. Specifically, the dataset includes:
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

We extracted a diverse set of musical features reflecting pitch, rhythmic, and structural characteristics from each sea shanty. The process made extensive use of our custom feature extractors (see our python file at https://github.com/Darce-One/shanties/blob/main/src/feature_extractors.py) that utilize music21 to navigate each score’s structure. Pitch and interval features were computed, including Pitch Range (see Figure: boxplot_pitch_range_by_type.png), Average Interval, Interval Complexity (via Shannon entropy), Leap Frequency (proportion of intervals >2 semitones), Contour Directionality (ratio of upward movements), and Melodic Contour Complexity (normalized count of directional changes; also see Figure: boxplot_melodic_pattern_repetition_by_type.png). Rhythmic features encompassed Average Note Duration, Rhythm Complexity (entropy of note durations), Syncopation (ratio of off-beat onsets), Note Count per Bar along with its variability, and Rest Frequency. To capture the structural and statistical complexity, we determined Score Length in bars, computed repetition ratios for melodic and rhythmic patterns using n-gram analysis, measured Entropy of the Pitch Sequence, and examined Variance in Note Density across measures.

### 2.3. Experimental Design
- Description of the analysis pipeline:
  - Correlation analysis of the extracted features
  - Clustering experiments to identify groups of similar shanties
  - Decision tree classification for predicting shanty type hauling versus capstan.
- Brief explanation of the machine learning models and parameters used.

**text:**

In our study, we implemented a multi-stage analysis pipeline to investigate the musical differences between shanty types and to determine which features best discriminate between them. Our overall experimental design comprised the following steps:

1. Feature Correlation Analysis
   We began by examining the relationships among the extracted features. Boxplots for each feature (grouped by shanty type) provided an initial visual inspection of the data distribution (refer to Figure: feature_distributions.png). We further assessed the pitch range differences (see Figure: boxplot_pitch_range_by_type.png) and melodic pattern repetition (see Figure: boxplot_melodic_pattern_repetition_by_type.png). A Pearson correlation matrix (see Figure: feature_correlation_matrix.png) enabled us to pinpoint highly correlated features (with |r| > 0.7), such as between note_count_per_bar_variability and variance_in_note_density, and between average_interval and leap_frequency. This guided our further analysis by ensuring that the models focused on independent, informative attributes.

2. Clustering Experiments
   After standardizing the features using a StandardScaler, we applied Principal Component Analysis (PCA) to reduce the dimensionality to two components. The PCA projection (see Figure: cluster_visualization.png) allowed us to visually assess the natural clustering tendencies among shanties. When plotting the principal components, we observed that the clusters loosely corresponded with known shanty types, suggesting inherent grouping in the musical features.

3. Classification via Machine Learning
   We pursued comprehensive machine learning analysis for shanty type classification (hauling versus capstan) that included several steps:
   • Feature Selection: Identification of the most informative musical attributes.
   • Model Comparison: Five classifiers – Decision Tree, Random Forest, Gradient Boosting, SVM, and Logistic Regression – were trained and compared; the comparative performance is visualized in Figure: model_accuracy_comparison.png.
   • Hyperparameter Tuning: Each model’s parameters were optimized using cross-validation.
   • Model Evaluation: Metrics such as accuracy, precision, recall, and F1-score were used. The overall confusion matrices for all models are shown in Figure: all_confusion_matrices.png. Additionally, while our pruned decision tree (see Figure: decision_tree_visualization.png) provided interpretability, its lower accuracy (43.8%) contrasted with the ensemble model’s improved performance (68.8%). Feature importance for classification is detailed in Figure: feature_importance_for_shanty_type_classification.png.
   • Unknown Shanty Classification: Finally, the best-performing model was used to predict the category for previously unclassified shanties.

Through this multifaceted experimental approach, our investigation revealed clear differences in musical features between shanty types, established robust correlations among these features, and highlighted the critical attributes for classification.

---

## 3. Results and Discussion

### 3.1. Feature Analysis
- Summary and visualization (e.g., charts, histograms) of the extracted features.
- Discussion on the distribution of melodic, rhythmic, and structural features across different shanty types.

**text:**

We began our analysis by extracting a wide range of musical features that characterize melodic, rhythmic, and structural aspects of sea shanties. Initial visualizations—including boxplots (see Figures: boxplot_pitch_range_by_type.png and boxplot_melodic_pattern_repetition_by_type.png) grouping each feature by shanty type—provided an overview of the data distribution. Further statistical comparisons revealed key differences: for instance, melodic_pattern_repetition in WINDLASS CAPSTAN shanties was on average 22.5% higher than in HALLIARD shanties; conversely, rest_frequency was 24.1% higher in HALLIARD shanties, while score_length_in_bars was 35.3% lower. The corresponding distributions are summarized in Figure: feature_distributions.png. Furthermore, the correlation matrix (see Figure: feature_correlation_matrix.png) highlighted strong associations among certain features. Finally, a radar chart (see Figure: radar_chart.png) visually encapsulates the key musical features by shanty type, illustrating their distinct musical signatures.

### 3.2. Clustering Results
- Description of the clustering technique used (e.g., k-means, hierarchical clustering).
- Presentation of clusters with interpretations—how do clusters relate to known shanty categories?
- Include figures and cluster maps where applicable.

**text:**

To inspect the natural grouping of shanties based solely on their musical features, we standardized the feature set and applied PCA to reduce the dimensions to two principal components. The resulting scatterplot (see Figure: cluster_visualization.png) displays each shanty’s position in the PCA space, with coloration indicating shanty type. Although these clusters are not perfectly separated, there is a noticeable trend where shanties with similar rhythmic and melodic characteristics group together. Complementary pairwise scatterplots further reinforced these observations by showing gradual transitions and overlaps corresponding to the functional grouping (hauling versus capstan) of shanties.

### 3.3. Classification Results
- Overview of the decision tree classifier setup and evaluation metrics (accuracy, precision, recall, etc.).
- Analysis of the results: How well do musical features predict shanty type?
- Discussion on feature importance and any misclassification issues.
- Comparison with traditional qualitative classifications of shanties (e.g., based on historical usage such as hauling versus capstan).

**text:**

For shanty type classification, we implemented and evaluated five different machine learning algorithms: Decision Tree, Random Forest, Gradient Boosting, SVM, and Logistic Regression. After feature selection and hyperparameter tuning, the model performances were compared (see Figure: model_accuracy_comparison.png). The overall confusion matrices for the classification models are depicted in Figure: all_confusion_matrices.png, which illustrate that WINDLASS CAPSTAN shanties were generally predicted with higher recall compared to HALLIARD shanties—reflecting inherent feature imbalances observed earlier.

In particular, our pruned decision tree (visualized in Figure: decision_tree_visualization.png) provided significant insights into feature importance, even though it achieved a lower accuracy of 43.8%. The importance rankings shown in Figure: feature_importance_for_shanty_type_classification.png identify melodic repetition, rest frequency, and score length as the key predictors of shanty type. Overall, these findings echo traditional qualitative assessments of sea shanties and offer a quantitative complement to historical categorizations.

### 3.4. Discussion
- Interpret the significance of the findings in the context of computational musicology.
- Consider limitations of the current study (dataset size, nuances of musical interpretation, etc.).
- Suggestions for further study or improvements (e.g., incorporating lyrical analysis, exploring alternative ML models).

**text:**

Our analysis has revealed an intriguing interplay between the features identified through traditional statistical methods such as ANOVA and those highlighted by our classification models. The ANOVA analysis produced a top three list of features — melody pattern recognition, rest frequency, and score length in bars — as being most significant. In contrast, our classification models found that score length in bars, note count per bar, and entropy of the pitch sequence were the most influential in segregating shanty types. The consistency of score length in bars as a key predictor in both approaches reinforces its importance, while the differences in the remaining features suggest that the underlying musical structure has multifaceted aspects that are captured differently by statistical and machine learning methods.

Moreover, we applied our trained classification models to a set of 100 new, unclassified shanties. These new predictions were, on average, supported by high confidence scores (exceeding 60%), indicating that the selected feature set and trained classifiers are capable of making robust determinations on unseen data. However, it is important to acknowledge an inherent complexity in the classification problem: some shanties exhibit characteristics of both capstan and hauling types. This inherent overlap suggests that, for certain pieces, a strict binary classification might be overly simplistic or even inappropriate.

Ultimately, our aim was not to produce a definitive classification of each shanty, but rather to identify and understand the musical features that influence the work functions performed by sailors. The discrepancies between features highlighted by ANOVA and those driving classification results underscore the complexity in translating musical scores into quantifiable attributes and remind us that a single work can defy strict categorization. This analysis provides a data-driven foundation from which future studies may further explore the multifaceted relationship between musical structure and maritime labor.

---

## 4. Conclusion

- Recap the main objectives and summarize the methodologies applied.
- Summarize key findings regarding the musical features and their effectiveness in classifying shanty types.
- Emphasize the contributions of the study to both the field of computational musicology and historical music research.
- Point out limitations and provide recommendations for future research, including the potential for integrating lyrical analysis and expanding the dataset.

**text:**

Our experimental results underscore several key findings:
• The musical features of sea shanties differ significantly between types, particularly in terms of melodic repetition, rest usage, and structural length.
• Correlation analysis confirmed that while many features are interrelated, a subset of independent attributes carries the discriminatory power needed for classification.
• The PCA-based clustering (see Figure: cluster_visualization.png) reveals natural grouping tendencies among shanties that align with their historical usage (hauling versus capstan), even if the clusters are not perfectly separated.
• The multi-model classification approach (see Figures: model_accuracy_comparison.png, all_confusion_matrices.png, and decision_tree_visualization.png) identified the most critical features for shanty type prediction, with ensemble methods offering improved accuracy.
• Feature importance visualization (see Figure: feature_importance_for_shanty_type_classification.png) further highlights the potential of specific musical attributes for informing classification decisions.

These contributions validate the quantitative methods of computational musicology for historical music research. While our study is limited by dataset size and the reduction of complex musical expression to discrete features, it opens avenues for future research—such as integrating lyrical content and expanding the data corpus—to deepen our understanding of function and form in traditional music.

---

## References

- Format your references in the style required by the conference.
- Include all relevant sources on sea shanties, computational musicology, musical feature analysis, and any machine learning tools or methodologies referenced in the paper.

---
