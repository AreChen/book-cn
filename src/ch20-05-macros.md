## 宏，macro

在这本书中，我们一直使用像 `println!` 这样的宏，但尚未全面探讨什么是宏，以及他的工作原理。 *宏，macro* 这个术语，指的是 Rust 中的一类特性 -- 通过 `macro_rules!` 的 *声明式宏，declarative macro*，以及如下三种 *程序式宏，procedural macro*：

- 自定义的 `#[derive]` 宏，他们通过 `derive` 属性，对结构体和枚举指定添加的代码（译注：这类似于 Python 中的 @ 装饰语法）；
- 类属性的宏，定义可用于任何项目的自定义属性；
- 类函数的宏，看起来像函数调用，但对指定为其参数的标记（程序项目）执行操作。

我们将依次讨论其中的每一种，但首先，我们来看看既然有了函数，为什么我们还需要宏。

### 宏与函数的区别

从根本上说，宏属于一种编写生成其他代码的代码的方式，这被称为 *元编程，metaprogramming*。在 [附录 C] 中，我们会讨论 `derive` 属性，其会为咱们生成各种特质的实现。在这本书的各处，我们也已使用了 `println!` 与 `vec!` 两个宏。所有这些宏都会 *展开，expand*，从而生成比咱们手写的代码更多的代码。

元编程对于减少咱们必须编写和维护代码量很有用，这也是函数的作用之一。但是，宏有着函数不具备的一些额外能力。

函数签名必须声明函数具有的参数个数和类型。另一方面，宏可以取可变数量的参数：我们可以以一个参数调用 `println!("hello")`，也可以以两个参数调用 `println!("hello {}", name)`。此外，宏会在编译器解析代码含义之前得以展开，因此宏就可以，比如对给定类型实现特质。函数则无法做到这点，因为函数是在运行时被调用的，而特质需要在编译时实现。

实现宏而非函数的缺点在于，宏的定义比函数的定义更为复杂，因为咱们要编写生成 Rust 代码的 Rust 代码。由于这种间接性，宏的定义通常比函数的定义更难阅读、理解和维护。

宏与函数之间的另一重要区别在于，在文件中调用宏 *之前*，咱们必须先定义宏或带入他们到作用域，这与咱们可以在任何地方定义和调用任何地方的函数相反。

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### 用于通用元编程的声明式宏

Rust 中使用最广泛的宏形式属于 **声明式宏，declarative macro**。这些宏有时也被称为 `macro_rules!` `match` `match`
为了定义宏，咱们要使用 `macro_rules!` 结构体。我们通过分析 `macro_rules!` 宏的定义方式，来了解怎样使用 `vec!`。第 8 章介绍了怎样使用 `vec!` 宏创建带有特定值的新矢量值。例如，以下宏会创建一个包含三个整数的新矢量值：

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

我们也可以使用 `vec!` 宏构造一个包含两个整数的矢量值，或者一个包含五个字符串切片的矢量值。我们无法使用函数来执行同样的操作，因为我们事先不知道值的数量或类型。

下面清单 20-35 展示了 `vec!` 宏的略微简化的定义。

<Listing number="20-35" file-name="src/lib.rs" caption="`vec!` 宏定义的简化版本">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> **注意**：标准库中 `vec!` 宏的实际定义，包含了预先分配正确数量内存的代码。该代码属于一种优化，为了使示例更简单，我们没有包含该代码。

其中 `#[macro_export]` 注解表明，只要定义该宏的代码箱被带入作用域，那么这个宏就应可用。若没有这个注解，该宏就无法被带入作用域。

然后我们以 `macro_rules!` 以及 *不带* 感叹号的我们正在定义的宏的名字，来开始宏的定义。在这一情形下名字即为 `vec`，后跟表示宏定义主体的花括号。

其中 `vec!` 注解表明，只要定义该宏的代码箱被带入作用域，那么这个宏就应可用。若没有这个注解，该宏就无法被带入作用域。 `match` `( $( $x:expr ),* )` `=>`
当模式匹配时，关联代码块将得以生成。鉴于这是这个宏中唯一的模式，因此只有一种有效的匹配方式；任何其他模式都将导致报错。更复杂的宏将有着多个支臂。

首选，我们使用一对圆括号来环绕整个模式。我们使用美元符号（`$`）声明宏系统中的一个变量，该变量将包含匹配模式的 Rust 代码。美元符号清楚地表明这是个宏变量，而非普通 Rust 变量。接下来的一对圆括号，捕获匹配其内模式的值，供替换代码中使用。在 `$()` 内的是 `$x:expr`，这会匹配任意 Rust 表达式，并给予表达式名字 `$x`。

`$()` 后的逗号表示，在匹配 `$()` 中代码的每个代码实例之间必须出现一个字面上的逗号分隔符。随后的 `*` 指定该模式会匹配 `*` 之前的内容零次或多次（译注：这一点与正则表达式类似）。

当我们通过 `vec![1, 2, 3];` 调用这个宏时，`$x` 模式会与三个表达式 `1`、`2` 和 `3` 匹配三次。

现在我们来看看与这个支臂关联的代码主体中的模式：`temp_vec.push()` 内的 `$()*` 会针对匹配模式中的 `$()` 每个部分，而生成零次或多次，具体取决于该模式匹配的次数。其中 `$x` 以每个匹配的表达式替换。当我们以 `vec![1, 2, 3];` 调用这个宏时，生成的替换这次宏调用的代码将如下：

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

我们定义了一个宏，他可以取任意数量、任意类型的参数，并且可以生成代码来创建一个包含指定元素的矢量。

要了解有关如何编写宏的更多信息，请查阅在线文档或其他资源，比如由 Daniel Keep 撰写，Lukas Wirth 接续编写的 [The Little Book of Rust Macros]。

### 用于根据属性生成代码的过程宏

- 自定义的 `derive` 宏、
- 类属性宏，attribute-like macros、
- 及类函数宏，function-like macros。

在创建过程宏时，其定义必须位于一个有着特殊代码箱类型的他们自己的代码箱中。这是出于一些复杂的技术原因，我们（Rust 开发团队）希望今后能消除这些原因。在下面清单 20-36 中，我们展示了怎样定义一个过程宏，其中 `some_attribute` 是使用特定宏变种的占位符。

<Listing number="20-36" file-name="src/lib.rs" caption="定义过程宏的示例">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

定义过程宏的函数，会取一个 `TokenStream` 值作为输入，并生成一个 `TokenStream` 作为输出。`TokenStream` 类型由 Rust 附带的 `proc_macro` 代码箱定义，表示令牌序列，a sequence of tokens。这是这种宏的核心：宏所操作的源代码构成输入的 `TokenStream`，而宏生成的代码则是输出的 `TokenStream`。该函数附带了一个属性，指定我们正在创建何种类别的过程宏。我们可以在同一个代码箱中包含多种类别的过程宏。

我们来看看不同类别的过程宏。我们将从自定义 `derive` 宏开始，然后探讨使其他形式有所不同的细微差异。

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### 自定义 `derive` 宏

我们来创建一个名为 `hello_macro` 的代码箱，他通过一个名为 `HelloMacro` 的关联函数，定义了个名为 `hello_macro` 的特质。与其让用户为他们的每个类型都实现 `HelloMacro` 特质，我们提供一个过程宏，以便用户可以通过 `#[derive(HelloMacro)]` 来注解他们的类型，以获得 `hello_macro` 函数的默认实现。默认实现将打印 `Hello, Macro! My name is
TypeName!`，其中的 `TypeName` 是该特质被定义所在的类型的名字。换句话说，我们将编写一个代码箱，使其他程序员能够编写如下清单 20-37 中的代码。

<Listing number="20-37" file-name="src/main.rs" caption="我们的代码箱用户在使用我们的过程宏时，将能够编写的代码">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

当我们完成时，这段代码将打印 `Hello, Macro! My name is Pancakes!`。第一步是构造一个新的库代码箱，如下所示：

```console
$ cargo new hello_macro --lib
```

接下来，在清单 20-38 中，我们将定义 `HelloMacro` 特质及其关联函数。

<Listing file-name="src/lib.rs" number="20-38" caption="一个我们将与 `derive` 宏一起使用的简单特质">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

我们有一个特质及其函数。此时，我们的代码箱用户可以实现这个特质，以实现所需的功能，如下清单 20-39 中所示。

<Listing number="20-39" file-name="src/main.rs" caption="当用户编写 `HelloMacro` 特质的手动实现时，会是什么样子">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

然而，他们需要针对他们打算与 `hello_macro` 一起使用的每种类型，都编写实现代码块；我们希望省去他们这部分工作。

此外，我们还无法为 `hello_macro` 函数提供将打印对其实现该特质的类型的名字的默认实现：Rust 不具备反射能力，因此无法在运行时查找类型的名字。我们需要一个宏在编译时生成代码。

下一步是定义过程宏。在撰写本文时，过程宏需要位于自己的代码箱中。最终，这一限制可能会被取消。组织代码箱和组织宏代码箱方面的约定如下：对于名为 `foo` 的代码箱，则自定义的 `derive` 过程宏代码箱应名为 `foo_derive`。我们来在 `hello_macro_derive` 项目内，启动一个名为 `hello_macro` 的新代码箱：

```console
$ cargo new hello_macro_derive --lib
```

这两个代码箱紧密相关，因此我们在 `hello_macro` 代码箱目录下创建这个过程宏代码箱。当我们修改 `hello_macro` 中的特质定义时，也必须修改 `hello_macro_derive` 中的过程宏。这两个代码箱需要单独发布，而使用这两个代码箱的程序员则需要添加他们为依赖项，并带入他们到作用域。我们也可以让 `hello_macro` 代码箱作为依赖项使用 `hello_macro_derive`，并重新导出过程宏的代码。然而，我们组织项目的方式，让程序员即使不想要 `hello_macro` 的功能，也可以使用 `derive`。

我们需要声明 `hello_macro_derive` 代码箱为一个过程宏的代码箱。稍后咱们就会看到，我们还需要 `syn` 和 `quote` 代码箱中的功能，因此我们需要添加他们为依赖。请添加以下内容到 `hello_macro_derive` 的 Cargo.toml 文件：

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

这样做让编写过程宏更加方便。外层函数（这一情形下的 `hello_macro_derive` ）中的这种代码，对于咱们所见或创建的几乎所有过程宏代码箱，都将是相同的。而咱们在内层函数（这一情形下的 `impl_hello_macro`）的主体指定的代码，将根据过程宏的用途而有所不同。

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="大多数过程宏代码箱为了处理 Rust 代码都需要的代码">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

当我们的库用于在某种类型上指定 `hello_macro_derive` 时，`TokenStream` 函数就会被调用。这样做之所以可行，是因为我们在这里以 `impl_hello_macro` 注解了 `hello_macro_derive` 函数，并指定了名字 `impl_hello_macro`，其与我们的特质名字匹配；这是大多数过程宏遵循的约定。

我们引入了三个新的代码箱：`proc_macro`、[`syn`][syn]<!-- ignore --> 和
[`quote`][quote]<!-- ignore -->。`proc_macro` 代码箱随 Rust 一起提供，因此不需要
将它添加到 _Cargo.toml_ 的依赖中。`proc_macro` 代码箱是编译器提供的 API，允许我们
从自己的代码读取和操作 Rust 代码。
`syn` 函数首选会将 input 从 TokenStream 转换为一种数据结构，我们随后对其解析并执行操作。这是 `quote` 发挥作用的地方。`syn` 中的 parse 函数会取一个 TokenStream 并返回一个 DeriveInput 结构体，解析后的 Rust 代码。下面清单 20-41 展示了我们从解析 struct Pancakes; 字符串，得到的 DeriveInput 结构体的相关部分。

咱们可能已经注意到，我们调用了 `hello_macro_derive`，以在这里的 `#[derive(HelloMacro)]` 函数调用失败时，引起 `hello_macro_derive` 函数终止运行。我们的过程宏有必要在出现错误时终止运行，因为 `proc_macro_derive` 函数必须返回 `HelloMacro` 而不是 Result，以符合过程宏 API。我们通过使用 unwrap 简化了这个示例；在生产代码中，咱们应该通过使用 panic! 或 expect，提供有关出错原因的更具体的错误消息。

这样做让编写过程宏更加方便。外层函数（这一情形下的 `hello_macro_derive` ）中的这种代码，对于咱们所见或创建的几乎所有过程宏代码箱，都将是相同的。而咱们在内层函数（这一情形下的 `input`）的主体指定的代码，将根据过程宏的用途而有所不同。 `TokenStream` `syn` `parse` `syn` `TokenStream` `DeriveInput` `DeriveInput` `struct Pancakes;`

<Listing number="20-41" caption="我们在解析有着清单 20-37 中宏属性的代码时，得到的 `DeriveInput` 实例">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

我们使用 `ident` 得到一个 `Pancakes` 结构体实例，包含被注解类型的名字（标识符）。清单 20-41 中的结构体表明，当我们对清单 20-37 中的代码运行 `syn` 函数时，我们得到的 `DeriveInput` 就将有着值为 "Pancakes" 的 ident 字段。因此，清单 20-42 中的 name 变量将包含一个 Ident 结构体实例，其在打印出时将是字符串 "Pancakes"，即清单 20-37 中结构体的名字。

其中 `impl_hello_macro` 宏让我们可以定义打算返回的 Rust 代码。编译器期望的类型与 `derive` 宏执行的直接结果不同，因此我们需要将其转换为 `TokenStream`。我们通过调用 `TokenStream` 方法完成这一操作，其会消费中间表示形式，并返回所需的 `TokenStream` 类型的值。

`unwrap` 代码箱是 Rust 默认自带的，因此我们无需添加他到 `hello_macro_derive` 中的依赖项。`syn::parse` 代码箱属于编译器的 API，允许我们在代码中读取和操作 Rust 代码。 `proc_macro_derive` `TokenStream` `Result` `unwrap` `panic!` `expect`
类函数的宏定义了看起来像函数调用的宏。与 `TokenStream` 宏类似，他们比函数更为灵活；例如，他们可以取未知数量的参数。然而，`DeriveInput` 的宏只能使用我们在 [用于通用元编程的声明式宏] 小节中讨论过的类似匹配的语法来定义。而类函数的宏会取一个 `HelloMacro` 参数，并且他们的定义会像其他两种过程宏一样，使用 Rust 代码来操作该 TokenStream。类函数宏的一个示例为 sql! 宏，其可以被如下调用：

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="使用解析后的 Rust 代码实现 `HelloMacro` 特质">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

当我们的库用于在某种类型上指定 `Ident` 时，`ast.ident` 函数就会被调用。这样做之所以可行，是因为我们在这里以 `impl_hello_macro` 注解了 `ident` 函数，并指定了名字 `ident`，其与我们的特质名字匹配；这是大多数过程宏遵循的约定。 `"Pancakes"` `name` `Ident` `"Pancakes"`
`quote!` 函数首选会将 `quote!` 从 `TokenStream` 转换为一种数据结构，我们随后对其解析并执行操作。这是 `into` 发挥作用的地方。`TokenStream` 中的 parse 函数会取一个 TokenStream 并返回一个 DeriveInput 结构体，解析后的 Rust 代码。下面清单 20-41 展示了我们从解析 struct Pancakes; 字符串，得到的 DeriveInput 结构体的相关部分。
`quote!` 宏还提供了非常灵活的模板机制：我们可以写入 `#name`，`quote!` 会将其替换为变量 `name` 中的值。你甚至可以像普通宏那样进行重复操作。若想深入了解，请参阅 [`quote` 箱的文档][quote-docs]。
很快我们将定义 `HelloMacro` 函数，其中我们将构建想要包含的新 Rust 代码。但在我们开始之前，请注意 `#name` 宏的输出也是个 `hello_macro`。返回的 `Hello, Macro! My name is` 会被添加到我们的代码箱用户编写的代码中，因此当他们编译自己的代码箱时，他们将获得咱们在修改后的 TokenStream 中提供的额外功能。
咱们可能已经注意到，我们调用了 `stringify!`，以在这里的 `1 + 2` 函数调用失败时，引起 `"1 + 2"` 函数终止运行。我们的过程宏有必要在出现错误时终止运行，因为 `format!` 函数必须返回 `println!` 而不是 `String`，以符合过程宏 API。我们通过使用 `#name` 简化了这个示例；在生产代码中，咱们应该通过使用 `stringify!` 或 `stringify!`，提供有关出错原因的更具体的错误消息。 `#name`
现在我们有了将注解后的 Rust 代码从 `cargo build` 转换为 `hello_macro` 实例的代码，接下来让我们生成对注解的类型实现 `hello_macro_derive` 特质的代码，如下清单 20-42 中所示。 [crates.io](https://crates.io/) `cargo new pancakes` `hello_macro` `hello_macro_derive` `pancakes` `hello_macro` `hello_macro_derive` `path` <!-- ignore -->
```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

我们使用 `cargo run` 得到一个 `Hello, Macro! My name is Pancakes!` 结构体实例，包含被注解类型的名字（标识符）。清单 20-41 中的结构体表明，当我们对清单 20-37 中的代码运行 `HelloMacro` 函数时，我们得到的 `pancakes` 就将有着值为 `#[derive(HelloMacro)]` 的 ident 字段。因此，清单 20-42 中的 name 变量将包含一个 Ident 结构体实例，其在打印出时将是字符串 "Pancakes"，即清单 20-37 中结构体的名字。
这一定义类似于自定义 `derive` 宏的签名：我们接收圆括号内的令牌，并返回我们希望生成的代码。

### 类属性的宏

类属性的宏与自定义 `derive` 宏类似，但他们针对 `derive` 属性生成代码，他们允许咱们创建新的属性。他们还更加灵活：`derive` 适用于结构体和枚举；而属性还可以应用于其他项目，比如函数。下面是一个使用类属性宏的示例。假设咱们有个名为 `route` 的属性，会在使用某种 web 应用框架时注解函数：
```rust,ignore
#[route(GET, "/")]
fn index() {
```

这个 `#[route]` 属性将由框架定义为一个过程宏。该宏定义的函数的签名将看起来像下面这样：
```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

这里，我们两个 `TokenStream` 类型的参数。第一个用于属性的内容：即 `GET, "/"` 部分。第二个则是该属性所附加的项目的主体：在这一情形下，即 `fn index() {}` 及函数主体的其余部分。
除此之外，类属性的宏与自定义 `derive` 宏的工作原理相同：咱们要创建一个 `proc-macro` 代码箱类型的代码箱，并实现一个生成所需代码的函数！
### 类函数的宏

类函数的宏定义了看起来像函数调用的宏。与 `macro_rules!` 宏类似，他们比函数更为灵活；例如，他们可以取未知数量的参数。然而，`macro_rules!` 的宏只能使用我们在 [“Declarative
Macros for General Metaprogramming”][decl] 小节中讨论过的类似匹配的语法来定义。而类函数的宏会取一个 `TokenStream` 参数，并且他们的定义会像其他两种过程宏一样，使用 Rust 代码来操作该 `TokenStream`。类函数宏的一个示例为 `sql!` 宏，其可以被如下调用： <!-- ignore -->
```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

这个宏会解析其内部的 SQL 语句并检查其语法是否正确，这比 `macro_rules!` 宏所能处理的要复杂得多。`sql!` 宏可能定义如下：
```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

这一定义类似于自定义 `derive` 宏的签名：我们接收圆括号内的令牌，并返回我们希望生成的代码。
## 本章小结

哇！现在，咱们的工具箱中有了一些咱们可以不会经常使用的 Rust 特性，不过咱们会明白，在一些极为特别的情况下他们是可用的。我们介绍了几个复杂的主题，以便在咱们在一些错误消息建议，或其他人的代码中遇到他们时，就能识别出这些概念和语法。请将这一章作为参考来指导咱们找到解决方案。
接下来，我们将把整本书中讨论的所有内容付诸实践，再完成一个项目！

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
