# 编写猜数游戏

我们来一起完成一个实践项目，开始学习 Rust！这一章通过向咱们展示如何在实际程序中如何运用他们，向咱们介绍一些常见 Rust 概念。咱们将了解

- `let`
- `match`
- 方法
- 关联函数
- 外部代码箱

等等！在接下来的章节中，我们将更详细地探讨这些概念。在本章中，咱们将只练习这些基本知识。

我们将实现一个经典的初学者编程问题：猜数游戏。其原理如下：

- 程序将随机生成一个介于 1 和 100 之间的整数；
- 然后，程序会提示玩家，输入一个猜测值；
- 猜测值输入后，程序会显示猜测值是过低还是过高；
- 如猜测正确，游戏将打印一条祝贺信息并退出。

## 建立一个新项目

要创建新项目，请进入第 1 章中创建的 _projects_ 目录，并使用 Cargo 创建一个新项目，如下所示：

```console
$ cargo new guessing_game
$ cd guessing_game
```

第一条命令 `cargo new` 将项目名称（`guessing_game`）作为第一个参数。第二条命令进入新项目的目录。

看看生成的 _Cargo.toml_ 文件：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">文件名： Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

正如你在第 1 章看到的，`cargo new` 会为你生成一个“Hello, world!”程序。看看 _src/main.rs_ 文件：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

现在我们来使用 `cargo run` 命令，在同一步骤编译并运行这个 "Hello, world!" 程序：

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

当你需要快速迭代项目时，`run` 命令非常有用；就像我们在这个游戏中要做的那样，可以在进入下一次迭代前快速测试当前迭代。

重新打开 _src/main.rs_ 文件。我们会在这个文件中编写全部代码。

## 处理猜数

猜数游戏程序的第一部分会请求用户输入、处理输入，并检查输入是否符合预期格式。首先，让玩家输入一个猜测值。将清单 2-1 中的代码输入 _src/main.rs_。

<Listing number="2-1" file-name="src/main.rs" caption="获取用户猜测并将其打印出来的代码">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

这段代码包含很多信息，所以让我们逐行看看。为了获取用户输入并将结果打印为输出，我们需要把 `io` 输入/输出库引入作用域。`io` 库来自称为 `std` 的标准库：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

默认情况下，Rust 会把标准库中定义的一组项目引入每个程序的作用域。这组项目称为_预导入模块（prelude）_，你可以在[标准库文档中的相关内容][prelude]中查看其中的全部项目。

如果想使用的类型不在预导入模块中，就必须通过 `use` 语句显式地将该类型引入作用域。使用 `std::io` 库可以获得许多有用功能，包括接收用户输入的能力。

正如你在第 1 章看到的，`main` 函数是程序的入口点：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

`fn` 语法声明一个新函数；括号 `()` 表示没有参数；左花括号 `{` 开始函数体。

正如你在第 1 章中学到的，`println!` 是一个将字符串打印到屏幕上的宏：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

这段代码打印出说明游戏内容并请求用户输入的提示。

### 以变量存储值

接下来，我们将创建一个 *变量，variable* 存储用户输入，就像这样：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

现在，程序开始变得有趣起来！在这短短一行中，发生了很多事情。我们使用 `let` 语句创建变量。下面是另一个例子：

```rust,ignore
let apples = 5;
```

这一行创建了一个名为 `apples` 的新变量，并将它绑定到值 `5`。在 Rust 中，变量默认不可变，也就是说一旦给变量赋值，该值就不会改变。我们会在第 3 章的[“变量与可变性”][variables-and-mutability]<!-- ignore -->部分详细讨论这个概念。要让变量可变，需要在变量名之前添加 `mut`：

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> 注意：`//` 语法开始一条持续到行尾的注释。Rust 会忽略注释中的所有内容。我们会在[第 3 章][comments]<!-- ignore -->中更详细地讨论注释。

回到猜数游戏程序，现在你知道 `let mut guess` 会引入一个名为 `guess` 的可变变量。等号（`=`）告诉 Rust 我们现在要把某个值绑定到该变量。等号右侧是 `guess` 所绑定的值，也就是调用 `String::new` 的结果；这个函数会返回一个新的 `String` 实例。[`String`][string]<!-- ignore --> 是标准库提供的一种字符串类型，表示可增长的 UTF-8 编码文本。

`::` 这一行中的 `::new` 语法表示 `new` 是 `String` 类型的关联函数。_关联函数_ 是在某个类型上实现的函数，本例中是 `String`。这个 `new` 函数会创建一个新的空字符串。许多类型都有名为 `new` 的函数，因为这是创建某种新值时常用的函数名。

总的来说，`let mut guess = String::new();` 这一行创建了一个可变变量，它当前绑定到一个新的空 `String` 实例。呼！

### 接收用户输入

回顾一下，在程序的第一行，我们使用 `use std::io;` 包含了标准库中的输入/输出功能。现在，我们将调用 `stdin` 模组中的 `io` 函数，其将允许咱们处理用户输入：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

如果没有在程序开头通过 `io` 导入 `use std::io;` 模块，仍然可以把函数调用写成 `std::io::stdin` 来使用它。`stdin` 函数返回 [`std::io::Stdin`][iostdin]<!-- ignore --> 的实例；这种类型表示终端标准输入的句柄。

接下来，`.read_line(&mut guess)` 会在标准输入句柄上调用 [`read_line`][read_line]<!--
ignore --> 方法来获取用户输入。我们还将 `&mut guess` 作为参数传给 `read_line`，告诉它把用户输入存储到哪个字符串中。`read_line` 的完整工作是获取用户在标准输入中输入的内容，并将其追加到字符串中（而不是覆盖原有内容），所以我们把该字符串作为参数传入。字符串参数必须是可变的，这样方法才能修改字符串内容。

`&` 表示这个参数是一个_引用_，它让代码的多个部分可以访问同一份数据，而不需要多次将数据复制到内存中。引用是一个复杂特性，而 Rust 的主要优势之一就是引用既安全又易于使用。完成这个程序不需要了解太多细节。现在只需知道，和变量一样，引用默认不可变。因此，要让它可变，需要写成 `&mut guess`，而不是 `&guess`。（第 4 章会更深入地解释引用。）

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### 以 `Result` 处理潜在失效

我们仍在研究这行代码。我们现在讨论的是第三行文字，但要注意，他仍是单个逻辑代码行的一部分。下一部分是这个方法：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```


我们本可以将这段代码写成：

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

不过，过长的代码行很难阅读，因此最好将它拆开。在使用
`.method_name()` 语法调用方法时，适当加入换行和其他空白，通常有助于
拆分过长的代码行。现在来看看这行代码做了什么。

如前所述，`read_line` 会把用户输入的内容放入我们传给它的字符串中，
但它还会返回一个 `Result` 值。[`Result`][result]<!--
ignore --> 是一种[_枚举_][enums]<!-- ignore -->（通常简称为 _enum_），
表示一个可以处于多个可能状态之一的类型。我们把每种可能的状态称为
_变体_。

[第 6 章][enums]<!-- ignore --> 将更详细地介绍枚举。这些 `Result` 类型的
用途是编码错误处理信息。

`Result` 的变体是 `Ok` 和 `Err`。`Ok` 变体表示操作成功，并包含成功生成的
值。`Err` 变体表示操作失败，并包含操作如何或为何失败的信息。

和其他类型的值一样，`Result` 类型的值也有定义在其上的方法。`Result` 的
实例有一个可以调用的 [`expect` 方法][expect]<!-- ignore -->。如果这个
`Result` 实例是 `Err` 值，`expect` 会让程序崩溃，并显示传给 `expect` 的
参数作为消息。如果 `read_line` 方法返回 `Err`，通常意味着底层操作系统
发生了错误。如果这个 `Result` 实例是 `Ok` 值，`expect` 会取出 `Ok` 中
保存的返回值，只把这个值返回给你，以便你使用。在这里，这个值是用户
输入所占的字节数。

如果不调用 `expect`，程序仍然可以编译，但你会收到警告：

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust 会警告你没有使用 `Result` 返回的 `read_line` 值，这说明程序没有处理
可能发生的错误。

消除警告的正确方式是实际编写错误处理代码；但在这个例子中，我们只想在
发生问题时让程序崩溃，因此可以使用 `expect`。你将在[第 9
章][recover]<!-- ignore --> 学习如何从错误中恢复。

### 以 `println!` 的占位符打印值

这段代码中，除了结尾的大括号，到目前为止就只有一行需要讨论了：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

这行会打印现在包含着用户输入的那个字符串。其中的 `{}` 花括号组是个占位符：把 `{}` 想象成固定某个值位置的两个小螃蟹钳子。在打印某个变量的值时，变量名可以放在这对花括号内。在打印对表达式求值的结果时，就要在格式字符串中放置空的大括号，然后在格式字符串后，跟上以逗号分隔的表达式列表，以相同顺序在各个空的大括号占位符中打印。在对 `println!` 的一次调用中，打印某个变量及某个表达式的结果，将如下所示：

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

此代码将打印出 `x = 5 and y + 2 = 12`。

### 测试第一部分

来测试猜数游戏的第一部分。使用 `cargo run` 运行它：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

至此，这个游戏的第一部分就已完成：我们从键盘获取输入，并随后将其打印。

## 生成秘密数字

接下来，我们需要生成一个让用户猜的秘密数字。秘密数字应当每次都不同，
这样游戏才能重复玩而不失趣味。我们会使用 1 到 100 之间的随机数，以免
游戏太难。Rust 的标准库目前还不包含生成随机数的功能。不过，Rust 团队
提供了一个具有此功能的 [`rand` 代码包][randcrate]。

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### 以代码箱增加功能

记住，代码包是 Rust 源代码文件的集合。我们一直在构建的项目是一个二进制
代码包，也就是一个可执行文件。`rand` 代码包则是库代码包，其中包含供
其他程序使用的代码，不能独立执行。

Cargo 对外部代码包的协调正是它的强项。在编写使用 `rand` 的代码之前，
我们需要修改 _Cargo.toml_ 文件，将 `rand` 代码包加入依赖项。现在打开
该文件，在 Cargo 为你创建的 `[dependencies]` 节标题下方、文件末尾添加
下面这一行。请务必像这里一样准确指定 `rand` 及其版本号，否则本教程中
的代码示例可能无法运行：

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">文件名： Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

在 _Cargo.toml_ 文件中，标题之后的所有内容都属于该节，直到下一个节开始。
在 `[dependencies]` 中，你要告诉 Cargo 项目依赖哪些外部代码包，以及需要
这些代码包的哪些版本。在这里，我们使用语义版本说明符 `rand` 指定
`0.10.1` 代码包。Cargo 理解[语义化版本][semver]<!-- ignore -->（有时称为
_SemVer_），这是一种编写版本号的标准。说明符 `0.10.1` 实际上是
`^0.10.1` 的简写，表示版本至少为 0.10.1、但低于 0.11.0 的任何版本。

Cargo 认为这些版本的公开 API 与 0.10.1 兼容；这个说明符可以确保你获得
仍能与本章代码一起编译的最新补丁版本。不能保证 0.11.0 或更高版本具有
与下面示例所使用的 API 相同的 API。

现在不修改任何代码，按照示例 2-2 所示构建项目。

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="将 `cargo build` 代码包加入依赖后运行 `rand` 的输出">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

你看到的版本号可能不同（但得益于 SemVer，它们都应与代码兼容！），输出
的行也可能不同（取决于操作系统），而且行的顺序也可能不同。

当我们加入外部依赖时，Cargo 会从_注册表_中获取该依赖所需的所有内容的
最新版本。注册表是 [Crates.io][cratesio] 数据的副本。Crates.io 是 Rust
生态中的人们发布开源 Rust 项目、供他人使用的地方。

更新注册表后，Cargo 会检查 `[dependencies]` 节，并下载其中列出但尚未下载
的代码包。在这个例子中，虽然我们只列出了 `rand` 这一项依赖，Cargo 还
获取了 `rand` 正常工作所依赖的其他代码包。下载这些代码包后，Rust 会先
编译它们，再使用这些依赖编译项目。

如果不做任何更改就立即再次运行 `cargo build`，除了 `Finished` 行之外，
你不会看到其他输出。Cargo 知道依赖已经下载并编译过，而你没有在
_Cargo.toml_ 文件中修改它们。Cargo 也知道代码没有变化，因此不会重新
编译代码。没有事情可做时，它会直接退出。

如果打开 _src/main.rs_ 文件，做一个微小的修改，保存后再次构建，你只会
看到两行输出：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

这些行表明，Cargo 只根据你对 _src/main.rs_ 文件所做的微小更改更新构建
结果。依赖没有变化，因此 Cargo 知道可以重用已经下载并编译好的依赖。

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### 确保可复现的构建

Cargo 有一种机制，可以确保每次你或其他人构建代码时都能重新构建出相同
的产物：除非你明确要求，否则 Cargo 只会使用你指定的依赖版本。例如，
假设下周 `rand` 代码包发布了 0.10.2 版本，其中包含重要的错误修复，
但也引入了会破坏代码的回归问题。为处理这种情况，Rust 会在你第一次
运行 `cargo build` 时创建 _Cargo.lock_ 文件，因此现在 _guessing_game_
目录中会有这个文件。

第一次构建项目时，Cargo 会找出符合条件的所有依赖版本，然后将它们写入
_Cargo.lock_ 文件。以后构建项目时，Cargo 会发现 _Cargo.lock_ 文件已经
存在，并使用其中指定的版本，而不再重新完成查找版本的工作。这样就能
自动实现可复现构建。换句话说，得益于 _Cargo.lock_ 文件，在你明确升级
之前，项目会一直使用 0.10.1。由于 _Cargo.lock_ 对可复现构建很重要，
它通常会和项目的其余代码一起纳入版本控制。

#### 更新代码箱获取新版本

当你确实想要更新代码包时，Cargo 提供了 `update` 命令。该命令会忽略
_Cargo.lock_ 文件，并找出符合 _Cargo.toml_ 中说明的所有最新版本。然后
Cargo 会将这些版本写入 _Cargo.lock_ 文件。否则，Cargo 默认只会查找大于
0.10.1 且小于 0.11.0 的版本。如果 `rand` 代码包发布了 0.10.2 和
0.999.0 两个新版本，运行 `cargo update` 时会看到如下输出：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

Cargo 会忽略 0.999.0 版本。此时你还会看到 _Cargo.lock_ 文件发生变化，
其中记录了当前使用的 `rand` 代码包版本为 0.10.2。若要使用 `rand` 的
0.999.0 版本，或 0.999._x_ 系列中的任何版本，你必须把 _Cargo.toml_ 文件
改成下面这样（不要真的做出此修改，因为后面的示例假定你使用 `rand` 0.10）：

```toml
[dependencies]
rand = "0.999.0"
```

下一次运行 `cargo build` 时，Cargo 会更新可用代码包的注册表，并根据你
指定的新版本重新评估 `rand` 的要求。

关于 [Cargo][doccargo]<!-- ignore --> 及其[生态系统][doccratesio]<!-- ignore --> 还有很多内容，我们会在第 14 章讨论；现在你只需要了解这些。
Cargo 让重用库变得非常容易，因此 Rustacean 可以编写由多个包组装而成的
更小项目。

### 生成随机数

现在开始使用 `rand` 生成要猜的数字。下一步是按照示例 2-3 修改
_src/main.rs_。

<Listing number="2-3" file-name="src/main.rs" caption="添加生成随机数的代码">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

首先，添加一行 `use rand::prelude::*;`。`prelude` 模块包含 `rand` 代码包中
最常用的部分，而 `use` 会让这些项在程序的作用域中可用。

接下来，在中间添加两行代码。第一行调用 `rand::rng` 函数，得到我们要使用
的特定随机数生成器：它属于当前执行线程，并由操作系统提供种子。然后，
在随机数生成器上调用 `random_range` 方法。该方法由 `RngExt` 特征定义，
属于我们通过 `rand::prelude` 语句引入作用域的 `use
rand::prelude::*;`
模块。`random_range` 方法接受一个范围表达式作为参数，并生成该范围内的
随机数。这里使用的范围表达式形式为 `start..=end`，包含下界和上界，
因此需要指定 `1..=100` 来请求一个 1 到 100 之间的数字。

> 注意：你不可能凭空知道该从代码包中引入什么，以及应该调用哪些方法和
> 函数，因此每个代码包都会提供使用说明文档。Cargo 的另一个实用功能是，
> 运行 `cargo doc --open` 命令会在本地构建所有依赖提供的文档，并在浏览器
> 中打开它。如果你想了解 `rand` 代码包的其他功能，可以运行
> `cargo doc --open`，然后点击左侧边栏中的 `rand`。

第二行新增代码会打印秘密数字。在开发程序、进行测试时这很有用，但我们会
在最终版本中删除它。如果程序一启动就打印答案，那就不算什么游戏了！

试着运行程序几次：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

你应该会得到不同的随机数，而且它们都应当是 1 到 100 之间的数字。如果
收到警告，可以放心忽略。如果收到错误，请检查 *Cargo.toml* 中是否有
`rand = "0.10.1"`，因为未来版本的 `rand` 可能具有不同的 API；不过，
`0.10` 系列中的任何版本都应能与本章代码一起工作。

## 比较猜数与秘密数

现在我们已经有了用户输入和随机数，可以比较二者了。示例 2-4 展示了这
一步。注意，这段代码暂时还无法编译，原因稍后解释。

<Listing number="2-4" file-name="src/main.rs" caption="处理比较两个数字时可能返回的值">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

首先，再添加一条 `use` 语句，从标准库中将名为 `std::cmp::Ordering` 的
类型引入作用域。`Ordering` 类型也是一个枚举，具有 `Less`、`Greater` 和
`Equal` 三个变体。比较两个值时，可能出现的结果正是这三种。

然后，在底部添加五行使用 `Ordering` 类型的新代码。`cmp` 方法比较两个值，
可以在任何能够进行比较的值上调用。它接受一个要与之比较的值的引用：
这里是将 `guess` 与 `secret_number` 比较。接着，它会返回我们通过 `Ordering`
语句引入作用域的 `use` 枚举的某个变体。我们使用 [`match`][match]<!-- ignore --> 表达式，根据对 `Ordering` 和 `cmp` 中的值调用 `guess`
后返回的 `secret_number` 变体来决定下一步做什么。

`match` 表达式由多个_分支_组成。一个分支包含一个要匹配的_模式_，以及
当传给 `match` 的值符合该分支模式时应运行的代码。Rust 会取得传给
`match` 的值，然后依次查看各个分支的模式。模式和 `match` 构造是 Rust
中强大的功能：它们让你能够表达代码可能遇到的各种情况，并确保你处理
所有情况。第 6 章和第 19 章将分别详细介绍这些功能。

下面通过一个例子看看这里使用的 `match` 表达式。假设用户猜了 50，而这次
随机生成的秘密数字是 38。

当代码比较 50 和 38 时，因为 50 大于 38，`cmp` 方法会返回
`Ordering::Greater`。`match` 表达式得到 `Ordering::Greater` 值后，开始
检查每个分支的模式。它先查看第一个分支的模式 `Ordering::Less`，发现
`Ordering::Greater` 与 `Ordering::Less` 不匹配，于是忽略该分支中的代码，
继续查看下一个分支。下一个分支的模式是 `Ordering::Greater`，这次确实
匹配 `Ordering::Greater`！该分支关联的代码会执行，并向屏幕打印 `Too big!`。`match` 表达式
在第一次成功匹配后结束，因此在这种情况下不会查看最后一个分支。

不过，示例 2-4 中的代码目前还无法编译。试着编译它：

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

错误的核心是指出存在_类型不匹配_。Rust 拥有强大的静态类型系统，同时也
支持类型推断。我们写下 `let mut guess = String::new()` 时，Rust 能推断
出 `guess` 应该是 `String`，因此不要求我们写出类型。另一方面，
`secret_number` 是数字类型。Rust 的一些数字类型可以表示 1 到 100 之间
的值：`i32` 是 32 位数字，`u32` 是无符号 32 位数字，`i64` 是 64 位数字，
还有其他类型。除非另有指定，Rust 默认使用 `i32`；如果你没有在其他地方
添加会让 Rust 推断出不同数字类型的类型信息，`secret_number` 就是
i32 类型。产生错误的原因是，Rust 不能比较字符串和数字类型。

最终，我们希望将程序读入的 `String` 输入转换为数字类型，这样就能将它与
秘密数字进行数值比较。通过把下面这行代码添加到 `main` 函数体中即可：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

代码行如下：

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

我们创建了一个名为 `guess` 的变量。不过，程序不是已经有一个名为 `guess`
的变量了吗？确实有，但 Rust 允许我们用新值遮蔽之前的 `guess` 值，这很
方便。_遮蔽_让我们可以重用 `guess` 这个变量名，而不必创建两个不同的
变量名，例如 `guess_str` 和 `guess`。我们会在[第 3 章][shadowing]<!-- ignore --> 更详细地介绍这一点；现在只要知道，当你想把一个值从一种类型
转换为另一种类型时，经常会使用这个功能。

我们将这个新变量绑定到表达式 `guess.trim().parse()`。表达式中的 `guess`
指的是原来的 `guess` 变量，它包含作为字符串的输入。`trim` 实例上的
`String` 方法会去除开头和结尾的空白；在把字符串转换为只能包含数值数据的
`u32` 之前，必须先做这件事。用户必须按下 <kbd>enter</kbd> 来满足
`read_line` 并输入猜测，这会在字符串中加入换行字符。例如，用户输入
<kbd>5</kbd> 并按下 <kbd>enter</kbd> 后，`guess` 看起来是 `5\n`。`\n`
表示“换行”。（在 Windows 上，按下 <kbd>enter</kbd> 会产生回车和换行，
即 `\r\n`。）`trim` 方法会去除 `\n` 或 `\r\n`，最后只剩下 `5`。

[字符串中的 `parse` 方法][parse]<!-- ignore --> 会将字符串转换为另一种类型。
在这里，我们用它把字符串转换为数字。通过使用 `let guess: u32`，我们需要
告诉 Rust 想要的确切数字类型。`:` 标记位于 `guess` 后面，告诉 Rust 我们
要标注变量的类型。Rust 有几种内置数字类型；这里的 `u32` 是无符号的
32 位整数，是表示小型正数的不错默认选择。你将在[第 3 章][integers]<!-- ignore --> 了解其他数字类型。

此外，这个示例程序中的 `u32` 标注以及与 `secret_number` 的比较，意味着
Rust 会推断 `secret_number` 也应当是 `u32`。这样，比较的就是两个相同
类型的值了！

`parse` 方法只能处理逻辑上能够转换为数字的字符，因此很容易出错。例如，
如果字符串包含 `A👍%`，就没有办法把它转换为数字。
由于转换可能失败，`parse` 方法会返回 `Result` 类型，就像前面介绍的
`read_line` 方法（参见[“以 `Result` 处理潜在失效”](#handling-potential-failure-with-result)<!-- ignore -->）一样。
我们会以相同方式处理这个 `Result`，再次使用 `expect` 方法。如果 `parse`
因为无法从字符串创建数字而返回 `Err` `Result` 变体，
调用 `expect` 会让游戏崩溃，并打印我们传给它的消息。如果 `parse` 能成功
将字符串转换为数字，它会返回 `Ok` 变体的 `Result` 值，而 `expect` 会从
`Ok` 值中返回我们需要的数字。

现在运行程序：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

很好！虽然猜测前面加了空格，程序仍然正确判断出用户猜的是 76。再运行
程序几次，使用不同类型的输入验证不同的行为：猜中数字、猜一个过大的
数字，以及猜一个过小的数字。

现在游戏的大部分功能已经正常，但用户只能猜一次。让我们添加循环来改变
这一点！

## 以循环实现多次猜数

`loop` 关键字会创建一个无限循环。我们添加循环，让用户有更多机会猜数字：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

如你所见，我们把从猜测输入提示开始的所有内容都移到了循环中。务必让
循环内部的每一行再缩进四个空格，然后再次运行程序。现在程序会不停地
要求用户继续猜，这实际上引入了一个新问题：用户似乎无法退出！

用户当然可以使用键盘快捷键 <kbd>ctrl</kbd>-<kbd>C</kbd> 中断程序。不过，
正如[“比较猜数与秘密数”](#comparing-the-guess-to-the-secret-number)<!-- ignore --> 中讨论 `parse` 时提到的，还有另一种逃离这个贪得无厌的循环的
方法：如果用户输入非数字答案，程序就会崩溃。我们可以利用这一点让用户
退出，如下所示：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

输入 `quit` 将退出游戏，但正如咱们将发现的，输入任何其他非数字输入也会这样。至少可以说，这是次优的；我们希望正确数字猜到后游戏也会停止。

### 猜对后的退出

通过添加 `break` 语句，让游戏在用户获胜时退出：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

在 `break` 后添加 `You win!` 行，会让程序在用户正确猜出秘密数字时退出
循环。退出循环也意味着退出程序，因为循环是 `main` 的最后一部分。

### 处理无效输入

为了进一步改进游戏的行为，我们不让程序在用户输入非数字时崩溃，而是让
游戏忽略非数字输入，以便用户继续猜。可以按照示例 2-5 修改将 `guess`
从 `String` 转换为 `u32` 的那一行。

<Listing number="2-5" file-name="src/main.rs" caption="忽略非数字猜测并要求再次猜测，而不是让程序崩溃">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

我们从调用 `expect` 改为使用 `match` 表达式，将遇到错误时崩溃改为处理
错误。记住，`parse` 返回 `Result` 类型，而 `Result` 是具有 `Ok` 和 `Err`
变体的枚举。这里使用 `match` 表达式的方式，与处理 `Ordering` 方法返回的
`cmp` 结果时相同。

如果 `parse` 能成功将字符串转换为数字，它会返回包含结果数字的 `Ok` 值。
这个 `Ok` 值会匹配第一个分支的模式，`match` 表达式只会返回 `num`
生成并放入 `parse` 值中的 `Ok` 值。这个数字最终会出现在我们正在创建的
新 `guess` 变量中。

如果 `parse` 无法将字符串转换为数字，它会返回包含更多错误信息的 `Err`
值。`Err` 值不匹配第一个 `Ok(num)` 分支中的 `match` 模式，但会匹配第二
个分支中的 `Err(_)` 模式。下划线 `_` 是一个兜底值；在这个例子中，
我们表示希望匹配所有 `Err` 值，不论其中包含什么信息。因此，程序会执行
第二个分支中的 `continue`，告诉程序进入 `loop` 的下一次迭代，并再次要求
用户猜测。这样一来，程序实际上会忽略 `parse` 可能遇到的所有错误！

现在程序中的一切都应按预期工作。试试看：

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

太棒了！再做一个很小的最后调整，猜数游戏就完成了。记住，程序仍在打印
秘密数字。这对测试很有帮助，但会破坏游戏体验。让我们删除输出秘密数字
的 `println!`。示例 2-6 展示了最终代码。

<Listing number="2-6" file-name="src/main.rs" caption="完整的猜数游戏代码">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

至此，咱们已成功构建了这个猜数游戏。恭喜！

## 本章小结

这个项目以实践的方式向你介绍了许多 Rust 新概念：`let`、`match`、函数、
使用外部代码包等。接下来的几章会更详细地讲解这些概念。第 3 章介绍大多数
编程语言都有的概念，例如变量、数据类型和函数，并展示如何在 Rust 中使用
它们。第 4 章探讨所有权，这是让 Rust 区别于其他语言的特性。第 5 章讨论
结构体和方法语法，第 6 章解释枚举的工作方式。

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
