/**
 * LisPy Syntax Highlighter
 * Tokenizes LisPy code and applies syntax highlighting CSS classes
 */

class LisPySyntaxHighlighter {
    constructor() {
        // Define token patterns - order matters!
        this.tokens = [
            // Comments
            { type: 'comment', pattern: /;[^\r\n]*/ },
            
            // Strings
            { type: 'string', pattern: /"(?:[^"\\]|\\.)*"/ },
            
            // Numbers (integers and floats)
            { type: 'number', pattern: /-?\d+(?:\.\d+)?/ },
            
            // Booleans
            { type: 'boolean', pattern: /\b(?:true|false)\b/ },
            
            // Nil
            { type: 'nil', pattern: /\bnil\b/ },
            
            // Parentheses and brackets (before operators to avoid conflicts)
            { type: 'punctuation', pattern: /[()[\]{}]/ },
            
            // Symbols/identifiers (including hyphenated names, question marks, etc.)
            // This will catch function names, special forms, and variables
            { type: 'symbol', pattern: /[a-zA-Z_][a-zA-Z0-9_\-?!*+/<>=]*/ },
            
            // Standalone operators (for cases like (+ 1 2) where + is not part of a larger symbol)
            { type: 'operator', pattern: /[+\-*/%=<>!&|]/ },
            
            // Whitespace
            { type: 'whitespace', pattern: /\s+/ }
        ];
    }
    
    tokenize(code) {
        const tokens = [];
        let remaining = code;
        let position = 0;
        
        while (remaining.length > 0) {
            let matched = false;
            
            for (const tokenDef of this.tokens) {
                const match = remaining.match(tokenDef.pattern);
                if (match && match.index === 0) {
                    const value = match[0];
                    
                    tokens.push({
                        type: tokenDef.type,
                        value: value,
                        position: position
                    });
                    
                    remaining = remaining.slice(value.length);
                    position += value.length;
                    matched = true;
                    break;
                }
            }
            
            if (!matched) {
                // If no pattern matches, treat as a regular character
                tokens.push({
                    type: 'text',
                    value: remaining[0],
                    position: position
                });
                remaining = remaining.slice(1);
                position += 1;
            }
        }
        
        return tokens;
    }
    
    highlight(code) {
        const tokens = this.tokenize(code);
        let html = '';
        
        // Post-process tokens to identify functions in function position
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];
            const prevToken = i > 0 ? tokens[i - 1] : null;
            
            // Check if this token is in function position (after opening paren, possibly with whitespace)
            const isInFunctionPosition = this.isInFunctionPosition(tokens, i);
            
            if (token.type === 'whitespace' || token.type === 'text') {
                html += this.escapeHtml(token.value);
            } else if ((token.type === 'symbol' || token.type === 'operator') && isInFunctionPosition) {
                // Anything in function position gets highlighted as a function
                html += `<span class="token function">${this.escapeHtml(token.value)}</span>`;
            } else {
                html += `<span class="token ${token.type}">${this.escapeHtml(token.value)}</span>`;
            }
        }
        
        return html;
    }
    
    isInFunctionPosition(tokens, currentIndex) {
        // Look backwards to see if we're immediately after an opening paren
        for (let i = currentIndex - 1; i >= 0; i--) {
            const token = tokens[i];
            
            if (token.type === 'whitespace') {
                continue; // Skip whitespace
            } else if (token.value === '(') {
                return true; // Found opening paren
            } else {
                return false; // Found something else, not in function position
            }
        }
        
        // If we reach the beginning without finding anything, check if we're at the start
        return currentIndex === 0 || (currentIndex === 1 && tokens[0].type === 'whitespace');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    highlightElement(element) {
        const code = element.textContent;
        element.innerHTML = this.highlight(code);
    }
    
    highlightAll() {
        // Find all code elements with language-lisp class
        const codeElements = document.querySelectorAll('code.language-lisp');
        
        codeElements.forEach(element => {
            this.highlightElement(element);
        });
    }
}

// Initialize syntax highlighting when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const highlighter = new LisPySyntaxHighlighter();
    highlighter.highlightAll();
});

// Export for potential use by other scripts
window.LisPySyntaxHighlighter = LisPySyntaxHighlighter; 