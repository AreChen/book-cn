## `if let` 与 `let...else` 下的简明控制流

`if let` 语法将 `if` 和 `let` 结合起来，以一种更简洁的方式处理匹配某个模式而忽略其他模式的值。请看示例 6-6：它对 `Option<u8>` 变量中的 `config_max` 值进行匹配，但只希望在值为 `Some` 变体时执行代码。

<Listing number="6-6" caption="仅在值为 `match` 时执行代码的 `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

如果值是 `Some`，我们会在模式中将其中的值绑定到变量 `Some`，然后打印出 `max` 变体中的值。我们不想对 `None` 值做任何事情。为了满足 `match` 表达式的要求，在只处理一个变体之后，我们还必须添加 `_ =>
()`，这是一段令人厌烦的样板代码。

相反，我们可以使用 `if let` 以更简短的方式编写这段代码。下面的代码与示例 6-6 中的 `match` 行为相同：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

`if let` 语法接受一个模式和一个表达式，两者之间用等号分隔。它的工作方式与 `match` 相同：将表达式交给 `match`，并把该模式作为它的第一个分支。在这个例子中，模式是 `Some(max)`，其中的 `max` 会绑定到 `Some` 内部的值。之后，我们可以使用 `max`，然后在 `if let` 代码块中再次使用 `max`，就像我们在对应的 `match` 分支中使用它一样。只有当值匹配该模式时，`if let` 代码块中的代码才会运行。

使用 `if let` 意味着需要输入的内容更少、缩进更少，样板代码也更少。不过，这会失去 `match` 强制执行的穷举检查，而这项检查能确保你没有忘记处理任何情况。在 `match` 和 `if
let` 之间进行选择，取决于具体情境，以及用简洁性换取放弃穷举检查是否适合你的需求。

换句话说，你可以把 `if let` 看作 `match` 的语法糖：当值匹配某个模式时运行代码，然后忽略所有其他值。

我们可以加入 `else` 与 `if let`。`else` 对应的代码块，与等价表达式中 `_` 分支的代码块相同；该 `match` 表达式对应于 `if let` 和 `else`。回忆一下示例 6-4 中 `Coin` 枚举的定义，其中 `Quarter` 变体还包含一个 `UsState` 值。如果我们想统计看到的所有非 25 美分硬币，同时公布 25 美分硬币所属的州，就可以使用 `match` 表达式来实现：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

或者，我们也可以使用 `if let` 和 `else` 表达式：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## 使用 `let...else` 保持在“顺畅路径”上

一种常见模式是：当值存在时执行某些计算，否则返回一个默认值。继续使用包含 `UsState` 值的硬币示例，如果我们想根据 25 美分硬币所属州的历史长短说些俏皮话，就可以在 `UsState` 上定义一个方法来检查该州的年龄，如下所示：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

然后，我们可以使用 `if let` 匹配硬币的类型，并在条件的代码体中引入 `state` 变量，如示例 6-7 所示。

<Listing number="6-7" caption="使用嵌套在 `if let` 中的条件判断某个州在 1900 年是否已经存在">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

这样确实完成了任务，但它把工作都塞进了 `if
let` 语句的代码体中；如果要完成的工作更复杂，就可能很难准确看清顶层分支之间的关系。我们还可以利用表达式会产生值这一事实：要么从 `state` 产生 `if let`，要么提前返回，如示例 6-8 所示。（使用 `match` 也可以做类似的事情。）

<Listing number="6-8" caption="使用 `if let` 产生一个值或提前返回">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

不过，这种写法本身也有些难以理解！`if
let` 的一个分支产生值，另一个分支则直接从整个函数返回。

为了更好地表达这种常见模式，Rust 提供了 `let...else`。`let...else` 语法与 `if let` 非常相似：左侧是模式，右侧是表达式；但它没有 `if` 分支，只有 `else` 分支。如果模式匹配，模式中的值会绑定到外部作用域。如果模式*不*匹配，程序就会进入 `else` 分支，而该分支必须从函数返回。

在示例 6-9 中，你可以看到把 `let...else` 换成 `if let` 后，示例 6-8 会变成什么样。

<Listing number="6-9" caption="使用 `let...else` 明确函数中的控制流">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

注意，这样一来函数主体始终沿着“顺畅路径”执行，不会像使用 `if let` 那样，因为两个分支而产生明显不同的控制流。

如果你的程序中有些逻辑用 `match` 表达起来过于冗长，请记住，`if let` 和 `let...else` 也都是 Rust 工具箱中的工具。

## 本章小结

我们现在已经介绍了如何使用枚举来创建可以是多个枚举变体之一的自定义类型。我们还展示了标准库的 `Option<T>` 类型如何帮助我们利用类型系统防止错误。当枚举变体包含数据时，我们可以使用 `match` 或 `if let` 来提取并使用这些值，具体取决于需要处理的情况数量。

我们的 Rust 程序现在可以使用结构体和枚举来表达领域中的概念。在 API 中使用自定义类型可以确保类型安全：编译器会确保函数只得到符合其预期类型的值。

为了向用户提供组织良好、简单易用且只暴露所需 API 的代码，我们现在来看看 Rust 的模块。
