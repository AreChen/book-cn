## 定义枚举

结构体提供了一种将相关字段和数据组合在一起的方式，例如一个 `Rectangle`，它有 `width` 和 `height`；而枚举提供了一种表达某个值属于一组可能值之一的方式。例如，我们可能想表达 `Rectangle` 是一组可能形状中的一种，这组形状还包括 `Circle` 和 `Triangle`。为此，Rust 允许我们将这些可能性编码为枚举。

让我们看看一种可能需要在代码中表达的情况，并了解为什么枚举在此处比结构体更有用、更合适。假设我们需要处理 IP 地址。目前，IP 地址使用两种主要标准：版本四和版本六。因为我们的程序遇到的 IP 地址只有这两种可能性，所以我们可以_枚举_所有可能的变体，这也是“枚举”一词得名的原因。

任何 IP 地址都可以是版本四地址或版本六地址，但不能同时是两者。IP 地址的这一属性使枚举数据结构很合适，因为一个枚举值只能是其变体中的一个。版本四和版本六地址在本质上仍然都是 IP 地址，因此当代码处理适用于任何类型 IP 地址的情况时，应将它们视为同一种类型。

我们可以通过定义 `IpAddrKind` 枚举并列出 IP 地址可能的类型（`V4` 和 `V6`）来用代码表达这个概念。这些是枚举的变体：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

现在，`IpAddrKind` 是一种自定义数据类型，我们可以在代码的其他地方使用它。

### 枚举值

我们可以像这样创建 `IpAddrKind` 两个变体的实例：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

请注意，枚举的变体位于其标识符的命名空间下，我们使用双冒号将两者分隔开。这很有用，因为现在 `IpAddrKind::V4` 和 `IpAddrKind::V6` 两个值的类型都是 `IpAddrKind`。于是，我们可以定义一个接收任意 `IpAddrKind` 的函数：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

然后，我们可以使用任一变体调用这个函数：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

使用枚举还有更多优点。进一步思考我们的 IP 地址类型：目前，我们没有办法存储实际的 IP 地址_数据_；我们只知道它属于哪种_类型_。鉴于你刚刚在第 5 章学习了结构体，你可能会想用结构体解决这个问题，如示例 6-1 所示。

<Listing number="6-1" caption="使用 `IpAddrKind` 变体存储 IP 地址数据的 `struct`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

这里，我们定义了一个 `IpAddr` 结构体，它有两个字段：`kind` 字段的类型为 `IpAddrKind`（我们之前定义的枚举），以及 `address` 字段，其类型为 `String`。我们有这个结构体的两个实例。第一个是 `home`，它的值是 `IpAddrKind::V4`，作为其 `kind`，并带有关联的地址数据 `127.0.0.1`。第二个实例是 `loopback`。它有 `IpAddrKind` 的另一个变体作为其 `kind` 值，即 `V6`，并且关联了地址 `::1`。我们使用结构体将 `kind` 和 `address` 值绑定在一起，因此现在变体与值相关联。

不过，只使用枚举来表示同一概念会更简洁：我们不必在结构体中嵌套枚举，而是可以直接将数据放入每个枚举变体中。这个新的 `IpAddr` 枚举定义表示，`V4` 和 `V6` 变体都将关联 `String` 值：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

我们直接将数据附加到枚举的每个变体上，因此不需要额外的结构体。在这里，也更容易看出枚举工作方式的另一个细节：我们定义的每个枚举变体的名称也会成为一个用于构造该枚举实例的函数。也就是说，`IpAddr::V4()` 是一个函数调用，它接收 `String` 参数并返回 `IpAddr` 类型的实例。定义枚举后，我们会自动获得这个构造函数。

与结构体相比，使用枚举还有另一个优点：每个变体可以拥有不同类型和数量的关联数据。版本四 IP 地址始终有四个数值组件，其值在 0 到 255 之间。如果我们想将 `V4` 地址存储为四个 `u8` 值，同时仍将 `V6` 地址表示为一个 `String` 值，那么使用结构体无法做到这一点。枚举可以轻松处理这种情况：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

我们展示了几种定义数据结构以存储版本四和版本六 IP 地址的不同方式。不过，事实证明，想要存储 IP 地址并编码其类型非常常见，因此[标准库已经提供了一个可供我们使用的定义！][IpAddr]<!-- ignore -->。我们来看看标准库如何定义 `IpAddr`。它具有我们定义并使用过的完全相同的枚举及其变体，但将地址数据嵌入变体内部，形式是两个不同的结构体，每个变体的定义都不同：

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

这段代码说明，你可以将任何类型的数据放入枚举变体中，例如字符串、数值类型或结构体。你甚至可以包含另一个枚举！此外，标准库类型通常并不会比你自己可能设计出的类型复杂多少。

请注意，尽管标准库包含 `IpAddr` 的定义，我们仍然可以创建和使用自己的定义而不会冲突，因为我们没有将标准库的定义引入当前作用域。我们将在第 7 章更详细地讨论如何将类型引入作用域。

让我们看看示例 6-2 中的另一个枚举：它的变体中嵌入了各种各样的类型。

<Listing number="6-2" caption="一种 `Message` 枚举，其变体分别存储不同数量和类型的值">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

这个枚举有四个不同类型的变体：

- `Quit`：完全不关联任何数据
- `Move`：包含像结构体一样的命名字段
- `Write`：包含一个 `String`
- `ChangeColor`：包含三个 `i32` 值

定义一个具有示例 6-2 中这类变体的枚举，类似于定义不同类型的结构体，只是枚举不使用 `struct` 关键字，并且所有变体都归在 `Message` 类型下。下面的结构体可以保存前面枚举变体所保存的相同数据：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

但是，如果我们使用这些不同的结构体，由于每个结构体都有自己的类型，我们就无法像使用示例 6-2 中定义的 `Message` 枚举那样，轻松定义一个接收这些类型消息中任意一种的函数；而该枚举只有一种类型。

枚举和结构体还有一个相似之处：正如我们可以使用 `impl` 为结构体定义方法一样，也可以为枚举定义方法。下面是一个名为 `call` 的方法，我们可以在 `Message` 枚举上定义：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

方法体会使用 `self` 获取调用该方法的值。在这个例子中，我们创建了一个变量 `m`，其值为 `Message::Write(String::from("hello"))`，而这个值就是 `self`，位于 `call` 方法的主体中；当运行 `m.call()` 时也是如此。

让我们看看标准库中的另一个非常常见且有用的枚举：`Option`。

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### `Option` 枚举

本节将研究 `Option` 这一案例，它是标准库定义的另一个枚举。`Option` 类型编码了一种非常常见的情况：一个值可能有内容，也可能什么都没有。

例如，如果你请求一个非空列表中的第一项，就会得到一个值。如果你请求一个空列表中的第一项，就什么也得不到。用类型系统来表达这个概念意味着编译器可以检查你是否处理了应该处理的所有情况；这一功能可以防止其他编程语言中极其常见的错误。

编程语言设计通常会考虑包含哪些特性，但排除哪些特性也同样重要。Rust 没有许多其他语言拥有的空值特性。_空值_是一种表示那里没有值的值。在拥有空值的语言中，变量总是处于两种状态之一：空值或非空值。

在 2009 年的演讲《空引用：价值十亿美元的错误》中，空值的发明者 Tony Hoare 曾这样说：

> 我称之为我价值十亿美元的错误。当时，我正在为一种面向对象语言中的引用设计第一个完整的类型系统。我的目标是确保所有引用的使用都绝对安全，并由编译器自动执行检查。但我抵挡不住加入空引用的诱惑，仅仅因为它太容易实现了。这导致了无数错误、漏洞和系统崩溃，而在过去四十年中，这些问题可能造成了价值十亿美元的痛苦和损失。

空值的问题在于，如果你试图将空值当作非空值使用，就会以某种方式得到错误。由于这种空值或非空值的属性无处不在，因此极易犯下这类错误。

不过，空值试图表达的概念仍然很有用：空值是一个由于某种原因当前无效或缺失的值。

问题并不在这个概念本身，而在于具体的实现。因此，Rust 没有空值，但有一个可以编码值存在或缺失这一概念的枚举。这个枚举是 `Option<T>`，它由[标准库定义][option]<!-- ignore -->，如下所示：

```rust
enum Option<T> {
    None,
    Some(T),
}
```

`Option<T>` 枚举非常有用，甚至被包含在前奏中；你无需显式将其引入作用域。它的变体也包含在前奏中：你可以直接使用 `Some` 和 `None`，而无需 `Option::` 前缀。`Option<T>` 枚举仍然只是一个普通枚举，而 `Some(T)` 和 `None` 仍然是 `Option<T>` 类型的变体。

`<T>` 语法是 Rust 的一个特性，我们还没有讨论过。它是一个泛型类型参数，我们将在第 10 章更详细地介绍泛型。目前，你只需知道，`<T>` 表示 `Some` 变体（属于 `Option` 枚举）可以容纳任意类型的一项数据，并且用来替代 `T` 的每个具体类型都会让整体的 `Option<T>` 类型成为不同的类型。下面是一些使用 `Option` 值保存数字类型和字符类型的示例：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

`some_number` 的类型是 `Option<i32>`。`some_char` 的类型是 `Option<char>`，这是一个不同的类型。Rust 可以推断出这些类型，因为我们在 `Some` 变体中指定了一个值。对于 `absent_number`，Rust 要求我们标注整体的 `Option` 类型：编译器仅凭 `Some` 值无法推断相应的 `None` 变体将保存的类型。在这里，我们告诉 Rust，`absent_number` 的类型应为 `Option<i32>`。

当我们有一个 `Some` 值时，就知道有一个值存在，而该值保存在 `Some` 中。当我们有一个 `None` 值时，从某种意义上说，它与空值含义相同：我们没有有效值。那么，拥有 `Option<T>` 为什么比拥有空值更好呢？

简而言之，这是因为 `Option<T>` 和 `T`（其中 `T` 可以是任何类型）是不同的类型，编译器不会允许我们把 `Option<T>` 值当作确定有效的值来使用。例如，下面的代码无法编译，因为它试图将一个 `i8` 加到 `Option<i8>` 上：

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

如果我们运行这段代码，就会得到类似下面这样的错误消息：

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

这很严格！实际上，这条错误消息意味着，Rust 不知道如何将 `i8` 和 `Option<i8>` 相加，因为它们是不同的类型。当我们在 Rust 中拥有一个 `i8` 之类类型的值时，编译器会确保我们始终拥有有效值。我们可以放心继续使用它，而不必在使用该值之前检查空值。只有当我们拥有 `Option<i8>`（或者我们正在处理的其他类型的值）时，才需要担心可能没有值，而编译器会确保我们在使用该值之前处理这种情况。

换句话说，必须先将 `Option<T>` 转换为 `T`，之后才能对它执行 `T` 操作。通常，这有助于捕获与空值相关的最常见问题之一：假设某个东西不是空值，而实际上是空值。

消除错误地假定值非空的风险，会让你对代码更有信心。为了拥有一个可能为空的值，你必须明确选择将该值的类型设为 `Option<T>`。然后，在使用该值时，你必须显式处理该值为空的情况。凡是值的类型不是 `Option<T>` 的地方，你都可以安全地假定该值不为空。这是 Rust 有意采取的设计决策，用于限制空值的普遍存在并提高 Rust 代码的安全性。

那么，如何取出 `T` 值，并在拥有一个 `Some` 变体（其枚举类型为 `Option<T>`）时使用它呢？`Option<T>` 枚举提供了大量在各种场景中都很有用的方法；你可以在[它的文档][docs]<!-- ignore -->中查看这些方法。熟悉 `Option<T>` 的方法将会对你在 Rust 中的学习之旅非常有用。

通常，为了使用一个 `Option<T>` 值，你需要编写能够处理每个变体的代码。你需要一些仅在拥有 `Some(T)` 值时运行的代码，并且这段代码可以使用内部的 `T`。你还需要另一段仅在拥有 `None` 值时运行的代码，而那段代码没有可用的 `T` 值。与枚举一起使用时，`match` 表达式正好就是这样一种控制流结构：它会根据所处理的枚举变体运行不同的代码，而这些代码可以使用匹配值中的数据。

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
