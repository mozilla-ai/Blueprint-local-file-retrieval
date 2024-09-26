<!-- ![Project Logo](/images/to/Blueprints-logo.png) -->

# Build an AI-powered Local File-Retrieval System

This project is an AI-powered system designed for local file retrieval. It uses local language models and local indexing to retrieve files based on semantic user queries, providing fast and accurate access to files stored on local devices. This eliminates the need for manual searching, improving productivity. The system supports various file types, including text documents, images, and PDFs.

## Pre-requisites

- **System requirements**: 
  - OS: Windows, macOS, or Linux
  - Minimum RAM: 8 GB (Dependent on language model used)
  - Disk space: 10 GB minimum

- **Dependencies**:
  - Python 3.8 or higher
  - Dependencies listed in `requirements.txt`
    
## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mozilla-ai/Blueprint-local-file-retrieval.git
   cd Blueprint-local-file-retrieva
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Quick-start (example)

1. Index your files:
   ```
   python index_files.py --directory /path/to/your/files
   ```

2. Start the retrieval system:
   ```
   python retrieval_system.py
   ```

3. Query your files:
   ```
   python query_files.py --query "Find all documents related to project XYZ"
   ```

## Project Structure

- `index_files.py`: Indexes the files in the specified directory
- `retrieval_system.py`: Main script for the retrieval system
- `query_files.py`: Interface for querying indexed files
- `models/`: Directory containing the local language models
- `utils/`: Helper functions and utilities
- `config.yaml`: Configuration file for the system

## How it Works (example)

1. File Indexing: The indexes the specified directory and stores the using sqlite-vec.
2. Query Processing: User queries are processed using a local language model to understand the semantic meaning.
3. Retrieval: The system compares the processed query against the indexed files to find the most relevant matches.
4. Result Presentation: Relevant files are presented to the user, ranked by relevance.

## Configuration and Customization

You can customize the system by modifying the `config.yaml` file. Key configurations include:

- `index_directory`: Path to the directory containing files to be indexed
- `model_name`: Name of the local language model to use
- `file_types`: List of file types to include in indexing
- `max_results`: Maximum number of results to return per query

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Additional Resources

- https://future.mozilla.org/builders/news_insights/llamafiles-for-embeddings-in-local-rag-applications/
