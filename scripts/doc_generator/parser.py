"""
Documentation parsing functionality.
"""

from typing import List, Dict
from .models import FunctionDoc


class DocumentationParser:
    """Parse documentation strings into structured data."""
    
    def parse_function_doc(self, doc_string: str, func_name: str, category: str, file_path: str, doc_type: str = "function") -> FunctionDoc:
        """Parse a documentation string into a FunctionDoc object."""
        lines = doc_string.strip().split('\n')
        
        # Extract basic info
        function_line = lines[0] if lines else f"Function: {func_name}"
        symbol = self.extract_symbol(function_line, func_name)
        arguments = self.extract_arguments(lines)
        description = self.extract_description(lines)
        examples = self.extract_examples(lines)
        notes = self.extract_notes(lines)
        see_also = self.extract_see_also(lines)
        
        return FunctionDoc(
            name=func_name,
            symbol=symbol,
            type=doc_type,
            category=category,
            arguments=arguments,
            description=description,
            examples=examples,
            notes=notes,
            see_also=see_also,
            file_path=file_path
        )
    
    def extract_symbol(self, function_line: str, func_name: str) -> str:
        """Extract the symbol from the function line."""
        # Look for "Function: symbol" pattern
        if ':' in function_line:
            symbol = function_line.split(':', 1)[1].strip()
            return symbol if symbol else func_name
        return func_name
    
    def extract_arguments(self, lines: List[str]) -> str:
        """Extract the arguments pattern."""
        for line in lines:
            if line.strip().startswith('Arguments:'):
                return line.split(':', 1)[1].strip()
        return ""
    
    def extract_description(self, lines: List[str]) -> str:
        """Extract the description."""
        for line in lines:
            if line.strip().startswith('Description:'):
                return line.split(':', 1)[1].strip()
        return ""
    
    def extract_examples(self, lines: List[str]) -> List[Dict[str, str]]:
        """Extract examples from the documentation."""
        examples = []
        in_examples = False
        current_example_lines = []
        
        # Section headers that indicate end of examples
        section_headers = [
            'Notes:', 'See also:', 'See Also:', 'Error Handling:', 'Use Cases:', 
            'Delay Pattern:', 'Step Forms:', 'Behavior:', 'Implementation:', 
            'Return Values:', 'Arguments:', 'Description:'
        ]
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('Examples:'):
                in_examples = True
                continue
            
            if in_examples:
                # Check if this line starts any section header
                if any(stripped.startswith(header) for header in section_headers):
                    # End of examples section - save any current example
                    if current_example_lines:
                        examples.append({
                            'code': '\n'.join(current_example_lines),
                            'result': '',
                            'description': ''
                        })
                    break
                
                # Check if this is a blank/whitespace line (example separator)
                if not stripped:
                    # Save current example if we have one
                    if current_example_lines:
                        examples.append({
                            'code': '\n'.join(current_example_lines),
                            'result': '',
                            'description': ''
                        })
                        current_example_lines = []
                else:
                    # Add non-empty line to current example
                    current_example_lines.append(stripped)
        
        # Don't forget the last example if the section ends without a blank line
        if current_example_lines:
            examples.append({
                'code': '\n'.join(current_example_lines),
                'result': '',
                'description': ''
            })
        
        return examples
    
    def extract_notes(self, lines: List[str]) -> List[str]:
        """Extract notes from the documentation."""
        notes = []
        in_notes = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('Notes:'):
                in_notes = True
                continue
            
            if in_notes:
                if stripped.startswith('See also:') or stripped.startswith('Examples:'):
                    break
                
                if stripped and stripped.startswith('-'):
                    notes.append(stripped[1:].strip())
                elif stripped and not stripped.startswith('  '):
                    notes.append(stripped)
        
        return notes
    
    def extract_see_also(self, lines: List[str]) -> List[str]:
        """Extract see also references."""
        see_also = []
        in_see_also = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('See also:'):
                in_see_also = True
                # Check if there's content on the same line
                content = stripped.split(':', 1)[1].strip()
                if content:
                    see_also.extend([func.strip() for func in content.split(',')])
                continue
            
            if in_see_also:
                if stripped.startswith('Notes:') or stripped.startswith('Examples:'):
                    break
                
                if stripped:
                    see_also.extend([func.strip() for func in stripped.split(',')])
        
        return [func for func in see_also if func] 