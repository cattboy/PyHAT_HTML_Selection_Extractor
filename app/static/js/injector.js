// Function to generate XPath for an element
function generateXPath(element) {
    if (!element) return '';
    
    const idx = (sib, name) => sib 
        ? idx(sib.previousElementSibling, name || sib.localName) + (sib.localName == name)
        : 1;
    const segs = elm => !elm || elm.nodeType !== 1 
        ? ['']
        : elm.id && document.getElementById(elm.id) === elm
            ? [`//*[@id="${elm.id}"]`]
            : [...segs(elm.parentNode), `${elm.localName}[${idx(elm)}]`];
    return segs(element).join('/');
}

// Function to handle element selection
document.addEventListener('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const element = e.target;
    
    // Create element data object with reordered properties
    const selectedData = {
        url: window.originalUrl,
        // Use parent's getSelectedRadioValue if available, otherwise default to 'price-element'
        elementType: (window.opener && typeof window.opener.getSelectedRadioValue === 'function' ? window.opener.getSelectedRadioValue() : 'price-element'),
        xpath: generateXPath(element),
        tag: element.tagName.toLowerCase(),
        content: element.innerText.trim().slice(0, 200),
        classes: Array.from(element.classList),
        attributes: Object.assign({}, ...Array.from(element.attributes).map(attr => ({ [attr.name]: attr.value }))),
        parent_tag: element.parentElement ? element.parentElement.tagName.toLowerCase() : null,
        child_tags: Array.from(element.children).map(child => child.tagName.toLowerCase()),
        html: element.outerHTML
    };
    
    // Send data back to parent window
    if (window.opener && !window.opener.closed) {
        window.opener.postMessage({ selectedElement: selectedData }, '*');
    }
});

// Add visual feedback for hovering over elements
document.addEventListener('mouseover', function(e) {
    const element = e.target;
    element.style.outline = '2px solid #4f46e5';
    element.style.cursor = 'pointer';
});

document.addEventListener('mouseout', function(e) {
    const element = e.target;
    element.style.outline = '';
    element.style.cursor = '';
}); 