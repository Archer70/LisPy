// LisPy Documentation Search

document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    // Determine the correct path to search-index.json based on current location
    const currentPath = window.location.pathname;
    let searchIndexPath;
    
    if (currentPath.includes('/functions/') || currentPath.includes('/special-forms/')) {
        // We're in a function or special form page (nested directory)
        searchIndexPath = '../../search-index.json';
    } else {
        // We're on the index page (root level)
        searchIndexPath = 'search-index.json';
    }
    
    // Load search index
    fetch(searchIndexPath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            searchInput.addEventListener('input', function() {
                const query = this.value.toLowerCase().trim();
                
                if (query.length === 0) {
                    searchResults.innerHTML = '';
                    searchResults.style.display = 'none';
                    return;
                }
                
                const results = data.filter(item => 
                    item.name.toLowerCase().includes(query) ||
                    item.symbol.toLowerCase().includes(query) ||
                    item.description.toLowerCase().includes(query)
                ).slice(0, 10); // Limit to 10 results
                
                if (results.length > 0) {
                    searchResults.innerHTML = results.map(item => {
                        // Convert absolute URLs to relative based on current context
                        let linkUrl = item.url;
                        if (currentPath.includes('/functions/') || currentPath.includes('/special-forms/')) {
                            // We're in a nested page, convert absolute URL to relative
                            if (linkUrl.startsWith('/')) {
                                linkUrl = '../..' + linkUrl;
                            }
                        } else {
                            // We're on index page, remove leading slash for relative path
                            if (linkUrl.startsWith('/')) {
                                linkUrl = linkUrl.substring(1);
                            }
                        }
                        
                        // Create display title - avoid redundancy when symbol and name are the same
                        let displayTitle;
                        if (item.symbol === item.name) {
                            displayTitle = item.symbol;
                        } else {
                            displayTitle = `${item.symbol} (${item.name})`;
                        }
                        
                        return `<div class="search-result">
                            <a href="${linkUrl}">${displayTitle}</a>
                            <div class="search-result-desc">${item.description.substring(0, 100)}...</div>
                        </div>`;
                    }).join('');
                    searchResults.style.display = 'block';
                } else {
                    searchResults.innerHTML = '<div class="no-results">No results found</div>';
                    searchResults.style.display = 'block';
                }
            });
        })
        .catch(error => {
            console.error('Error loading search index:', error);
            console.error('Attempted to load from:', searchIndexPath);
        });
} 