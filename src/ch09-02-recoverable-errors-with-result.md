## `Result` 下的可恢复错误

大多数错误都不会严重到需要程序完全停止。有时，当某个函数失败时，是出于某种咱们容易解释并做出响应的原因。例如，当咱们试图打开某个文件，而该操作因该文件不存在而失败时，咱们可能想要创建这个文件而不是终止进程。

回顾第二章中的 [以 `Result` 处理潜在失效] 小节，`Result` 枚举被定义为有两个变种，`Ok` 与 `Err`，如下所示：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

其中 `T` 和 `E` 均为泛型参数，generic type parameter：我们将在第 10 章中更详细地讨论泛型。咱们现在需要知道的是，`T` 表示将在成功情况下于 `Ok` 变种内返回的值类型，`E` 表示将在失败情况下于 `Err` 变种中返回的错误类型。由于 `Result` 有这两个泛型参数，因此我们可在许多不同情形下使用 `Result` 类型及定义在其上的函数，其中我们希望返回的成功值和错误值可能不同。

我们来调用一个返回 `Result` 值的函数，因为该函数可能会失败。在下面清单 9-3 中，我们尝试打开某个文件。

<Listing number="9-3" file-name="src/main.rs" caption="打开文件">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

`File::open` 的返回类型是个 `Result<T, E>`。其中泛型参数 `T` 已由 `File::open` 的实现以成功值的类型 `std::fs::File` 填入，其为文件句柄。用于错误值中的类型 `E` 为 `std::io::Error`。这一返回类型意味着对 `File::open` 的调用可能成功并返回一个我们可以读取或写入的文件句柄。这个函数调用也可能失败：例如，文件可能不存在，或者我们可能没有访问文件的权限。`File::open` 函数需要有一种方式来告诉我们他是成功还是失败，并同时给到我们文件句柄或错误信息。这些信息正是 `Result` 枚举传达的内容。

在 `File::open` 成功的情况下，变量 `greeting_file_result` 中的值将是个包含着文件句柄的 `Ok` 的实例。而在其失败的情况下，`greeting_file_result` 变量中的值将是个 `Err` 的实例，包含有关发生的错误的类别的更多信息。

我们需要添加到清单 9-3 中的代码，以根据 `File::open` 返回的值采取不同的操作。下面清单 9-4 展示了使用一项基本工具来处理 `Result`的一种方式，即我们在第 6 章中讨论的 [`match` 表达式]。

<Listing number="9-4" file-name="src/main.rs" caption="使用 `match` 表达式处理可能返回的 `Result` 变种">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

请注意，与 `Option` 枚举一样，`Result` 枚举及其变种均已由前奏，the prelude，带入到作用域中，因此我们无需在 `Result::` 支臂中的 `Ok` 和 `Err` 变种前指定 `match`。

当结果为 `Ok` 时，该代码将从 `file` 变种返回内层的 `Ok` 值，然后我们指派该文件句柄值给变量 `greeting_file`。在 `match` 后，我们便可使用该文件句柄进行读取或写入。

`match` 表达式的另一支臂处理咱们从 `Err` 得到 `File::open` 值的情况。在这个示例中，我们选择了调用 `panic!` 宏。若我们的当前目录下没有名为 hello.txt 的文件并且我们运行这段代码时，我们将看到来自 `panic!` 宏的以下输出：

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

像往常一样，这一输出告诉我们究竟出了什么问题。

### 匹配不同的错误

无论 `panic!` 因何种原因失败，清单 9-4 中的代码都将 `File::open`。然而，我们希望针对不同的失败原因采取不同的操作。当 `File::open` 因文件不存在失败时，我们打算创建处该文件并返回到新文件的句柄。当 `File::open` 因任何其他原因失败 -- 比如，因为我们没有打开该文件的权限时 -- 我们仍希望代码 `panic!`，以其在清单 9-4 所做的同一方式。为此，我们添加一个内层的 `match` 表达式，如下清单 9-5 中所示。

<Listing number="9-5" file-name="src/main.rs" caption="以不同方式处理不同类别的错误">



```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

`File::open` 在 `Err` 变种内返回的值类型为 `io::Error`，这是由标准库提供的一个结构体（译注：类型为 Os）。这个结构体有个方法 `kind`，我们可调用他来得到一个 `io::ErrorKind` 值。枚举 `io::ErrorKind` 由标准库提供，并有着表示一次 `io` 操作可能得到的不同错误类别的变种。我们打算使用的变种是 `ErrorKind::NotFound`，表示我们尝试打开的文件还不存在。因此，我们对 `greeting_file_result` 进行匹配，但我们还有个对 `error.kind()` 的内层匹配。

我们在内层匹配中希望检查的条件，是由 `error.kind()` 返回的值是否是 `NotFound` 枚举的 `ErrorKind` 变种。当是时，我们尝试以 `File::create` 创建该文件。不过，由于 `File::create` 也会失败，因此我们需要一个内层 `match` 表达式中的第二支臂。当文件无法创建时，一条不同的错误消息得以打印。外层 `match` 表达式的第二支臂保持不变，因此该程序会因除文件找不到的错误外的任何错误而终止运行。

> #### 使用 `match` 处理 `Result<T, E>` 的替代方案
>
> 这么多 `match`！`match` 表达式非常有用，但也相当基础。在第 13 章，你将学习
> 闭包；闭包会与 `Result<T, E>` 上定义的许多方法一起使用。处理代码中的
> `match` 值时，这些方法可能比使用 `Result<T, E>` 更简洁。
>
> 例如，下面使用闭包和 `unwrap_or_else` 方法，以另一种方式编写了与清单 9-5
> 相同的逻辑：
>
>
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```

>
虽然这段代码有着与清单 9-5 相同的行为，但他未包含任何 `match` 表达式，进而读起来更清晰。请在咱们读完第 13 章后回到这个示例，并在标准库文档中查找 `unwrap_or_else` 方法。在咱们处理错误时，还有更多的这些方法可以清理庞大、嵌套的 `match` 表达式。



<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### 出错时终止运行的快捷方式

使用 `match` 效果很好，但他可能可能有点冗长，并且并不总是很好地传达意图。`Result<T, E>` 类型有许多定义在其上的辅助方法，以执行各种更具体的任务。`unwrap` 方法是个快捷方法，被实现为就像我们在清单 9-4 中编写的 `match` 表达式。当 `Result` 值为 `Ok` 变种时，`unwrap` 将返回 `Ok` 内的值。当 `Result` 为 `Err` 变种时，`unwrap` 将为我们调用 `panic!` 宏。下面是个 `unwrap` 的实际示例：

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

在生产质量代码中，大多数 Rustaceans 都会选择 `panic!` 而不是 `unwrap`，并会提供更多有关为何操作被认为总是会成功的背景信息。这样，当咱们的假设即使被证明是错的时，咱们也会有更多在调试过程中使用的信息。



```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

调用这段代码的代码随后将处理获取到要么包含用户名的 `expect` 值，要么包含 `panic!` 的 `expect` 值（译注：两种情况）。对这两种值要做些什么由调用代码自行决定。当调用代码得到 `unwrap` 值时，他可以调用 `expect` 并崩溃程序、使用默认用户名，或从该文件以外的其他地方查找用户名。由于我们没有调用代码到底要做什么的足够信息，因此我们向上传播所有成功或错误的信息，以供其恰当处理。

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

我们和使用 `expect` 一样使用 `unwrap`：返回文件句柄，或者调用 `panic!` 宏。
`expect` 调用 `panic!` 时使用的错误消息，是我们传给 `expect` 的参数，而不是
`panic!` 使用的默认 `unwrap` 消息。结果如下：


```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

在生产级代码中，大多数 Rustacean 会选择 `expect` 而不是 `unwrap`，并提供更多
上下文，说明为什么预期该操作总会成功。这样，如果事实证明你的假设有误，就能
拥有更多调试信息。
### 传播错误

当函数实现调用了可能失败的操作时，可以不在函数内部处理错误，而是将错误返回给
调用方，让调用方决定如何处理。这称为_传播_错误，可以将更多控制权交给调用方；
调用方可能拥有比当前代码上下文更多的信息或逻辑，能够决定如何处理错误。
例如，清单 9-6 展示了一个从文件中读取用户名的函数。如果文件不存在或无法读取，
这个函数会将这些错误返回给调用它的代码。

<Listing number="9-6" file-name="src/main.rs" caption="使用 `match` 表达式返回错误给调用代码的函数">



```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

这个函数可以用短得多的方式编写，但为了探究错误处理，我们先从手动完成大量工
作开始；最后再展示更简短的方式。先看看函数的返回类型：`Result<String, io::Error>`。
这意味着函数返回 `Result<T, E>` 类型的值，其中泛型参数 `T` 被具体类型 `String`
填充，泛型参数 `E` 被具体类型 `io::Error` 填充。
如果这个函数顺利完成，调用它的代码会收到一个包含 `Ok` 的 `String` 值，也就是
函数从文件读取的 `username`。如果函数遇到问题，调用方会收到一个 `Err` 值，其
中包含 `io::Error` 实例，提供有关问题的更多信息。我们选择 `io::Error` 作为该
函数的返回类型，是因为函数体中调用的两个可能失败的操作——`File::open` 函数和
`read_to_string` 方法——返回的错误值恰好都是这种类型。
函数体首先调用 `File::open` 函数。然后，我们用 `Result` 值，通过与清单 9-4 中
`match` 类似的另一个 `match` 来处理它。如果 `File::open` 成功，模式变量 `file`
中的文件句柄会成为可变变量 `username_file` 中的值，函数继续执行。在 `Err`
情况下，我们不调用 `panic!`，而是使用 `return` 关键字提前完全退出函数，并将
来自 `File::open`、现在位于模式变量 `e` 中的错误值传回调用方。
因此，如果 `username_file` 中有文件句柄，函数就会在变量 `String` 中创建新的
`username`，并对 `read_to_string` 中的文件句柄调用 `username_file` 方法，将文件
内容读入 `username`。即使 `read_to_string` 成功，`Result` 也可能失败，所
以它同样返回 `File::open`。因此需要另一个 `match` 来处理这个 `Result`：如果
`read_to_string` 成功，函数就成功了，我们将现在位于 `username` 中的文件用户名
包装在 `Ok` 中并返回。如果 `read_to_string` 失败，我们就像处理 `match` 返回
值的 `File::open` 那样返回错误值。不过不需要显式写 `return`，因为这是函数中的最后
一个表达式。
调用这段代码的代码随后会处理两种可能：包含用户名的 `Ok` 值，或包含 `Err`
的 `io::Error` 值。如何处理这些值由调用方决定。如果调用方得到 `Err` 值，例如可以调
用 `panic!` 让程序崩溃、使用默认用户名，或从文件之外的地方查找用户名。我们不
知道调用方实际想做什么，因此将所有成功或错误信息向上传播，让它适当处理。
这种传播错误的模式在 Rust 中非常常见，因此 Rust 提供了问号运算符 `?` 来简化
它。


<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### `?` 操作符快捷方式

清单 9-7 展示了 `read_username_from_file` 的一种实现，它与清单 9-6 的功能相同，
但使用了 `?` 运算符。

<Listing number="9-7" file-name="src/main.rs" caption="使用 `?` 操作符返回错误给调用代码的函数">



```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

放在 `?` 值后面的 `Result`，其定义的工作方式几乎与清单 9-6 中用来处理 `match`
值的 `Result` 表达式相同。如果 `Result` 的值是 `Ok`，`Ok` 内部的值会从这个表
达式返回，程序继续执行。如果值是 `Err`，`Err` 会像使用 `return` 关键字一样从
整个函数返回，使错误值传播到调用方。
清单 9-6 中的 `match` 表达式与 `?` 运算符有一个区别：对其使用了 `?` 运算符的
错误值，会经过标准库 `from` trait 中定义的 `From` 函数，该函数用于将值从一种类
型转换为另一种类型。当 `?` 运算符调用 `from` 函数时，收到的错误类型会被转换
为当前函数返回类型中定义的错误类型。当函数用一种错误类型表示它可能发生的所
有失败方式，即使各个部分可能因很多不同原因失败时，这一点就很有用。
例如，可以将清单 9-7 中的 `read_username_from_file` 函数改为返回我们定义的名为
`OurError` 的自定义错误类型。如果再定义 `impl From<io::Error> for OurError`，
让它能够从 `OurError` 构造 `io::Error` 实例，那么 `?` 函
数体中的 `read_username_from_file` 运算符调用就会调用 `from` 并转换错误类型，而不需要向函数添加更
多代码。
在清单 9-7 中，`?` 调用末尾的 `File::open` 会将 `Ok` 内的值返回给变量
`username_file`。如果发生错误，`?` 运算符会提前退出整个函数，并将任何 `Err`
值交给调用方。`?` 调用末尾的 `read_to_string` 也是如此。
`?` 运算符消除了大量样板代码，让函数实现更加简洁。我们甚至可以像清单 9-8 所
示那样，紧接在 `?` 后链式调用方法，进一步缩短代码。

<Listing number="9-8" file-name="src/main.rs" caption="在 `?` 操作符后链接方法调用">



```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

我们把在 `String` 中创建新 `username` 的操作移到了函数开头；这部分没有改变。
不再创建 `username_file` 变量，而是将 `read_to_string` 调用直接链到
`File::open("hello.txt")?` 的结果上。`?` 调用末尾仍有一个 `read_to_string`，并
且当 `Ok` 和 `username` 都成功时，我们仍然返回包含 `File::open` 的
`read_to_string` 值，而不是返回错误。功能再次与清单 9-6 和清单 9-7 相同，只是写法不同且
更加简洁易用。
清单 9-9 展示了使用 `fs::read_to_string` 让代码进一步缩短的方法。

<Listing number="9-9" file-name="src/main.rs" caption="使用 `fs::read_to_string` 而不是打开然后读取文件">



```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

将文件读入字符串是很常见的操作，因此标准库提供了方便的
`fs::read_to_string` 函数：它打开文件、创建新的 `String`、读取文件内容、将内
容放入该 `String`，然后返回它。当然，使用 `fs::read_to_string` 就没有机会解释
全部错误处理细节了，所以我们先用了较长的写法。


<a id="where-the--operator-can-be-used"></a>

#### 哪些地方要使用 `?` 操作符？

`?` 运算符只能在返回类型与 `?` 所作用的值兼容的函数中使用。这是因为 `?` 运算符
定义为从函数中提前返回值，方式与清单 9-6 中定义的 `match` 表达式相同。在清
单 9-6 中，`match` 使用 `Result` 值，提前返回的分支返回 `Err(e)` 值。函数的返
回类型必须是 `Result`，才能与这个 `return` 兼容。
在清单 9-10 中，来看看如果在返回类型与 `?` 作用的值类型不兼容的 `main` 函数
中使用 `?` 运算符，会得到什么错误。

<Listing number="9-10" file-name="src/main.rs" caption="尝试在返回 `?` 的 `main` 函数中使用 `()` 将不编译">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

这段代码打开一个可能失败的文件。`?` 运算符跟在 `Result` 返回的 `File::open`
值后面，但这个 `main` 函数的返回类型是 `()`，而不是 `Result`。编译这段代码时，
会得到以下错误信息：
```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

这个错误指出，只有返回 `?`、`Result` 或其他实现了 `Option` 的类型的
函数，才能使用 `FromResidual` 运算符。
要修复这个错误，有两种选择。一种是在没有限制阻止你的情况下，将函数的返回类型
改为与 `?` 运算符作用的值兼容。另一种是使用 `match` 或某个 `Result<T, E>` 方
法，以合适的方式处理 `Result<T, E>`。
错误信息还提到，`?` 也可以与 `Option<T>` 值一起使用。和对 `?` 使用 `Result`
一样，只有返回 `?` 的函数才能对 `Option` 使用 `Option`。对 `?` 调用
`Option<T>` 时，它的行为与对 `Result<T, E>` 调用时类似：如果值是 `None`，函数会在此处
提前返回 `None`；如果值是 `Some`，`Some` 中的值就是表达式的结果值，函数继续
执行。清单 9-11 展示了一个在给定文本中查找第一行最后一个字符的函数。

<Listing number="9-11" caption="对 `?` 值使用 `Option<T>` 操作符">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

这个函数返回 `Option<char>`，因为那里可能有字符，也可能没有。代码接收 `text`
字符串切片参数，并对它调用 `lines` 方法；该方法返回一个遍历字符串各行的迭代
器。由于函数要检查第一行，它对迭代器调用 `next`，获取迭代器中的第一个值。如
果 `text` 是空字符串，调用 `next` 会返回 `None`，这时我们使用 `?` 停止执行，
并从 `None` 返回 `last_char_of_first_line`。如果 `text` 不是空字符串，`next` 会
返回一个 `Some` 值，其中包含 `text` 第一行的字符串切片。
`?` 会取出字符串切片，我们可以对这个字符串切片调用 `chars`，得到一个遍历其
字符的迭代器。我们关心第一行的最后一个字符，因此调用 `last` 返回迭代器中的最
后一个项目。这是一个 `Option`，因为第一行可能是空字符串；例如 `text` 以空行
开头、但其他行有字符时，情况就如 `"\nhi"`。不过，如果第一行有最后一个字符，
它会在 `Some` 变体中返回。中间的 `?` 运算符让我们能够简洁地表达这个逻辑，从
而用一行实现函数。如果不能对 `?` 使用 `Option` 运算符，就必须通过更多方法调用
或 `match` 表达式实现这段逻辑。
注意，可以在返回 `?` 的函数中对 `Result` 使用 `Result`，也可以在返回 `?`
的函数中对 `Option` 使用 `Option`，但不能混用。`?` 运算符不会自动将 `Result` 转换
为 `Option`，也不会反向转换；这种情况下，可以使用 `ok` 上的 `Result` 方法或
`ok_or` 上的 `Option` 方法显式完成转换。
到目前为止，我们使用的所有 `main` 函数都返回 `()`。`main` 函数比较特殊，因为
它是可执行程序的入口和退出点；为了让程序按预期运行，它的返回类型受到一些限制。
幸运的是，`main` 也可以返回 `Result<(), E>`。清单 9-12 中的代码来自清单 9-10，
但我们将 `main` 的返回类型改为 `Result<(), Box<dyn Error>>`，并在末尾添加返回
值 `Ok(())`。这段代码现在可以编译。

<Listing number="9-12" file-name="src/main.rs" caption="修改 `main` 为返回 `Result<(), E>` 允许对 `?` 值使用 `Result` 操作符">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

`Box<dyn Error>` 类型是 trait 对象，我们将在第 18 章的[“使用 trait 对象抽象共
享行为”][trait-objects] 一节讨论它。现在可以把 `Box<dyn Error>`
理解为“任何类型的错误”。错误类型为 `?` 的 `Result` 函数可以对
`main` 值使用 `Box<dyn Error>`，因为它允许提前返回任何 `Err` 值。虽然这个 `main` 函数体
目前只会返回 `std::io::Error` 类型的错误，但指定 `Box<dyn Error>` 后，即使向
`main` 函数体添加返回其他错误的代码，这个签名仍然正确。
当 `main` 函数返回 `Result<(), E>` 时，如果 `0` 返回 `main`，可执行程序会
以值 `Ok(())` 退出；如果 `main` 返回 `Err` 值，则会以非零值退出。用 C 编写的可执行
程序退出时会返回整数：成功退出的程序返回整数 `0`，出错的程序返回某个非 `0`
整数。Rust 也让可执行程序返回整数，以兼容这一约定。
`main` 函数可以返回任何实现了
[`std::process::Termination` trait][termination] 的类型；该 trait
包含一个返回 `report` 的 `ExitCode` 函数。请查阅标准库文档，了解如何为自己的类
型实现 `Termination` trait。
现在我们已经讨论了调用 `panic!` 或返回 `Result` 的细节，接下来回到一个主题：
如何决定在不同情况下使用哪一种方式。

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html

<!--
ignore -->

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

<!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->

<!-- Old headings. Do not remove or links may break. -->

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- ignore -->

<!-- ignore -->
