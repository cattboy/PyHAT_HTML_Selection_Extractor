# PyHAT HTML Selection Extractor

A Hypermedia Driven Application (HDA) built with the PyHAT-stack that allows users to select HTML elements in the browser and save their data.

## Tech Stack

- FastAPI - Backend framework
- HTMX - Dynamic HTML updates
- Alpine.js - Frontend interactivity
- Tailwind CSS - Styling
- Jinja2 - Template engine

## Features

- Interactive element selection with hover highlighting
- Real-time element detail display
- Save selected element data to JSON
- Modern, responsive UI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Open your browser to http://127.0.0.1:8000

## Project Structure

```
my-hda-app/
├── app/
│   ├── main.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── element_detail.html
│   └── static/
│       ├── css/
│       │   └── tailwind.css
│       └── js/
│           └── alpine.js
└── 2_output/
    └── data.json
``` 