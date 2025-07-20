"""
HTML generation functionality for documentation.
"""

import json
import shutil
import urllib.parse
from pathlib import Path
from typing import Dict
from .models import FunctionDoc


class HTMLGenerator:
    """Generate HTML documentation."""
    
    def __init__(self, output_dir: Path, template_dir: Path, project_root: Path):
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.project_root = project_root
    
    def safe_filename(self, name: str) -> str:
        """Convert function name to safe filename using pure URL encoding approach."""
        # Use systematic URL encoding for all characters
        encoded = urllib.parse.quote(name, safe='')
        
        # Replace percent signs with underscores to make it more filename-friendly
        # This converts %XX sequences to _XX which is more readable
        filename_safe = encoded.replace('%', '_')
        
        # Ensure it starts with a letter or underscore (some filesystems don't like leading numbers)
        if filename_safe and filename_safe[0].isdigit():
            filename_safe = '_' + filename_safe
            
        return filename_safe

    def generate_site(self, docs: Dict[str, FunctionDoc]):
        """Generate the complete documentation site."""
        print(f"Generating documentation site with {len(docs)} functions...")
        
        self.setup_output_directory()
        self.copy_static_assets()
        self.generate_search_index(docs)
        self.generate_function_pages(docs)
        self.generate_index_page(docs)
        
        print(f"Documentation generated in: {self.output_dir}")
    
    def setup_output_directory(self):
        """Set up the output directory structure."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / 'functions').mkdir(exist_ok=True)
        (self.output_dir / 'special-forms').mkdir(exist_ok=True)
        (self.output_dir / 'assets').mkdir(exist_ok=True)
        (self.output_dir / 'assets' / 'css').mkdir(exist_ok=True)
        (self.output_dir / 'assets' / 'js').mkdir(exist_ok=True)
        (self.output_dir / 'assets' / 'images').mkdir(exist_ok=True)
    
    def copy_static_assets(self):
        """Copy CSS, JS, and other static assets."""
        source_css_dir = self.project_root / 'docs' / 'assets' / 'css'
        target_css_dir = self.output_dir / 'assets' / 'css'
        
        if source_css_dir.exists():
            for css_file in source_css_dir.glob('*.css'):
                target_file = target_css_dir / css_file.name
                shutil.copy2(css_file, target_file)
                print(f"Copied CSS: {css_file.name}")
        
        # Copy JS files if they exist
        source_js_dir = self.project_root / 'docs' / 'assets' / 'js'
        target_js_dir = self.output_dir / 'assets' / 'js'
        
        if source_js_dir.exists():
            for js_file in source_js_dir.glob('*.js'):
                target_file = target_js_dir / js_file.name
                shutil.copy2(js_file, target_file)
                print(f"Copied JS: {js_file.name}")
        
        # Copy image files if they exist
        source_images_dir = self.project_root / 'docs' / 'assets' / 'images'
        target_images_dir = self.output_dir / 'assets' / 'images'
        
        if source_images_dir.exists():
            for image_file in source_images_dir.glob('*'):
                if image_file.is_file():
                    target_file = target_images_dir / image_file.name
                    shutil.copy2(image_file, target_file)
                    print(f"Copied Image: {image_file.name}")
    
    def generate_search_index(self, docs: Dict[str, FunctionDoc]):
        """Generate JSON search index."""
        search_data = []
        for doc in docs.values():
            # Determine URL based on type
            if doc.type == 'special-form':
                url = f'/special-forms/{self.safe_filename(doc.name)}.html'
            else:
                url = f'/functions/{doc.category}/{self.safe_filename(doc.name)}.html'
                
            search_data.append({
                'name': doc.name,
                'symbol': doc.symbol,
                'category': doc.category,
                'description': doc.description,
                'type': doc.type,
                'url': url
            })
        
        search_file = self.output_dir / 'search-index.json'
        with open(search_file, 'w', encoding='utf-8') as f:
            json.dump(search_data, f, indent=2)
    
    def generate_function_pages(self, docs: Dict[str, FunctionDoc]):
        """Generate individual function documentation pages."""
        for doc in docs.values():
            self.generate_function_page(doc, docs)
    
    def generate_function_page(self, func_doc: FunctionDoc, all_docs: Dict[str, FunctionDoc]):
        """Generate HTML for individual function documentation."""
        # Create appropriate directory based on type
        if func_doc.type == 'special-form':
            output_dir = self.output_dir / 'special-forms'
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{self.safe_filename(func_doc.name)}.html"
        else:
            category_dir = self.output_dir / 'functions' / func_doc.category
            category_dir.mkdir(parents=True, exist_ok=True)
            output_file = category_dir / f"{self.safe_filename(func_doc.name)}.html"
        
        # Generate the HTML content
        html_content = self.render_function_template(func_doc, all_docs)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated: {output_file}")
    
    def render_function_template(self, func_doc: FunctionDoc, all_docs: Dict[str, FunctionDoc]) -> str:
        """Render the function documentation template."""
        # Generate examples HTML
        examples_html = ""
        for example in func_doc.examples:
            examples_html += f"""
            <div class="example">
                <pre><code class="language-lisp">{example['code']}</code></pre>
                {f'<div class="description">{example["description"]}</div>' if example['description'] else ''}
            </div>
            """
        
        notes_html = ""
        if func_doc.notes:
            notes_html = "<ul>" + "".join(f"<li>{note}</li>" for note in func_doc.notes) + "</ul>"
        
        see_also_html = ""
        if func_doc.see_also:
            see_also_html = ", ".join(f'<a href="../{ref}.html">{ref}</a>' for ref in func_doc.see_also)
        
        # Generate complete sidebar navigation (same as index page)
        categories = {}
        special_forms = []
        
        for doc in all_docs.values():
            if doc.type == 'special-form':
                special_forms.append(doc)
            else:
                if doc.category not in categories:
                    categories[doc.category] = []
                categories[doc.category].append(doc)
        
        sidebar_nav = ""
        
        # Add special forms section first
        if special_forms:
            form_links = ""
            for form in sorted(special_forms, key=lambda f: f.name):
                # Mark current form as active
                active_class = ' class="active"' if form.name == func_doc.name else ''
                # Determine correct path based on current doc type
                if func_doc.type == 'special-form':
                    link_path = f"{self.safe_filename(form.name)}.html"
                else:
                    link_path = f"../../special-forms/{self.safe_filename(form.name)}.html"
                form_links += f'<li{active_class}><a href="{link_path}">{form.symbol}</a></li>\n'
            
            sidebar_nav += f"""
            <div class="nav-category">
                <h4>Special Forms ({len(special_forms)})</h4>
                <ul class="nav-functions">
                    {form_links}
                </ul>
            </div>
            """
        
        # Add functions by category
        for category, funcs in sorted(categories.items()):
            func_links = ""
            for func in sorted(funcs, key=lambda f: f.name):
                # Mark current function as active
                active_class = ' class="active"' if func.name == func_doc.name else ''
                # Determine correct path based on current doc type
                if func_doc.type == 'special-form':
                    link_path = f"../functions/{category}/{self.safe_filename(func.name)}.html"
                else:
                    link_path = f"../../functions/{category}/{self.safe_filename(func.name)}.html"
                func_links += f'<li{active_class}><a href="{link_path}">{func.symbol}</a></li>\n'
            
            sidebar_nav += f"""
            <div class="nav-category">
                <h4>{category.title()} ({len(funcs)})</h4>
                <ul class="nav-functions">
                    {func_links}
                </ul>
            </div>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{func_doc.symbol} ({func_doc.name}) - LisPy Documentation</title>
    <link rel="stylesheet" href="../../assets/css/main.css">
    <link rel="stylesheet" href="../../assets/css/syntax.css">
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <div class="logo">
                <a href="../../index.html">
                    <img src="../../assets/images/logo.png" alt="LisPy Logo">
                </a>
            </div>
            
            <div class="search-section">
                <input type="text" id="search-input" placeholder="Search functions...">
                <div id="search-results"></div>
            </div>
            
            <div class="nav-section">
                {sidebar_nav}
            </div>
        </nav>
        
        <main class="content">
            <div class="function-header">
                <h1 class="function-symbol">{func_doc.symbol}</h1>
                <div class="function-meta">
                    <span class="category">{func_doc.category}</span>
                    <span class="type">{func_doc.type}</span>
                </div>
            </div>
            
            <section class="arguments">
                <h2>Arguments</h2>
                <pre><code class="language-lisp">{func_doc.arguments}</code></pre>
            </section>
            
            <section class="description">
                <h2>Description</h2>
                <p>{func_doc.description}</p>
            </section>
            
            {f'<section class="notes"><h2>Notes</h2>{notes_html}</section>' if func_doc.notes else ''}
            
            {f'<section class="examples"><h2>Examples</h2>{examples_html}</section>' if func_doc.examples else ''}
            
            {f'<section class="see-also"><h2>See Also</h2><p>{see_also_html}</p></section>' if func_doc.see_also else ''}
        </main>
    </div>
    
    <script src="../../assets/js/search.js"></script>
    <script src="../../assets/js/navigation.js"></script>
    <script src="../../assets/js/syntax-highlighter.js"></script>
</body>
</html>"""
    
    def generate_index_page(self, docs: Dict[str, FunctionDoc]):
        """Generate the main index page."""
        # Separate functions and special forms
        categories = {}
        special_forms = []
        
        for doc in docs.values():
            if doc.type == 'special-form':
                special_forms.append(doc)
            else:
                if doc.category not in categories:
                    categories[doc.category] = []
                categories[doc.category].append(doc)
        
        # Generate special forms section first
        category_sections = ""
        if special_forms:
            form_links = ""
            for form in sorted(special_forms, key=lambda f: f.name):
                form_links += f'<li><a href="special-forms/{self.safe_filename(form.name)}.html">{form.symbol}</a></li>\n'
            
            category_sections += f"""
            <div class="category-section">
                <h3>Special Forms ({len(special_forms)} forms)</h3>
                <ul class="function-list">
                    {form_links}
                </ul>
            </div>
            """
        
        # Generate category sections for functions
        for category, funcs in sorted(categories.items()):
            func_links = ""
            for func in sorted(funcs, key=lambda f: f.name):
                func_links += f'<li><a href="functions/{category}/{self.safe_filename(func.name)}.html">{func.symbol}</a></li>\n'
            
            category_sections += f"""
            <div class="category-section">
                <h3>{category.title()} ({len(funcs)} functions)</h3>
                <ul class="function-list">
                    {func_links}
                </ul>
            </div>
            """
        
        # Generate sidebar navigation - special forms first
        sidebar_nav = ""
        
        # Add special forms to sidebar first
        if special_forms:
            form_links = ""
            for form in sorted(special_forms, key=lambda f: f.name):
                form_links += f'<li><a href="special-forms/{self.safe_filename(form.name)}.html">{form.symbol}</a></li>\n'
            
            sidebar_nav += f"""
            <div class="nav-category">
                <h4>Special Forms ({len(special_forms)})</h4>
                <ul class="nav-functions">
                    {form_links}
                </ul>
            </div>
            """
        
        # Generate sidebar navigation for functions
        for category, funcs in sorted(categories.items()):
            func_links = ""
            for func in sorted(funcs, key=lambda f: f.name):
                func_links += f'<li><a href="functions/{category}/{self.safe_filename(func.name)}.html">{func.symbol}</a></li>\n'
            
            sidebar_nav += f"""
            <div class="nav-category">
                <h4>{category.title()} ({len(funcs)})</h4>
                <ul class="nav-functions">
                    {func_links}
                </ul>
            </div>
            """

        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LisPy Documentation</title>
    <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <div class="logo">
                <a href="index.html">
                    <img src="assets/images/logo.png" alt="LisPy Logo">
                </a>
            </div>
            
            <div class="search-section">
                <input type="text" id="search-input" placeholder="Search functions...">
                <div id="search-results"></div>
            </div>
            
            <div class="nav-section">
                {sidebar_nav}
            </div>
        </nav>
        
        <main class="content">
            <header class="header">
                <h1>LisPy Documentation</h1>
                <p>Comprehensive documentation for all LisPy functions and special forms.</p>
            </header>
            
            <div class="overview">
                <h2>Function Categories</h2>
                <div class="category-grid">
                    {category_sections}
                </div>
            </div>
        </main>
    </div>
    
    <script src="assets/js/search.js"></script>
    <script src="assets/js/navigation.js"></script>
    <script src="assets/js/syntax-highlighter.js"></script>
</body>
</html>"""
        
        index_file = self.output_dir / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"Generated index: {index_file}") 