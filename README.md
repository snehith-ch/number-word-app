# Number to Word Converter

Convert numbers to meaningful words/sentences using the Major System phonetic rules.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m nltk.downloader words
Run `python -m app.webapp` to start web UI.
Run tests via terminal: `python -m unittest discover -s tests`
