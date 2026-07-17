## 使用字符串存储 UTF-8 编码的文本

我们在第 4 章讨论过字符串，现在来更深入地了解它们。Rust 新手经常会在字符串上
遇到困难，原因有三个：Rust 倾向于暴露潜在错误；字符串这种数据结构比许多程序
员想象的更加复杂；以及 UTF-8。当你从其他编程语言转来时，这些因素结合在一起，
可能会让字符串显得难以理解。

我们在集合的语境下讨论字符串，是因为字符串实际上是字节的集合，另外还提供了
一些方法，以便将这些字节解释为文本时执行有用的操作。本节将讨论 `String` 所
支持的、每种集合类型都具备的操作，例如创建、更新和读取。我们还会讨论 `String`
与其他集合的不同之处，也就是人类和计算机解释 `String` 数据的方式不同，使得对
`String` 使用索引变得复杂。

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### 定义字符串

首先，我们来明确术语 _字符串_ 的含义。Rust 核心语言只有一种字符串类型，即字
符串切片 `str`，它通常以借用形式 `&str` 出现。第 4 章讨论过字符串切片：它们是
指向存储在其他地方的 UTF-8 编码字符串数据的引用。例如，字符串字面量存储在程
序的二进制文件中，因此属于字符串切片。

`String` 类型由 Rust 标准库提供，而不是内置于核心语言中。它是一种可增长、可变、
拥有所有权且使用 UTF-8 编码的字符串类型。当 Rustacean 在 Rust 中提到“字符串”
时，可能指 `String` 或字符串切片 `&str` 中的任一种，而不只是其中一种类型。虽
然本节主要讨论 `String`，但这两种类型都在 Rust 标准库中被广泛使用，并且 `String`
和字符串切片都采用 UTF-8 编码。

### 创建新字符串

`Vec<T>` 支持的许多操作同样适用于 `String`，因为 `String` 实际上是字节向量的
包装器，并附带一些额外的保证、限制和能力。`Vec<T>` 与 `String` 中行为相同的一
个函数是用于创建实例的 `new` 函数，如清单 8-11 所示。

<Listing number="8-11" caption="创建新的空 `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

这行代码创建了一个名为 `s` 的新空字符串，之后我们可以向其中加载数据。通常，
我们会有一些希望作为字符串初始内容的数据。这时可以使用 `to_string` 方法；凡
是实现了 `Display` trait 的类型都可以使用它，字符串字面量就是这样。清单 8-12
展示了两个示例。

<Listing number="8-12" caption="使用 `to_string` 方法从字符串字面量创建 `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

这段代码创建了一个包含 `initial contents` 的字符串。

我们也可以使用 `String::from` 函数从字符串字面量创建 `String`。清单 8-13 中
的代码与清单 8-12 中使用 `to_string` 的代码等价。

<Listing number="8-13" caption="使用 `String::from` 函数从字符串字面量创建 `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

因为字符串的用途非常广泛，我们可以使用许多不同的字符串泛型 API，因此有很多
选择。有些选择看起来可能重复，但各自都有适用场景！在这里，`String::from` 和
`to_string` 做的是同一件事，所以选择哪一个取决于风格和可读性。

请记住，字符串采用 UTF-8 编码，因此可以包含任何经过正确编码的数据，如清单
8-14 所示。

<Listing number="8-14" caption="在字符串中存储不同语言的问候语">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

这些都是有效的 `String` 值。

### 更新字符串

如果向 `String` 中加入更多数据，它的大小就可以增长，内容也可以改变，就像
`Vec<T>` 的内容一样。此外，还可以方便地使用 `+` 运算符或 `format!` 宏连接多
个 `String` 值。

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### 使用 `push_str` 或 `push` 追加

我们可以使用 `String` 方法追加字符串切片来增长 `push_str`，如清单 8-15 所示。

<Listing number="8-15" caption="使用 `String` 方法向 `push_str` 追加字符串切片">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

执行这两行后，`s` 将包含 `foobar`。`push_str` 方法接收字符串切片，是因为我们
不一定想取得参数的所有权。例如，在清单 8-16 的代码中，我们希望将 `s2` 的内容
追加到 `s1` 后仍然能够继续使用它。

<Listing number="8-16" caption="向 `String` 追加字符串切片后继续使用它">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

如果 `push_str` 方法取得了 `s2` 的所有权，我们就无法在最后一行打印它的值。但
这段代码按预期正常工作！

`push` 方法接收一个字符作为参数，并将它添加到 `String` 中。清单 8-17 使用
`String` 方法向 `push` 添加字母 _l_。

<Listing number="8-17" caption="使用 `String` 向 `push` 值添加一个字符">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

结果是，`s` 将包含 `lol`。

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### 使用 `+` 或 `format!` 连接

通常，你会希望组合两个已有的字符串。一种方法是使用 `+` 运算符，如清单 8-18
所示。

<Listing number="8-18" caption="使用 `+` 运算符将两个 `String` 值组合成新的 `String` 值">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

字符串 `s3` 将包含 `Hello, world!`。相加后 `s1` 不再有效，以及我们为什么对 `s2`
使用引用，都与使用 `+` 运算符时所调用方法的签名有关。`+` 运算符使用 `add` 方
法，它的签名大致如下：

```rust,ignore
fn add(self, s: &str) -> String {
```

在标准库中，你会看到 `add` 使用泛型和关联类型定义。这里我们替换成了具体类型，
这正是使用 `String` 值调用该方法时发生的情况。我们将在第 10 章讨论泛型。这个
签名为我们理解 `+` 运算符中棘手的部分提供了线索。

首先，`s2` 前面有一个 `&`，表示我们要把第二个字符串的引用添加到第一个字符
串。这是因为 `s` 函数的 `add` 参数：我们只能把字符串切片添加到 `String`，不
能直接把两个 `String` 值相加。但等等，`&s2` 的类型是 `&String`，而不是 `&str`
第二个参数指定的 `add`。那么，为什么清单 8-18 能够编译呢？

我们可以在调用 `&s2` 时使用 `add`，是因为编译器能够将 `&String` 参数强制转换
为 `&str`。调用 `add` 方法时，Rust 会使用解引用强制转换，在这里就是把 `&s2`
转换为 `&s2[..]`。我们将在第 15 章更深入地讨论解引用强制转换。由于 `add` 不会
取得 `s` 参数的所有权，因此执行这次操作后，`s2` 仍然是有效的 `String`。

其次，从签名可以看出，`add` 会取得 `self` 的所有权，因为 `self` 没有 `&`。这
意味着清单 8-18 中的 `s1` 会被移动到 `add` 调用中，此后不再有效。因此，虽然
`let s3 = s1 + &s2;` 看起来像是复制两个字符串并创建一个新字符串，但这条语句
实际上会取得 `s1` 的所有权，追加一份 `s2` 内容的副本，然后返回结果的所有权。
换句话说，它看起来好像进行了很多复制，但实际上并没有；这种实现比复制更高效。

如果需要连接多个字符串，`+` 运算符的写法会变得笨重：

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

此时，`s` 将是 `tic-tac-toe`。夹杂了这么多 `+` 和 `"` 字符后，很难看清代码在
做什么。要以更复杂的方式组合字符串，可以改用 `format!` 宏：

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

这段代码同样会将 `s` 设置为 `tic-tac-toe`。`format!` 宏的工作方式类似
`println!`，但它不会把输出打印到屏幕上，而是返回一个包含这些内容的 `String`。
使用 `format!` 的代码更容易阅读，而且 `format!` 宏生成的代码使用引用，因此这
次调用不会取得任何参数的所有权。

### 对字符串使用索引

在许多其他编程语言中，通过索引访问字符串中的单个字符是有效且常见的操作。但
是，在 Rust 中如果尝试使用索引语法访问 `String` 的一部分，就会得到错误。请看
清单 8-19 中无效的代码。

<Listing number="8-19" caption="尝试对 `String` 使用索引语法">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

这段代码会产生以下错误：

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

错误信息已经说明了原因：Rust 字符串不支持索引。但为什么呢？要回答这个问题，
我们需要讨论 Rust 如何在内存中存储字符串。

#### 内部表示

`String` 是 `Vec<u8>` 的包装器。让我们看看清单 8-14 中几个正确编码的 UTF-8
示例字符串。首先是这个：

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

在这种情况下，`len` 会是 `4`，这意味着存储字符串 `"Hola"` 的向量长度为 4 个
字节。这些字母在 UTF-8 中编码时各占 1 个字节。不过，下面这行可能会让你感到
意外（注意，这个字符串以大写西里尔字母 _Ze_ 开头，而不是数字 3）：

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

如果有人问你这个字符串有多长，你可能会回答 12。事实上，Rust 的答案是 24：这
是以 UTF-8 编码“Здравствуйте”所需的字节数，因为该字符串中的每个 Unicode 标量
值都占用 2 个字节。因此，字符串字节的索引并不总能对应一个有效的 Unicode 标
量值。下面这段无效的 Rust 代码可以说明这一点：

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

你已经知道，`answer` 不会是第一个字母 `З`。`З` 使用 UTF-8 编码时，第一个字节
是 `208`，第二个是 `151`，所以看起来 `answer` 实际上应该是 `208`；但单独的
`208` 不是有效字符。如果用户请求这个字符串的第一个字母，返回 `208` 很可能不
是他们想要的结果；然而，这正是 Rust 在字节索引 0 处拥有的唯一数据。即使字符
串只包含拉丁字母，用户通常也不希望得到字节值：如果 `&"hi"[0]` 是一段有效代
码并返回字节值，它会返回 `104`，而不是 `h`。

所以答案是：为了避免返回意外的值并造成可能不会立即发现的 bug，Rust 根本不会
编译这段代码，从开发过程一开始就防止误解。

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### 字节、标量值和字素簇

关于 UTF-8 还需要注意，从 Rust 的角度看字符串实际上有三种相关的观察方式：字
节、标量值和字素簇（最接近我们所说的_字母_）。

以天城文书写的印地语单词“नमस्ते”为例，它以 `u8` 值向量的形式存储，看起来如
下：

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

这就是 18 个字节，也是计算机最终存储这些数据的方式。如果把它们看作 Unicode
标量值，也就是 Rust `char` 类型表示的值，这些字节看起来如下：

```text
['न', 'म', 'स', '्', 'त', 'े']
```

这里有六个 `char` 值，但第四个和第六个不是字母：它们是脱字符号，单独存在时
没有意义。最后，如果把它们看作字素簇，我们会得到人们会称为组成这个印地语单
词的四个字母：

```text
["न", "म", "स्", "ते"]
```

Rust 提供了多种解释计算机存储的原始字符串数据的方式，因此无论数据使用哪种人
类语言，每个程序都可以选择自己需要的解释方式。

Rust 不允许我们通过对 `String` 使用索引来获取字符，还有最后一个原因：索引操作
通常应该始终花费固定时间（O(1)）。但对 `String` 无法保证这种性能，因为 Rust 必
须从头遍历内容直到目标索引，才能确定其中有多少个有效字符。

### 切分字符串

对字符串使用索引通常不是好主意，因为字符串索引操作的返回类型并不明确：它应该
是字节值、字符、字素簇，还是字符串切片？因此，如果确实需要使用索引创建字符
串切片，Rust 要求你明确指定范围。

你可以使用 `[]` 加一个范围来创建包含特定字节的字符串切片，而不是使用 `[]` 加
单个数字进行索引：

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

这里的 `s` 会是一个 `&str`，包含字符串的前 4 个字节。前面提到过，这些字符每
个占 2 个字节，因此 `s` 会是 `Зд`。

如果尝试使用类似 `&hello[0..1]` 的方式只切分字符的一部分字节，Rust 会在运行时
触发 panic，就像访问向量中的无效索引一样：

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

使用范围创建字符串切片时应当谨慎，因为这样做可能导致程序崩溃。

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### 遍历字符串

处理字符串片段的最佳方式，是明确你需要的是字符还是字节。对于单独的 Unicode 标
量值，可以使用 `chars` 方法。对“Зд”调用 `chars` 会将它拆分并返回两个 `char`
类型的值，然后你可以遍历结果来访问每个元素：

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

这段代码会打印以下内容：

```text
З
д
```

另一种方式是使用 `bytes` 方法返回每个原始字节；这可能更适合你的领域：

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

这段代码会打印组成这个字符串的 4 个字节：

```text
208
151
208
180
```

但一定要记住，有效的 Unicode 标量值可能由多个字节组成。

从字符串中获取字素簇（例如天城文中的字素簇）比较复杂，因此标准库没有提供此
功能。如果你需要这种功能，[crates.io](https://crates.io/)<!-- ignore --> 上有
可用的 crate。

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### 处理字符串的复杂性

总之，字符串很复杂。不同编程语言会选择不同的方式向程序员呈现这种复杂性。
Rust 选择将正确处理 `String` 数据作为所有 Rust 程序的默认行为，这意味着程序
员必须在一开始就更多地考虑如何处理 UTF-8 数据。这种取舍暴露出的字符串复杂性
比其他编程语言中更明显，但它可以避免你在开发后期处理涉及非 ASCII 字符的错误。

好消息是，标准库基于 `String` 和 `&str` 类型提供了大量功能，可以帮助你正确处
理这些复杂情况。请务必查看相关文档，了解 `contains`（在字符串中搜索）和
`replace`（用另一个字符串替换部分内容）等实用方法。

接下来我们讨论稍微简单一些的内容：哈希映射！
