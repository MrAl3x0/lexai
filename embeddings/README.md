# Legal Document Embeddings

This directory contains the pre-computed vector embeddings for legal documents from various jurisdictions. These embeddings are used by the `lexai` application to find relevant documents based on semantic similarity to a user's query.

## File Format

Each file is a NumPy `.npz` archive containing the following arrays:

- `embeddings`: A 2D NumPy array where each row is a vector embedding of a document chunk.
- `urls`: A list of source URLs corresponding to each document.
- `titles`: A list of document titles.
- `subtitles`: A list of document subtitles or section headers.
- `contents`: The raw text content of the document chunks that were embedded.

## Generation Process

These files were generated using the `text-embedding-ada-002` model from OpenAI. The process involves:

1.  Scraping and parsing legal documents for each jurisdiction.
2.  Chunking the documents into manageable sections.
3.  Calling the OpenAI API to generate an embedding for each chunk.
4.  Saving the embeddings and associated metadata into the `.npz` format.

_(Note: The script used to generate these embeddings is maintained separately and is not included in this repository.)_

## Git LFS

These files are tracked using Git LFS (Large File Storage) due to their size. Ensure you have Git LFS installed (`git lfs install`) to clone and pull these files correctly.
