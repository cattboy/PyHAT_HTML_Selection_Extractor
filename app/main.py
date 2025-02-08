import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = FastAPI(title="PyHAT HTML Selection Extractor")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, url: str = None):
    """Render the main page with URL input or website content."""
    if not url:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "url": None, "content": None}
        )
    
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f"https://{url}"
        
        # Fetch website content
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            
        # Parse HTML and extract elements
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = []
        
        # Extract common elements
        for i, elem in enumerate(soup.find_all(['div', 'section', 'article', 'header', 'footer', 'nav', 'main', 'aside']), 1):
            # Get element text content
            content = elem.get_text(strip=True)[:200] + "..." if len(elem.get_text(strip=True)) > 200 else elem.get_text(strip=True)
            
            # Get element type and any identifying classes
            elem_type = elem.name
            elem_class = " ".join(elem.get("class", []))
            elem_id = elem.get("id", "")
            
            elements.append({
                "id": i,
                "name": f"{elem_type.title()}{f' - {elem_id}' if elem_id else ''}{f' ({elem_class})' if elem_class else ''}",
                "content": content,
                "html": str(elem),
                "xpath": generate_xpath(elem)
            })
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "url": url,
                "elements": elements
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "url": url,
                "error": str(e)
            }
        )

def generate_xpath(element):
    """Generate XPath for a BeautifulSoup element."""
    components = []
    child = element
    for parent in element.parents:
        if parent.name == '[document]':
            break
        siblings = parent.find_all(child.name, recursive=False)
        if len(siblings) > 1:
            index = siblings.index(child) + 1
            components.append(f"{child.name}[{index}]")
        else:
            components.append(child.name)
        child = parent
    components.reverse()
    return '/' + '/'.join(components)

@app.get("/element/{element_id}", response_class=HTMLResponse)
async def get_element_detail(request: Request, element_id: int):
    """Return HTML snippet with element details."""
    return templates.TemplateResponse(
        "element_detail.html",
        {"request": request, "element": {"id": element_id}}
    )

@app.post("/save", response_class=JSONResponse)
async def save_data(request: Request):
    """Save selected element data to JSON file."""
    try:
        form_data = await request.form()
        element_data = json.loads(form_data.get("element-data"))
        element_data["timestamp"] = str(datetime.datetime.now())
        
        output_dir = "2_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = os.path.join(output_dir, "data.json")

        # Load existing data if available
        data_list = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    data_list = json.load(f)
                except json.JSONDecodeError:
                    data_list = []
        
        # Append new data and write back to file
        data_list.append(element_data)
        with open(file_path, "w") as f:
            json.dump(data_list, f, indent=4)
        
        return JSONResponse(
            content={
                "message": f"Element saved successfully!",
                "status": "success"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error saving data: {str(e)}", "status": "error"},
            status_code=500
        ) 