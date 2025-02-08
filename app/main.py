import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, Response
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

# Store scraped elements in memory
elements_store = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page for HTML selection extraction from a secondary browser window."""
    return templates.TemplateResponse("index.html", {"request": request})

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
    element = elements_store.get(element_id, {
        "id": element_id,
        "name": "Unknown Element",
        "content": "Element not found",
        "xpath": "",
        "classes": [],
        "attributes": {},
        "tag": "",
        "parent_tag": "",
        "child_tags": []
    })
    
    return templates.TemplateResponse(
        "element_detail.html",
        {"request": request, "element": element}
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

@app.get("/proxy")
async def proxy(request: Request, url: str):
    """Proxy the target URL and inject our element selector script."""
    try:
        # Validate and normalize URL
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        # Fetch the target website
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Inject our script
        script_tag = soup.new_tag('script', src='/static/js/injector.js')
        soup.body.append(script_tag)
        
        # Return the modified HTML
        return HTMLResponse(content=str(soup), status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to proxy URL: {str(e)}"},
            status_code=500
        ) 