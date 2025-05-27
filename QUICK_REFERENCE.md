# LisPy Quick Reference

**A concise reference for LisPy syntax and functions**

This is a quick reference companion to the comprehensive [LisPy Tutorial](TUTORIAL.md). For detailed explanations and examples, see the tutorial.

## Basic Syntax

```lisp
; Comments start with semicolon
(function arg1 arg2 ...)    ; Function call
(+ 1 2 3)                   ; => 6
(* 2 (+ 3 4))              ; => 14 (nested expressions)
```

## Arithmetic Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| Addition | `(+ a b ...)` | `(+ 1 2 3)` | `6` |
| Subtraction | `(- a b ...)` | `(- 10 3 2)` | `5` |
| Multiplication | `(* a b ...)` | `(* 2 3 4)` | `24` |
| Division | `(/ a b ...)` | `(/ 20 4 2)` | `2.5` |

## Comparison Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| Equal | `(= a b)` | `(= 5 5)` | `true` |
| Less than | `(< a b)` | `(< 3 5)` | `true` |
| Greater than | `(> a b)` | `(> 8 2)` | `true` |
| Less/equal | `(<= a b)` | `(<= 4 4)` | `true` |
| Greater/equal | `(>= a b)` | `(>= 7 3)` | `true` |

## Logical Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| AND | `(and a b ...)` | `(and true false)` | `false` |
| OR | `(or a b ...)` | `(or true false)` | `true` |
| NOT | `(not a)` | `(not true)` | `false` |

## Variables and Functions

```lisp
; Define variable
(define name value)
(define pi 3.14159)

; Define function
(define function-name (fn [param1 param2] body))
(define square (fn [x] (* x x)))

; Call function
(square 5)  ; => 25
```

## Conditionals

```lisp
; If expression
(if condition then-value else-value)
(if (> 5 3) "yes" "no")  ; => "yes"

; Complex conditions
(if (and (> age 18) has-license) "can-drive" "cannot-drive")
```

## Data Structures

### Vectors

```lisp
; Create vector
[1 2 3 4 5]
["apple" "banana" "cherry"]

; Vector operations (ALL IMMUTABLE - return new vectors)
(first [1 2 3])     ; => 1
(rest [1 2 3])      ; => [2 3] (returns NEW vector)
(count [1 2 3])     ; => 3
(conj [1 2] 3)      ; => [1 2 3] (returns NEW vector)
(empty? [])         ; => true
```

### Hash Maps

```lisp
; Create hash map
{:name "Alice" :age 30}
{"key1" "value1" "key2" "value2"}

; Hash map operations (ALL IMMUTABLE - return new maps)
(get map key)           ; Get value
(assoc map key value)   ; Add/update key (returns NEW map)
(dissoc map key)        ; Remove key (returns NEW map)
(keys map)              ; Get all keys
(vals map)              ; Get all values
```

## Module System

### Creating Modules

```lisp
; In math-utils.lpy
(define pi 3.14159)
(define square (fn [x] (* x x)))
(export pi square)  ; Export public functions
```

### Using Modules

```lisp
; Basic import
(import "math-utils")
(square 5)

; Prefixed import
(import "math-utils" :as "math")
(math/square 5)

; Selective import
(import "math-utils" :only (pi))
```

## Immutability

**LisPy is immutable by default!** All data structure operations return new structures.

```lisp
; Hash maps
(define user {:name "Alice"})
(define updated (assoc user ':age 30))
; user is unchanged, updated is new map

; Vectors  
(define nums [1 2 3])
(define extended (conj nums 4))
; nums is unchanged, extended is new vector

; This prevents bugs and enables safe functional programming
```

## Common Patterns

### Recursion

```lisp
; Factorial
(define factorial (fn [n]
  (if (<= n 1) 1 (* n (factorial (- n 1))))))

; Process vector recursively
(define sum-vector (fn [vec]
  (if (empty? vec) 0
    (+ (first vec) (sum-vector (rest vec))))))
```

### Higher-Order Functions

```lisp
; Function that returns function
(define make-adder (fn [x] (fn [y] (+ x y))))
(define add-5 (make-adder 5))

; Function that takes function
(define apply-twice (fn [f x] (f (f x))))
```

## Built-in Functions Reference

### Arithmetic
- `+`, `-`, `*`, `/` - Basic arithmetic
- `=`, `<`, `>`, `<=`, `>=` - Comparisons

### Logic
- `and`, `or`, `not` - Boolean operations

### Data Structure Functions
- `first`, `rest`, `count`, `conj` - Vector operations
- `get`, `assoc`, `dissoc`, `keys`, `vals` - Hash map operations
- `empty?` - Check if collection is empty

### Control Flow
- `if` - Conditional expression
- `define` - Create variables and functions
- `fn` - Create anonymous functions

### Module System
- `import` - Import modules
- `export` - Export symbols from modules

## Command Line Usage

```bash
# Start REPL
python bin/lispy_interpreter.py --repl

# Run file
python bin/lispy_interpreter.py program.lpy

# Add module search paths
python bin/lispy_interpreter.py -I lib -I vendor program.lpy

# Convenience scripts
bin/lispy.sh --repl          # Unix/Linux/macOS
bin\lispy.bat program.lpy    # Windows
```

## Common Idioms

### Data Validation

```lisp
(define valid-user? (fn [user]
  (and (get user :name)
       (get user :email)
       (> (get user :age) 0))))
```

### Safe Operations

```lisp
(define safe-divide (fn [x y]
  (if (= y 0) nil (/ x y))))
```

### Data Transformation

```lisp
(define update-user (fn [user new-email]
  (assoc user :email new-email)))
```

### Collection Processing

```lisp
; Find element in vector
(define contains? (fn [vec item]
  (if (empty? vec) false
    (if (= (first vec) item) true
      (contains? (rest vec) item)))))
```

## Error Handling

LisPy uses return values for error handling:

```lisp
; Return nil for errors
(define safe-get (fn [map key]
  (if (get map key) (get map key) nil)))

; Use conditionals to check results
(define result (safe-divide 10 0))
(if result result "Division by zero!")
```

## Best Practices

1. **Embrace immutability**: LisPy is immutable by default - use it!
2. **Use descriptive names**: `calculate-area` not `calc`
3. **Keep functions small**: One responsibility per function
4. **Prefer pure functions**: Same input → same output
5. **Use modules**: Organize code into logical units
6. **Handle edge cases**: Check for empty vectors, nil values
7. **Comment complex logic**: Explain the "why", not the "what"

## Learning Path

1. **Start with basics**: Arithmetic, variables, simple functions
2. **Learn data structures**: Vectors and hash maps
3. **Master conditionals**: if expressions and boolean logic
4. **Practice recursion**: Essential for functional programming
5. **Explore modules**: Code organization and reuse
6. **Build projects**: Apply concepts in real programs

## Resources

- **[Complete Tutorial](TUTORIAL.md)** - Comprehensive learning guide
- **[Language Specification](Requirements.md)** - Detailed language reference
- **[Interpreter Guide](INTERPRETER.md)** - Command-line usage
- **[Examples](examples/)** - Working code examples
- **[Tests](tests/)** - See how features are tested

---

**Need more detail?** Check out the [comprehensive tutorial](TUTORIAL.md) for in-depth explanations and exercises! 