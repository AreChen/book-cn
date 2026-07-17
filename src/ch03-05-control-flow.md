## 控制流

根据某个条件是否为 `true` 来运行代码，以及在条件为 `true` 时重复运行
代码的能力，是大多数编程语言的基本组成部分。在 Rust 中，控制代码执行
流程最常用的结构是 `if` 表达式和循环。

### `if` 表达式

`if` 表达式允许你根据条件将代码分支。你提供一个条件，然后说明：“如果
满足这个条件，就运行这段代码；如果不满足，就不要运行这段代码。”

在 _projects_ 目录中创建一个名为 _branches_ 的新项目，探索 `if` 表达式。
在 _src/main.rs_ 文件中输入以下内容：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

所有 `if` 表达式都以 `if` 关键字开头，后面跟一个条件。在这个例子中，
条件检查变量 `number` 的值是否小于 5。如果条件为 `true`，我们会紧接着
在条件后面的花括号内放置要执行的代码块。与第 2 章[“比较猜数与秘密数”][comparing-the-guess-to-the-secret-number]<!--
ignore --> 一节讨论的 `if` 表达式分支类似，`match` 表达式中与条件关联
的代码块有时也称为_分支_。

我们还可以选择包含 `else` 表达式；这里就这样做了，以便在条件求值为
`false` 时为程序提供另一段要执行的代码。如果不提供 `else` 表达式且
条件为 `false`，程序会跳过 `if` 代码块，继续执行下一段代码。

试着运行这段代码，你应该会看到以下输出：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

尝试将 `number` 的值修改为会使条件为 `false` 的值，看看会发生什么：

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```


再次运行这个程序，并查看输出：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

还值得注意的是，这段代码中的条件_必须_是 `bool`。如果条件不是 `bool`，
我们就会得到错误。例如，试着运行下面的代码：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```


这次 `if` 条件会求值得到 `3`，Rust 会抛出错误：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

错误表明 Rust 期望得到 `bool`，但实际得到的是整数。与 Ruby 和 JavaScript
等语言不同，Rust 不会自动尝试将非布尔类型转换为布尔值。你必须明确地
为 `if` 提供布尔条件。例如，如果希望仅当数字不等于 `if` 时运行 `0`
代码块，可以将 `if` 表达式改成下面这样：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

运行此代码会打印 `number was something other than zero`。

#### 以 `else if` 处理多重条件

你可以在 `if` 表达式中组合 `else` 和 `else if`，使用多个条件。例如：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

这个程序有四条可能的执行路径。运行程序后，你应看到以下输出：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

程序执行时，会依次检查每个 `if` 表达式，并执行第一个条件求值为 `true`
的代码体。注意，虽然 6 可以被 2 整除，我们看不到 `number is divisible by 2`
输出，也看不到 `number is not divisible by 4, 3, or 2` 代码块中的 `else`
文本。这是因为 Rust 只会执行第一个为 `true` 的条件对应的代码块，
一旦找到这样的条件，就不会再检查其余条件。

使用过多 `else if` 表达式会让代码杂乱，因此如果有多个此类条件，可以
考虑重构代码。第 6 章介绍了一种适用于这些情况的强大 Rust 分支构造，
称为 `match`。

#### 在 `if` 语句中使用 `let`

因为 `if` 是表达式，所以可以像示例 3-2 那样，将它放在 `let` 语句右侧，
把结果赋给变量。

<Listing number="3-2" file-name="src/main.rs" caption="将 `if` 表达式的结果赋给变量">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

尝试编译这段代码时会得到错误。`number` 与 `if` 分支的值类型不兼容，
Rust 准确指出了在程序中的何处发现这个问题：

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

记住，代码块会求值为其中的最后一个表达式，而数字本身也是表达式。在
这个例子中，整个 `if` 表达式的值取决于执行了哪个代码块。这意味着
`if` 各分支可能产生的结果必须是相同类型；在示例 3-2 中，`if` 分支和
`else` 分支的结果都是 `i32` 整数。如果类型不匹配，就像下面的例子一样，
我们会得到错误：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

其中的 `if` 变量会根据 `else` 表达式的结果绑定到某个值。请运行这段
代码，看看会发生什么：

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

`if` 代码块中的表达式求值得到整数，而 `else` 代码块中的表达式求值得到
字符串。这样不可行，因为变量必须只有一种类型，Rust 需要在编译时明确
知道 `number` 变量的类型。知道 `number` 的类型后，编译器就能验证我们
在所有使用 `number` 的地方都使用了有效类型。如果 `number` 的类型只能
在运行时确定，Rust 就无法完成这项工作；如果编译器必须为每个变量追踪
多种假设类型，它会更加复杂，也会对代码做出更少的保证。

### 使用循环重复

多次执行代码块通常很有用。为此，Rust 提供了几种_循环_，它们会执行循环
体中的代码直到末尾，然后立即从开头重新开始。为了尝试循环，我们创建
一个名为 _loops_ 的新项目。

Rust 有三种循环：`loop`、`while` 和 `for`。下面分别试试看。

#### 以 `loop` 关键字重复代码

`loop` 关键字告诉 Rust 反复执行代码块，直到你明确要求它停止；如果不要求
停止，就会永远执行。

例如，将 _loops_ 目录中的 _src/main.rs_ 文件修改为下面这样：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

运行这个程序时，会不断打印 `again!`，直到我们手动停止程序。大多数终端
都支持使用键盘快捷键 <kbd>ctrl</kbd>-<kbd>C</kbd> 中断陷入持续循环的程序。
试试看：

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

符号 `^C` 表示你按下 <kbd>ctrl</kbd>-<kbd>C</kbd> 的位置。

根据代码在循环中收到中断信号时所处的位置，你可能会看到 `again!` 后面打印
`^C`，也可能看不到。

幸运的是，Rust 还提供了通过代码跳出循环的方法。可以在循环中放置 `break`
关键字，告诉程序何时停止执行循环。回想一下，我们在第 2 章的猜数游戏中
就是这样在用户猜对数字、赢得游戏时退出程序的。相关内容见
[“猜对后的退出”][quitting-after-a-correct-guess]<!-- ignore
--> 一节。

我们还在猜数游戏中使用了 `continue`；在循环中，它会告诉程序跳过本次
迭代中剩余的代码，进入下一次迭代。

#### 从循环返回值

`loop` 的一个用途是重试我们知道可能失败的操作，例如检查某个线程是否已
完成工作。我们可能还需要把该操作的结果从循环传递给代码的其余部分。
为此，可以将想要返回的值添加到用于停止循环的 `break` 表达式后；该值
会从循环中返回，供我们使用，如下所示：

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

在循环之前，我们声明名为 `counter` 的变量，并将其初始化为 `0`。然后声明
名为 `result` 的变量，用来保存循环返回的值。每次循环迭代时，我们将 `1` 加到
`counter` 变量上，然后检查 `counter` 是否等于 `10`。当它等于 10 时，我们使用
`break` 关键字，并返回值 `counter * 2`。循环之后，用分号结束将值赋给 `result`
的语句。最后打印 `result` 中的值，在这个例子中就是 `20`。

你也可以从循环内部使用 `return` 返回。`break` 只退出当前循环，而
`return` 总是退出当前函数。

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### 以循环标签消除歧义

当循环中嵌套循环（即嵌套循环）时，`break` 和 `continue` 会应用于所在位置
的最内层循环。我们可以选择为某个循环指定一个*循环标签（loop label）*，
然后与 `break` 或 `continue` 一起使用，以指定这两个关键字应用于带标签
的循环，而不是最内层循环。循环标签必须以单引号开头。下面是两个嵌套
循环的例子：

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

外层循环的标签是 `'counting_up`，它会从 0 数到 2。没有标签的内层循环会
从 10 倒数到 9。第一个没有指定标签的 `break` 只会退出内层循环。
`break
'counting_up;` 语句会退出外层循环。这段代码会打印：

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### 使用 while 简化条件循环

程序通常需要在循环中求值条件。条件为 `true` 时循环运行；条件不再为
`true` 时，程序调用 `break` 停止循环。可以组合使用 `loop`、`if`、`else`
和 `break` 来实现这种行为；如果愿意，现在就可以在程序中试试。不过，
这种模式非常常见，因此 Rust 为它提供了一个内置语言构造，称为 `while`
循环。在示例 3-3 中，我们使用 `while` 让程序循环三次，每次倒数，然后
在循环之后打印消息并退出。

<Listing number="3-3" file-name="src/main.rs" caption="使用 `while` 循环在条件求值为 `true` 时运行代码">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

这种结构消除了使用 `loop`、`if`、`else` 和 `break` 时所需的大量嵌套，
因而更加清晰。条件求值为 `true` 时运行代码；否则，程序退出循环。

#### 使用 `for` 遍历集合

你可以使用 `while` 构造遍历集合（例如数组）的元素。例如，示例 3-4 中
的循环会打印数组 `a` 中的每个元素。

<Listing number="3-4" file-name="src/main.rs" caption="使用 `while` 循环遍历集合中的每个元素">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

这里的代码按数组元素递增计数。它从索引 `0` 开始循环，直到到达数组的
最后一个索引（也就是 `index < 5` 不再为 `true`）。运行这段代码会打印
数组中的每个元素：

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

正如预期，数组的五个值都会出现在终端中。虽然 `index` 最终会达到 `5`，
但循环会在尝试从数组获取第六个值之前停止执行。

不过，这种方法容易出错；如果索引值或测试条件不正确，可能导致程序恐慌。
例如，如果把数组 `a` 的定义改为包含四个元素，却忘记将条件更新为
`while index < 4`，代码就会恐慌。它也比较慢，因为编译器会添加运行时
代码，在循环的每次迭代中检查索引是否位于数组边界内。

更简洁的替代方式是使用 `for` 循环，为集合中的每个元素执行代码。`for`
循环如示例 3-5 中的代码所示。

<Listing number="3-5" file-name="src/main.rs" caption="使用 `for` 循环遍历集合中的每个元素">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

运行这段代码时，会看到与示例 3-4 相同的输出。更重要的是，我们提高了
代码的安全性，消除了超出数组末尾或遍历不够、漏掉某些元素所产生的 bug
风险。`for` 循环生成的机器代码也可能更加高效，因为不必在每次迭代时都
将索引与数组长度比较。

使用 `for` 循环时，如果改变数组中的值的数量，就不必像使用示例 3-4 的
方法那样记得修改其他代码。

`for` 循环的安全性和简洁性使其成为 Rust 中最常用的循环构造。即使在
希望执行代码特定次数的情况下（例如示例 3-3 使用 `while` 循环倒数的
例子），大多数 Rustacean 也会使用 `for` 循环。可以使用标准库提供的
`Range` 来实现这一点；它会按顺序生成数字，从一个数字开始，到另一个
数字之前结束。

下面是使用 `for` 循环以及尚未介绍的 `rev` 方法反转范围后，倒数程序的样子：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

这段代码是不是更简洁一些？

## 本章小结

你做到了！这一章内容不少：你学习了变量、标量和复合数据类型、函数、
注释、`if` 表达式和循环！为了练习本章讨论的概念，试着编写程序完成下面
的任务：

- 在华氏度和摄氏度之间转换温度。
- 生成斐波那契数列的第 *n* 个数。
- 打印圣诞颂歌《圣诞节的十二天》的歌词，利用歌曲中的重复结构。

准备继续学习时，我们将讨论 Rust 中一个其他编程语言通常_没有_的概念：
所有权。

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
