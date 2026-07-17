<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## 重定向错误到标准错误

目前，我们使用 `println!` 宏将所有输出写入终端。在大多数终端中，输出分为两类：用于一般信息的*标准输出*（`stdout`），以及用于错误消息的*标准错误*（`stderr`）。这种区分让用户可以选择将程序成功运行时的输出重定向到文件，同时仍然把错误消息打印到屏幕上。
`println!` 宏只能打印到标准输出，因此我们必须使用其他东西来打印到标准错误。
### 检查错误被写到何处

首先，我们来观察 `minigrep` 打印的内容目前是如何写到标准输出的，包括我们打算写到标准错误的任何错误信息。我们将通过重定向标准输出流到文件，同时故意引发一个报错来实现这点。我们不会重定向标准错误流，因此发送到标准错误的内容，都将继续在屏幕上显示。

命令行程序应发送错误信息到标准错误流，这样即使我们重定向了标准输出流到文件，我们仍然可以在屏幕上看到错误信息。我们的程序目前表现不佳：我们将看到他反而会保存错误消息输出到文件中！

为了演示这一行为，我们将以 `>`，和我们打算重定向标准输出流到其中的文件路径 output.txt 运行程序。我们将不传递任何参数，这应引发错误：

```console
$ cargo run > output.txt
```

`>` 语法告诉 shell 将标准输出的内容写到 output.txt 而不是屏幕。我们没有看到我们期望打印到屏幕的错误信息，所以这意味着其必定已在文件中。下面是 output.txt 包含的内容：

```text
Problem parsing arguments: not enough arguments
```

没错，我们的错误信息正被打印到标准输出。这样的错误信息打印到标准错误会更有用，这样只有成功运行的数据才会出现在文件中。我们将改变这一点。

### 打印错误到标准错误

我们将使用下面清单 12-24 中的代码，来修改错误消息的打印方式。由于我们在这一章前面所做的重构，所有打印错误消息的代码都在 `main` 一个函数中。标准库提供了 `eprintln!` 宏，可以打印到标准错误流，因此咱们来修改我们之前调用 `println!` 打印错误的两处为使用 `eprintln!`。

<Listing number="12-24" file-name="src/main.rs" caption="使用 `eprintln!` 将错误消息写到标准错误而不是标准输出">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

现在咱们来以同一方式再次运行程序，不带任何参数并以 `>` 重定向标准输出：

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

现在我们在屏幕上看到错误，并且 output.txt 不包含任何内容，这正是我们对命令行程序所期望的行为。

我们来以不会导致错误的参数运行程序，但仍会重定向标准输出到文件，就像这样：

```console
$ cargo run -- to poem.txt > output.txt
```

我们不会看到任何到终端的输出，而 output.txt 将包含我们的结果：

<span class="filename">文件名： output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

这表明我们现在正恰如其分地对成功输出使用标准输出，对错误输出使用标准错误。

## 本章小节

这一章回顾了咱们迄今为止学过的一些主要概念，并介绍了在 Rust 中怎样执行常见的 I/O 操作。通过使用命令行参数、文件、环境变量以及用于打印错误的 `eprintln!` 宏，咱们现在已经准备好编写命令行应用了。结合前几章中的概念，咱们的代码将组织良好、能有效地存储数据于适当的数据结构中、很好地处理错误，并得以良好测试。

接下来，我们将探讨一些受函数式编程影响的 Rust 特性：闭包与迭代器。
