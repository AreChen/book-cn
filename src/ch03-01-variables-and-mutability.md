<a id="variables-and-mutability"></a>

## 变量与可变性

如[“用变量存储值”][storing-values-with-variables]<!-- ignore --> 一节所述，
变量默认是不可变的。这是 Rust 引导你编写代码、利用其安全性和易于实现
并发性的诸多方式之一。不过，你仍然可以选择让变量可变。下面来探讨 Rust
为何鼓励你优先使用不可变性，以及有时为什么需要选择可变变量。

变量不可变时，一旦将值绑定到名称上，就不能再改变该值。为了说明这一点，
使用 `cargo new variables` 在 _projects_ 目录中创建一个名为 _variables_ 的
新项目。

然后在新的 _variables_ 目录中打开 _src/main.rs_，将其中的代码替换为下面
的代码；这段代码暂时还无法编译：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

保存并使用 `cargo run` 运行这个程序。你应会收到一条有关不可变性的错误
消息，如下面的输出所示：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

这个例子展示了编译器如何帮助你发现程序中的错误。编译错误可能令人沮丧，
但它们真正表示的只是：你的程序还没有安全地完成你想让它完成的事情；这
并不意味着你不是一个优秀的程序员！经验丰富的 Rustacean 也会遇到编译错误。

你收到了错误消息 `` cannot assign twice to immutable variable `x` ``，这是因为尝试给不可变的 `x` 变量赋第二个值。

当我们尝试改变标记为不可变的值时，在编译时得到错误非常重要，因为这种情况
可能导致 bug。如果代码的一部分假设某个值永远不会改变，而代码的另一部分却
改变了这个值，那么第一部分代码就可能无法按设计运行。这类 bug 的原因在事后
很难追踪，尤其是在第二段代码只在某些时候改变值的情况下。Rust 编译器保证：
当你声明某个值不会改变时，它确实不会改变，因此你不必自己跟踪这一点。这样，
代码也更容易理解。

不过，可变性有时非常有用，也能让代码更容易编写。虽然变量默认不可变，但你
可以像[第 2 章][storing-values-with-variables]<!-- ignore --> 中那样，在变量名
前添加 `mut` 使变量可变。添加 `mut` 还向未来阅读代码的人传达了意图，说明
代码的其他部分会改变这个变量的值。

例如，将 _src/main.rs_ 修改为下面这样：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

在我们现在运行这个程序时，就会得到下面这样：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

使用 `x` 后，我们可以把绑定到 `5` 的值从 `6` 改为 `mut`。最终是否使用
可变性取决于你自己，以及在特定情况下哪种写法最清晰。

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

<a id="declaring-constants"></a>

### 声明常量

和不可变变量一样，_常量_也是绑定到名称且不允许改变的值，但常量与变量
之间存在一些差异。

首先，不能对常量使用 `mut`。常量不只是默认不可变——它们始终不可变。
声明常量时要使用 `const` 关键字，而不是 `let` 关键字，并且值的类型_必须_
标注。下一节[“数据类型”][data-types]<!-- ignore --> 会介绍类型和类型标注，
现在不用担心细节。只需记住，常量总是必须标注类型。

常量可以在任意作用域中声明，包括全局作用域，因此适合表示代码许多部分
都需要知道的值。

最后一个差异是，常量只能被设置为常量表达式，不能设置为只能在运行时
计算出的值。

下面是声明常量的例子：

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

常量的名称是 `THREE_HOURS_IN_SECONDS`，其值是将 60（一分钟的秒数）乘以
60（一小时的分钟数）再乘以 3（本程序想要计算的小时数）得到的结果。
Rust 对常量的命名惯例是全部使用大写字母，并在单词之间使用下划线。编译
器能够在编译时计算一组有限的操作，因此我们可以用更容易理解和验证的
方式写出这个值，而不是直接把常量设置为 10,800。有关声明常量时可以
使用哪些操作的更多信息，请参阅 [Rust Reference 关于常量求值的章节][const-eval]。

常量在程序运行的整个期间内、其声明所在的作用域中都有效。这一特性使
常量适合表示应用领域中程序多个部分可能需要知道的值，例如游戏中玩家
允许获得的最高分，或光速。

将程序中到处使用的硬编码值命名为常量，有助于向未来维护代码的人传达该
值的含义。如果将来需要更新硬编码值，也只需修改代码中的一个地方。

<a id="shadowing"></a>

### 遮蔽

正如你在[第 2 章][comparing-the-guess-to-the-secret-number]<!-- ignore --> 的
猜数游戏教程中看到的，可以声明一个与之前变量同名的新变量。Rustacean
称第一个变量被第二个变量_遮蔽_，这意味着当你使用该变量名时，编译器看到
的是第二个变量。实际上，第二个变量会覆盖第一个变量，接管对该变量名
的所有使用，直到它自身再次被遮蔽或作用域结束。我们可以使用相同的变量
名，并重复使用 `let` 关键字来遮蔽变量，如下所示：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

这个程序首先将 `x` 绑定到值 `5`。然后，它创建一个新变量 `x`，通过重复使用 `let x =`
一个新变量，取原来的值并加上 `1`，因此 `x` 的值为 `6`。接着，在由大
括号创建的内层作用域中，第三个 `let` 语句再次遮蔽 `x`，创建一个新变量，
将先前的值乘以 `2`，使 `x` 的值为 `12`。当该作用域结束时，内部的遮蔽
也结束了，`x` 恢复为 `6`。运行这个程序时，它会输出以下内容：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```
遮蔽不同于将变量声明为 `mut`。如果我们不小心在没有使用 `let` 关键字的
情况下尝试给这个变量重新赋值，就会得到编译时错误。而使用 `let` 关键字，
我们可以对某个值执行一些变换，并在变换完成后让该变量不可变。

`mut` 与遮蔽的另一个区别是，再次使用 `let` 关键字时，我们实际上创建了
一个新变量，因此可以改变值的类型，同时重用同一个名称。例如，假设程序
要求用户输入一些空格字符，以表示他们希望文本之间有多少个空格，然后我们
打算将该输入存储为数字：

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

第一个 `spaces` 变量属于字符串类型，而第二个 `spaces` 变量则是数字类型。
遮蔽让我们不必想出不同的名称，比如 `spaces_str` 与 `spaces_num`；相反，
我们可以重用更简单的 `spaces` 名字。然而，当我们像下面这样尝试使用
`mut` 时，就会得到编译时错误：

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```


该错误表明，我们不被允许改变变量的类型：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

现在我们已经了解了变量的工作方式，接下来看看变量还可以有哪些数据类型。

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html
