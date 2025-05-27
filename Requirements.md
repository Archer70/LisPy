# LisPy

## Project Description

Provides a basic Lisp language interpreter running on Python.

## Language Features

### Primitive Types

- Numbers: Examples: `1`, `-10`, `3.14`, `-0.5`
  - LisPy recognizes both integer and floating-point number formats.
  - Internally, these may be parsed into Python's `int` or `float` types.
  - Arithmetic operations (like `+`, `-`, `*`, `/`) will generally operate seamlessly between integers and floats. For example, `(+ 1 2.5)` will result in `3.5`.
  - The division operator `/` will perform floating-point division (e.g., `(/ 5 2)` results in `2.5`).
- Strings: `"Anything surrounded in double quotes."`
  - Single quotes are not valid string enclosing symbols.
  - Strings can contain the following standard escape sequences:
    - `\n` - Represents a newline character.
    - `\t` - Represents a tab character.
    - `\"` - Represents a double quote character within the string.
    - `\\` - Represents a literal backslash character.
  - A backslash followed by any character not listed above is an invalid escape sequence and will result in a parsing error.
- Booleans:
  - The boolean literal `true`.
  - The boolean literal `false`.
  - Boolean literals are case-insensitive (e.g., `True`, `FALSE` are also valid).
- Nil: Represents nothingness or an empty/null value. Literalled as `nil`.
- Symbols: These are special, stand-alone pieces of data used primarily as identifiers.
  - Symbols are typically alphanumeric but can also include a range of special characters such as `+ - * / < > = ? ! . : _` (and others not reserved for parsing other literal types or syntax like parentheses, quotes, brackets, and braces).
  - Example: `my_symbol`, `another-symbol!`, `*value*`, `+`, `key1:`, `:foo`.
  - They are used for variable names, function names, and often as keys in maps. For example: `(define my_symbol "assigned string value")`.

#### Truthiness and Falsiness
In boolean contexts (like conditional expressions):
- The boolean value `false` is considered falsy.
- The value `nil` is considered falsy.
- All other values (including `true`, numbers (even 0), strings (even empty ones), symbols, lists, vectors, maps, and functions) are considered truthy.

### Forms and Evaluation

All code in LisPy is written as *forms*, which are lists enclosed in parentheses, like `(+ 1 1)`.

When a form is evaluated:
- If the first element of the form is a *special form* (e.g., `define`, `fn`, `if`), it follows its own specific rules for evaluation and may not evaluate all its arguments, or may evaluate them in a special order.
- Otherwise, the first element is treated as a function to be called. All subsequent elements in the form (the arguments) are evaluated (typically from left-to-right), and then the function is invoked with these evaluated arguments.
- An empty list `()` when encountered as a form to be evaluated is an error, as it does not represent a valid function call or special form. (Note: for representing an empty sequence as data, see Vectors or the value `nil`).

### Comments

Comments are used to annotate code and are ignored by the LisPy interpreter. LisPy supports single-line comments.

- Any text from a semicolon (`;`) to the end of the line is considered a comment.

Example:
```lisp
; This is a comment
(define x 10) ; This is also a comment, explaining the line
; (define y 20) -- this line is entirely commented out
```

### Self-Evaluating Data

Certain types of data in LisPy evaluate to themselves. This means when the evaluator encounters them, the result of evaluation is the data itself. These include:
- Numbers (e.g., `1` evaluates to `1`, `3.14` evaluates to `3.14`)
- Strings (e.g., `"hello"` evaluates to `"hello"`)
- Booleans (`true` evaluates to `true`, `false` evaluates to `false`)
- Nil (`nil` evaluates to `nil`)
- Vectors (e.g., `[1 2 3]` evaluates to the vector `[1 2 3]`)
- Maps (e.g., `{:a 1}` evaluates to the map `{:a 1}`)

Symbols, by contrast, are evaluated by looking up the value they refer to in the current environment. Lists are evaluated as forms (function calls or special forms), unless explicitly quoted (see Quoting).

### Vectors

LisPy provides a "vector" type, comparable to an "array" in other languages. It is a sequenced list of values, where the type may be mixed, and it is enclosed in square brackets.

- `[1, 2, 3]`
- `[1, "two", :three]`

Both of the above are valid.

Additionally, commas are optional. `[1 2 3]`

### Maps

For data structures arranged in key, value pairs, we provide the "map" type. Map types are enclosed in curly braces. The key side of the data structure must be an symbol. String keys are not allowed. The value side can be any type. Again, comma separation is optional.

If a colon is used in a key (e.g., `key1:` or `:another_key`), it is considered part of the symbol name itself and not a special separator or type indicator. Since separators are optional, we must make sure that maps always contain an even number of arguments in order to assign the values to their corresponding symbol keys.

- `{key "value"}`
- `{key1: "value1", key2: "value2"}`
- `{:another_key "another value", regular-key 123}`
- `{key1: "value1", nested_map: {nested_key: "nested_value"}}`

### Functions

Functions are fundamental units of operation in LisPy. The `fn` special form is used to create a new function. Its syntax is:

  ```lisp
  (fn [param1 param2 ...]
    ; ... body: one or more expressions ...
    (expression1)
    (expression2) ; Value of this last expression is returned
  )
  ```

- **Parameters:** The `[param1 param2 ...]` part defines the names of the parameters the function will accept. These names must be symbols. Syntactically, this list of parameter symbols is enclosed in square brackets. When the function is called, these symbols are bound to the argument values provided in the call. Commas between parameter symbols are optional and ignored (e.g., `[arg1 arg2]` is preferred).
- **Body:** The body can contain one or more expressions. These expressions are evaluated in order when the function is called.
- **Return Value:** The value of the *last* expression evaluated in the body is automatically returned as the result of the function call.
- **Closures:** Functions in LisPy are closures. This means they "capture" and remember the lexical environment (bindings of symbols to values) in which they were defined. They can access and use these captured values even if the function is called from a different scope.
- **Self-Evaluating:** Function objects themselves (the result of an `fn` expression) are a distinct data type and are self-evaluating (as noted in "Self-Evaluating Data").

### Definitions (Top-Level)

The `define` special form is used to assign a value to a symbol in the top-level (global) environment of the program or REPL session. It takes two arguments: the symbol to be defined, and the expression whose evaluated result will be assigned to the symbol.

`(define my_variable "My Value")`
`(define my_function (fn [x] (* x x)))`
`(define calculated_value (+ 10 20))`

Once a symbol is defined at the top level, LisPy uses a single, straightforward way to look up its value, regardless of whether that symbol was defined as a simple variable or as a function. For example, after the definitions above, `my_variable` directly refers to its string value, and `my_function` directly refers to the created function. You would then call the function like so: `(my_function 10)`.

For creating local bindings within a specific scope (e.g., inside a function body), see the `let` special form.

### Local Bindings (`let`)

The `let` special form is used to create local bindings for symbols within a specific lexical scope. These bindings are only visible within the body of the `let` form.

Its syntax is:
```lisp
(let [symbol1 expression1
      symbol2 expression2
      ...]
  ; ... body: one or more expressions ...
  (body_expression1)
  (body_expression2) ; Value of this last expression is returned
)
```

- **Bindings:** The `[...]` part contains pairs of a symbol and an expression.
  - The bindings are established in sequence, similar to a series of `define` statements. Each expression is evaluated, and its result is bound to the corresponding symbol.
  - An earlier binding *can* be used in the expression of a later binding within the same `let` binding block (e.g., `(let [x 1 y (+ x 1)] ...)` is allowed, and `y` would be bound to `2`).
- **Body:** The body can contain one or more expressions. These expressions are evaluated in order within the lexical scope created by the `let` (i.e., they can use the symbols bound in the `let`).
- **Return Value:** The value of the *last* expression evaluated in the `let` body is returned as the result of the `let` form.
- **Shadowing:** Bindings within a `let` can "shadow" (temporarily hide) bindings of the same symbol name from an outer scope.

Example:
```lisp
(define x 10) ; Top-level x

(let [x 5         ; New local x, shadows the top-level x
      y (+ x 2)]  ; This x refers to the local x (5), so y becomes 7
  (println "Local x:" x ", y:" y) ; Assuming println for example output
  (+ x y))      ; Returns 12 (5 + 7)

; (println "Top-level x:" x) ; Would print "Top-level x: 10" if println existed
```

### Conditional Execution (`if`)

The `if` special form provides conditional execution. It allows LisPy to choose which code to execute based on a condition.

Its syntax is:
```lisp
(if condition-expression
    then-expression
    else-expression) ; Optional
```

- **Evaluation:**
  1.  The `condition-expression` is evaluated first.
  2.  If the result of `condition-expression` is truthy (any value other than `false` or `nil`), the `then-expression` is evaluated, and its result becomes the result of the `if` form. The `else-expression` is not evaluated.
  3.  If the result of `condition-expression` is falsy (`false` or `nil`), the `else-expression` is evaluated, and its result becomes the result of the `if` form. The `then-expression` is not evaluated.
- **Optional `else`:**
  - If the `else-expression` is omitted and the `condition-expression` evaluates to falsy, the `if` form will return `nil`.
- **"Short-circuiting":** Only one of `then-expression` or `else-expression` (if present) will be evaluated.

Examples:
```lisp
(if true
    "it was true"
    "it was false") ; Returns "it was true"

(if false
    "it was true"
    "it was false") ; Returns "it was false"

(if (> 10 5)
    (define result "Greater")
    (define result "Not greater")) ; result becomes "Greater"

(if (< 0 5)
    "Positive") ; Returns "Positive"

(if (> 0 5)
    "Positive") ; Returns nil (else-expression is omitted and condition is false)

(define x 10)
(if (= x 10)
    (println "x is 10")
    (println "x is not 10")) ; "x is 10" would be printed (assuming println)
```

### Quoting / Preventing Evaluation (`quote` and `'`)

LisPy, like other Lisp dialects, has the powerful feature of treating code as data (homoiconicity). Quoting is the mechanism that allows you to prevent evaluation of a form, treating it literally as a data structure.

There are two ways to quote:

1.  **The `quote` special form:**
    ```lisp
    (quote something)
    ```
    The `quote` special form takes a single argument (`something`) and returns that argument *without evaluating it*.

2.  **The single quote reader macro (`'`):**
    The single quote character (`'`) is a shorthand syntax (a "reader macro") for `quote`. When the LisPy reader encounters `'something`, it automatically expands it to `(quote something)` before evaluation.
    ```lisp
    'something ; Is equivalent to (quote something)
    ```

**Purpose and Examples:**

- **Symbols:** To treat a symbol literally, rather than looking up its value:
  ```lisp
  (define x 10)
  x          ; Evaluates to 10
  'x         ; Evaluates to the symbol x itself
  (quote x)  ; Also evaluates to the symbol x itself
  ```

- **Lists:** To create literal lists without them being interpreted as function calls or special forms:
  ```lisp
  '(1 2 3)                     ; Evaluates to the list (1 2 3)
  '(+ 1 2)                   ; Evaluates to the list (+ 1 2), does NOT perform addition
  (define my-list '(a b c))   ; my-list is now bound to the list (a b c)
  ```
  Without quoting, `(1 2 3)` would be an error (trying to call `1`), and `(+ 1 2)` would evaluate to `3`.

- **Other Types:** Quoting can be used with any form. For self-evaluating types (like numbers, strings, booleans, nil, vectors, maps), quoting has no effect on the final value, as they would evaluate to themselves anyway. However, it's not an error to quote them.
  ```lisp
  '10         ; Evaluates to 10
  '"hello"    ; Evaluates to "hello"
  '[1 2 3]   ; Evaluates to the vector [1 2 3]
  ```

The `quote` mechanism is fundamental for writing macros (code that writes code), manipulating code as data, and constructing literal data structures that include symbols or lists.

### Error Handling

LisPy will attempt to detect and report errors during the evaluation of code. When an error occurs, the interpreter will halt execution of the current form and print an error message indicating the nature of the problem. Initial error reporting will cover common issues such as:

- **Unbound Symbols:** Referencing a symbol that has not been defined.
- **Incorrect Argument Count:** Calling a function with the wrong number of arguments.
- **Type Mismatches:** Attempting an operation with incompatible data types (e.g., arithmetic on a string).
- **Syntax Issues:** Problems like improperly structured forms or invalid map definitions.

## Interaction Model

The primary way to interact with the LisPy interpreter will be through a REPL (Read-Eval-Print Loop). This interactive environment will allow users to:

1.  **Read:** Input LisPy expressions.
2.  **Eval:** Have the interpreter evaluate those expressions.
3.  **Print:** See the results of the evaluation printed to the console.
4.  **Loop:** Continue this process, facilitating experimentation and iterative development.

