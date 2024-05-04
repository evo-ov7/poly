# Poly WIP

Poly is a very simple programming language designed around easy portability to any platform.
As such it doesn't contain any I/O functionality but focuses on a simple yet powerful semantic core, allowing the same codebase to be reliably deployed across various platforms.

The transpiller is written in Python 3, synopsis: `poly.py [-options...] inputfile backend [-backend_options...]`

Currently implemented backends: C99+, Python 2.7+

### Options

`-indentation=n` (default:2) Indent code blocks by `n` spaces

`-namespace_separator=string` (default:_) Separate the namespace from names using this `string`

`-prefix=string` (default:) Prefix all identifiers with `string`

`-debug` Produce debug output

### C Backend Options

`-typedef`  Object types can be referred to by name, instead of having to use the "struct" prefix

`-exact_integers`  The created output will use exact-bitwidth integer types. note that these are not available on every C compiler

`-same_field_order`  Object fields will appear in the same order as in the source, instead of using an optimized layout based on the type sizes

`-allow_visible_overflow`  If exact-bitwidth integer types are unavailable on the C compiler then this option allows integer variables returned by functions and passed into functions to contain garbage data in the excess bits

### Python Backend Options

`-allow_visible_overflow` Allows integer variables returned by functions and passed into functions to contain garbage data in the excess bits

# Poly Language Specification

Poly is still under development, so the specification is subject to change. For some examples check the test file test.poly.

A Poly program consists of objects and functions. Objects are a named collection of fields while functions are a sequence of statements containing operators and variables.

## Type System

Poly is statically typed, so all variables and fields have a known type before any code execution takes place. To allow for limited dynamicity, the void type `*` allows explicitly casting some types at runtime.

### Numeric Types

A byte is defined as 8 bits. All numeric types come in 4 sizes: 1,2,4,8 bytes containing 8,16,32,64 bits respectively.

`b1` `b2` `b4` `b8` unsigned numbers with the specified number of bytes

`s1` `s2` `s4` `s8` integers with the specified number of bytes, negative numbers are represented using [two's complement](https://en.wikipedia.org/wiki/Two%27s_complement)

`f1` `f2` `f4` `f8` floating point numbers with the specified number of bytes. These types do not have a defined binary representation or precision besides bigger types possibly having higher numeric precision.

### Reference Types

All of these types refer to some data in memory. Several references may refer to the same data or may refer to no data at all (null reference). Any object has a reference type of the same name as the object.

`fun[*][([[parametername ]type[,[parametername ]type]...])->([type[,type]...])]` Function types refer to a function as well as a signature indicating the parameters and return values. A function type lacking its signature is a void function type, which merely serves explicit typecasting and cannot be called.

Lastly there is the void type `*`, which merely serves explicit typecasting and has no behavior of its own.

### Array Types

Any type other than void can be turned into array form by appending a `*` to the typename. Array types are reference types of a sequence of values, which can only be accessed by a numerical index.

### Typeconversion

Values of some types can be converted into each other. The allowed conversions are as follows:

Any non-array numeric type can be converted to any other non-array numeric type. The resulting value is the closest value to the original value that the new type can contain. The only exception are conversions between integers and unsigned numbers, where the bitpattern may be truncated or extended with zero bits but not changed regardless of the changing interpretation.

Any particular object type can be converted to void and back to the original type.

Any function type can be converted to any other function type, but may only be called if the signature of the referenced function and the function type match.

Any array numeric type can be converted to void and back to the original type.

## Syntax & Semantics

Custom identifiers for functions, objects, namespaces, fields and variables may only contain the [ASCII](https://en.wikipedia.org/wiki/ASCII) encoding of the following characters: `abcdefghijklmnopqrstuvwxyz0123456789_`. The first symbol must be a character.

Operators consist of the ASCII encoding of the following characters: `+-*/~^!=><|&%#v()[]}.,`.

Values consist of the ASCII encoding of the following characters: `0123456789.xbsilqhfd`. The first symbol must be a number.

`//` Denotes the start of a comment until the end of the line. Any symbols following it have no semantic meaning.

Poly's reserved identifiers are: `if`,`else`,`elif`,`loop`,`break`,`continue`,`v`,`delete`,`return`.

### Top-Level Declarations

Poly's syntax is based on the indentation of lines, being defined as the number of ASCII ` ` characters appearing at the start of the line. All top-level declarations must occur without indentation.

### Namespace Delimiters

`namespace [name]` - Declare the start of namespace `name`.

`namespace [name] end` - Declare the end of namespace `name`.

Every other top-level declaration must occur between two matching namespace delimiters. All namespaces must have a unique name, including the nameless namespace.

### Object Declaration

`object name` - Declare the start of the definition of object `name`. The definitions for the object's fields will be on the following lines.

### Function Declaration

`function name([name[=value] type[,name[=value] type]...])->([name type[,name type]...])`

Declare function `name` and provide its signature, containing the order, `type`, `name` and possibly a default `value` for its parameters and return values. The function's code will be on the following lines

## Indented Statements

All indented statements refer to the previous statement with a lower amount of indentation, unless stated otherwise.

### Object Field Definition

`name type` - Define field `name` with `type`. Function types are not allowed. Object fields can be of a special type, indicated by the array signifier `*` followed by a number. This type indicates that the field's value will be located inside the object. If the number is 0, then it is not an array but a reference type. Fields of this special type cannot have their reference changed.

## Operators

All operators in Poly only operate on operands of the same type, unless stated otherwise.

### Unary Operators

* `+` - Turns its integer or floating point operand positive
* `-` - Changes the sign of its integer or floating point operand
* `~` - Rounds to nearest integer if the operand is floating point, performs bitwise not otherwise
* `~.` - Rounds its floating point operand towards zero (truncates the fractional part)
* `~^` - Rounds its floating point operand towards infinity
* `~v` - Rounds its floating point operand towards negative infinity
* `+#1` - Counts the number of 1 bits in its integer/number operand
* `+0..` - Counts the number of leading 0 bits in its integer/number operand
* `+..0` - Counts the number of trailing 0 bits in its integer/number operand

### Access Operators

The operands of all access operators don't have to be of the same type
* `.` - Used to access the field of a value of type object, like `variable.field`
* `[]` - Used to index into a value of type array, like `array[index]`
* `()` - Used to call a value of type function, like `function(param1,param2)`
* `()` - Used to cast the type of a value, like `variable(type)`

### Binary Operators

* `+` - Performs addition
* `-` - Performs subtraction
* `*` - Performs multiplication
* `/` - Performs division on floating point numbers (sign is undefined). Performs integer division on integers/numbers with the result being rounded towards zero.
* `%` - Computes the remainder of division for floating point numbers (sign is undefined). Computes the remainder of integer division for integers/numbers. The sign of the remainder is the same as the sign of the quotient
* `^` - Performs bitwise exclusive or
* `|` - Performs bitwise or
* `&` - Performs bitwise and
* `<<` - Performs bitwise left shift. Both operands have to be integers/numbers, but they don't have to be of the same type
* `>>` - Performs bitwise right shift for number operands and arithmetic right shift for integers. Both operands have to be integers/numbers, but they don't have to be of the same type.
* `>>>` - Performs bitwise right rotation. Both operands have to be integers/numbers, but they don't have to be of the same type
* `<<<` - Performs bitwise left rotation. Both operands have to be integers/numbers, but they don't have to be of the same type
* `>` - Checks if numeric operand 1 is greater than numeric operand 2
* `<` - Checks if numeric operand 1 is lesser than numeric operand 2
* `>=` - Checks if numeric operand 1 is greater than or equal to numeric operand 2
* `<=` - Checks if numeric operand 1 is lesser than or equal to numeric operand 2
* `=` - Checks if operand 1 and 2 have the same value
* `!=` - Checks if operand 1 and 2 don't have the same value

## Function Statements

The code of a function is defined by a sequence of function statements, with each occupying a line. There are 4 types:

`expression1=expression2` - Ordinary assignment of the value resulting from `expression1` to the location resulting from `expression2`.

`expression1}expression2` - Assignment with compound operation. The value resulting from `expression1` is copied to the location resulting from `expression2`, with the old value of `expression1` also contributing to the computation in `expression2`.

`function([param1[,param2]...])` - A function call for its side-effects.
`expression1[=return],expression2[=return][,expression3[=return]]...=function([param1[,param2]...])` - A compound assignment with each expression left of the `=` receiving a return value from the function in `expression3` producing multiple return values. The name of a return value may be specified to not rely on the position of the return value. A `_` may be substituted for an expression to discard unwanted return values.

Variables are defined by simply assigning a value to their identifier, though the value's type must be unambiguous.


## Expressions

An expression is a sequence of operators, identifiers and literal values. An expression may either designate a location where a value will be stored, or a location from which a value will be loaded for further computation by operators. Expressions are subdivided into blocks by space ` `.

The order of operations within an expression is determined by a few simple rules:
* Unary operators within a block are executed before Binary operators
* Binary operators within a block are executed left to right
* Blocks which are separated by the same amount of ` ` are executed left to right
* Blocks which are separated by less ` ` are executed before blocks separated by more ` `

The abacus operator `}` can be used to explicitly change the execution order. The abacus operator causes operators, which are to its left in the same block, to be executed before operators to its right within the same block. If the abacus is the first symbol of a block, then it causes *all* operators to its left to be executed before any operators to its right.

The abacus operator may also appear as the first operator in a compound assignment. In this case it is substituted by the value of the assignment's destination expression.

### Literal Values

Literal values of numeric type represent a specific value of their type. Floating point literals use base 10 and always contain the decimal point `.` in addition to at least 1 digit. They can be suffixed by a type specifier: `d`ouble(f8), `f`loat(f4), `h`alf(f2), `q`uarter(f1). Number literals use base 10 by default and may be suffixed by a type specifier: `l`ong(b8), `i`nt(b4), `s`hort(b2), `b`yte(b1). Type suffxes are generally only necessary when defining a new variable. Number literals can also be specified in base 2(binary), by using the `0b` prefix. Number literals can also be specified in base 16(hexadecimal), by using the `0x` prefix. Note that hexadecimal literals must contain an even number of digits (excluding the prefix).