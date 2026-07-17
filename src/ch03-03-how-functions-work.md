## 函数

函数在 Rust 代码中随处可见。你已经见过这门语言中最重要的函数之一：`main` 函数，它是许多程序的入口点。你也见过 `fn` 关键字，它允许你声明新函数。

Rust 代码使用*蛇形命名法*作为函数和变量名称的惯用风格：所有字母都小写，单词之间用下划线分隔。下面的程序包含一个函数定义示例：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

在 Rust 中，我们输入 `fn`，后跟函数名和一对括号来定义函数。花括号告诉编译器函数体从哪里开始、到哪里结束。

我们可以输入已定义函数的名称，后跟一对括号，来调用这个函数。由于程序中定义了 `another_function`，所以可以在 `main` 函数内部调用它。注意，我们在源代码中将 `another_function` 定义在 `main` 函数*之后*；当然也可以在之前定义。Rust 不在意你在哪里定义函数，只要函数定义在调用者可见的某个作用域中即可。

让我们创建一个名为*functions*的新二进制项目，进一步探索函数。将 `another_function` 示例放入*src/main.rs*并运行它。你应该会看到如下输出：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

这些代码行按照它们在 `main` 函数中出现的顺序执行。首先打印“Hello, world!”，然后调用 `another_function` 并打印它的消息。

### 参数

我们可以定义带有*参数*的函数。参数是函数签名中的特殊变量。当函数有参数时，你可以为这些参数提供具体值。严格来说，这些具体值称为*实参*，但在日常交流中，人们往往会交替使用“形参”和“实参”这两个词，既指函数定义中的变量，也指调用函数时传入的具体值。

在这个版本的 `another_function` 中，我们添加一个参数：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

尝试运行这个程序；你应该会得到如下输出：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

`another_function` 的声明有一个名为 `x` 的参数。`x` 的类型被指定为 `i32`。当我们将 `5` 传入 `another_function` 时，`println!` 宏会将 `5` 放在格式字符串中原本包含 `x` 的那对花括号处。

在函数签名中，你*必须*声明每个参数的类型。这是 Rust 设计中经过深思熟虑的决定：要求在函数定义中添加类型注解，意味着编译器几乎永远不需要你在代码的其他地方再使用类型注解来判断你指的是什么类型。如果编译器知道函数期望哪些类型，它也能提供更有帮助的错误消息。

定义多个参数时，用逗号分隔参数声明，如下所示：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

这个示例创建了一个名为 `print_labeled_measurement`、带有两个参数的函数。第一个参数名为 `value`，类型是 `i32`。第二个参数名为 `unit_label`，类型是 `char`。随后，该函数会打印包含 `value` 和 `unit_label` 的文本。

让我们尝试运行这段代码。将*functions*项目当前*src/main.rs*文件中的程序替换为前面的示例，然后使用 `cargo
run` 运行它：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

由于我们调用函数时将 `5` 作为 `value` 的值、将 `'h'` 作为 `unit_label` 的值，所以程序输出包含这两个值。

### 语句与表达式

函数体由一系列语句组成，末尾可以选择性地跟随一个表达式。到目前为止，我们介绍的函数都不包含结尾表达式，但你已经见过作为语句一部分的表达式。由于 Rust 是一种基于表达式的语言，这是一个需要理解的重要区别。其他语言没有同样的区别，所以让我们看看什么是语句和表达式，以及它们的差异如何影响函数体。

- *语句*是执行某些操作且不返回值的指令。
- *表达式*会计算出一个结果值。

让我们看一些示例。

实际上，我们已经使用过语句和表达式。使用 `let` 关键字创建变量并为其赋值，就是一条语句。在清单 3-1 中，`let y = 6;` 就是一条语句。

<Listing number="3-1" file-name="src/main.rs" caption="包含一条语句的 `main` 函数声明">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

函数定义也是语句；前面的整个示例本身就是一条语句。（稍后我们会看到，调用函数并不是语句。）

语句不会返回值。因此，你不能将一条 `let` 语句赋给另一个变量，下面的代码试图这样做，所以你会得到一个错误：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

运行这个程序时，你会得到类似下面的错误：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

`let y = 6` 语句不会返回值，因此没有任何东西可以绑定到 `x`。这与 C 和 Ruby 等其他语言中的情况不同，在那些语言中，赋值会返回被赋的值。在这些语言中，你可以写出 `x = y = 6`，让 `x` 和 `y` 都拥有值 `6`；Rust 并非如此。

表达式会计算出一个值，并构成你将要编写的大部分 Rust 代码。考虑一个数学运算，例如 `5 + 6`，它是一个计算结果为 `11` 的表达式。表达式可以是语句的一部分：在清单 3-1 中，语句里的 `6`（也就是 `let y = 6;`）是一个计算结果为 `6` 的表达式。调用函数是表达式，调用宏也是表达式。用花括号创建的新作用域块也是表达式，例如：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

这个表达式：

```rust,ignore
{
    let x = 3;
    x + 1
}
```

在这里是一个值为 `4` 的代码块。这个值会绑定到 `y`，作为 `let` 语句的一部分。注意，`x + 1` 这一行末尾没有分号，这一点不同于你目前看到的大多数代码行。表达式不包含结尾分号。如果在表达式末尾添加分号，就会把它转换为语句，此时它不会返回值。接下来探索函数返回值和表达式时，请记住这一点。

### 带返回值的函数

函数可以向调用它的代码返回值。我们不为返回值命名，但必须在箭头（`->`）后声明它的类型。在 Rust 中，函数的返回值等同于函数体代码块中最后一个表达式的值。你可以使用 `return` 关键字并指定一个值，让函数提前返回，但大多数函数都会隐式返回最后一个表达式。下面是一个返回值的函数示例：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

这里没有函数调用、宏，甚至没有 `let` 语句出现在 `five` 函数中，只有数字 `5` 本身。这在 Rust 中是一个完全有效的函数。注意，这个函数也指定了返回类型，即 `-> i32`。尝试运行这段代码；输出应该如下所示：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

数字 `5` 在 `five` 中是函数的返回值，这就是返回类型为 `i32` 的原因。让我们更详细地看看这一点。这里有两个重要方面：首先，`let x = five();` 这一行表明，我们使用函数的返回值初始化一个变量。由于函数 `five` 返回 `5`，这行代码等同于下面这行：

```rust
let x = 5;
```

其次，`five` 函数没有参数，并定义了返回值的类型，但函数体只是一个没有分号的孤零零的 `5`，因为它是我们希望返回其值的表达式。

让我们看另一个示例：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

运行这段代码会打印 `The value of x is: 6`。但是，如果我们在包含 `x + 1` 的那一行末尾加上分号，将它从表达式改成语句，会发生什么呢？

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

编译这段代码会产生如下错误：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

主要错误消息 `mismatched types` 揭示了这段代码的核心问题。函数 `plus_one` 的定义表明它会返回一个 `i32` 值，但语句不会计算出值，这由 `()`（单元类型）表示。因此，函数没有返回任何值，这与函数定义相矛盾，于是产生了错误。在这段输出中，Rust 提供了一条可能有助于解决问题的消息：它建议移除分号，这样就能修复错误。
