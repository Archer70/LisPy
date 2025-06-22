# LisPy BDD Tutorial: Write Awesome Specs! 🚀

Welcome to the world of Behavior-Driven Development (BDD) in LisPy! If you love writing clear, understandable, and executable specifications for your software, you're in the right place. Let's dive in and make testing a joyous part of your LisPy journey! 🎉

## Table of Contents

1.  [Why BDD? What's the Buzz?](#why-bdd-whats-the-buzz)
2.  [Getting Started: Your First BDD Test](#getting-started-your-first-bdd-test)
3.  [LisPy's BDD Superstars: The Keywords](#lispys-bdd-superstars-the-keywords)
    *   [`describe` / `feature`](#describe--feature-your-storys-title)
    *   [`it` / `scenario`](#it--scenario-the-exciting-chapters)
    *   [`given`](#given-setting-the-stage)
    *   [`when`](#when-the-action-happens)
    *   [`then`](#then-the-grand-reveal--assertions)
4.  [Assert Yourself! Making Sure Things Work](#assert-yourself-making-sure-things-work)
    *   [`assert-equal?`](#assert-equal-are-they-twins)
    *   [`assert-true?`](#assert-true-is-it-really-true)
    *   [`assert-false?`](#assert-false-is-it-truly-false)
    *   [`assert-nil?`](#assert-nil-is-it-nothingness)
    *   [`assert-not-nil?`](#assert-not-nil-is-it-something)
    *   [`assert-raises?`](#assert-raises-expecting-the-unexpected-errors)
5.  [Showtime! Running Your BDD Tests](#showtime-running-your-bdd-tests)
6.  [A Full Feature Showcase](#a-full-feature-showcase)
7.  [BDD Best Practices: The LisPy Way](#bdd-best-practices-the-lispy-way)
8.  [Go Forth and Specify!](#go-forth-and-specify)

---

## Why BDD? What's the Buzz? 🤔✨

BDD is all about collaboration and clear communication. Instead of just "testing code," you're describing how your software *should behave* from a user's perspective, using a language that everyone on the team can understand.

**Benefits in LisPy:**

*   **Living Documentation**: Your BDD tests become documentation that's always up-to-date.
*   **Clearer Requirements**: Writing BDD helps clarify what you're building.
*   **Functional Focus**: Perfectly complements LisPy's functional style.
*   **Confidence Boost**: Know your features work as intended!

---

## Getting Started: Your First BDD Test 🔰

Let's jump right in!

1.  **Create a Feature File**:
    BDD tests in LisPy typically live in files ending with `.lpy` (just like other LisPy code), often organized into a `features` or `specs` directory. For example, `tests/bdd_features/my_calculator_feature.lpy`.

2.  **Basic Structure**:
    A BDD file is structured using LisPy's BDD keywords. Here's a sneak peek:

    ```lisp
    ; tests/bdd_features/arithmetic_feature.lpy

    (describe "Arithmetic Operations"
      (it "adds two numbers correctly"
        (given "I have the number 5"
          (define a 5))
        (given "I also have the number 7"
          (define b 7))
        (action "I add them together"
          (define result (+ a b)))
        (then "the result should be 12"
          (assert-equal? 12 result))))
    ```

    Wow, that reads like plain English, right? That's the magic of BDD! Note that while some BDD syntaxes use "And" or "But" for subsequent steps of the same type, in LisPy, you simply use another `given`, `when`, or `then` form.

---

## LisPy's BDD Superstars: The Keywords 🌟

LisPy provides a set of special forms (keywords) to structure your BDD tests. They often have aliases like `feature` for `describe` and `scenario` for `it` to match common BDD Gherkin syntax.

### `describe` / `feature`: Your Story's Title 📖

*   **Purpose**: Groups related scenarios under a single feature or component of your system. It's the "big picture."
*   **Syntax**: `(describe "Feature Name As a String" ... scenario1 ... scenario2 ...)`
*   **Example**:
    ```lisp
    (describe "User Authentication Feature"
      ; ... 'it' blocks will go here ...
    )
    ```

### `it` / `scenario`: The Exciting Chapters 🎬

*   **Purpose**: Defines a specific behavior or an example of how the feature should work. Each `it` block is one test case.
*   **Syntax**: `(it "A specific scenario description as a string" ... given/when/then steps ...)`
*   **Context**: Must be used inside a `describe` block.
*   **Example**:
    ```lisp
    (describe "Shopping Cart"
      (it "allows adding items to the cart"
        ; ... steps ...
      )
      (it "calculates the total price correctly"
        ; ... steps ...
      ))
    ```

### `given`: Setting the Stage 🎭

*   **Purpose**: Sets up the initial context or preconditions for your scenario. What state should the system be in?
*   **Syntax**: `(given "A precondition description as a string" ... lispy-code-to-setup ...)`
    If you have multiple setup steps, you can simply use multiple `given` forms. While other BDD syntaxes sometimes use `And` or `But` for subsequent steps of the same type (e.g., a second `Given` step), in LisPy, you just repeat the keyword (e.g., use `given` again). This keeps the structure clear and explicit.
*   **Context**: Must be used inside an `it` block.
*   **Example**:
    ```lisp
    (it "allows adding items to the cart"
      (given "I have an empty shopping cart"
        (define cart []))
      (given "there is a product 'Super Widget' costing 10"
        (define widget {:name "Super Widget" :price 10})))
    ```

### `action`: The Action Happens! 💥

*   **Purpose**: Describes the key action or event that occurs, the behavior you're testing.
*   **Syntax**: `(action "The action/event description as a string" ... lispy-code-for-action ...)`
*   **Context**: Must be used inside an `it` block, usually after `given` steps.
*   **Example**:
    ```lisp
    (action "I add the 'Super Widget' to the cart"
      (set! cart (conj cart widget))) ; Assuming 'set!' or a way to update 'cart' if needed
                                      ; Or, more functionally: (define new-cart (conj cart widget))
    ```

### `then`: The Grand Reveal & Assertions! 🕵️‍♀️✅

*   **Purpose**: Specifies the expected outcome or result after the `action` step. This is where you make your assertions!
*   **Syntax**: `(then "The expected outcome description as a string" ... lispy-code-with-assertions ...)`
*   **Context**: Must be used inside an `it` block, usually after an `action` step.
*   **Example**:
    ```lisp
    (then "the cart should contain 1 item"
      (assert-equal? 1 (count new-cart)))
    (then "the total price should also be 10"
      (assert-equal? 10 (calculate-total new-cart)))
    ```

---

## Assert Yourself! Making Sure Things Work 💪

Inside your `then` blocks, you'll use LisPy's BDD assertion functions to verify outcomes. If an assertion fails, the test step is marked as "failed."

### `assert-equal?`: Are They Twins? 👯

*   **Purpose**: Checks if two values are equal.
*   **Syntax**: `(assert-equal? expected-value actual-value)`
*   **Example**:
    ```lisp
    (then "the sum should be 10"
      (define actual-sum (+ 5 5))
      (assert-equal? 10 actual-sum))
    ```

### `assert-true?`: Is It Really True? ✅

*   **Purpose**: Checks if a condition evaluates to `true`.
*   **Syntax**: `(assert-true? condition)`
*   **Example**:
    ```lisp
    (then "the user should be active"
      (define user {:name "Test" :active true})
      (assert-true? (get user :active)))
    ```

### `assert-false?`: Is It Truly False? ❌

*   **Purpose**: Checks if a condition evaluates to `false`.
*   **Syntax**: `(assert-false? condition)`
*   **Example**:
    ```lisp
    (then "the user should not be an admin"
      (define user {:name "Test" :admin false})
      (assert-false? (get user :admin)))
    ```

### `assert-nil?`: Is It Nothingness? 💨

*   **Purpose**: Checks if a value is `nil` (LisPy's representation of null/None).
*   **Syntax**: `(assert-nil? value)`
*   **Example**:
    ```lisp
    (then "finding a non-existent user should return nil"
      (define non-user (find-user-by-id 999))
      (assert-nil? non-user))
    ```

### `assert-not-nil?`: Is It Something? 🧐

*   **Purpose**: Checks if a value is *not* `nil`.
*   **Syntax**: `(assert-not-nil? value)`
*   **Example**:
    ```lisp
    (then "finding an existing user should return user data"
      (define existing-user (find-user-by-id 1))
      (assert-not-nil? existing-user))
    ```

### `assert-raises?`: Expecting the Unexpected (Errors)! 💥🚨

*   **Purpose**: Checks if a specific LisPy `EvaluationError` is raised when a form is executed, and that the error message contains an expected substring. This is crucial for testing error handling!
*   **Syntax**: `(assert-raises? "expected part of error message" (form-that-should-raise-error))`
*   **Important**: `assert-raises?` is a **special form**. This means it controls the evaluation of its arguments. The `form-that-should-raise-error` is *not* evaluated before being passed to `assert-raises?`; `assert-raises?` evaluates it internally to catch the error.
*   **Example**:
    ```lisp
    (describe "Division"
      (it "handles division by zero"
        (given "I have the number 10" (define x 10))
        (action "I attempt to divide it by zero" nil) ; The action is in the 'then' for this kind of test
        (then "it should raise a 'Division by zero' error"
          (assert-raises? "Division by zero" (/ x 0))))) ; Error occurs here

    (it "handles invalid argument types for +"
              (action "I attempt to add a number and a string" nil)
      (then "it should raise a TypeError"
        (assert-raises? "TypeError: unsupported operand type(s) for +" (+ 1 "oops"))))
    ```
    If the expected error (or any part of its message) occurs, the assertion passes. If no error occurs, or a different error occurs, it fails.

---

## Showtime! Running Your BDD Tests 🏃💨

LisPy comes with a handy BDD test runner integrated into the interpreter.

*   **Command**:
    ```bash
    python bin/lispy_interpreter.py --bdd "path/to/your/features/*.lpy"
    ```
    You can use glob patterns to specify multiple feature files. For example:
    *   `"tests/bdd_features/*.lpy"` (all feature files in that directory)
    *   `"tests/bdd_features/specific_feature.lpy"` (a single feature file)

*   **Understanding the Output**:
    The runner will give you a summary of your features and scenarios:
    *   **Passing tests** are marked with ✅.
    *   **Failing tests** (assertions that didn't hold true) are marked with ❌ and show details about the failure.
    *   **Errors in steps** (e.g., trying to call an undefined function, or an unexpected critical error during a step) are marked with 🔥 and include error details.

    The output is designed to be clear and help you quickly pinpoint what went wrong.

    Example snippet of output:
    ```
    Feature: Arithmetic Operations ✅
      Scenario: Adding two numbers correctly ✅
        Given I have the number 5 ✅
        And I have the number 7 ✅
        When I add them together ✅
        Then the result should be 12 ✅

    Feature: Advanced Math ❌
      Scenario: Division by zero throws error ✅
        Given the number 10 ✅
        When I attempt to divide by zero ✅
        Then an error 'Division by zero' should occur ✅
      Scenario: Failing test example ❌
        Given a setup ✅
        When an action occurs ✅
        Then this assertion fails ❌
          Details: Assertion Failed: Expected [false] (type: bool) but got [true] (type: bool).
                   In step: (assert-false? true)

    --- Summary ---
    Features: 2 run, 1 passed, 1 failed
    Scenarios: 3 run, 2 passed, 1 failed
    Steps: 10 run, 9 passed, 1 failed
    ```

---

## A Full Feature Showcase 🎬✨

Let's put it all together with a more complete example.

**`tests/bdd_features/calculator_feature.lpy`**:
```lisp
(describe "Calculator Feature"

  (it "correctly adds two positive numbers"
    (given "I have a calculator" 
      (define calc-add +)) ; Using LisPy's built-in +
            (action "I input 5 and 7"
      (define num1 5)
      (define num2 7)
      (define result (calc-add num1 num2)))
    (then "the displayed result should be 12"
      (assert-equal? 12 result)))

  (it "correctly subtracts a larger number from a smaller number"
    (given "I have a calculator"
      (define calc-subtract -))
            (action "I input 3 and 10 for subtraction"
      (define num1 3)
      (define num2 10)
      (define result (calc-subtract num1 num2)))
    (then "the displayed result should be -7"
      (assert-equal? -7 result)))

  (it "handles division by zero by raising an error"
    (given "I have a calculator that can divide"
      (define calc-divide /))
    (and "I have the number 10"
      (define dividend 10))
    (and "I attempt to divide by zero"
      (define divisor 0))
    (then "an error 'Division by zero' should be raised"
      (assert-raises? "Division by zero" (calc-divide dividend divisor))))

  (it "intentionally failing scenario for demonstration"
    (given "a simple setup"
      (define value true))
            (action "I check a condition that will fail"
      nil) ; No action needed, the check is in 'then'
    (then "the condition should be false, but it's true"
      (assert-false? value))) ; This will fail as value is true
)
```
Run this with:
`python bin/lispy_interpreter.py --bdd "tests/bdd_features/calculator_feature.lpy"`

You'll see a mix of passing and failing scenarios, demonstrating the runner's output!

---

## BDD Best Practices: The LisPy Way 🏆

*   **Clarity is King**: Write descriptions for features, scenarios, and steps in clear, unambiguous natural language. Think about how another developer (or your future self!) would read it.
*   **One Focus per Scenario**: Each `it` block should test one specific behavior or rule.
*   **Declarative Steps**: `given`, `when`, `then` descriptions should state *what* is happening or *what* state is expected, not *how* it's implemented in the code. The LisPy code within the step handles the "how."
*   **Reusable Steps (Conceptually)**: While LisPy BDD doesn't have explicit step definition re-use like some Gherkin-based tools, you can achieve reusability by defining helper functions in your LisPy code and calling them within your steps.
*   **Embrace Immutability**: Leverage LisPy's immutable data structures. Your `given` steps set up initial states, `when` steps often produce new states from old ones, and `then` steps assert against these new states.
*   **Test Error Conditions**: Use `assert-raises?` to ensure your code handles errors gracefully and as expected.

---

## Go Forth and Specify! 🗺️✍️

You're now equipped with the knowledge to write powerful, expressive BDD tests in LisPy! This approach will not only improve the quality of your code but also make your development process more collaborative and understandable.

BDD is a journey of continuous improvement. As you write more tests, you'll develop a better feel for crafting effective specifications.

**Happy BDD-ing with LisPy!** May your tests be green and your features well-understood! 💚 