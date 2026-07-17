## 你好，Cargo！

Cargo 是 Rust 的构建系统和包管理器。大多数 Rust 开发者都使用这个工具管理 Rust 项目，因为 Cargo 会替你处理许多任务，例如构建代码、下载代码所依赖的库，以及构建这些库。（我们把代码所需的库称为_依赖项_。）

像我们目前编写的程序这样最简单的 Rust 程序，没有任何依赖。如果我们使用 Cargo 构建“Hello, world!”项目，它只会用到 Cargo 中负责构建代码的部分。随着 Rust 程序变得更加复杂，你会添加依赖；如果从一开始就使用 Cargo 创建项目，添加依赖会容易得多。

由于绝大多数 Rust 项目都使用 Cargo，本书其余部分也假定你使用 Cargo。如果你使用[“安装”][installation]<!-- ignore -->部分介绍的官方安装程序，Cargo 会随 Rust 一起安装。如果你通过其他方式安装了 Rust，请在终端中输入以下命令检查是否安装了 Cargo：

```console
$ cargo --version
```

如果看到版本号，就说明已经安装好了！如果看到诸如 `command
not found` 这样的错误，请查看你的安装方式对应的文档，了解如何单独安装 Cargo。

### 使用 Cargo 创建项目

让我们使用 Cargo 创建一个新项目，看看它与最初的“Hello, world!”项目有何不同。回到 _projects_ 目录（或你决定存放代码的任何位置），然后在任意操作系统上运行以下命令：

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

第一条命令会创建一个名为 _hello_cargo_ 的新目录和项目。我们将项目命名为 _hello_cargo_，Cargo 会在同名目录中创建项目文件。

进入 _hello_cargo_ 目录并列出文件。你会看到 Cargo 为我们生成了两个文件和一个目录：一个 _Cargo.toml_ 文件，以及一个内部包含 _main.rs_ 文件的 _src_ 目录。

它还会同时初始化一个新的 Git 仓库和一个 _.gitignore_ 文件。如果在已有 Git 仓库中运行 `cargo new`，就不会生成 Git 文件；你可以使用 `cargo new --vcs=git` 覆盖这一行为。

> 注意：Git 是一种常见的版本控制系统。你可以让 `cargo new` 使用其他版本控制系统，或者不使用版本控制系统；使用 `--vcs` 标志可以改变这一行为。运行 `cargo new --help` 查看可用选项。

在你选择的文本编辑器中打开 _Cargo.toml_。它应该与清单 1-2 中的代码相似。

<Listing number="1-2" file-name="Cargo.toml" caption="由 `cargo new` 生成的 *Cargo.toml* 内容">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

这个文件采用 [_TOML_][toml]<!-- ignore -->（_汤姆的显而易见的最小语言_）格式，这是 Cargo 的配置格式。

第一行 `[package]` 是一个小节标题，表示接下来的语句正在配置一个包。随着我们向这个文件添加更多信息，还会添加其他小节。

接下来的三行设置了 Cargo 编译程序所需的配置信息：名称、版本，以及要使用的 Rust 版本。我们会在[附录 E][appendix-e]<!-- ignore -->中讨论 `edition` 键。

最后一行 `[dependencies]` 是一个小节的开头，你可以在其中列出项目的所有依赖项。在 Rust 中，代码包称为_代码箱_。这个项目不需要其他代码箱，但第 2 章的第一个项目会用到，所以到那时我们会使用这个依赖项小节。

现在打开 _src/main.rs_ 看看：

<span class="filename">文件名： src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo 为你生成了一个“Hello, world!”程序，就像我们在清单 1-1 中编写的程序一样！到目前为止，我们的项目与 Cargo 生成的项目之间的区别在于：Cargo 将代码放在了 _src_ 目录中，而我们在顶层目录中有一个 _Cargo.toml_ 配置文件。

Cargo 要求源文件位于 _src_ 目录中。顶层项目目录只用于存放 README 文件、许可证信息、配置文件，以及其他任何与代码无关的内容。使用 Cargo 有助于你组织项目：每样东西都有自己的位置，而且各就各位。

如果你像我们在“Hello, world!”项目中那样，开始了一个不使用 Cargo 的项目，也可以将它转换为使用 Cargo 的项目。将项目代码移入 _src_ 目录，并创建一个合适的 _Cargo.toml_ 文件。获取这个 _Cargo.toml_ 文件的一种简单方法是运行 `cargo init`，它会自动为你创建该文件。

### 构建和运行 Cargo 项目

现在让我们看看使用 Cargo 构建和运行“Hello, world!”程序时有哪些不同！在 _hello_cargo_ 目录中输入以下命令来构建项目：

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

这条命令会在 _target/debug/hello_cargo_（Windows 上则是 _target\debug\hello_cargo.exe_）中创建可执行文件，而不是放在当前目录中。由于默认构建是调试构建，Cargo 会将二进制文件放在名为 _debug_ 的目录中。你可以使用以下命令运行可执行文件：

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

如果一切顺利，`Hello, world!` 应该会打印到终端。第一次运行 `cargo
build` 还会让 Cargo 在顶层目录创建一个新文件：_Cargo.lock_。这个文件会记录项目依赖项的确切版本。这个项目没有依赖项，所以该文件内容很少。你永远不需要手动修改这个文件；Cargo 会为你管理其内容。

我们刚刚使用 `cargo build` 构建了一个项目，并使用 `./target/debug/hello_cargo` 运行了它，但也可以使用 `cargo run` 在一条命令中编译代码，然后运行生成的可执行文件：

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

使用 `cargo run` 比记住先运行 `cargo
build`、再使用二进制文件的完整路径更方便，所以大多数开发者都会使用 `cargo
run`。

注意，这次我们没有看到 Cargo 正在编译 `hello_cargo` 的输出。Cargo 发现文件没有变化，所以没有重新构建，而是直接运行了二进制文件。如果你修改了源代码，Cargo 会在运行程序前重新构建项目，你会看到如下输出：

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo 还提供了一个名为 `cargo check` 的命令。这个命令会快速检查代码，确保代码可以编译，但不会生成可执行文件：

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

为什么不想要可执行文件呢？通常，`cargo check` 比 `cargo build` 快得多，因为它跳过了生成可执行文件的步骤。如果你在编写代码时持续检查工作进展，使用 `cargo check` 会加快确认项目是否仍能编译的过程！因此，许多 Rust 开发者会在编写程序时定期运行 `cargo check`，确保程序能够编译；准备使用可执行文件时，再运行 `cargo build`。

让我们回顾一下目前对 Cargo 的了解：

- 我们可以使用 `cargo new` 创建项目。
- 我们可以使用 `cargo build` 构建项目。
- 我们可以使用 `cargo run` 一步构建并运行项目。
- 我们可以使用 `cargo check` 在不生成二进制文件的情况下构建项目，以检查错误。
- Cargo 不会将构建结果保存在与代码相同的目录中，而是将其存放在 _target/debug_ 目录中。

使用 Cargo 的另一个优点是，无论你在哪个操作系统上工作，命令都相同。因此，从现在开始，我们不再分别提供 Linux 和 macOS 与 Windows 的具体说明。

### 为发布而构建

项目最终准备发布时，可以使用 `cargo build
--release` 通过优化来编译它。这条命令会在 _target/release_ 而不是 _target/debug_ 中创建可执行文件。优化会让 Rust 代码运行得更快，但启用优化会延长程序编译所需的时间。因此存在两种不同的配置：一种用于开发，在需要快速且频繁地重新构建时使用；另一种用于构建最终程序，将它交给用户后不会反复重建，并且会尽可能快地运行。如果你要对代码的运行时间进行基准测试，请务必运行 `cargo build --release`，并使用 _target/release_ 中的可执行文件进行基准测试。

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### 利用 Cargo 的约定

对于简单项目，Cargo 相比只使用 `rustc` 并没有提供太多价值，但随着程序变得更加复杂，它会证明自己的价值。一旦程序扩展到多个文件或需要依赖项，让 Cargo 协调构建就容易得多。

尽管 `hello_cargo` 项目很简单，但它已经使用了你在 Rust 开发生涯中会用到的许多真实工具。事实上，要处理任何现有项目，你可以使用下面的命令，通过 Git 检出代码，进入项目目录并构建它：

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

更多 Cargo 信息，请查看[它的文档][cargo]。

## 小结

你的 Rust 之旅已经有了一个很好的开始！在本章中，你学会了如何：

- 使用 `rustup` 安装最新的 Rust 稳定版。
- 更新到更新的 Rust 版本。
- 打开本地安装的文档。
- 直接使用 `rustc` 编写并运行“Hello, world!”程序。
- 遵循 Cargo 的约定创建并运行新项目。

现在正是构建一个更完整的程序、熟悉阅读和编写 Rust 代码的好时机。因此，在第 2 章中，我们将构建一个猜数游戏程序。如果你更想先学习常见编程概念在 Rust 中如何运作，请参阅第 3 章，然后再回到第 2 章。

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
