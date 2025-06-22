// LisPy Documentation Navigation

document.addEventListener('DOMContentLoaded', function() {
    initializeCollapsibleNavigation();
});

function initializeCollapsibleNavigation() {
    // Initially collapse all categories
    const categories = document.querySelectorAll('.nav-category');
    categories.forEach(category => {
        category.classList.add('collapsed');
        const functionsList = category.querySelector('.nav-functions');
        if (functionsList) {
            functionsList.style.display = 'none';
        }
    });
    
    // Add click handlers to category headers
    const categoryHeaders = document.querySelectorAll('.nav-category h4');
    
    categoryHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const category = this.parentElement;
            const functionsList = category.querySelector('.nav-functions');
            
            if (functionsList) {
                const isCollapsed = category.classList.contains('collapsed');
                
                if (isCollapsed) {
                    // Expand
                    category.classList.remove('collapsed');
                    functionsList.style.display = 'block';
                } else {
                    // Collapse
                    category.classList.add('collapsed');
                    functionsList.style.display = 'none';
                }
            }
        });
    });
    
    // Auto-expand active category
    setTimeout(() => {
        autoExpandActiveCategory();
    }, 50); // Small delay to ensure DOM is fully ready
}

function autoExpandActiveCategory() {
    const categories = document.querySelectorAll('.nav-category');
    
    // Check if we're on the index page
    const isIndexPage = window.location.pathname.endsWith('/') || 
                       window.location.pathname.endsWith('/index.html') ||
                       window.location.pathname === '/';
    
    if (isIndexPage) {
        // On index page, expand all categories
        categories.forEach(category => {
            const functionsList = category.querySelector('.nav-functions');
            if (functionsList) {
                category.classList.remove('collapsed');
                functionsList.style.display = 'block';
            }
        });
        return;
    }
    
    // Find the current category by looking for active links
    let currentCategory = null;
    categories.forEach(category => {
        const activeLink = category.querySelector('.nav-functions li.active a') || 
                          category.querySelector('.nav-functions a.active');
        if (activeLink) {
            currentCategory = category;
        }
    });
    
    if (currentCategory) {
        // Expand only the current category
        const functionsList = currentCategory.querySelector('.nav-functions');
        if (functionsList) {
            currentCategory.classList.remove('collapsed');
            functionsList.style.display = 'block';
        }
    }
} 