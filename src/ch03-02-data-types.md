<a id="data-types"></a>

## 数据类型

Rust 中的每个值都有特定的_数据类型_，它告诉 Rust 当前指定的是什么数据，
从而让 Rust 知道如何处理这些数据。我们将了解两类数据类型：标量类型和
复合类型。

请记住，Rust 是一种_静态类型_语言，这意味着它必须在编译时知道所有变量
的类型。编译器通常可以根据值及其使用方式推断出我们想使用的类型。当
存在多种可能类型时，例如第 2 章[“比较猜数与秘密数”][comparing-the-guess-to-the-secret-number]<!-- ignore --> 一节中使用 `String` 将 `parse` 转换为数字类型时，我们必须
添加类型标注，如下所示：

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

如果不添加前面代码中的 `: u32` 类型标注，Rust 会显示以下错误。这意味着
编译器需要更多信息，才能知道我们打算使用哪种类型：

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

下面我们会看到其他数据类型的不同类型标注。

### 标量类型

所谓*标量（scalar）*类型表示单个值。Rust 有四种主要的标量类型：

- 整数
- 浮点数
- 布尔值
- 字符

你可能在其他编程语言中见过这些类型。下面来了解它们在 Rust 中的工作原理。

<a id="integer-types"></a>

#### 整型

_整数_是不带小数部分的数字。我们在第 2 章使用过一种整数类型，即 `u32`
类型。这个类型声明表示与它关联的值应当是无符号整数（有符号整数类型
以 `i` 开头，而不是 `u`），并占用 32 位空间。表 3-1 展示了 Rust 的
内置整数类型。我们可以使用其中任意一种变体来声明整数值的类型。

<span class="caption">表 3-1：Rust 中的整数类型</span>

| 长度  | 有符号  | 无符号 |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| 取决于架构 | `isize` | `usize`  |

每种变体都可以是有符号或无符号，并具有明确的大小。_有符号_和_无符号_
表示数字是否可能为负数——换句话说，数字是否需要带符号（有符号），
还是始终为正数、因而可以不带符号表示（无符号）。这就像在纸上写数字：
符号很重要时，数字会带加号或减号；可以确定数字为正数时，则不写符号。
有符号数字使用[二进制补码][twos-complement]<!-- ignore
--> 表示。

每种有符号变体可以存储从 −(2<sup>n − 1</sup>) 到 2<sup>n − 1</sup> − 1
（含边界）的数字，其中 _n_ 是该变体使用的位数。因此，`i8` 可以存储
从 −(2<sup>7</sup>) 到 2<sup>7</sup> − 1 的数字，也就是 −128 到 127。
无符号变体可以存储从 0 到 2<sup>n</sup> − 1 的数字，所以 `u8` 可以存储
从 0 到 2<sup>8</sup> − 1 的数字，即 0 到 255。

此外，`isize` 和 `usize` 类型取决于程序运行所在计算机的架构：64 位架构
使用 64 位，32 位架构使用 32 位。

你可以用表 3-2 所示的任意形式书写整数字面量。可以属于多种数字类型的
数字字面量允许使用类型后缀（例如 `57u8`）来指定类型。数字字面量还可以
使用 `_` 作为视觉分隔符，让数字更容易阅读，例如 `1_000` 与写成 `1000`
具有相同的值。

<span class="caption">表 3-2：Rust 中的整数字面量</span>

| 数字字面量  | 示例       |
| ---------------- | ------------- |
| 十进制          | `98_222`      |
| 十六进制              | `0xff`        |
| 八进制            | `0o77`        |
| 二进制           | `0b1111_0000` |
| 字节（仅限 `u8`） | `b'A'`        |

那么如何知道应该使用哪种整数类型？如果不确定，Rust 的默认值通常是不错
的起点：整数类型默认为 `i32`。使用 `isize` 或 `usize` 的主要情况，是
需要为某种集合建立索引。

> ##### 整数溢出
>
> 假设有一个 `u8` 类型的变量，它可以保存 0 到 255 之间的值。如果尝试将
> 变量改为该范围之外的值（例如 256），就会发生_整数溢出_，可能产生两种
> 行为之一。在调试模式下编译时，Rust 会加入整数溢出检查；如果发生这种
> 情况，检查会让程序在运行时_恐慌_。Rust 使用_恐慌（panicking）_一词
> 表示程序带着错误退出；第 9 章[“不可恢复的错误与 `panic!`”][unrecoverable-errors-with-panic]<!-- ignore --> 一节将更深入地讨论恐慌。
>
> 在使用 `--release` 标志以发布模式编译时，Rust 不会加入会导致恐慌的
> 整数溢出检查。相反，如果发生溢出，Rust 会执行_二进制补码回绕_。简言
> 之，超过类型可保存最大值的数值会“回绕”到该类型可保存的最小值。
> 对于 `u8`，256 会变成 0，257 会变成 1，以此类推。程序不会恐慌，但
> 变量的值可能不是你所预期的值。依赖整数溢出的回绕行为会被视为错误。
>
> 要明确处理溢出的可能性，可以使用标准库为基本数字类型提供的以下几组
> 方法：
>
> - 使用 `wrapping_*` 方法（例如 `wrapping_add`）在所有编译模式下进行回绕。
> - 使用 `None` 方法在发生溢出时返回 `checked_*`。
> - 使用 `overflowing_*` 方法返回该值，以及一个表示是否发生溢出的布尔值。
> - 使用 `saturating_*` 方法将结果限制在该类型的最小值或最大值。

#### 浮点类型

Rust 还有两种表示_浮点数_的基本类型，浮点数就是带小数点的数字。Rust 的
浮点类型是 `f32` 和 `f64`，大小分别为 32 位和 64 位。默认类型是 `f64`，
因为在现代 CPU 上，它的速度大致与 `f32` 相同，但精度更高。所有浮点类型
都是有符号的。

下面的例子展示了浮点数的使用：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

浮点数按照 IEEE-754 标准表示。

#### 数值运算

Rust 支持所有数字类型应有的基本数学运算：加法、减法、乘法、除法和取余。
整数除法会向零截断为最接近的整数。下面的代码展示了如何在 `let` 语句中
使用每种数字运算：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

这些语句中的每个表达式都使用一个数学运算符，并求值得到单个值，然后将
该值绑定到变量。[附录 B][appendix_b]<!-- ignore --> 包含 Rust 提供的所有
运算符列表。

#### 布尔值类型

和大多数其他编程语言一样，Rust 中的布尔类型有两个可能的值：`true` 和
`false`。布尔值占用一个字节。Rust 使用 `bool` 指定布尔类型。例如：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

使用布尔值的主要方式是通过条件语句，例如 `if` 表达式。我们会在[“控制
流”][control-flow]<!-- ignore --> 一节介绍 `if` 表达式在 Rust 中的工作
方式。

#### 字符类型

Rust 的 `char` 类型是语言中最基本的字母类型。下面是声明 `char` 值的一些
例子：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

注意，我们使用单引号指定 `char` 字面量，而字符串字面量使用双引号。Rust
的 `char` 类型大小为 4 个字节，表示 Unicode 标量值，因此能够表示远超
ASCII 的内容。带重音符号的字母、中文、日文和韩文字符、表情符号以及
零宽空格，都是 Rust 中有效的 `char` 值。Unicode 标量值的范围包括从
`U+0000` 到 `U+D7FF`，以及从 `U+E000` 到 `U+10FFFF`（含边界）。不过，
“字符”并不是 Unicode 中真正的概念，因此你对“字符”的直觉可能与 Rust
中 `char` 的含义不完全一致。第 8 章的[“用字符串存储 UTF-8 编码文本”][strings]<!-- ignore --> 会详细讨论这个主题。

### 复合类型

所谓*复合类型（compound types）*可以将多个值组合成一个类型。Rust 有两种
基本复合类型：

- 元组
- 数组

<a id="the-tuple-type"></a>

#### 元组类型

_元组_是将多个不同类型的值组合成一个复合类型的通用方式。元组长度固定：
一旦声明，就不能增大或缩小。

我们将逗号分隔的值列表写在圆括号中来创建元组。元组中的每个位置都有一
种类型，而元组中不同值的类型不必相同。下面的例子添加了可选的类型标注：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

变量 `tup` 绑定到整个元组，因为元组被视为一个复合元素。要从元组中取出
各个值，可以使用模式匹配来解构元组值，如下所示：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

这个程序首先创建一个元组，并将它绑定到变量 `tup`。然后使用带有 `let`
的模式取得 `tup`，将它变成三个独立的变量 `x`、`y` 和 `z`。这称为_解构_，
因为它把一个元组拆成了三部分。最后，程序打印变量 `y` 的值，也就是 `6.4`。

我们还可以使用句点（`.`）后跟要访问的值的索引，直接访问元组元素。例如：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```


这个程序创建了一个元组 `x`，然后使用相应的索引访问元组中的各个元素。
和大多数编程语言一样，元组中的第一个索引为 0。

没有任何值的元组有一个特殊名称：*单元值（unit）*。这个值及其对应的类型
都写作 `()`，表示空值或空的返回类型。当表达式不返回任何其他值时，就会
隐式返回单元值。

#### 数组类型

另一种保存多个值的集合是_数组_。与元组不同，数组的每个元素必须具有相同
的类型。与某些其他语言中的数组不同，Rust 中的数组长度固定。

我们将数组中的值作为逗号分隔的列表写在方括号内：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

当你希望数据像目前见过的其他类型一样分配在栈上，而不是堆上（我们会在
[第 4 章][stack-and-heap]<!-- ignore --> 更详细地讨论栈和堆），或者希望
确保始终拥有固定数量的元素时，数组很有用。不过，数组不如向量灵活。
向量是标准库提供的类似集合类型，因为内容存放在堆上，所以允许增大或
缩小。如果不确定应该使用数组还是向量，很可能应该使用向量。[第 8 章][vectors]<!-- ignore --> 会更详细地介绍向量。

不过，如果你知道元素数量不会改变，数组会更有用。例如，如果程序要使用
月份名称，你可能会使用数组而不是向量，因为你知道它始终包含 12 个元素：

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```


我们会使用带有元素类型、分号以及数组元素数量的方括号来编写数组类型，
如下所示：

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```


这里，`i32` 是每个元素的类型。分号后的数字 `5` 表示数组包含五个元素。

我们还可以在方括号中指定初始值，后跟分号和数组长度，将数组初始化为
每个元素都包含同一个值，如下所示：

```rust
let a = [3; 5];
```

名为 `a` 的数组包含 `5` 个元素，初始时每个元素都设置为 `3`。这与写成
`let a = [3, 3, 3, 3, 3];` 相同，但更加简洁。

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### 数组元素的访问

数组是一块大小已知且固定的连续内存，可以分配在栈上。你可以使用索引访问
数组元素，如下所示：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

在这个例子中，名为 `first` 的变量会得到值 `1`，因为数组索引 `[0]` 处的
值就是 1。名为 `second` 的变量会得到值 `2`，它来自数组中的索引 `[1]`。

#### 无效数组元素访问

来看看尝试访问数组末尾之外的元素会发生什么。假设你像第 2 章的猜数游戏
一样运行下面的代码，从用户那里获取数组索引：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

这段代码可以成功编译。如果使用 `cargo run` 运行它，并输入 `0`、`1`、`2`、
`3` 或 `4`，程序会打印数组中对应索引处的值。如果输入数组末尾之外的
数字，例如 `10`，你会看到类似下面的输出：

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

程序在索引操作使用无效值的位置产生了运行时错误。程序带着错误消息退出，
没有执行最后的 `println!` 语句。当你使用索引访问元素时，Rust 会检查指定
的索引是否小于数组长度。如果索引大于或等于长度，Rust 就会恐慌。这项
检查必须在运行时进行，尤其是在这个例子中，因为编译器不可能知道用户
稍后运行代码时会输入什么值。

这是 Rust 内存安全原则发挥作用的例子。在许多底层语言中不会进行这种检查，
提供错误索引时可能访问无效内存。Rust 会立即退出，而不是允许访问内存并
继续执行，从而保护你免受这类错误的影响。第 9 章会进一步讨论 Rust 的
错误处理，以及如何编写既不会恐慌、也不允许访问无效内存的可读安全代码。

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
