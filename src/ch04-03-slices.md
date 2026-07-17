## 切片类型

_切片_让你可以引用[集合](ch08-00-common-collections.md)<!-- ignore -->中连续的一系列
元素。切片是一种引用，因此不拥有所有权。

下面是一个小编程问题：编写一个函数，接收由空格分隔的单词字符串，并返回它在该字符串
中找到的第一个单词。如果函数在字符串中找不到空格，那么整个字符串就是一个单词，应
返回整个字符串。

> 注意：为了介绍切片，本节只假定使用 ASCII；第 8 章[“用字符串存储 UTF-8 编码文本”][strings]<!-- ignore -->
> 一节会更全面地讨论 UTF-8 的处理。

先看看不使用切片时如何编写这个函数的签名，以便理解切片要解决的问题：

```rust,ignore
fn first_word(s: &String) -> ?
```

函数 `first_word` 的参数类型为 `&String`。我们不需要所有权，所以这样就很好。（在
惯用 Rust 中，除非有必要，函数不会获取参数的所有权；随着继续学习，原因会变得清楚。）
但我们应该返回什么？我们确实没有描述字符串_一部分_的方式。不过，可以返回由空格标
示的单词末尾的索引。让我们试试，如清单 4-7 所示。

<Listing number="4-7" file-name="src/main.rs" caption="返回 `first_word` 函数中 `String` 参数的字节索引值">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

</Listing>

因为我们需要逐个遍历 `String` 的元素并检查值是否为空格，所以会将我们的 `String` 转换
为字节数组，使用 `as_bytes` 方法。

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

接下来，我们使用 `iter` 方法在字节数组上创建迭代器：

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

我们将在[第 13 章][ch13]<!-- ignore -->更详细地讨论迭代器。现在只需知道，`iter` 是
一个返回集合中每个元素的方法，而 `enumerate` 会包装 `iter` 的结果，将每个元素作为元
组的一部分返回。`enumerate` 返回的元组的第一个元素是索引，第二个元素是指向该元素的
引用。这比我们自己计算索引方便一些。

因为 `enumerate` 方法返回元组，所以我们可以使用模式解构该元组。我们将在[第 6 章][ch6]<!-- ignore -->
更详细地讨论模式。在 `for` 循环中，我们指定一个模式，其中 `i` 表
示元组中的索引，`&item` 表示元组中的单个字节。因为我们从 `.iter().enumerate()` 得
到的是元素的引用，所以在模式中使用 `&`。

在 `for` 循环中，我们使用字节字面量语法搜索表示空格的字节。如果找到空格，就返回它
的位置。否则，使用 `s.len()` 返回字符串长度。

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

现在我们有了找出字符串中第一个单词末尾索引的方法，但存在一个问题。我们单独返回一个
`usize`，但它只有在 `&String` 的上下文中才是有意义的数字。换句话说，因为它是独立于
`String` 的值，所以无法保证它将来仍然有效。请看清单 4-8 中的程序，它使用了清单 4-7
中的 `first_word` 函数。

<Listing number="4-8" file-name="src/main.rs" caption="存储调用 `first_word` 函数的结果，然后修改 `String` 的内容">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-08/src/main.rs:here}}
```

</Listing>

这段程序可以无误编译，即使在使用 `word` 后调用 `s.clear()` 也一样。因为 `word` 完全
没有连接到 `s` 的状态，所以 `word` 仍然包含值 `5`。我们可以将值 `5` 与变量 `s` 一起
使用来尝试提取第一个单词，但这会是一个错误，因为自从 `s` 的内容在我们将 `5` 保存到
`word` 之后，已经发生了变化。

必须担心 `word` 中的索引与 `s` 中的数据不同步，既乏味又容易出错！如果我们编写
`second_word` 函数，管理这些索引会更加脆弱。它的签名必须如下所示：

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

现在我们要跟踪起始索引_和_结束索引，而且还有更多根据特定状态下的数据计算出的值，
却完全没有与该状态绑定。我们有三个互不相关、需要保持同步的变量在四处存在。

幸运的是，Rust 有解决这个问题的办法：字符串切片。

### 字符串切片

_字符串切片_是对 `String` 中连续元素序列的引用，看起来如下：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-17-slice/src/main.rs:here}}
```

与整个 `String` 的引用不同，`hello` 是对 `String` 一部分的引用，这由额外的 `[0..5]`
部分指定。我们通过在方括号中指定范围 `[starting_index..ending_index]` 来创建切片，
其中_`starting_index`_是切片中的第一个位置，_`ending_index`_比切片中最后一个位置多
一个。在内部，切片数据结构存储切片的起始位置和长度，对应于_`ending_index`_减去
_`starting_index`_。因此，在 `let world = &s[6..11];` 的情况下，`world` 是一个切片，
包含一个指向 `s` 的索引 6 处字节的指针，长度值为 `5`。

图 4-7 用图示展示了这一点。

<img alt="三张表：一张表示 s 的栈数据，指向堆上字符串数据表中索引 0 处的字节 &quot;hello world&quot;。第三张表示切片 world 的栈数据，长度值为 5，指向堆数据表中的第 6 个字节。"
src="img/trpl04-07.svg" class="center" style="width: 50%;" />

<span class="caption">图 4-7：引用 `String` 一部分的字符串切片</span>

使用 Rust 的 `..` 范围语法时，如果想从索引 0 开始，可以省略两个句点前的值。换句话
说，下面两种写法相同：

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

同样，如果切片包含 `String` 的最后一个字节，就可以省略末尾的数字。这意味着下面两种
写法相同：

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

也可以同时省略两个值来获取整个字符串的切片。因此，下面两种写法相同：

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> 注意：字符串切片的范围索引必须位于有效的 UTF-8 字符边界。如果试图在多字节字符的
> 中间创建字符串切片，程序将因错误退出。

了解这些信息后，让我们重写 `first_word` 使其返回切片。表示“字符串切片”的类型写作
`&str`：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

</Listing>

我们用与清单 4-7 相同的方式获取单词末尾的索引，即查找第一次出现的空格。找到空格
后，我们以字符串开头和空格索引作为起始、结束索引，返回一个字符串切片。

现在调用 `first_word` 时，会得到一个与底层数据绑定的单一值。这个值由指向切片起点的
引用和切片中元素的数量组成。

让 `second_word` 函数返回切片同样可行：

```rust,ignore
fn second_word(s: &String) -> &str {
```

现在我们有了一个直观且不易出错的 API，因为编译器会确保指向 `String` 的引用保持有效。
还记得清单 4-8 中程序的错误吗？当时我们得到第一个单词末尾的索引，但随后清空了字符
串，使索引失效。那段代码在逻辑上不正确，却没有立即报错。如果继续尝试在空字符串上
使用第一个单词的索引，问题稍后才会出现。切片使这个错误不可能发生，并让我们更早知道
代码有问题。使用切片版本的 `first_word` 会产生编译时错误：

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/src/main.rs:here}}
```

</Listing>

编译器错误如下：

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

回想一下借用规则：如果我们拥有某个值的不可变引用，就不能同时创建可变引用。因为
`clear` 需要截断 `String`，所以它需要获取可变引用。`println!` 在调用 `clear` 后使用了
`word` 中的引用，因此此时不可变引用仍然必须处于活动状态。Rust 不允许 `clear` 中的
可变引用和 `word` 中的不可变引用同时存在，所以编译失败。Rust 不仅让我们的 API 更易
于使用，还在编译时消除了整类错误！

<!-- Old headings. Do not remove or links may break. -->

<a id="string-literals-are-slices"></a>

#### 作为切片的字符串字面量

回想一下，我们曾讨论过字符串字面量存储在二进制文件中。现在知道了切片，我们就能更
准确地理解字符串字面量：

```rust
let s = "Hello, world!";
```

这里 `s` 的类型是 `&str`：它是一个指向二进制文件中特定位置的切片。这也解释了字符
串字面量为什么不可变；`&str` 是不可变引用。

#### 字符串切片作为参数

知道可以对字面量和 `String` 值创建切片后，我们可以进一步改进 `first_word`，也就是改
进它的签名：

```rust,ignore
fn first_word(s: &String) -> &str {
```

更有经验的 Rust 开发者会改为使用清单 4-9 中所示的签名，因为它允许我们对 `&String`
值和 `&str` 值使用同一个函数。

<Listing number="4-9" caption="改进 `first_word` 函数：将字符串切片用作 `s` 参数的类型">

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

</Listing>

如果有字符串切片，可以直接传递它。如果有 `String`，可以传递 `String` 的切片或 `String`
的引用。这种灵活性利用了解引用强制转换，这是我们将在第 15 章[“在函数和方法中使用
解引用强制转换”][deref-coercions]<!--
ignore -->一节介绍的功能。

将函数定义为接收字符串切片，而不是接收 `String` 的引用，可以让我们的 API 更通用、更
有用，同时不会损失任何功能：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

</Listing>

### 其他切片

如你所想，字符串切片专用于字符串。不过还有一种更通用的切片类型。考虑下面这个数组：

```rust
let a = [1, 2, 3, 4, 5];
```

正如我们可能想引用字符串的一部分，也可能想引用数组的一部分。可以这样做：

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

这个切片的类型是 `&[i32]`。它与字符串切片的工作方式相同，都存储指向第一个元素的引
用和长度。你会在各种其他集合中使用这种切片。我们将在第 8 章讨论向量时详细介绍这些
集合。

## 总结

所有权、借用和切片的概念在编译时确保 Rust 程序的内存安全。Rust 语言像其他系统编程语
言一样让你能够控制内存的使用。但让数据的所有者在离开作用域时自动清理数据，意味着你
不必为了获得这种控制而编写和调试额外的代码。

所有权会影响 Rust 许多其他部分的工作方式，因此在本书剩余内容中我们还会继续讨论这些
概念。接下来进入第 5 章，看看如何将数据片段组合到 `struct` 中。

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#using-deref-coercions-in-functions-and-methods
