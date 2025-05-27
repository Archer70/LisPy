# LisPy Interpreter

A command-line interpreter for running LisPy programs with full module system support.

## Usage

### Running LisPy Files

```bash
# Run a LisPy program
python bin/lispy_interpreter.py program.lpy

# Or use the convenience launcher (Windows)
bin\lispy.bat program.lpy

# Or use the convenience launcher (Unix/Linux/macOS)
bin/lispy.sh program.lpy
```

### Interactive REPL Mode

```bash
# Start interactive mode
python bin/lispy_interpreter.py          # Default behavior
python bin/lispy_interpreter.py --repl   # Explicit REPL mode

# Or with launcher
bin\lispy.bat --repl        # Windows
bin/lispy.sh --repl         # Unix/Linux/macOS
```

### Command Line Options

```bash
python bin/lispy_interpreter.py [OPTIONS] [file.lpy]

Options:
  -h, --help                    Show help message
  --repl                        Start interactive REPL mode (default if no file)
  --version                     Show version information
  -I, --include-path PATH       Add directory to module load path
```

## Features

### Multi-File Programs

The interpreter supports multi-file LisPy programs using the module system:

```lisp
; main.lpy
(import "math-utils")
(import "string-utils" :as "str")

(define result (circle-area 5))
result
```

### Module Loading

- Modules are loaded from the current directory by default
- Additional load paths can be specified with `-I` option
- Module files should have `.lpy` extension
- Modules are cached to prevent duplicate loading

### Qualified Module Names

**The module system supports path-qualified imports to avoid naming conflicts:**

```lisp
; Import from specific subdirectories
(import "lib1/utils")     ; loads lib1/utils.lpy
(import "lib2/utils")     ; loads lib2/utils.lpy  
(import "math/advanced")  ; loads math/advanced.lpy

; Both modules can coexist
(lib1-function)  ; from lib1/utils
(lib2-function)  ; from lib2/utils
```

**Directory structure example:**
```
project/
├── main.lpy
├── lib1/
│   └── utils.lpy
├── lib2/
│   └── utils.lpy
└── math/
    └── advanced.lpy
```

**Namespace resolution:**
- **First-found wins**: `(import "utils")` loads the first `utils.lpy` found in search paths
- **Explicit paths**: `(import "lib1/utils")` specifically loads from `lib1/` directory
- **No conflicts**: Qualified imports allow multiple modules with same base name

### REPL Features

- Interactive evaluation of LisPy expressions
- Module imports work in REPL mode
- Exit with `exit`, `quit`, `(exit)`, `(quit)`, or Ctrl+C
- Error handling with helpful messages

## Examples

### Running a Simple Program

```bash
# Create hello.lpy
echo '(define greeting "Hello, LisPy!")' > hello.lpy
echo 'greeting' >> hello.lpy

# Run it
python bin/lispy_interpreter.py hello.lpy
# Output: Program result: Hello, LisPy!
```

### Multi-Module Program

```bash
# Run the demo program
python bin/lispy_interpreter.py examples/main.lpy
```

### Avoiding Module Conflicts

```bash
# Create conflicting modules
mkdir lib1 lib2
echo '(define version "v1") (export version)' > lib1/config.lpy
echo '(define version "v2") (export version)' > lib2/config.lpy

# Use qualified imports to avoid conflicts
echo '(import "lib1/config" :as "cfg1")' > main.lpy
echo '(import "lib2/config" :as "cfg2")' >> main.lpy
echo '(list cfg1/version cfg2/version)' >> main.lpy

python bin/lispy_interpreter.py main.lpy
# Output: Program result: [v1 v2]
```

### Interactive Session

**Multiple ways to start REPL mode:**

```bash
# Explicit REPL mode
python bin/lispy_interpreter.py --repl

# Default behavior (no arguments)
python bin/lispy_interpreter.py

# Using launchers
bin\lispy.bat --repl        # Windows
bin/lispy.sh --repl         # Unix/Linux/macOS
```

**Example REPL session:**

```bash
python bin/lispy_interpreter.py --repl
# LisPy Interactive Interpreter
# Type expressions to evaluate them, or 'exit' to quit.
# Use (import "module-name") to load modules.
# 
# lispy> (+ 2 3)
# => 5
# lispy> (define x 10)
# => nil
# lispy> (* x x)
# => 100
# lispy> (import "math-utils")
# => nil
# lispy> (circle-area 3)
# => 28.2743338823
# lispy> exit
# Goodbye!
```

### Using Include Paths

```bash
# Add custom module directories
python bin/lispy_interpreter.py -I ./lib -I ./modules main.lpy
```

## Error Handling

The interpreter provides clear error messages for:

- File not found errors
- Syntax errors in LisPy code
- Runtime evaluation errors
- Module loading errors

Example:
```bash
python bin/lispy_interpreter.py nonexistent.lpy
# Error: File 'C:\path\to\nonexistent.lpy' not found.
```

## Integration with Development Workflow

### Testing Programs

```bash
# Run your program
python bin/lispy_interpreter.py my-program.lpy

# Run tests
python -m unittest discover -s tests -p '*_test.py'
```

### Development Tips

1. Use the REPL for quick testing and experimentation
2. Organize code into modules for better structure
3. Use qualified imports (`"dir/module"`) to avoid naming conflicts
4. Use the `-I` option to set up custom library paths
5. The interpreter automatically adds the program's directory to the module path

## Technical Details

### Module Resolution

1. Current directory of the executed file
2. Directories specified with `-I` option
3. Modules are resolved by filename (e.g., `"math-utils"` → `math-utils.lpy`)
4. Qualified names use path separators (e.g., `"lib/utils"` → `lib/utils.lpy`)

### Namespace Behavior

- **Unqualified imports**: `(import "utils")` searches all paths, first-found wins
- **Qualified imports**: `(import "lib1/utils")` loads specifically from `lib1/` directory
- **Caching**: Each unique module path is cached separately
- **No shadowing warnings**: Silent conflicts with unqualified imports

### Environment

- Each program runs with a fresh global environment
- Built-in functions are available by default
- Modules share the same environment space within a program

### Performance

- Modules are cached after first load
- Circular dependency detection prevents infinite loops
- Minimal overhead for small programs 