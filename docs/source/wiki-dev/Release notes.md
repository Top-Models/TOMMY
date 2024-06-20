# Release notes TOMMY

## Version 1.0.0 - Release date: 25/06/2024

### Features:

#### Operating System Support:
- Supports multiple operating systems:
  - Windows, MacOS, Linux

#### Topic Modelling:
- Introduces topic modelling algorithms:
  - LDA (Latent Dirichlet Allocation)
  - NMF (Non-Negative Matrix Factorization)

#### File Import:
- Added support for importing various file types:
  - Text, CSV, PDF, DOCX

#### Data Visualization:
- Visualizes imported data with:
  - Sorting of documents per Topic after topic modelling is done

#### Preprocessing Pipeline:
- Includes a comprehensive preprocessing pipeline:
  - Tokenization
  - Stopword removal
  - Lemmatization
  - User-defined stopword removal
  - User-defined synonym replacement

#### Settings:
- Customizable settings include:
  - Number of topic words for visualization
  - Topic modelling algorithm selection
  - Number of topics for modelling
  - Corpus language options: Dutch and English
  - Hyperparameter customization for LDA

#### Asynchronous Topic Modelling:
- Support for asynchronous topic modelling

#### Advanced Visualization:
- Provides extensive visualization options:
  - Document:
    - Word distribution per document
  - General topics:
    - K-value optimization
    - Documents over time
    - Topics in documents
    - Topic correlation
    - Word network
    - Document network
  - Specific topics:
    - Word cloud
    - Word weights
    - Document trends over time
  - Topic view:
    - Clicking on words within topics highlights the same words across all topics
    - Clicking on topics sorts files based on topic correspondence
    - Scalable window with custom flow layout to show multiple topics side-by-side

#### Information View:
- Detailed information on:
  - Document details
  - Topic specifics
  - Topic model overview

#### Configuration Support:
- Saving user settings in configurations
- Supports configuration management:
  - Save, delete, and load configurations

#### Saving and Loading:
- Enables saving and loading of configurations
- Facilitates sharing configurations

#### Exporting:
- Export capabilities include:
  - Graphs to Gephi (.gefx format)
  - Plots to PNG
  - Topic data to CSV
  - Document-topic correspondence to CSV

#### Custom User Interface (UI):
- Dynamic and responsive graphical user interface (GUI)
- Scalable and collapsible widgets
  - Custom splitter for resizing widgets
- client color theme

#### Error Handling:
- user-friendly error messages

#### Documentation:
- Comprehensive documentation suite:
  - User manual
  - Developer manual
  - Release notes
  - Wiki
  - Style guide
  - Source control guide
  - Installation guide