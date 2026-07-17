## 你好，世界！

现在你已经安装了 Rust，是时候编写你的第一个 Rust 程序了。学习新语言时，通常会先编写一个在屏幕上打印 `Hello, world!` 的小程序，所以我们也这样做！

> 注意：本书假定你基本熟悉命令行。Rust 不要求你使用特定的编辑器或工具，也不限制代码存放的位置，因此如果你更喜欢使用集成开发环境而不是命令行，尽管使用你喜欢的集成开发环境。如今许多集成开发环境都在一定程度上支持 Rust；详情请查阅集成开发环境的文档。Rust 团队一直在通过 `rust-analyzer` 致力于提供出色的集成开发环境支持。更多信息请参见 [附录 D][devtools]<!-- ignore -->。

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### 项目目录设置

首先，你要创建一个用于存放 Rust 代码的目录。对 Rust 来说，代码存放在哪里并不重要，但对于本书中的练习和项目，我们建议你在主目录下创建一个 _projects_ 目录，并将所有项目放在那里。

打开终端，输入以下命令，创建一个 _projects_ 目录，并在其中创建“Hello, world!”项目的目录。

对于 Linux、macOS 和 Windows 上的 PowerShell，请输入：

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

对于 Windows CMD，请输入：

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Rust 程序基础

接下来，创建一个新的源文件，并将其命名为 _main.rs_。Rust 文件总是以 _.rs_ 扩展名结尾。如果文件名包含多个单词，惯例是使用下划线分隔它们。例如，使用 _hello_world.rs_，而不是 _helloworld.rs_。

现在打开刚创建的 _main.rs_ 文件，输入清单 1-1 中的代码。

<Listing number="1-1" file-name="main.rs" caption="打印 `Hello, world!` 的程序">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

保存文件，然后回到 _~/projects/hello_world_ 目录中的终端窗口。在 Linux 或 macOS 上输入以下命令，编译并运行文件：

```console
$ rustc main.rs
$ ./main
Hello, world!
```

在 Windows 上，使用命令 `.\main` 代替 `./main`：

```powershell
> rustc main.rs
> .\main
Hello, world!
```

无论使用哪种操作系统，字符串 `Hello, world!` 都应该打印到终端。如果没有看到这个输出，请参阅安装小节中的[“故障排除”][troubleshooting]<!-- ignore -->部分，了解如何获得帮助。

如果打印出了 `Hello, world!`，恭喜你！你已经正式编写了一个 Rust 程序。这使你成为一名 Rust 程序员——欢迎加入！

<!-- Old headings. Do not remove or links may break. -->
<a id="anatomy-of-a-rust-program"></a>

### Rust 程序的结构

让我们详细看看这个“Hello, world!”程序。下面是其中的第一块内容：

```rust
fn main() {

}
```

这些代码行定义了一个名为 `main` 的函数。`main` 函数很特殊：它总是每个可执行 Rust 程序中最先运行的代码。在这里，第一行声明了一个名为 `main` 的函数，它没有参数，也不返回任何值。如果有参数，它们应放在括号（`()`）中。

函数体由 `{}` 包围。Rust 要求所有函数体都使用花括号。将左花括号放在函数声明所在的同一行，并在两者之间加一个空格，是一种良好的代码风格。

> 注意：如果你想在 Rust 项目中统一遵循标准风格，可以使用名为 `rustfmt` 的自动格式化工具，以特定风格格式化代码（关于 `rustfmt` 的更多信息，请参见[附录 D][devtools]<!-- ignore -->）。Rust 团队将这个工具和 `rustc` 一样包含在标准 Rust 发行版中，因此它应该已经安装在你的计算机上了！

`main` 函数体包含以下代码：

```rust
println!("Hello, world!");
```

这行代码完成了这个小程序的全部工作：将文本打印到屏幕上。这里有三个重要细节需要注意。

首先，`println!` 调用了 Rust 宏。如果它调用的是函数，写法会是 `println`（不带 `!`）。Rust 宏是一种编写代码的方式，可以生成代码来扩展 Rust 语法；我们将在[第 20 章][ch20-macros]<!-- ignore -->中更详细地讨论宏。现在你只需要知道，使用 `!` 表示调用的是宏而不是普通函数，而且宏不总是遵循与函数相同的规则。

其次，你会看到字符串 `"Hello, world!"`。我们将这个字符串作为参数传给 `println!`，字符串就会被打印到屏幕上。

第三，我们以分号（`;`）结束这一行，它表示这个表达式已经结束，下一个表达式可以开始。Rust 代码的大多数行都以分号结尾。

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### 编译与运行

你刚刚运行了一个新创建的程序，现在让我们检查这个过程中的每一步。

运行 Rust 程序之前，必须使用 Rust 编译器编译它：输入 `rustc` 命令，并传入源文件名，如下所示：

```console
$ rustc main.rs
```

如果你有 C 或 C++ 背景，会注意到这与 `gcc` 或 `clang` 类似。成功编译后，Rust 会输出一个二进制可执行文件。

在 Linux、macOS 和 Windows 上的 PowerShell 中，可以在终端里输入 `ls` 命令查看可执行文件：

```console
$ ls
main  main.rs
```

在 Linux 和 macOS 上，你会看到两个文件。使用 Windows PowerShell 时，你会看到与使用 CMD 时相同的三个文件。在 Windows CMD 中，应输入以下命令：

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

这会显示扩展名为 _.rs_ 的源代码文件、可执行文件（Windows 上是 _main.exe_，其他平台上都是 _main_），以及 Windows 下包含调试信息的 _.pdb_ 文件。接下来，像这样运行 _main_ 或 _main.exe_ 文件：

```console
$ ./main # or .\main on Windows
```

如果你的 _main.rs_ 是“Hello, world!”程序，这一行会在终端中打印出 `Hello,
world!`。

如果你更熟悉 Ruby、Python 或 JavaScript 等动态语言，可能不习惯把编译和运行程序作为两个独立步骤。Rust 是一种_提前编译_语言，这意味着你可以编译一个程序，把可执行文件交给别人；即使对方没有安装 Rust，也能运行它。如果你把 _.rb_、_.py_ 或 _.js_ 文件交给别人，对方就需要安装相应的 Ruby、Python 或 JavaScript 实现。不过在这些语言中，你只需要一条命令就能编译并运行程序。语言设计中的一切都是权衡。

使用 `rustc` 编译简单程序没有问题，但随着项目不断增长，你会希望管理所有选项，并让代码更容易共享。接下来，我们将介绍 Cargo 工具，它能帮助你编写真实世界中的 Rust 程序。

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
