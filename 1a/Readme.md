# Round 1A: Understand Your Document - PDF Outline Extractor

This project provides a robust solution for extracting a structured outline (Title, H1, H2, H3) from PDF documents. It's designed to be fast, accurate, and run entirely offline within a Docker container, adhering to the competition's constraints.

## My Approach

The core strategy is to infer the document's structure by analyzing the visual and textual properties of its content, rather than relying on simple or brittle rules. The solution uses the `PyMuPDF` library for its speed and detailed text extraction capabilities.

The process works in two main passes:

1.  **Style & Candidate Collection**: The script first iterates through the entire PDF to gather all potential headings. It identifies candidates based on font size, text capitalization, and line length. It filters out text that is likely part of a paragraph or table. During this pass, it also identifies potential titles from the first page based on the largest font sizes.

2.  **Hierarchy Definition & Outline Generation**:
    * **Heading Levels**: The collected heading candidates are clustered by their style (font size and name). The most frequent and prominent styles are mapped to H1, H2, and H3 levels. This heuristic is more reliable than assuming "biggest is H1."
    * **Title Selection**: The title is determined by selecting the most prominent text candidate from the first page.
    * **Final Outline**: The script performs a second pass, matching text blocks against the identified heading styles to build the final, correctly ordered outline.

This method avoids hardcoding and is resilient to variations in PDF formatting, while being efficient enough to meet the performance requirements.

## Models and Libraries Used

* **Python 3.10**: The core programming language.
* **PyMuPDF (fitz)**: A high-performance Python library for PDF parsing and text extraction. It provides access to low-level details like font size, name, and position for each text block.
* **No ML Models**: This solution does not use any pre-trained machine learning models, keeping it lightweight and fast.

## How to Build and Run the Solution

The solution is designed to be built and run using Docker.

### Prerequisites

* Docker installed on your system.

### Build the Docker Image

Navigate to the project's root directory (where the `Dockerfile` is located) and run the following command.

```sh
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .