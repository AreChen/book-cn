## 附录 D：有用的开发工具

在这个附录中，我们讨论 Rust 项目提供的一些有用的开发工具。我们将探讨自动格式化、快速修复告警的方法、代码静态分析工具，以及与 IDE 的集成。

### 通过 `rustfmt` 自动格式化

`rustfmt` 工具会依据社区编码风格，重新格式化咱们的代码。许多协作项目都使用 `rustfmt`，以防止在编写 Rust 时因风格选择而产生争议：每个人都使用这个工具来格式化自己的代码。

Rust 的安装默认包含 `rustfmt`，因此咱们的系统上应该已经安装了 `rustfmt` 和 `cargo-fmt` 这两个程序。这两个命令与 `rustc` 和 `cargo` 类似：`rustfmt` 允许更细粒度的控制，而 `cargo-fmt` 则能理解使用 Cargo 项目的约定。要格式化任何 Cargo 项目，请输入以下命令：

```console
$ cargo fmt
```

运行这个命令将重新格式化当前代码箱中的所有 Rust 代码。这只应改变代码的格式，不会改变代码的语义。有关 `rustfmt` 的更多信息，请参阅 [its documentation][rustfmt].

### 通过 `rustfix` 修复代码

`rustfix` 工具包含在 Rust 安装中，能够修复那些有明确修正问题的方法的一些编译器告警，大致是咱们希望的。咱们可能之前就已见到过编译器告警。例如，设想下面这段代码：

<span class="filename">文件名： src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

在这里，我们定义变量 `x` 为可变的，但我们实际上从未真正改变他。Rust 会就此发出告警：

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

这个告警建议我们移除 `mut` 关键字。我们可以使用 `rustfix` 工具运行 `cargo
fix` 命令，自动应用这一建议：

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

当我们再次查看 `cargo fix` 时，将发现 cargo fix 已修改了代码：

<span class="filename">文件名： src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

变量 `x` 现在是不可变的，并且告警也不再出现。

咱们还可以使用 `cargo fix` 命令在不同的 Rust 版本之间转换代码。版本在 [Appendix E][editions] 中得以介绍。 <!--
ignore -->

### Clippy 下的更多代码静态分析

Clippy 工具 是一个用于分析代码的静态分析工具的集合，以便咱们可以发现常见错误，仅而改进 Rust 代码。

要对任何 Cargo 项目运行 Clippy 的静态分析工具，请输入以下命令：

```console
$ cargo clippy
```

例如，假设咱们编写了个程序，使用某个数学常数，比如 π 的近似值，就像下面这个程序所做的那样：

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

对这个项目上运行 `cargo clippy` 会得到下面这个报错：

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

这个报错让咱们知道，Rust 已经定义了个更精确的 `PI` 常量，并且若咱们使用这个常量时，程序将更为正确。因此，咱们就要修改代码为使用 `PI` 常量。

以下代码不会导致来自 Clippy 的任何报错或告警：

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

有关 Clippy 的更多信息，请参阅 [its documentation][clippy]。

### 使用 `rust-analyzer` 的 IDE 集成

为了帮助 IDE 集成，Rust 社区建议使用 [`rust-analyzer`][rust-analyzer]。这个工具是一组以编译器为中心的实用程序，支持 [Language Server Protocol][lsp] ，该协议是 IDE 和编程语言之间相互通信的规范。不同客户端均可以使用 `rust-analyzer`，比如 [the Rust analyzer plug-in for Visual Studio Code][vscode]。 <!-- ignore --> <!--
ignore -->

请访问 `rust-analyzer` 项目 [home page][rust-analyzer] 查看安全说明，随后在咱们的特定 IDE 中安装语言服务器支持。咱们的 IDE 将获得自动补全、跳转到定义以及内联报错等能力。 <!-- ignore -->

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
