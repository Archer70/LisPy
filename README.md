# LisPy 🚀

**A modern, feature-rich Lisp interpreter with a powerful module system**

LisPy brings the elegance of Lisp to the modern world with clean syntax, comprehensive data structures, and a robust module system that makes building real applications a joy.

[![Tests](https://img.shields.io/badge/tests-359%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Why LisPy?

- **🎯 Simple yet Powerful**: Clean Lisp syntax with modern conveniences
- **🔒 Immutable by Default**: All data operations return new structures - no accidental mutations!
- **🚀 Tail Call Optimization**: Deep recursion without stack overflow - handle thousands of recursive calls!
- **📦 Module System**: Organize code across files with imports and exports
- **🏗️ Rich Data Types**: Vectors, hash maps, and more built-in
- **⚡ Interactive REPL**: Instant feedback for rapid development
- **🔧 Easy to Extend**: Add new functions and features effortlessly
- **📚 Well Tested**: 367+ tests ensure reliability

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/your-username/LisPy.git
cd LisPy
```

### Hello, World!

```bash
# Start the REPL
python bin/lispy_interpreter.py --repl

# Or run a file
echo "(define greeting 42) greeting" > hello.lpy
python bin/lispy_interpreter.py hello.lpy
```

## 🎨 Language Features

### Core Syntax

```lisp
; Variables and functions
(define pi 3.14159)
(define square (fn [x] (* x x)))
(square 5)  ; => 25

; Conditionals and logic
(if (> 10 5) "yes" "no")  ; => "yes"
(and true false)          ; => false
(or true false)           ; => true
```

### Rich Data Structures (Immutable!)

```lisp
; Vectors (arrays) - operations return NEW vectors
(define numbers [1 2 3 4 5])
(first numbers)    ; => 1
(rest numbers)     ; => [2 3 4 5] (new vector, numbers unchanged)
(count numbers)    ; => 5
(conj numbers 6)   ; => [1 2 3 4 5 6] (new vector, numbers unchanged)

; Hash Maps (dictionaries) - operations return NEW maps
(define person {:name "Alice" :age 30 :city "NYC"})
(get person :name)  ; => "Alice"
(assoc person :job "Engineer")  ; => NEW map with job added, person unchanged
(dissoc person :city)           ; => NEW map without city, person unchanged
```

### Powerful Module System

LisPy's module system enables clean code organization with explicit imports and exports, supporting multiple import styles and namespace management.

**Key Features:**
- 🔒 **Explicit Exports**: Only export what you want to be public
- 🏷️ **Multiple Import Styles**: Basic, prefixed, and selective imports
- 📁 **Qualified Names**: Avoid conflicts with path-based module names
- 🔄 **Circular Dependency Detection**: Prevents infinite import loops
- ⚡ **Module Caching**: Modules loaded once and cached for performance
- 🛣️ **Flexible Search Paths**: Configure where modules are found

#### Basic Module Creation and Import

**math-utils.lpy:**
```lisp
; Mathematical utilities module
(define pi 3.14159265359)
(define e 2.71828182846)

(define circle-area (fn [r] (* pi (* r r))))
(define circle-circumference (fn [r] (* 2 pi r)))
(define square (fn [x] (* x x)))
(define cube (fn [x] (* x x x)))

; Only export what you want to be public
(export pi e circle-area circle-circumference square cube)
```

**main.lpy:**
```lisp
; Import all exports into current namespace
(import "math-utils")

(define radius 5)
(define area (circle-area radius))        ; Direct access
(define circumference (circle-circumference radius))
```

#### Import Styles

**1. Basic Import (all exports)**
```lisp
(import "math-utils")
(circle-area 3)    ; Direct access to exported functions
(square 4)         ; All exports available
```

**2. Prefixed Import (namespace isolation)**
```lisp
(import "math-utils" :as "math")
(math/circle-area 3)    ; Prefixed access
(math/square 4)         ; Clear namespace separation
```

**3. Selective Import (cherry-picking)**
```lisp
(import "math-utils" :only (pi circle-area))
(circle-area 3)    ; Only imported functions available
; (square 4)       ; Error: square not imported
```

#### Qualified Module Names (Avoiding Conflicts)

**Directory structure:**
```
project/
├── main.lpy
├── geometry/
│   └── shapes.lpy
├── physics/
│   └── shapes.lpy
└── vendor/
    └── awesome-lib/
        └── utils.lpy
```

**Using qualified imports:**
```lisp
; Import from specific directories
(import "geometry/shapes" :as "geo")
(import "physics/shapes" :as "phys")
(import "vendor/awesome-lib/utils" :as "awesome")

; No naming conflicts
(geo/circle-area 5)
(phys/particle-collision obj1 obj2)
(awesome/helper-function data)
```

#### Real-World Module Organization

**config.lpy:**
```lisp
; Application configuration
(define app-name "MyLispyApp")
(define version "1.0.0")
(define debug-mode true)

(export app-name version debug-mode)
```

**utils/string.lpy:**
```lisp
; String utilities
(define length (fn [s] (count s)))
(define empty? (fn [s] (= (count s) 0)))

(export length empty?)
```

**models/user.lpy:**
```lisp
; User data model
(import "config")
(import "utils/string" :as "str")

(define create-user (fn [name email]
  (if (str/empty? name)
    nil
    {:name name :email email :created-at (current-time)})))

(define validate-user (fn [user]
  (and (get user :name) (get user :email))))

(export create-user validate-user)
```

**main.lpy:**
```lisp
; Main application
(import "config")
(import "models/user" :as "user")
(import "utils/string" :as "str")

; Use imported modules
(if debug-mode
  (println "Debug mode enabled"))

(define new-user (user/create-user "Alice" "alice@example.com"))
(if (user/validate-user new-user)
  (println "User created successfully"))
```

### Advanced Features

```lisp
; Functions and closures
(define make-adder (fn [x] 
  (fn [y] (+ x y))))

(define add-5 (make-adder 5))
(add-5 10)  ; => 15

; Recursive functions
(define factorial (fn [n]
  (if (<= n 1)
    1
    (* n (factorial (- n 1))))))

(factorial 5)  ; => 120
```

### Tail Call Optimization 🚀

LisPy automatically optimizes tail calls, enabling deep recursion without stack overflow:

```lisp
; Tail-recursive countdown - can handle huge numbers!
(define countdown (fn [n]
  (if (<= n 0)
    n
    (countdown (- n 1)))))  ; <- Tail call (last operation)

(countdown 10000)  ; => 0 (works perfectly!)

; Tail-recursive factorial with accumulator
(define factorial-tail (fn [n acc]
  (if (<= n 1)
    acc
    (factorial-tail (- n 1) (* n acc)))))  ; <- Optimized tail call

(define factorial (fn [n] (factorial-tail n 1)))
(factorial 1000)  ; => huge number (no stack overflow!)

; Even/odd checker using tail recursion
(define is-even (fn [n]
  (if (= n 0)
    true
    (if (= n 1)
      false
      (is-even (- n 2))))))  ; <- Tail call in conditional

(is-even 9999)  ; => false (handles large numbers easily)
```

**Key Benefits:**
- **🔄 Constant Stack Space**: Tail recursive functions use O(1) stack space
- **📈 Handle Large Inputs**: Process thousands of recursive calls safely  
- **⚡ Better Performance**: Faster than regular recursion
- **🎯 Automatic**: No special syntax needed - LisPy detects and optimizes automatically

## 🛠️ Command Line Interface

```bash
# Interactive REPL
python bin/lispy_interpreter.py --repl

# Run a program
python bin/lispy_interpreter.py program.lpy

# Add module search paths
python bin/lispy_interpreter.py -I ./lib -I ./vendor program.lpy

# Convenience launchers
bin/lispy.sh --repl          # Unix/Linux/macOS
bin\lispy.bat program.lpy    # Windows
```

### Module Search Paths

LisPy automatically searches for modules in:
1. **Current directory** of the executed file
2. **Additional paths** specified with `-I` option

```bash
# Example project structure
my-project/
├── main.lpy
├── lib/
│   ├── utils.lpy
│   └── math/
│       └── advanced.lpy
└── vendor/
    └── third-party/
        └── json.lpy

# Run with custom module paths
python bin/lispy_interpreter.py -I lib -I vendor main.lpy
```

**In main.lpy:**
```lisp
; These imports work because of the -I flags
(import "utils")                    ; From lib/utils.lpy
(import "math/advanced")            ; From lib/math/advanced.lpy  
(import "third-party/json")         ; From vendor/third-party/json.lpy
```

### Try It Yourself

LisPy includes working examples you can run immediately:

```bash
# Basic module usage
python bin/lispy_interpreter.py examples/main.lpy

# Comprehensive module demo showing all import styles
python bin/lispy_interpreter.py examples/module-demo.lpy

# Fibonacci with modules
python bin/lispy_interpreter.py examples/fibonacci.lpy

# Immutability demonstration
python bin/lispy_interpreter.py examples/immutability-demo.lpy

# Tail call optimization in action
python bin/lispy_interpreter.py examples/tail_call_optimization_demo.lpy
```

## 📁 Project Structure

```
LisPy/
├── bin/                     # Executable files
│   ├── lispy_interpreter.py # Main interpreter
│   ├── lispy.bat           # Windows launcher
│   └── lispy.sh            # Unix launcher
├── lispy/                  # Core language implementation
│   ├── lexer.py           # Tokenization
│   ├── parser.py          # AST generation
│   ├── evaluator.py       # Expression evaluation
│   ├── functions/         # Built-in functions
│   └── special_forms/     # Language constructs
├── examples/              # Example programs and modules
├── tests/                 # Comprehensive test suite
├── README.md              # This file
├── INTERPRETER.md         # Command-line usage guide
└── Requirements.md        # Language specification
```

## 🎯 Example Programs

### Fibonacci Sequence

```lisp
(define fib (fn [n]
  (if (<= n 1)
    n
    (+ (fib (- n 1)) (fib (- n 2))))))

; Calculate individual fibonacci numbers
(fib 0)   ; => 0
(fib 1)   ; => 1
(fib 5)   ; => 5
(fib 10)  ; => 55
```

### Data Processing (Immutable Operations)

```lisp
; Working with hash maps - all operations return NEW maps
(define user {:name "Alice" :age 30 :active true})

; Access and modify data (original user never changes!)
(get user :name)                    ; => "Alice"
(get user :age)                     ; => 30
(define user-with-city (assoc user :city "NYC"))     ; NEW map with city
(define user-without-active (dissoc user :active))   ; NEW map without active
; user is still {:name "Alice" :age 30 :active true}

; Working with vectors - all operations return NEW vectors
(define numbers [1 2 3 4 5])
(first numbers)                     ; => 1
(define without-first (rest numbers))        ; => [2 3 4 5] (NEW vector)
(count numbers)                     ; => 5
(define with-six (conj numbers 6))           ; => [1 2 3 4 5 6] (NEW vector)
; numbers is still [1 2 3 4 5]
```

### Module Best Practices

#### 1. Clear Export Boundaries
```lisp
; Good: Explicit exports
(define internal-helper (fn [x] (* x 2)))  ; Private function
(define public-api (fn [x] (internal-helper x)))

(export public-api)  ; Only export what's needed
```

#### 2. Namespace Prefixes for Clarity
```lisp
; When importing multiple modules with similar functions
(import "geometry/shapes" :as "geo")
(import "ui/shapes" :as "ui")

(geo/circle 5)    ; Geometric circle
(ui/circle 5)     ; UI circle widget
```

#### 3. Selective Imports for Performance
```lisp
; Import only what you need
(import "large-library" :only (specific-function))
```

#### 4. Module-Based Architecture Example
```lisp
; web-server.lpy
(import "http/router" :as "router")
(import "db/users" :as "users")
(import "utils/json" :as "json")

(define app (router/create))
(router/get app "/users" (fn [req] 
  (json/encode (users/find-all))))

(router/listen app 3000)
```

#### 5. Circular Dependency Prevention
```lisp
; Instead of circular imports, use a shared module
; shared/types.lpy
(define user-type {:name "" :email ""})
(export user-type)

; models/user.lpy
(import "shared/types" :only (user-type))

; services/auth.lpy  
(import "shared/types" :only (user-type))
```

## 🧪 Testing

LisPy comes with a comprehensive test suite:

```bash
# Run all tests
python -m unittest discover -s tests -p '*_test.py'

# Test specific components
python -m unittest tests.lexer_test
python -m unittest tests.module_system_test
```

## 📖 Documentation

- **[Language Tutorial](TUTORIAL.md)** - Comprehensive step-by-step learning guide
- **[Quick Reference](QUICK_REFERENCE.md)** - Concise syntax and function reference
- **[Language Guide](Requirements.md)** - Complete language reference
- **[Interpreter Guide](INTERPRETER.md)** - Command-line usage and options

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Write tests** for your changes
4. **Run the test suite**: `python -m unittest discover -s tests -p '*_test.py'`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/your-username/LisPy.git
cd LisPy

# Run tests to ensure everything works
python -m unittest discover -s tests -p '*_test.py'

# Start developing!
python bin/lispy_interpreter.py --repl
```

## 🎨 Language Philosophy

LisPy embraces the power and elegance of Lisp while adding modern conveniences:

- **Homoiconicity**: Code is data, enabling powerful metaprogramming
- **Functional Programming**: First-class functions and immutable data structures by default
- **Immutability First**: All data operations return new structures, preventing bugs
- **Modularity**: Clean separation of concerns with a robust module system
- **Simplicity**: Minimal syntax that's easy to learn and reason about
- **Extensibility**: Easy to add new features and customize behavior

## 🚧 Roadmap

- [ ] **Macros**: Compile-time code generation
- [ ] **Standard Library**: Common utilities and data structures
- [ ] **Package Manager**: Easy installation of third-party libraries
- [ ] **Performance**: Bytecode compilation and optimization
- [ ] **Interop**: Integration with Python libraries

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by classic Lisp dialects and modern functional languages
- Built with love for the elegance of symbolic computation
- Thanks to all contributors and the Lisp community

---

**Ready to explore the power of LisPy?** 

```bash
python bin/lispy_interpreter.py --repl
```

*Start your functional programming journey today!* 🎉 