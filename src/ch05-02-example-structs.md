## 使用结构体的示例程序

为了理解何时应该使用结构体，我们来编写一个计算矩形面积的程序。先使用单独的
变量，然后逐步重构程序，直到使用结构体为止。

我们来用 Cargo 创建一个名为 _rectangles_ 的新二进制项目。它接收以像素为单位指定
的矩形宽度和高度，并计算矩形的面积。示例 5-8 展示了在项目的 _src/main.rs_ 中
完成这件事的一种简短程序。

<Listing number="5-8" file-name="src/main.rs" caption="使用单独的宽度和高度变量计算矩形面积">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

现在，使用 `cargo run` 运行这个程序：

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

这段代码通过将两个维度分别传给 `area` 函数，成功计算出了矩形的面积，但我们还
可以做更多事情，让这段代码更清晰、更易读。

这段代码的问题在 `area` 的签名中很明显：

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

`area` 函数本应计算一个矩形的面积，但我们编写的函数有两个参数，并且程序中的
任何地方都没有明确说明这两个参数是相关的。将宽度和高度分组在一起会更易于阅读
和管理。我们已经在第 3 章的[“元组类型”][the-tuple-type]<!-- ignore -->一节中
讨论过一种实现方式：使用元组。

### 使用元组重构

示例 5-9 展示了使用元组的另一版本程序。

<Listing number="5-9" file-name="src/main.rs" caption="使用元组指定矩形的宽度和高度">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

从某种意义上说，这个程序更好。元组让我们增加了一点结构，而且现在只需传递一个
参数。但从另一方面来说，这个版本不够清晰：元组不会命名其元素，因此我们必须
索引元组的各个部分，使计算不那么直观。

混淆宽度和高度对于面积计算并不重要，但如果想在屏幕上绘制矩形，就很重要了！我们
必须记住 `width` 是元组索引 `0`，而 `height` 是元组索引 `1`。如果其他人要使用
我们的代码，就更难弄清楚并记住这一点。因为我们没有在代码中传达数据的含义，现在
更容易引入错误。

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### 使用结构体重构

我们使用结构体通过标记数据来增加含义。可以将正在使用的元组转换为一个结构体，
为整体以及各个部分分别命名，如示例 5-10 所示。

<Listing number="5-10" file-name="src/main.rs" caption="定义 `Rectangle` 结构体">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

这里，我们定义了一个结构体，并将其命名为 `Rectangle`。在花括号内，我们将字段
定义为 `width` 和 `height`，二者的类型都是 `u32`。然后，在 `main` 中，我们创建
了一个具体的 `Rectangle` 实例，其宽度为 `30`、高度为 `50`。

现在，`area` 函数只接收一个参数，我们将其命名为 `rectangle`；参数类型是对一个
`Rectangle` 结构体实例的不可变借用。正如第 4 章所述，我们希望借用结构体，而不是
取得它的所有权。这样，`main` 就能保留所有权并继续使用 `rect1`，这也是我们在
函数签名和调用函数的地方使用 `&` 的原因。

`area` 函数访问实例的 `width` 和 `height` 字段（注意，访问借用的 `Rectangle` 结构体
实例的字段不会移动字段值，这也是你经常会看到结构体借用的原因）。现在，`area`
函数签名准确表达了我们的意思：使用 `Rectangle` 的 `width` 和 `height` 字段计算
面积。这说明宽度和高度彼此相关，并且为这些值提供了描述性名称，而不是使用元组
索引值 `0` 和 `1`。这让代码更清晰。

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### 使用派生特质添加功能

在调试程序时，如果能打印 `Rectangle` 的实例并查看其所有字段的值，会很有用。示例
5-11 尝试像前几章那样使用[`println!` 宏][println]<!-- ignore -->。然而，这样行不通。

<Listing number="5-11" file-name="src/main.rs" caption="尝试打印 `Rectangle` 实例">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

编译这段代码时，会得到一条包含以下核心消息的错误：

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

`println!` 宏可以进行多种格式化。默认情况下，花括号告诉 `println!` 使用一种名为
`Display` 的格式化方式：输出供最终用户直接使用的内容。到目前为止我们看到的原始
类型默认都实现了 `Display`，因为向用户显示 `1` 或其他原始类型时，通常只有一种
合理方式。但对于结构体，`println!` 应如何格式化输出就不那么明确了，因为存在更多
显示可能性：要不要逗号？要不要打印花括号？是否应显示所有字段？由于这种歧义，
Rust 不会试图猜测我们的意图，结构体也没有提供 `Display` 实现，供 `println!` 与
`{}` 占位符一起使用。

继续阅读错误信息，会找到下面这条有帮助的说明：

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

让我们试试！`println!` 宏调用现在会是 `println!("rect1 is
{rect1:?}");`。将说明符 `:?` 放在花括号内，告诉 `println!` 我们要使用一种名为
`Debug` 的输出格式。`Debug` 特质让我们可以用对开发者有用的方式打印结构体，从而
在调试代码时看到它的值。

按此修改编译代码。糟糕！仍然会得到一个错误：

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

不过，编译器再次给出了一条有帮助的说明：

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust 确实包含打印调试信息的功能，但必须显式选择，才能让我们的结构体使用该功能。
为此，如示例 5-12 所示，我们要紧挨着结构体定义之前添加外部属性
`#[derive(Debug)]`。

<Listing number="5-12" file-name="src/main.rs" caption="添加派生 `Debug` 特质的属性，并使用调试格式打印 `Rectangle` 实例">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

现在运行程序不会得到任何错误，并会看到下面的输出：

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

不错！虽然输出不算漂亮，但它显示了这个实例所有字段的值，这在调试时肯定很有
帮助。结构体较大时，更易读的输出会很有用；这时可以使用 `{:#?}`，而不是
`{:?}`，将其放在 `println!` 字符串中。在这个示例中，使用 `{:#?}` 样式会输出：

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

使用 `Debug` 格式打印值的另一种方式是使用[`dbg!`
宏][dbg]<!-- ignore -->。它会取得表达式的所有权（而 `println!` 取得的是引用），
打印代码中调用 `dbg!` 宏所在的文件和行号以及表达式的结果值，然后返回该值的所有权。

> 注意：调用 `dbg!` 宏会将输出打印到标准错误控制台流
>（`stderr`），而不是像 `println!` 那样打印到标准输出控制台流（`stdout`）。我们会在
> [第 12 章“将错误重定向到标准错误”一节][err]<!-- ignore -->中进一步讨论
> `stderr` 和 `stdout`。

下面是一个示例：我们既关注赋给 `width` 字段的值，也关注 `rect1` 中整个结构体的值：

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

我们可以将 `dbg!` 放在表达式 `30 * scale` 周围；由于 `dbg!` 会返回表达式值的所有权，
`width` 字段会得到与没有调用 `dbg!` 时相同的值。我们不希望 `dbg!` 取得 `rect1` 的
所有权，因此在下一次调用中对 `rect1` 使用引用。下面是这个示例的输出：

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

可以看到，第一部分输出来自 _src/main.rs_ 第 10 行，我们在那里调试表达式
`30 * scale`，其结果值为 `60`（为整数实现的 `Debug` 格式化只打印其值）。_src/main.rs_
第 14 行的 `dbg!` 调用输出 `&rect1` 的值，也就是 `Rectangle` 结构体。该输出使用
`Debug` 格式化的 `Rectangle` 类型。尝试弄清楚代码正在做什么时，`dbg!` 宏会非常有用！

除了 `Debug` 特质之外，Rust 还提供了许多可与 `derive` 属性一起使用的特质，为自定义
类型增加有用的行为。这些特质及其行为列在[附录 C][app-c]<!--
ignore -->中。我们将在第 10 章介绍如何以自定义行为实现这些特质，以及如何创建自己的
特质。除了 `derive` 之外还有许多其他属性；更多信息请参阅 Rust Reference 的
[“属性”一节][attributes]。

我们的 `area` 函数非常具体：它只计算矩形的面积。由于它不能用于其他类型，将这种
行为与 `Rectangle` 结构体更紧密地关联起来会很有帮助。接下来看看如何继续重构这段
代码，把 `area` 函数变成 `area` 方法，并将其定义在 `Rectangle` 类型上。

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
