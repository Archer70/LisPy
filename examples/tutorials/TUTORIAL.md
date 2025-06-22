# LisPy Language Tutorial

**Learn LisPy from the ground up - A comprehensive guide to functional programming with Lisp**

Welcome to LisPy! This tutorial will take you from complete beginner to confident LisPy programmer. Each section builds on the previous one, so it's best to work through them in order.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Syntax and Expressions](#basic-syntax-and-expressions)
3. [Numbers and Arithmetic](#numbers-and-arithmetic)
4. [Variables and Definitions](#variables-and-definitions)
5. [Functions](#functions)
6. [Conditionals and Logic](#conditionals-and-logic)
7. [Data Structures](#data-structures)
8. [Working with Lists and Vectors](#working-with-lists-and-vectors)
9. [Hash Maps](#hash-maps)
10. [Advanced Functions](#advanced-functions)
11. [Recursion](#recursion)
12. [Immutability in LisPy](#immutability-in-lispy)
13. [Module System](#module-system)
14. [Best Practices](#best-practices)
15. [Common Patterns](#common-patterns)
16. [Next Steps](#next-steps)

---

## Getting Started

### What is LisPy?

LisPy is a modern Lisp dialect that combines the elegance of traditional Lisp with practical features for real-world programming. It features:

- Clean, minimal syntax
- Powerful functional programming capabilities
- Rich data structures (vectors, hash maps)
- Comprehensive module system
- Interactive REPL for rapid development

### Starting the REPL

The easiest way to learn LisPy is through the interactive REPL (Read-Eval-Print Loop):

```bash
python bin/lispy_interpreter.py --repl
```

You'll see:
```
LisPy Interactive Interpreter
Type expressions to evaluate them, or 'exit' to quit.
Use (import "module-name") to load modules.

lispy> 
```

Try typing `(+ 2 3)` and press Enter. You should see `=> 5`.

---

## Basic Syntax and Expressions

### The Power of Parentheses

LisPy uses a simple, consistent syntax based on parentheses. Everything is an expression that returns a value.

**Basic Structure:**
```lisp
(function argument1 argument2 ...)
```

**Examples:**
```lisp
; This is a comment
(+ 1 2)          ; => 3
(* 4 5)          ; => 20
(- 10 3)         ; => 7
(/ 15 3)         ; => 5
```

**Try it yourself:**
```lisp
lispy> (+ 1 2 3 4)
=> 10

lispy> (* 2 (+ 3 4))
=> 14
```

### Key Concepts

1. **Prefix Notation**: The operator comes first: `(+ 1 2)` not `1 + 2`
2. **Nested Expressions**: You can nest expressions: `(* 2 (+ 3 4))`
3. **Everything Returns a Value**: Every expression evaluates to something

---

## Numbers and Arithmetic

LisPy supports integers and floating-point numbers with standard arithmetic operations.

### Basic Arithmetic

```lisp
; Addition
(+ 5 3)          ; => 8
(+ 1 2 3 4 5)    ; => 15 (multiple arguments)

; Subtraction  
(- 10 4)         ; => 6
(- 20 5 3)       ; => 12

; Multiplication
(* 6 7)          ; => 42
(* 2 3 4)        ; => 24

; Division
(/ 15 3)         ; => 5
(/ 20 4 2)       ; => 2.5
```

### Comparison Operations

```lisp
; Equality
(= 5 5)          ; => true
(= 3 4)          ; => false

; Inequality
(< 3 5)          ; => true
(> 8 2)          ; => true
(<= 4 4)         ; => true
(>= 7 3)         ; => true
```

**Exercise:** Calculate the area of a circle with radius 5. (Hint: area = π × r²)
```lisp
; π is approximately 3.14159
(* 3.14159 (* 5 5))
```

---

## Variables and Definitions

### Creating Variables

Use `define` to create variables:

```lisp
(define pi 3.14159)
(define radius 5)
(define area (* pi (* radius radius)))

; Use the variables
area                 ; => 78.53975
```

### Variable Naming

- Use descriptive names: `user-count` not `uc`
- Use hyphens for multi-word names: `circle-area`
- Variables are case-sensitive: `myVar` and `myvar` are different

```lisp
(define user-name "Alice")
(define user-age 30)
(define is-admin true)
```

**Exercise:** Create variables for your name, age, and favorite number, then use them in expressions.

---

## Functions

Functions are the heart of LisPy. They're first-class values that can be passed around and combined.

### Creating Functions

```lisp
; Basic function syntax
(define function-name (fn [parameter1 parameter2] body))

; Example: square function
(define square (fn [x] (* x x)))

; Use the function
(square 5)           ; => 25
(square 10)          ; => 100
```

### Functions with Multiple Parameters

```lisp
; Rectangle area function
(define rectangle-area (fn [width height] 
  (* width height)))

(rectangle-area 4 6) ; => 24

; Greeting function
(define greet (fn [name] 
  name))             ; Simplified - just returns the name

(greet "Alice")      ; => "Alice"
```

### Anonymous Functions

You can use functions without naming them:

```lisp
; Anonymous function
((fn [x] (* x 2)) 5) ; => 10

; Useful for short operations
(define double (fn [x] (* x 2)))
(double 7)           ; => 14
```

**Exercise:** Create a function that calculates the volume of a cube (volume = side³).

---

## Conditionals and Logic

### The `if` Expression

```lisp
; Basic if: (if condition then-value else-value)
(if true "yes" "no")     ; => "yes"
(if false "yes" "no")    ; => "no"

; With variables
(define age 25)
(if (>= age 18) "adult" "minor")  ; => "adult"
```

### Boolean Operations

```lisp
; Logical AND
(and true true)      ; => true
(and true false)     ; => false

; Logical OR
(or true false)      ; => true
(or false false)     ; => false

; Logical NOT
(not true)           ; => false
(not false)          ; => true
```

### Complex Conditions

```lisp
(define check-access (fn [age has-permission]
  (if (and (>= age 18) has-permission)
    "access granted"
    "access denied")))

(check-access 25 true)   ; => "access granted"
(check-access 16 true)   ; => "access denied"
```

**Exercise:** Create a function that determines if a number is positive, negative, or zero.

---

## Data Structures

LisPy provides rich data structures for organizing information.

### Vectors (Arrays)

Vectors are ordered collections of values:

```lisp
; Creating vectors
[1 2 3 4 5]          ; => [1 2 3 4 5]
["apple" "banana" "cherry"]  ; => ["apple" "banana" "cherry"]
[1 "hello" true]     ; => [1 "hello" true] (mixed types)

; Empty vector
[]                   ; => []
```

### Vector Operations

```lisp
(define numbers [1 2 3 4 5])

; Get first element
(first numbers)      ; => 1

; Get all but first (rest)
(rest numbers)       ; => [2 3 4 5]

; Count elements
(count numbers)      ; => 5

; Add element to front
(conj numbers 0)     ; => [0 1 2 3 4 5]
```

### Hash Maps (Dictionaries)

Hash maps store key-value pairs:

```lisp
; Creating hash maps
{:name "Alice" :age 30 :city "NYC"}

; Keys can be keywords (start with :) or strings
{"name" "Bob" "age" 25}

; Mixed keys
{:id 123 "name" "Charlie" :active true}
```

### Hash Map Operations

```lisp
(define person {:name "Alice" :age 30 :city "NYC"})

; Get value by key
(get person :name)   ; => "Alice"
(get person :age)    ; => 30

; Add/update key
(assoc person :job "Engineer")  ; => {:name "Alice" :age 30 :city "NYC" :job "Engineer"}

; Remove key
(dissoc person :city)  ; => {:name "Alice" :age 30}

; Get all keys
(keys person)        ; => [:name :age :city]

; Get all values  
(vals person)        ; => ["Alice" 30 "NYC"]
```

**Exercise:** Create a hash map representing a book with title, author, year, and page count.

---

## Working with Lists and Vectors

### Building and Manipulating Vectors

**Important**: All vector operations in LisPy are **immutable** - they return new vectors without modifying the original.

```lisp
; Start with empty vector and build up - each step creates a NEW vector
(define empty-vec [])
(define with-one (conj empty-vec 1))      ; => [1] (empty-vec still [])
(define with-two (conj with-one 2))       ; => [1 2] (with-one still [1])

; Working with existing vectors
(define fruits ["apple" "banana" "cherry"])

; Check if empty
(empty? fruits)      ; => false
(empty? [])          ; => true

; Get specific elements - these operations return NEW vectors
(first fruits)       ; => "apple" (fruits unchanged)
(rest fruits)        ; => ["banana" "cherry"] (fruits unchanged)
(first (rest fruits)) ; => "banana"

; Verify immutability
fruits               ; Still ["apple" "banana" "cherry"]
```

### Processing Vectors

```lisp
; Count elements
(define scores [85 92 78 96 88])
(count scores)       ; => 5

; Check for elements (when implemented)
; For now, we work with first/rest
(define has-high-score (fn [scores]
  (if (empty? scores)
    false
    (if (> (first scores) 90)
      true
      (has-high-score (rest scores))))))

(has-high-score scores)  ; => true (92 and 96 are > 90)
```

**Exercise:** Create a vector of your favorite colors and practice using first, rest, and count.

---

## Hash Maps

### Real-World Hash Map Usage

```lisp
; User profile
(define user {
  :id 12345
  :username "alice_dev"
  :email "alice@example.com"
  :preferences {:theme "dark" :language "en"}
  :active true
})

; Accessing nested data
(get user :username)                    ; => "alice_dev"
(get (get user :preferences) :theme)    ; => "dark"
```

### Updating Hash Maps

**Important**: All hash map operations in LisPy are **immutable** - they return new maps without modifying the original.

```lisp
; Add new field - returns NEW map, original unchanged
(define updated-user (assoc user ':last-login "2024-01-15"))

; Update existing field - returns NEW map, original unchanged
(define deactivated-user (assoc user ':active false))

; Remove field - returns NEW map, original unchanged
(define minimal-user (dissoc user ':preferences))

; Multiple updates (when chaining) - each step creates a new map
(define new-user (assoc (assoc user ':role "admin") ':verified true))

; Verify immutability
user            ; Original is unchanged!
updated-user    ; New map with added field
```

### Working with Keys and Values

```lisp
(define inventory {
  :apples 50
  :bananas 30
  :oranges 25
})

; Get all product names
(keys inventory)     ; => [:apples :bananas :oranges]

; Get all quantities
(vals inventory)     ; => [50 30 25]

; Check if key exists
(get inventory :apples)    ; => 50 (exists)
(get inventory :grapes)    ; => nil (doesn't exist)
```

**Exercise:** Create an inventory system with at least 5 items and practice adding, removing, and updating items.

---

## Advanced Functions

### Higher-Order Functions

Functions that take other functions as arguments or return functions:

```lisp
; Function that returns a function
(define make-adder (fn [x]
  (fn [y] (+ x y))))

(define add-5 (make-adder 5))
(add-5 10)           ; => 15
(add-5 3)            ; => 8

; Function that takes a function
(define apply-twice (fn [f x]
  (f (f x))))

(define square (fn [x] (* x x)))
(apply-twice square 3)  ; => 81 (3² = 9, 9² = 81)
```

### Closures

Functions can "capture" variables from their surrounding scope:

```lisp
(define make-counter (fn [start]
  (define current start)
  (fn []
    (define old current)
    (set! current (+ current 1))
    old)))

; Note: set! is not implemented yet, so this is conceptual
; But the closure concept is important
```

### Partial Application

```lisp
; Create specialized functions
(define multiply (fn [x y] (* x y)))
(define double (fn [x] (multiply 2 x)))
(define triple (fn [x] (multiply 3 x)))

(double 7)           ; => 14
(triple 4)           ; => 12
```

**Exercise:** Create a function that makes "greeter" functions for different languages.

---

## Recursion

Recursion is a fundamental technique in functional programming where functions call themselves.

### Basic Recursion

```lisp
; Factorial: n! = n × (n-1) × (n-2) × ... × 1
(define factorial (fn [n]
  (if (<= n 1)
    1
    (* n (factorial (- n 1))))))

(factorial 5)        ; => 120
(factorial 0)        ; => 1

; Note: This regular recursion is limited to prevent stack overflow
; For large values, use the recur-based version below
```

### Fibonacci Sequence

```lisp
; Fibonacci: F(n) = F(n-1) + F(n-2)
(define fib (fn [n]
  (if (<= n 1)
    n
    (+ (fib (- n 1)) (fib (- n 2))))))

(fib 0)              ; => 0
(fib 1)              ; => 1
(fib 5)              ; => 5
(fib 10)             ; => 55

; Note: This is not tail-recursive and will be slow for large n
; See the tail-recursive version with recur below
```

### Recursion with Lists

```lisp
; Sum all numbers in a vector
(define sum-vector (fn [vec]
  (if (empty? vec)
    0
    (+ (first vec) (sum-vector (rest vec))))))

(sum-vector [1 2 3 4 5])  ; => 15

; Find maximum in a vector
(define max-vector (fn [vec]
  (if (empty? (rest vec))
    (first vec)
    (define rest-max (max-vector (rest vec)))
    (if (> (first vec) rest-max)
      (first vec)
      rest-max))))

(max-vector [3 7 2 9 1])  ; => 9
```

### Explicit Tail Calls with `recur`

**LisPy provides explicit tail call optimization using the `recur` special form!** This means functions using `recur` can handle very large inputs without stack overflow.

#### What is `recur`?

`recur` is a special form that performs an explicit tail call to the current function. It can only be used in tail position (the last expression to be evaluated) and restarts the function with new argument values.

```lisp
; Tail-recursive factorial using recur - OPTIMIZED by LisPy
(define factorial-tail (fn [n acc]
  (if (<= n 1)
    acc
    (recur (- n 1) (* n acc)))))  ; <- Explicit tail call with recur

(define factorial (fn [n] (factorial-tail n 1)))

; This can handle very large numbers!
(factorial 1000)    ; Works perfectly thanks to recur
```

#### Comparison: Regular Recursion vs `recur`

```lisp
; Regular recursion (limited by stack size)
(define factorial-regular (fn [n]
  (if (<= n 1)
    1
    (* n (factorial-regular (- n 1))))))  ; <- Regular recursion

; Limited to prevent stack overflow
(factorial-regular 5)    ; => 120 (works)
; (factorial-regular 200) ; => RecursionError (hits depth limit)

; Tail recursive with recur (optimized by LisPy)
(define factorial-tail (fn [n acc]
  (if (<= n 1)
    acc
    (recur (- n 1) (* n acc)))))  ; <- Explicit tail call with recur

(define factorial (fn [n] (factorial-tail n 1)))

; Can handle very large numbers
(factorial 200)     ; => huge number (works perfectly!)
```

#### Deep Recursion Examples with `recur`

```lisp
; Countdown using recur - can handle huge numbers
(define countdown (fn [n]
  (if (<= n 0)
    n
    (recur (- n 1)))))

(countdown 10000)   ; => 0 (works thanks to recur!)

; Even/odd checker using recur
(define is-even (fn [n]
  (if (= n 0)
    true
    (if (= n 1)
      false
      (recur (- n 2))))))

(is-even 9999)      ; => false (works with large numbers!)

; Tail-recursive Fibonacci using recur
(define fib-tail (fn [n a b]
  (if (= n 0)
    a
    (recur (- n 1) b (+ a b)))))

(define fib-fast (fn [n] (fib-tail n 0 1)))

(fib-fast 100)      ; => very large number (much faster than regular fib!)
```

#### `recur` in Conditionals

`recur` works in any tail position, including conditional branches:

```lisp
(define process-list (fn [lst result]
  (if (empty? lst)
    result                                    ; <- Tail position
    (recur (rest lst)                         ; <- Explicit tail call with recur
           (conj result (first lst))))))

; Sum with early termination
(define sum-until-negative (fn [lst acc]
  (if (empty? lst)
    acc
    (define current (first lst))
    (if (< current 0)
      acc                                     ; <- Return early
      (recur (rest lst) (+ acc current))))))  ; <- Continue with recur
```

#### Benefits of `recur`

1. **Constant Stack Space**: No stack overflow on deep recursion
2. **Better Performance**: Faster than regular recursion
3. **Explicit Control**: You decide when to use tail call optimization
4. **Stack Safety**: Regular recursion is limited to prevent crashes
5. **Functional Programming**: Enables idiomatic recursive algorithms

#### Writing Functions with `recur`

**Pattern**: Accumulator parameter

```lisp
; Convert regular recursion to tail recursion using accumulator and recur
; Regular (not tail recursive):
(define sum-list (fn [lst]
  (if (empty? lst)
    0
    (+ (first lst) (sum-list (rest lst))))))

; Tail recursive version with recur:
(define sum-list-tail (fn [lst acc]
  (if (empty? lst)
    acc
    (recur (rest lst) (+ acc (first lst))))))

(define sum-list (fn [lst] (sum-list-tail lst 0)))
```

#### `recur` Rules and Best Practices

1. **Tail Position Only**: `recur` can only be used in tail position
2. **Same Arity**: `recur` must be called with the same number of arguments as the function parameters
3. **Current Function Only**: `recur` always calls the current function, not other functions
4. **Use for Performance**: Use `recur` when you need to handle large recursive calls

```lisp
; ✅ Good: recur in tail position
(define countdown (fn [n]
  (if (<= n 0)
    n
    (recur (- n 1)))))

; ❌ Bad: recur not in tail position
(define bad-example (fn [n]
  (if (<= n 0)
    n
    (+ 1 (recur (- n 1))))))  ; Error: recur not in tail position

; ❌ Bad: wrong arity
(define wrong-arity (fn [x y]
  (if (= x 0)
    y
    (recur x))))  ; Error: function takes 2 args, recur called with 1
```

**Exercise:** Write a tail-recursive function using `recur` to calculate the length of a vector without using `count`.

---

## Immutability in LisPy

**LisPy is immutable by default!** This is one of its greatest strengths for functional programming.

### What Does Immutability Mean?

Immutability means that data structures cannot be changed after they're created. Instead of modifying existing data, operations return new data structures with the desired changes.

### Why Immutability Matters

1. **Prevents Bugs**: No accidental data modification
2. **Enables Safe Sharing**: Data can be safely passed between functions
3. **Supports Functional Programming**: Pure functions with predictable behavior
4. **Thread Safety**: Immutable data is inherently thread-safe
5. **Easier Reasoning**: Code behavior is more predictable

### Immutable Operations in LisPy

#### Hash Maps
```lisp
(define user {:name "Alice" :age 30})

; These operations return NEW maps
(define user-with-city (assoc user ':city "NYC"))
(define user-without-age (dissoc user ':age))
(define updated-user (assoc user ':age 31))

; Original is NEVER modified
user                ; Still {:name "Alice" :age 30}
user-with-city      ; {:name "Alice" :age 30 :city "NYC"}
user-without-age    ; {:name "Alice"}
updated-user        ; {:name "Alice" :age 31}
```

#### Vectors
```lisp
(define numbers [1 2 3])

; These operations return NEW vectors
(define with-four (conj numbers 4))
(define without-first (rest numbers))

; Original is NEVER modified
numbers             ; Still [1 2 3]
with-four           ; [1 2 3 4]
without-first       ; [2 3]
```

#### Lists
```lisp
(define items '(a b c))

; These operations return NEW lists
(define with-x (conj items 'x))
(define without-first (rest items))

; Original is NEVER modified
items               ; Still (a b c)
with-x              ; (x a b c)
without-first       ; (b c)
```

### Immutable Programming Patterns

#### Building Data Incrementally
```lisp
; Start with empty and build up
(define empty-config {})
(define with-theme (assoc empty-config ':theme "dark"))
(define with-lang (assoc with-theme ':language "en"))
(define full-config (assoc with-lang ':notifications true))

; Each step creates a new map
full-config         ; {:theme "dark" :language "en" :notifications true}
```

#### Updating Nested Structures
```lisp
; Update nested data immutably
(define user {:profile {:settings {:theme "dark"}}})

; Update the theme (creates new nested structure)
(define updated-user 
  (assoc user ':profile 
    (assoc (get user ':profile) ':settings 
      (assoc (get (get user ':profile) ':settings) ':theme "light"))))

; Original user unchanged, updated-user has new theme
```

#### Functional Data Transformation
```lisp
; Transform data without mutation
(define process-user (fn [user]
  (assoc (assoc user ':processed true) ':timestamp (current-time))))

(define users [{:name "Alice"} {:name "Bob"}])
; Process each user (returns new list with new user objects)
(define processed-users 
  (if (empty? users) 
    []
    (conj (process-users (rest users)) (process-user (first users)))))
```

### Benefits in Practice

#### Safe Function Parameters
```lisp
(define update-user-theme (fn [user new-theme]
  (assoc user ':theme new-theme)))

(define my-user {:name "Alice" :theme "dark"})
(define updated (update-user-theme my-user "light"))

; my-user is safe from modification
my-user             ; Still {:name "Alice" :theme "dark"}
updated             ; {:name "Alice" :theme "light"}
```

#### Undo/Redo Functionality
```lisp
; Keep history of states
(define state-history [initial-state])

(define add-state (fn [history new-state]
  (conj history new-state)))

(define undo (fn [history]
  (if (> (count history) 1)
    (rest (reverse history))
    history)))
```

#### Safe Concurrent Access
```lisp
; Multiple functions can safely access the same data
(define shared-data {:counter 0 :items []})

; These can run concurrently without conflicts
(define increment-counter (fn [data] 
  (assoc data ':counter (+ (get data ':counter) 1))))

(define add-item (fn [data item]
  (assoc data ':items (conj (get data ':items) item))))
```

### Performance Considerations

LisPy's immutability uses **copy-on-write**:
- **Pros**: Simple, reliable, works with all data types
- **Cons**: O(n) copying for large structures

For most applications, this is perfectly fine. For high-performance scenarios with large data structures, consider:
- Breaking large structures into smaller pieces
- Using functional programming patterns that minimize copying
- Designing algorithms that work with the immutable model

### Key Takeaways

1. **All data structure operations return new structures**
2. **Original data is never modified**
3. **This prevents a huge class of bugs**
4. **It enables safe, predictable functional programming**
5. **LisPy makes immutability the default, not an option**

**Remember**: In LisPy, when you "update" data, you're actually creating new data. This is a feature, not a limitation!

---

## Module System

### Creating Modules

Modules help organize code into reusable components.

**math-utils.lpy:**
```lisp
; Mathematical utility functions
(define pi 3.14159265359)
(define e 2.71828182846)

(define square (fn [x] (* x x)))
(define cube (fn [x] (* x x x)))
(define circle-area (fn [r] (* pi (square r))))
(define circle-circumference (fn [r] (* 2 pi r)))

; Private helper (not exported)
(define internal-calc (fn [x] (* x 1.5)))

; Export public API
(export pi e square cube circle-area circle-circumference)
```

### Using Modules

**main.lpy:**
```lisp
; Import the math utilities
(import "math-utils")

; Use imported functions
(define radius 5)
(define area (circle-area radius))
(define circumference (circle-circumference radius))

; Display results
area                 ; => 78.53981633975
```

### Import Styles

```lisp
; 1. Import all exports
(import "math-utils")
(square 5)           ; Direct access

; 2. Import with prefix (namespace)
(import "math-utils" :as "math")
(math/square 5)      ; Prefixed access

; 3. Import specific functions only
(import "math-utils" :only (pi circle-area))
(circle-area 3)      ; Only imported functions available
```

### Module Organization

```
project/
├── main.lpy
├── utils/
│   ├── string.lpy
│   ├── math.lpy
│   └── validation.lpy
├── models/
│   ├── user.lpy
│   └── product.lpy
└── config.lpy
```

**utils/string.lpy:**
```lisp
(define length (fn [s] (count s)))
(define empty? (fn [s] (= (count s) 0)))
(export length empty?)
```

**main.lpy:**
```lisp
(import "config")
(import "utils/string" :as "str")
(import "models/user" :as "user")

; Use imported modules
(if debug-mode
  (println "Debug mode enabled"))
```

**Exercise:** Create a module for geometric calculations (area, perimeter of different shapes) and use it in a main program.

---

## Best Practices

### Code Organization

1. **Use Descriptive Names**
   ```lisp
   ; Good
   (define calculate-monthly-payment (fn [principal rate months] ...))
   
   ; Avoid
   (define calc (fn [p r m] ...))
   ```

2. **Keep Functions Small**
   ```lisp
   ; Break complex functions into smaller pieces
   (define validate-user-input (fn [input]
     (and (validate-email (get input :email))
          (validate-age (get input :age))
          (validate-name (get input :name)))))
   ```

3. **Use Comments Wisely**
   ```lisp
   ; Explain WHY, not WHAT
   ; Calculate compound interest using daily compounding
   ; because our bank compounds daily
   (define compound-interest (fn [principal rate days]
     (* principal (expt (+ 1 (/ rate 365)) days))))
   ```

### Functional Programming Principles

1. **Immutability by Default**
   ```lisp
   ; LisPy data structures are immutable - operations return new structures
   (define original-map {:name "Alice" :age 30})
   (define updated-map (assoc original-map ':city "NYC"))
   ; original-map is unchanged: {:name "Alice" :age 30}
   ; updated-map is new: {:name "Alice" :age 30 :city "NYC"}
   
   (define original-vec [1 2 3])
   (define extended-vec (conj original-vec 4))
   ; original-vec is unchanged: [1 2 3]
   ; extended-vec is new: [1 2 3 4]
   ```

2. **Prefer Pure Functions**
   ```lisp
   ; Pure function - same input always gives same output
   (define add (fn [x y] (+ x y)))
   
   ; Avoid side effects when possible
   ```

3. **Use Immutable Data**
   ```lisp
   ; Don't modify existing data, create new data
   (define add-item (fn [inventory item]
     (assoc inventory (get item :name) (get item :quantity))))
   ```

4. **Compose Functions**
   ```lisp
   (define process-user (fn [user]
     (validate-user (normalize-user (sanitize-user user)))))
   ```

### Error Handling

```lisp
; Use conditionals for error checking
(define safe-divide (fn [x y]
  (if (= y 0)
    nil
    (/ x y))))

; Validate inputs
(define create-user (fn [name age]
  (if (and (not (empty? name)) (> age 0))
    {:name name :age age}
    nil)))
```

---

## Common Patterns

### Data Transformation

```lisp
; Transform user data
(define format-user (fn [user]
  (assoc user :display-name 
    (get user :name))))

; Process collections
(define process-users (fn [users]
  (if (empty? users)
    []
    (conj (process-users (rest users))
          (format-user (first users))))))
```

### Configuration Pattern

```lisp
; config.lpy
(define app-config {
  :database-url "localhost:5432"
  :api-key "secret-key"
  :debug-mode true
  :max-connections 100
})

(export app-config)

; main.lpy
(import "config")
(define db-connection (connect (get app-config :database-url)))
```

### Factory Pattern

```lisp
; Create different types of objects
(define create-shape (fn [type dimensions]
  (if (= type "circle")
    {:type "circle" :radius (first dimensions)}
    (if (= type "rectangle")
      {:type "rectangle" :width (first dimensions) :height (second dimensions)}
      nil))))

(define circle (create-shape "circle" [5]))
(define rect (create-shape "rectangle" [4 6]))
```

### Validation Pattern

```lisp
(define validate-email (fn [email]
  (and (not (empty? email))
       (> (count email) 5))))  ; Simplified validation

(define validate-user (fn [user]
  (and (validate-email (get user :email))
       (> (get user :age) 0)
       (not (empty? (get user :name))))))
```

---

## Next Steps

Congratulations! You've learned the fundamentals of LisPy. Here's what to explore next:

### Practice Projects

1. **Calculator**: Build a calculator that handles complex expressions
2. **Todo List**: Create a todo list manager with add, remove, and list functions
3. **Address Book**: Build an address book with search and update capabilities
4. **Game**: Create a simple text-based game using conditionals and user input

### Advanced Topics to Explore

1. **Macros** (when implemented): Code that writes code
2. **Error Handling**: Robust error handling patterns
3. **Performance**: Understanding performance characteristics
4. **Interoperability**: Working with external libraries

### Resources

- **Language Reference**: See `Requirements.md` for complete language specification
- **Interpreter Guide**: See `INTERPRETER.md` for command-line usage
- **Examples**: Explore the `examples/` directory for working code
- **Tests**: Look at `tests/` to see how features are tested

### Community

- Contribute to LisPy development
- Share your projects and modules
- Help improve documentation and tutorials

---

## Exercises Solutions

Here are solutions to the exercises throughout the tutorial:

### Circle Area Exercise
```lisp
(define pi 3.14159)
(define radius 5)
(define area (* pi (* radius radius)))
area  ; => 78.53975
```

### Personal Variables Exercise
```lisp
(define my-name "Alice")
(define my-age 25)
(define favorite-number 42)
(+ my-age favorite-number)  ; => 67
```

### Cube Volume Function
```lisp
(define cube-volume (fn [side] (* side side side)))
(cube-volume 3)  ; => 27
```

### Number Sign Function
```lisp
(define number-sign (fn [n]
  (if (> n 0)
    "positive"
    (if (< n 0)
      "negative"
      "zero"))))

(number-sign 5)   ; => "positive"
(number-sign -3)  ; => "negative"
(number-sign 0)   ; => "zero"
```

### Book Hash Map
```lisp
(define book {
  :title "The LisPy Guide"
  :author "Jane Developer"
  :year 2024
  :pages 350
})

(get book :title)  ; => "The LisPy Guide"
```

### Vector Length Function
```lisp
(define vector-length (fn [vec]
  (if (empty? vec)
    0
    (+ 1 (vector-length (rest vec))))))

(vector-length [1 2 3 4 5])  ; => 5
```

---

**Happy coding with LisPy!** 🎉

Remember: The best way to learn is by doing. Try the examples, experiment with variations, and build your own projects. LisPy's interactive REPL makes it easy to test ideas quickly. 