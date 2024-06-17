<div align="center">
  <img src="tommy/data/assets/logo.png" width=135px alt="Top Models logo">
  <h1> Top Models | Style Guide </h1>
</div>

*"A style guide is about consistency. Consistency with this style guide is
important. Consistency within a project is
more
important. Consistency within one module or function is the most important."* -
PEP 8

This style guide describes what Python conventions and guidelines are used, on
top of the UU requirements. This document
also provides guidance on practices w.r.t. setting up a (Python) project
structure and writing (Python) project
documentation. This document does not try to explain how to use certain Python
language constructs and features in
particular.

- [Python Coding Style](#python-coding-style)
    - [General Formatting](#general-formatting)
    - [Code Formatting](#code-formatting)
    - [Imports](#imports)
    - [Naming Conventions](#naming-conventions)
    - [Type Annotations](#type-annotations)
    - [Best Practices](#best-practices)
- [Python Documentation](#python-documentation)
    - [Comments](#comments)
    - [Docstrings](#docstrings)
- [File Structure](#file-structure)
    - [Hierarchy](#hierarchy)
    - [Naming Files and Directories](#naming-files-and-directories)
- [Special Files](#special-files)
- [Content of Source Code Files](#content-of-source-code-files)
- [The Zen of Python](#the-zen-of-python)

## Python Coding Style

The project follows the python coding conventions & guidelines as described in
the [PEP 8](https://peps.python.org/pep-0008/) style guide. Bellow follows a
short summary of the most important points;
for further questions please refer to the official guide and of course adhere
to general coding practices also applied
in other programming languages.

### General Formatting

- **Indentation 4 spaces per level**. This is not required for continuation
  lines (e.g. function arguments over multiple
  lines), but indentation has to clearly distinguish independent lines that
  follow.
- Indentation has to be consistent (i.e. either tabs or spaces), given that
  some code editors will get confused by mixed
  usage. PEP 8 suggests spaces, so make sure that the **code editor** is
  configured in such a way that a **tab inserts 4
  spaces**.
- Maximum **line length** is **79** characters. Maximum **docstring/comment
  length** is **72** characters.
- The **end-of-file (EOF)** of a .py file should be a **newline**, meaning that
  the last line of a .py file in a code
  editor is a blank line.

### Code Formatting

- For line wrapping, do not use ` \ `, but use **implied line continuation with
  parentheses**.
- Put a **line break before binary operators**. This makes sure that operators
  are vertically aligned and that they are
  placed directly before the operand.
  ```python
  # Example of implied line continuation
  # and line breaks before binary operators.
  income = (gross_wages
            + taxable_interest
            + (dividends - qualified_dividends)
            - ira_deduction
            - student_loan_interest)
  ```
- The use of string quotes has to be consistent. PEP 8 does not suggest one
  over the other, but given that all
  developers are familiar with C#, make use of **double quotes** when writing *
  *strings**.
- Do **not** add **additional spaces around `=`** to **align assignments**.
- Do use **spaces around `=`** when used to indicate a **default value** in
  function declarations, as we use argument
  type annotations. (NOTE: do **not** use **spaces between the parameter
  keyword and the argument** when overriding the
  parameter's default value)
  ```python
  # Example of the assignment of default values 
  # to function parameters with argument type annotations. 
  def fib(p: int = 0, q: int = 1) -> int
  ```
- Add **2 blank lines** around **top-level functions** and **classes**.
- Add **1 blank line** around **methods** (within a class).
- It is allowed to add **blank lines** within functions to make a **distinction
  between logical sections**.

### Imports

- **Imports** are to be defined at the top of a file, **after module comments
  and docstrings** and **before module
  globals and constants**.
- **Imports** are to be **grouped** in the following order, with a **blank line
  between each group**:
    1. Standard library imports.
    2. Third party imports (i.e. acquired using `pip install`)
    3. Local imports from other libraries within the project.
    4. Local imports within the same library.
- Make use of **absolute imports**, meaning not relative to the file system.
- **Scope-specific imports** are preferred, so do not use wildcard `*`, but
  instead specify what is to be imported.
  ```python
  # Example of a scope-specific import.
  from bar import Foo
  ```

### Naming Conventions

Write all names in English, ASCII preferred. Avoid using names that are too
general or too specific (e.g. with a lot of
words). Language constructs that use the CamelCase convention must capitalize
all letters of an abbreviation (
e.g. `HTTPServer`). If a name collides with a reserved keyword, append 1
trailing underscore.

| Construct         | Naming Convention                                                                                                                                                                                                                                                                                                                                                                                                          |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Package           | All-lowercase, underscores should not be used <br> `pyramids`                                                                                                                                                                                                                                                                                                                                                              |
| Module            | All-lowercase, underscores may be used between individual words if required <br> `pyramid_giza.py`                                                                                                                                                                                                                                                                                                                         |
| Class/Exception   | CamelCase convention (NOTE: Python's built-in classes typically are lowercase) <br> `class PyramidGiza:` <br> Exception classes should include "Exception" as suffix <br> `class InputException:`                                                                                                                                                                                                                          |
| Global Variable   | All-lowercase, underscores should be used between individual words (NOTE: global variables should only be used inside the module in which they are defined) <br> `pyramid_giza = "pyramid of giza"`                                                                                                                                                                                                                        |
| Instance Variable | All-lowercase, underscores should be used between individual words <br> `pyramid_giza = "pyramid of giza"  # Public` <br> Protected instance variables should start with 1 underscore <br> `_pyramid_giza = "pyramid of giza"  # Protected` <br> Private instance variables should start with 2 underscores <br>  `__pyramid_giza = "pyramid of giza"  # Private`                                                          |
| Function          | All-lowercase, underscores should be used between individual words <br> `def pyramid_giza():`                                                                                                                                                                                                                                                                                                                              |
| Method            | All-lowercase, underscores should be used between individual words <br> `def pyramid_giza():  # Public` <br> Protected methods should start with 1 underscore <br> `def _pyramid_giza():  # Protected` <br> Private methods should start with 2 underscores <br> `def __pyramid_giza():  # Private`                                                                                                                        |
| Function Argument | All-lowercase, underscores should be used between individual words <br> `def function(function_argument : str)`                                                                                                                                                                                                                                                                                                            |
| Method Argument   | All-lowercase, underscores should be used between individual words <br> `def instance_method(self):` <br> Instance methods should have their first argument named "self" <br> `@classmethod` <br> `def class_method(cls):` <br> Class methods should have their first argument named "cls". Static methods are similar to class methods, but do not require any arguments <br> `@staticmethod` <br> `def static_method():` |
| PyTests           | test_*.py or \*_test.py in the current directory and its subdirectories.                                                                                                                                                                                                                                                                                                                                                   |

In practice, private variables and methods (i.e. with 2 underscores) should not
be used, since they are not actually
made private; they are just renamed internally in a way that makes them harder
to access (this is called "name
mangling"). Instead, use a single underscore to indicate that a variable or
method should not be touched outside the
class it is declared in. If the variable is to be altered, make use of getters
and setters (which are decorators in
Python). General practice in that case however is to expose (public) attributes
directly, and to only use getters and
setters when additional actions are required when getting or setting a value.

### Type Annotations

Given that most developers are more familiar with explicit typing, follow
the [PEP 484](https://peps.python.org/pep-0484/) type hint rules when
annotating function/method definitions. Since
Python remains to be a dynamically typed language, do not use variable type
annotations. Of course there remains to be
no type checking at runtime with type annotations.

- **Parameter**/**return** type annotations are defined by filling function
  annotation slots with **any class**. A type checker
  could use this to throw a warning when it suspects this is not the case.
  ```python
  # Example of a function annotation where 
  # the expected type of the argument is str,
  # the expected return type will also be a str.
  def greeting(name: str) -> str:
      return "Hello " + name 
  ```
- **Expressions** whose type is a **subtype** of a specific parameter/return
  type are also accepted as valid arguments/return
  values.
- The **type** of **wildcard parameters** (i.e. `*args` or `**kwargs`)
  should be the
  type of the **individual arguments** passed to
  the function. When **iterables** may also be passed as arguments,
  the `Iterable`
  type (from `collections.abc`) should be
  used explicitly as well.
  ```python
  # Example of a type annotation for an *args parameter.
  # An iterable may also be passed in this case.
  def sum(*args: int | Iterable[int]) -> int:
  ```
- For clear semantic type distinction, **type aliases** can be used, although
  they
  are **recommended to be used sparingly**.
  Alias names should be capitalized, as they represent user-defined types,
  which are generally declared that way.
  ```python
  # Example of the usage of type aliases in function annotations.
  Url = str
  def retry(url: Url, retry_count: int) -> None:
  ```
- The **return type of class constructors** (i.e. `__init__`) should be
  explicitly
  annotated as `None`.
- Types provided by the `typing` module are **deprecated** and should therefore
  not
  be used anymore. Use the **built-in
  (collection) types** from the **standard library** instead.

Type annotations may get rather complex, but try to keep them as simple as
possible. Since Python by design is an
implicitly typed language, readability should be maintained as much as
possible.

### Best Practices

- Use `is not` instead of `not ... is`, even though they semantically are the
  same.
- In general use `==` instead of `is`, only use `is` if some **value** is being
  **compared** to an **object in memory**.
- Always use a `def` statement instead of an assigment statement that would
  bind a **lambda expression** to the identifier.
  ```python
  def f(x: int) -> int: # Correct
      return 2 * x     
  f = lambda x: 2 * x   # Wrong
  ``` 
- **Derive exceptions** from `Exception` instead of `BaseException`. Also aim
  to answer the question "**What went wrong**"
  instead of stating something generic like "A problem occurred"
- If a certain **(I/O) resource** is used **locally** to only a section of
  code, use
  a `with` statement to ensure the resource
  is **cleaned up reliably** after use.
- Even though Python is dynamically typed, be consistent with return
  statements. **Always return values of the same type**
  or return nothing all. If a value should be returned, any return statements
  returning no actual value should be
  explicitly defined as `return None`. `None` is used to define **null values**
  in Python.
- **Type comparisons between objects** should always use `isinstance()` instead
  of
  using an `is` comparison.
  ```python
  if isinstance(obj, int):  # Correct 
  if type(obj) is type(1):  # Wrong
  ```
- For **any type of sequences** (e.g. strings, lists, tuples), use the
  property
  that **empty sequences** return `false`.
  Therefore, using the `len()` function is redundant.
  ```python
  if seq:       # Correct
  if len(seq):  # Wrong
  ```
- Make use of the **flow control statements** `return`/`break`/`continue` to
  **simplify control flow** whenever possible.
- Try to **avoid for loops** by using their more **functional counterparts**.
  For
  example, to map and select over a list, use
  **list comprehensions** and **generator expressions** as they are faster and
  take up
  less memory (on top of being more
  elegant).
- Only use **keywords for argument specification** when the **parameter** has a
  **default
  value**.
  ```python
  # Example of the usage of keywords in functions.
  def send(message : str, to : str, cc : str = None, bcc : str = None) -> None:
  send("Hello", "World", bcc="God", cc="Jezus")
  ```

## Python Documentation

Write all documentation in English, ASCII preferred. Prioritize keeping them
up-to-date when the code changes, as to not
cause any confusion. Documentation should be complete sentences; ending with a
period and starting capitalized, unless
it starts with a lower case identifier (e.g. a variable). The documentation of
a piece of functionality like a
method or function should usually start with the present simple without a
personal pronoun (e.g. "Calculates all
prime numbers within the given range.").

### Comments:

- **Block comments**: Indented at the same level as the code that they apply
  on. Each line of a block comment start with
  a `#` and 1 space. Paragraphs inside block comments are seperated by 1 line
  containing a `#`.
- **Inline comments**: Seperated by at least 2 spaces from the statement. They
  also start with a `#` and 1 space. Inline
  comments do not necessarily need to be complete sentences, depending on the
  goal of the comment. (NOTE: inline
  comments should be avoided when possible, as they often state the obvious.)

### Docstrings

Docstrings as described in the [PEP 257](https://peps.python.org/pep-0257/)
docstring documentation are string literals
that occur as the first statement in a module, class, method or function
definition. Docstrings are mainly used as
documentation for publicly accessible code from packages, and are used in a
similar way as C# XML documentation
comments. Docstrings should be declared for:

- Modules
- Functions & Classes exported by a module
- Public methods (which includes the `__init__` constructor)

Packages may be documented in the module docstring of the `__init__.py` file.
String literals may also be used elsewhere
in Python code as documentation, but should be used sparingly. Large and
important private/protected methods may for
example be documented with string literals, but do not document small pieces of
functionality in such a way. Smaller
methods should however be described by normal comments; these comments should
still appear after the `def` line.
Docstrings are always surrounded by `"""triple double quotes"""`.

- **One-line Docstrings**: Used in obvious cases where the documentation can
  fit in 1 line. One-line docstrings should
  not be descriptive, they rather follow a "Does this, returns that" structure.
  The closing quotes are on the same line
  as the opening quotes.
  ```python
  # Example of how One-line Docstrings should be used.
  def multiplier(a : int, b : int) -> int:
      """Takes in two numbers, returns their product."""
      return a*b
  ```
- **Multi-line Docstrings**: Consist of a one-line summary just like a one-line
  docstring, followed by a blank line,
  followed by a more elaborate description.
  The opening quotes are one their own separate line before the one-line
  summary, the closing quotes are one their
  own
  separate line after the description. The entire string literal is indented
  the same way as the opening quotes.
  Different Python constructs have different conventions for writing multi-line
  docstrings:

  | Construct       | Docstring Convention                                                                                                                                                            |
      |-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | Package         | Summarizes the functionality it contains and lists all modules and subpackages exported by the package                                                                          |
  | Module          | Summarizes the functionality it contains and lists all classes, exceptions and functions (and any other objects) that are exported by the module in a one-line summary each     |
  | Class/Exception | Summarizes its behaviour and lists its public methods and instance variables. Subclasses, constructors and methods should each have their own docstrings                        |
  | Function/Method | Summarizes its behaviour and lists its arguments, return value(s) side effects, exceptions that may be raised, etc... Optional arguments should be explicitly indicated as such |

  If a class inherits another class and its behaviour is not changed, the
  docstring should mention this and summarize
  how
  it differs from the base class. To indicate that a subclass method overrides
  a base class method, use the verb "
  override". To indicate that a subclass method also calls the base class
  method, use the verb "extend".
  <br/><br/>
  Multi-line docstrings should be written down using the Sphinx docstring
  format in the reStructuredText (reST) markup
  language as mentioned in the [PEP 287](https://peps.python.org/pep-0287/)
  docstring formatting documentation. By
  default, there are five docstring reST directives, which mostly should be
  used in function and method docstrings.
  Generally, such Sphinx docstrings have the following structure:

  ```python
  """
  [Summary]

  :param [parameter name]: [parameter description]

  :param [ParamName]: [ParamDescription](, defaults to [DefaultParamVal])
  :type [ParamName]: [ParamType](, optional)
  ...
  :raises [ErrorType]: [ErrorDescription]
  ...
  :return: [ReturnDescription]
  :rtype: [ReturnType]
  """
  ```

  A pair of `:param` and `:type` directives should be used for each parameter
  of a function or method. The `:raises:`
  directive is used to describe the exceptions that may be raised by the
  function or method. The `:return:`
  and `:rtype:`directives are used to describe the return value of the function
  or method. (NOTE: the `...` notation is
  onlys used here to indicate that the directive can be repeated multiple
  times.)
  <br/><br/>
  The following section lists some reST features that may be useful in
  docstrings:
    - **Markup escaping**: Use the backslash character `\ ` to escape reST
      markup functionality.
    - **Inline literals**: Use double backquotes ` `` ` to indicate inline
      literals of Python source code.
    - **Literal blocks**: Use indentation to indicate a literal block of Python
      source code. A double colon `::` (at the end of the preceding paragraph)
      should be used to indicate the start of such a block.
    - **Python identifiers**: Use single backquotes `` ` `` to indicate Python
      identifiers (e.g. class names, method names, etc...).

## File Structure

### Hierarchy

In general, try to bundle backend functionality of the same kind into
packages (i.e. add a `__init__.py` file to the directory that should be made a
package). This makes sure that the code is organized in a clear way and renders
importing pieces of functionality easier and more concise. Note that since
Python 3.3, the `__init__.py` file is not required to be defined anymore in
order to render directories as packages, but it is still good practice to do so
anyway.

Of course the hierarchy of Python packages and directories should reflect the
architecture as much as possible. In an MVC desing for example, different
subdirectories should be used for the Model, View and Controller. The depth of
the project directory should be kept to a minimum however, given that file
structure complexity should be reduced wherever possible.

### Naming Files and Directories

Write all names in English, only use ASCII alphabetic and numerical characters.

- **Files**: All-lowercase, underscores should be used between individual
  words. For special files stick to the naming
  conventions used there, even though some files are allowed to have other
  names as well.
- **Directories**: All-lowercase, underscores should be used between individual
  words. Again make exceptions for special
  directories.

## Special Files

- **`requirements.txt`**: Located at the base directory of a git-repository.
  Used to keep track of all used third party
  packages in the project, in which every line contains 1 package (
  e.g. `tensorflow==2.3.1`). When present, it can be
  used in a pip one-liner to install all required packages
  with `pip install -r requirements.txt`. For more information
  on the requirements file format itself, please refer to
  its [pip documentation](https://pip.pypa.io/en/latest/reference/requirements-file-format/).
- **`__init__.py`**: Bundles functionality together by creating a package from
  a directory of Python files. This makes importing pieces of functionality
  from modules within the package easier in different ways. Given that the
  entry-point of a package is defined by its `__init__.py` file, it can for
  instance be used to execute initialization code for the package. Furthermore,
  it can be a good place to export code from modules within the package, which
  renders importing functionality from the package more concise (s.t. one could
  use `from package import functionality` instead of `from package.module
  import functionality` for example). In the simplest case however,
  the `__init__.py` file may naturally be left empty.

## Content of Source Code Files

In the given Software Project manual, it is mentioned that every source code
file has to contain the following comment:

> This program has been developed by students from the bachelor Computer
> Science at Utrecht University within the
> Software Project course.  
> © Copyright Utrecht University (Department of Information and Computing
> Sciences)

On the GUI the following has to be displayed:

> © Utrecht University (ICS)

It is also recommended to add
a [colophon](https://en.wikipedia.org/wiki/Colophon_(publishing)) that
includes:

- The same comment that is also used in the source code files.
- The name of the client.
- The names of the developers.
- The name of the supervisor.
- The link https://softwareprojecten.sites.uu.nl/.

## The Zen of Python

Also known as the [PEP 20](https://peps.python.org/pep-0020/) guiding
principles in designing Pythonic code.

```
Beautiful is better than ugly. 
Explicit is better than implicit. 
Simple is better than complex. 
Complex is better than complicated. 
Flat is better than nested. 
Sparse is better than dense. 
Readability counts. 
Special cases aren't special enough to break the rules. 
Although practicality beats purity. 
Errors should never pass silently. 
Unless explicitly silenced. 
In the face of ambiguity, refuse the temptation to guess. 
There should be one-- and preferably only one --obvious way to do it. 
Although that way may not be obvious at first unless you're Dutch. 
Now is better than never. 
Although never is often better than *right* now. 
If the implementation is hard to explain, it's a bad idea. 
If the implementation is easy to explain, it may be a good idea. 
Namespaces are one honking great idea -- let's do more of those! 
```