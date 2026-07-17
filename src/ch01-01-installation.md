## 安装

第一步是安装 Rust。我们会通过 `rustup` 下载 Rust；它是一个用于管理 Rust 版本及相关工具的命令行工具。下载过程需要互联网连接。

> 注意：如果你出于某种原因不想使用 `rustup`，请参阅[其他 Rust 安装方式页面][otherinstall]，了解更多选项。

以下步骤会安装最新的 Rust 稳定版编译器。Rust 的稳定性保证本书中所有能够编译的示例在更新的 Rust 版本中仍然可以编译。不同版本的输出可能略有差异，因为 Rust 经常改进错误信息和警告。换句话说，使用这些步骤安装的任何更新后的稳定版 Rust，都应该能够按本书内容预期的方式工作。

> ### 命令行记法
>
> 在本章以及全书中，我们会展示一些在终端中使用的命令。需要输入终端的行都以 `$` 开头。你不需要输入 `$` 字符；它是表示命令开始的命令行提示符。不以 `$` 开头的行通常表示上一条命令的输出。此外，PowerShell 专用示例会使用 `>` 而不是 `$`。

### 在 Linux 与 macOS 上安装 `rustup`

如果咱们使用的是 Linux 或 macOS，请打开终端并输入以下命令：

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

这条命令会下载一个脚本并开始安装 `rustup` 工具，而 rustup 会安装最新的 Rust 稳定版。系统可能会提示你输入密码。如果安装成功，就会显示下面这一行：

```text
Rust is installed now. Great!
```

我们还需要一个链接器，把 Rust 的编译输出连接成一个文件。你很可能已经有了链接器。如果出现链接器错误，就需要安装一个通常包含链接器的 C 编译器。C 编译器也很有用，因为一些常见的 Rust 包依赖 C 代码，因此需要 C 编译器。

在 macOS 上，咱们可以通过运行：

```console
$ xcode-select --install
```

获得一个 C 编译器。

Linux 用户一般应根据其发行版的文档，安装 GCC 或 Clang。例如，如果咱们使用 Ubuntu，则可以安装 `build-essential` 软件包。

### 在 Windows 上安装 `rustup`

在 Windows 上，请前往 [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> 并按照说明安装 Rust。安装过程中的某个时刻，系统会提示你安装 Visual Studio。它提供编译程序所需的链接器和本机库。如果需要这一步的更多帮助，请参阅
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->。

本书其余部分使用的命令既可在 _cmd.exe_ 中运行，也可在 PowerShell 中运行。如果两者存在具体差异，我们会说明应使用哪一种。

### 问题排除

要检查 Rust 安装是否正确，请打开 shell 并输入这一行：

```console
$ rustc --version
```

你应该会看到最新发布的稳定版本的版本号、提交哈希和提交日期，格式如下：

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

如果看到这些信息，就说明 Rust 已经安装成功！如果没有看到，请按下面的方式检查 Rust 是否位于 `%PATH%` 系统变量中。

在 Windows CMD 中使用：

```console
> echo %PATH%
```

在 PowerShell 中，请使用：

```powershell
> echo $env:Path
```

在 Linux 及 macOS 中，请使用：

```console
$ echo $PATH
```

如果上述内容都正确而 Rust 仍然无法工作，你可以从许多地方获得帮助。请在[社区页面][community]了解如何联系其他 Rustaceans（这是我们给自己起的一个有趣昵称）。

### 更新与卸载

通过 `rustup` 安装 Rust 后，更新到新近发布的版本，就很容易了。请在 shell 中运行以下更新脚本：

```console
$ rustup update
```

若要卸载 Rust 和 `rustup`，请在 shell 中运行以下卸载脚本：

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### 本地文档

Rust 的安装还包含一份本地文档副本，方便你离线阅读。运行 `rustup doc`，即可在浏览器中打开本地文档。

当标准库提供了某个类型或函数，而你不确定它的作用或用法时，请查阅应用程序编程接口（API）文档来了解详情！

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### 使用文本编辑器与 IDE

本书不假定你使用什么工具编写 Rust 代码。几乎任何文本编辑器都能完成这项工作！不过，许多文本编辑器和集成开发环境（IDE）都内置了 Rust 支持。你可以在 Rust 网站的[工具页面][tools]找到一份相当新的编辑器和 IDE 列表。

### 离线使用本书

在几个示例中，我们会使用标准库之外的 Rust 包。要完成这些示例，你需要保持互联网连接，或者提前下载这些依赖。若要提前下载依赖，可以运行下面的命令。（我们稍后会详细解释 `cargo` 是什么，以及每条命令的作用。）

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

这会缓存这些包的下载内容，这样之后就不需要再次下载。运行此命令后，不必保留 `get-dependencies` 文件夹。运行过该命令后，你可以在本书其余部分的所有 `--offline` 命令中使用 `cargo` 标志，让 Cargo 使用缓存的版本，而不是尝试访问网络。

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
