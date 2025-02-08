# PyHAT HTML Selection Extractor

A Hypermedia Driven Application (HDA) built with the PyHAT stack that allows users to extract HTML element data from a secondary browser window.

## Overview

This application lets you:
- **Open a Target Website:** Enter a website URL in the main interface and open the target site in a secondary (proxy) window. The proxy injects custom JavaScript into the page to enable element selection.
- **Interactive Element Selection:** Hover over and click on any HTML element in the secondary window. The injected script captures element details such as tag, content, outer HTML, XPath, classes, attributes, and parent/child relationships.
- **Element Type Classification:** Four radio toggles—**price-element**, **download-element**, **upload-element**, and **details-element**—allow you to classify the selected element. Only one radio button is active at a time, and after saving, the next radio is automatically selected.
- **Organized Data Storage:** The selected element data is saved to a JSON file (`2_output/data.json`). Data is organized into plan arrays (e.g., "plans1", "plans2", …), with each plan array holding 4 objects before a new array is created.
- **Dark Mode User Interface:** The entire UI uses a dark theme (black background, white text) with Tailwind CSS styling.
- **Inter-Window Communication:** The custom JavaScript (injected via the proxy) uses `window.opener.postMessage` to send the captured element data from the secondary window back to the main window for display and saving.

## Tech Stack

- **FastAPI:** Backend framework for handling HTTP requests and serving templates.
- **HTMX:** Enables dynamic HTML updates.
- **Alpine.js:** Provides frontend interactivity.
- **Tailwind CSS:** Used for responsive, dark-mode styling.
- **Jinja2:** Templating engine for generating HTML views.
- **httpx & BeautifulSoup:** For asynchronous HTTP requests and HTML parsing, respectively.

## Features

- **Secondary Window Element Selection:** Open a website in a new window where a custom script highlights and allows selection of HTML elements.
- **Interactive Element Details:** On clicking an element, details such as tag, content, XPath, classes, attributes, parent, and child tags are captured and sent back to the main window.
- **Element Type Selection:** Use radio toggles to classify the selected element. The selected type is added to the JSON data, and the UI automatically selects the next type after each save.
- **Structured Data Storage:** Saved elements are stored in a JSON file in plan arrays. Each plan (e.g., "plans1", "plans2", etc.) contains 4 objects.
- **Dark Themed UI:** The entire application is styled with a black background and white text for a modern, sleek look.
- **Proxy Injection:** The app uses a proxy endpoint to inject the selection script into the target website, enabling a seamless selection experience.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   or
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Open the Application:**
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

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
│       │   └── styles.css
│       └── js/
│           └── injector.js
├── 2_output/
│   └── data.json
└── README.md
```

## Usage

1. **Enter URL & Open Website:** In the main window, enter the target website URL and click the "Open Website" button. This loads the site in a secondary window with our selection script injected.
2. **Select an Element:** In the secondary window, hover over HTML elements (which will be highlighted), then click an element to capture its details.
3. **Choose Element Type:** Use the radio toggles in the main interface to select one of the four element types (price-element, download-element, upload-element, details-element). Only one toggle can be active at a time.
4. **Save the Data:** Click the "Save Selected Element" button. The app adds the selected element data to the JSON file (`2_output/data.json`) organized under plan arrays of 4 objects each. After saving, the radio toggle automatically rotates to the next option.

## Future Improvements

- **Enhanced Validation & Security:** Adding origin validation for inter-window messages.
- **UI Enhancements:** Expanding options for reviewing and editing saved data.
- **Additional Extraction Options:** Implementing further HTML element extraction capabilities. 