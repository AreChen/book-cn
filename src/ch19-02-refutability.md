## 可证伪性：模式是否会匹配失败

模式有两种形式：可证伪与不可证伪的。对于任何可能传递的值都匹配的模式，属于
*不可证伪的，irrefutable*。例如，`x` 是语句 `let x = 5;` 中的变量；这个 `x`
会匹配任何值，因此不可能匹配失败。对于某些可能的值会匹配失败的模式，属于
*可证伪的，refutable*。例如，`Some(x)` 是表达式 `if let Some(x) =
a_value` 中的模式，因为当变量 `a_value` 中的值为 `None` 而不是 `Some` 时，
`Some(x)` 模式将不匹配。

函数参数、`let` 语句及 `for` 循环只能接受不可证伪的模式，因为当值不匹配时程序无法执行任何有意义的操作。`if let` 与 `while let` 表达式，以及 `let...else` 语句，接受可证伪和不可证伪的模式，但编译器会对不可证伪模式发出告警，因为根据定义，他们意图处理可能的失败：条件的功能在于其能够根据成功或失败，而以不同方式执行的能力。

一般来说，咱们不必担心可证伪与不可证伪模式的区别；但是，咱们确实需要熟悉可证伪性的概念，以便在在报错消息中看到时可以予以响应。在这种情形下，咱们需要根据代码的预期行为，修改模式或者与模式一起使用的结构。

我们来通过一个实例看看，当我们尝试在 Rust 要求使用不可证伪模式的地方使用可证伪模式，或者反之，会发生什么。下面清单 19-8 展示了一个 `let` 语句，但我们对模式指定了个可证伪的模式 `Some(x)`。正如咱们所料，这段代码将不编译。

<Listing number="19-8" caption="Attempting to use a refutable pattern with `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

当 `some_option_value` 是个 `None` 值时，他将与模式 `Some(x)` 匹配失败，这意味着该模式是可证伪的。但是，`let` 语句只能接受不可证伪模式，因为没有可处理 `None` 值的有效代码。在编译时，Rust 将抱怨我们试图在要求不可证伪模式的地方使用可证伪模式：

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

由于我们没有以模式 `Some(x)` 覆盖（也无法涵盖！）所有有效值，Rust 理所当然地会产生编译器报错。

当我们在需要不可证伪模式的地方使用了可证伪模式时，可以通过修改使用该模式的代码来修复：我们可以使用 `let`，而不是使用 `let...else`。然后，当模式不匹配时，花括号中的代码就会处理该值。下面清单 19-9 展示了如何修复清单 19-8 中的代码。

<Listing number="19-9" caption="Using `let...else` and a block with refutable patterns instead of `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

我们给予了代码一种退出条件！这段代码完全有效，尽管这意味着我们无法在没有收到告警的情况下，使用不可证伪模式。当我们给予 `let...else` 某个始终匹配的模式时，如下清单 19-10 中所示，编译器将给出告警。 `x`

<Listing number="19-10" caption="Attempting to use an irrefutable pattern with `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust 会抱怨，对 `let...else` 使用不可证伪模式没有意义： `else`

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

因此，匹配支臂必须使用可证伪模式，除了最后支臂外，他应以不可证伪模式匹配任何剩余的值。Rust 允许我们在仅有一个支臂的 `match` 中使用不可证伪模式，但这种语法并不是特别有用，可以更简单的 `let` 语句替换。

现在咱们知道了哪里使用模式，以及可证伪与不可证伪模式的区别，我们来介绍可用于创建模式的所有语法。
