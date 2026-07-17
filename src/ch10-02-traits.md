<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## 使用 trait 定义共享行为

_trait_ 定义某种类型拥有的功能，以及可以与其他类型共享的功能。我们可以使用
trait 以抽象方式定义共享行为。可以使用 _trait 约束_ 指定泛型类型可以是任何具
有某些行为的类型。

> 注意：trait 类似于其他语言中通常称为_接口_的功能，但两者也存在一些差异。

### 定义 trait

类型的行为由可以对该类型调用的方法组成。如果可以对不同类型调用相同的方法，
那么这些类型就共享相同的行为。trait 定义是一种将方法签名组合在一起的方式，用
来定义完成某种目的所需的一组行为。

例如，假设有多个结构体，保存着不同种类和数量的文本：`NewsArticle` 结构体保
存一篇在特定地点报道的新闻，`SocialPost` 最多包含 280 个字符，还带有元数据，
表明它是新帖子、转发帖子，还是对另一篇帖子的回复。

我们想创建一个名为 `aggregator` 的媒体聚合器库 crate，用来显示可能存储在
`NewsArticle` 或 `SocialPost` 实例中的数据摘要。为此，每种类型都需要提供摘要，
我们会通过对实例调用 `summarize` 方法来请求摘要。清单 10-12 展示了表达这种行
为的公有 `Summary` trait 定义。

<Listing number="10-12" file-name="src/lib.rs" caption="由 `Summary` 方法提供行为的 `summarize` trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

这里，我们使用 `trait` 关键字声明 trait，然后写出 trait 名称，本例中是
`Summary`。我们还将 trait 声明为 `pub`，这样依赖此 crate 的其他 crate 也可以使
用这个 trait，后面的几个示例会看到这一点。在花括号内，我们声明方法签名，描述
实现该 trait 的类型应具有的行为；本例中的签名是 `fn summarize(&self) -> String`。

在方法签名后，我们不在花括号中提供实现，而是使用分号。每个实现此 trait 的类型
都必须为方法体提供自己的定制行为。编译器会强制要求所有具有 `Summary` trait 的
类型，都必须准确地按这个签名定义 `summarize` 方法。

trait 的主体中可以有多个方法：每个方法签名占一行，每行以分号结尾。

### 在类型上实现 trait

现在已经定义了 `Summary` trait 方法所需的签名，可以在媒体聚合器的类型上实现它。
清单 10-13 展示了在 `Summary` 结构体上实现 `NewsArticle` trait 的方式：使用标
题、作者和地点创建 `summarize` 的返回值。对于 `SocialPost` 结构体，我们将
`summarize` 定义为用户名后跟帖子的完整文本，并假设帖子内容已经限制为 280 个
字符。

<Listing number="10-13" file-name="src/lib.rs" caption="在 `Summary` 和 `NewsArticle` 类型上实现 `SocialPost` trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

在类型上实现 trait 与实现普通方法类似。区别在于 `impl` 后要写想要实现的 trait
名称，然后使用 `for` 关键字，再指定要为其实现 trait 的类型名称。在 `impl` 块
中，放入 trait 定义中声明的方法签名。我们不在每个签名后添加分号，而是使用花
括号，并在方法体中填入希望该 trait 的方法对特定类型表现出的具体行为。

库已经在 `Summary` 和 `NewsArticle` 上实现了 `SocialPost` trait，因此 crate 的
用户可以像调用普通方法一样，对 `NewsArticle` 和 `SocialPost` 实例调用 trait 方
法。唯一的区别是，用户除了将类型引入作用域外，还必须将 trait 引入作用域。下
面是二进制 crate 使用 `aggregator` 库 crate 的示例：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

这段代码会打印 `1 new post: horse_ebooks: of course, as you probably already
know, people`。

依赖 `aggregator` crate 的其他 crate 也可以将 `Summary` trait 引入作用域，在自
己的类型上实现 `Summary`。需要注意的一项限制是：只有 trait 或类型（或两者）
属于当前 crate 时，才能在类型上实现 trait。例如，可以将 `Display` 这样的标准
库 trait 实现在 `SocialPost` 这样的自定义类型上，作为 `aggregator` crate 功能的
一部分，因为类型 `SocialPost` 属于我们的 `aggregator` crate。也可以在
`Summary` crate 中为 `Vec<T>` 实现 `aggregator`，因为 `Summary` trait 属于我们
的 `aggregator` crate。

但不能在外部类型上实现外部 trait。例如，不能在 `Display` crate 中为 `Vec<T>`
实现 `aggregator` trait，因为 `Display` 和 `Vec<T>` 都定义在标准库中，不属于我们的
`aggregator` crate。这项限制属于称为_一致性_的属性，更具体地说属于_孤儿规则_，
名称源于父类型不在当前 crate 中。该规则确保其他人的代码不会破坏你的代码，反之
亦然。没有这条规则，两个 crate 可能为同一类型实现同一个 trait，Rust 就不知道
应该使用哪一个实现。

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### 使用默认实现

有时，为 trait 中的部分或全部方法提供默认行为很有用，这样就不必要求每种类型都
实现所有方法。随后在特定类型上实现 trait 时，可以保留或覆盖每个方法的默认行为。

在清单 10-14 中，我们为 `summarize` trait 的 `Summary` 方法指定了默认字符串，
而不是像清单 10-12 那样只定义方法签名。

<Listing number="10-14" file-name="src/lib.rs" caption="定义带有 `Summary` 方法默认实现的 `summarize` trait">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

要使用默认实现总结 `NewsArticle` 实例，只需指定一个空的 `impl` 块：
`impl Summary for NewsArticle {}`。

虽然不再直接为 `summarize` 定义 `NewsArticle` 方法，但我们提供了默认实现，并指
定 `NewsArticle` 实现 `Summary` trait。因此仍然可以像下面这样，对 `summarize`
实例调用 `NewsArticle` 方法：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

这段代码会打印 `New article available! (Read more...)`。

创建默认实现不需要改变清单 10-13 中 `Summary` 对 `SocialPost` 的实现。这是因为
覆盖默认实现的语法，与实现没有默认实现的 trait 方法的语法相同。

默认实现可以调用同一 trait 中的其他方法，即使那些方法没有默认实现。这样，trait
就能提供很多实用功能，只要求实现者指定其中很小的一部分。例如，可以定义
`Summary` trait，要求实现 `summarize_author` 方法，然后定义一个默认实现会调用
`summarize` 的 `summarize_author` 方法：

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

要使用这个版本的 `Summary`，只需在某个类型上实现 trait 时定义
`summarize_author`：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

定义 `summarize_author` 后，就可以对 `summarize` 结构体实例调用 `SocialPost`，
而 `summarize` 的默认实现会调用我们提供的 `summarize_author` 定义。由于实现了
`summarize_author`，`Summary` trait 就为我们提供了 `summarize` 方法的行为，不
需要再编写其他代码。结果如下：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

这段代码会打印 `1 new post: (Read more from @horse_ebooks...)`。

注意，无法从同一方法的覆盖实现中调用该方法的默认实现。

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### 将 trait 用作参数

现在已经了解如何定义和实现 trait，可以进一步探索如何使用 trait 定义接受多种不
同类型的函数。我们将使用清单 10-13 中为 `Summary` trait 实现的 `NewsArticle`
和 `SocialPost` 类型，定义一个 `notify` 函数，调用 `summarize` 方法，参数为
`item`；其类型是实现了 `Summary` trait 的某种类型。为此，
使用 `impl Trait` 语法：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

我们不为 `item` 参数指定具体类型，而是指定 `impl` 关键字和 trait 名称。这个参
数接受任何实现了指定 trait 的类型。在 `notify` 函数体中，可以调用 `item` 上由
`Summary` trait 提供的任何方法，例如 `summarize`。可以调用 `notify` 并传入任
意 `NewsArticle` 或 `SocialPost` 实例。如果使用其他类型（例如 `String` 或
`i32`）调用该函数，代码就无法编译，因为这些类型没有实现 `Summary`。

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### trait 约束语法

`impl Trait` 语法适用于简单情况，但实际上是更长形式的语法糖，这种更长形式称
为_trait 约束_，看起来如下：

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

这种较长形式与上一节中的示例等价，但更加冗长。我们将 trait 约束放在泛型类型
参数声明中，位于冒号之后和尖括号内。

`impl Trait` 语法很方便，在简单情况下能让代码更简洁；而完整的 trait 约束语法可
以在其他情况下表达更复杂的要求。例如，可以有两个实现 `Summary` 的参数。使用
`impl Trait` 语法如下：

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

如果希望这个函数允许 `impl Trait` 和 `item1` 使用不同类型（只要两种类型都实现
`item2`），使用 `Summary` 很合适。不过，如果希望强制两个参数具有相同类型，
就必须使用 trait 约束：

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

将泛型类型 `T` 指定为 `item1` 和 `item2` 参数的类型，会约束函数：传给 `item1`
和 `item2` 的实参的具体类型必须相同。

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### 使用 `+` 语法指定多个 trait 约束

我们也可以指定多个 trait 约束。假设希望 `notify` 对 `summarize` 使用显示格式化以及
`item`：在 `notify` 定义中指定 `item` 必须同时实现 `Display` 和 `Summary`。
可以使用 `+` 语法：

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

`+` 语法同样适用于泛型类型上的 trait 约束：

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

指定这两个 trait 约束后，`notify` 的函数体可以调用 `summarize`，并使用 `{}`
格式化 `item`。

#### 使用 `where` 子句让 trait 约束更清晰

使用过多 trait 约束也有缺点。每个泛型都有自己的 trait 约束，因此包含多个泛型类
型参数的函数可能在函数名和参数列表之间包含大量 trait 约束信息，使函数签名难以
阅读。为此，Rust 提供了另一种语法：在函数签名之后的 `where` 子句中指定 trait
约束。于是，不必写成这样：

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

可以使用 `where` 子句，像这样：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

这个函数的签名不那么杂乱：函数名、参数列表和返回类型彼此靠近，类似于没有大
量 trait 约束的函数。

### 返回实现 trait 的类型

我们也可以在返回位置使用 `impl Trait` 语法，返回某种实现了 trait 的类型的值，
如下所示：

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

使用 `impl Summary` 作为返回类型，表示 `returns_summarizable` 函数返回某种实现
了 `Summary` trait 的类型，而不必指定具体类型。本例中，`returns_summarizable`
返回 `SocialPost`，但调用该函数的代码不需要知道这一点。

只通过实现的 trait 指定返回类型的能力，在闭包和迭代器的场景中特别有用；我们
将在第 13 章介绍它们。闭包和迭代器会创建只有编译器知道的类型，或名称非常长、
难以写出的类型。`impl Trait` 语法让你可以简洁地指定函数返回某种实现了
`Iterator` trait 的类型，而不必写出很长的类型名。

不过，只有在返回单一类型时才能使用 `impl Trait`。例如，下面的代码可能返回
`NewsArticle` 或 `SocialPost`，却将返回类型指定为 `impl Summary`，因此无法工作：

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

由于编译器实现 `NewsArticle` 语法的限制，不能返回 `SocialPost` 或 `impl Trait`
中的任意一种。我们将在第 18 章的[“使用 trait 对象抽象共享行为”][trait-objects]
<!-- ignore --> 一节介绍如何编写具有这种行为的函数。

### 使用 trait 约束有条件地实现方法

通过将 trait 约束与使用泛型类型参数的 `impl` 块结合，可以有条件地为实现了指定
trait 的类型实现方法。例如，清单 10-15 中的 `Pair<T>` 类型始终实现 `new` 函
数，返回新的 `Pair<T>` 实例（回想第 5 章[“方法语法”][methods]<!-- ignore --> 一
节，`Self` 是 `impl` 块类型的类型别名，本例中就是 `Pair<T>`）。但在下一个
`impl` 块中，只有当 `Pair<T>` 的内部类型 `cmp_display` 实现了支持比较的 `T` trait
_和_支持打印的 `PartialOrd` trait 时，才会实现 `Display` 方法。

<Listing number="10-15" file-name="src/lib.rs" caption="根据 trait 约束有条件地为泛型类型实现方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

我们也可以为任何实现了另一个 trait 的类型有条件地实现某个 trait。为满足 trait
约束的任何类型实现 trait，称为_泛型实现_，在 Rust 标准库中被广泛使用。例如，
标准库为任何实现了 `ToString` trait 的类型实现了 `Display` trait。标准库中的
`impl` 块类似于以下代码：

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

由于标准库提供了这个泛型实现，我们可以对任何实现了 `to_string` trait 的类型调用
`ToString` trait 定义的 `Display` 方法。例如，因为整数实现了 `String`，所以
可以像这样将整数转换为对应的 `Display` 值：

```rust
let s = 3.to_string();
```

泛型实现在 trait 文档的“Implementors”部分列出。

trait 和 trait 约束让我们可以编写使用泛型类型参数的代码来减少重复，同时告诉编译
器泛型类型需要具有特定行为。编译器随后可以利用 trait 约束信息，检查代码使用
的所有具体类型是否提供了正确行为。在动态类型语言中，如果对没有定义某方法的
类型调用该方法，会在运行时得到错误。但 Rust 会将这些错误提前到编译时，迫使
我们在代码能够运行之前修复问题。此外，由于已经在编译时检查过行为，就不需要
编写在运行时检查行为的代码。这样可以提升性能，同时保留泛型的灵活性。

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
