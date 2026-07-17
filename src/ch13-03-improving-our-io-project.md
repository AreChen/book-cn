## 改进我们的 I/O 项目

借助这些关于迭代器的新知识，我们可以通过使用迭代器改进第 12 章中的 I/O 项目，让代码中的一些地方更清晰、更简洁。让我们来看看迭代器如何改进 `Config::build` 函数和 `search` 函数的实现。

### 使用迭代器移除 `clone`

在清单 12-6 中，我们添加了代码，它接收一个 `String` 值切片，并通过索引切片、克隆其中的值来创建 `Config` 结构体的实例，从而使 `Config` 结构体能够拥有这些值。在清单 13-17 中，我们重现了清单 12-23 中 `Config::build` 函数的实现。

<Listing number="13-17" file-name="src/main.rs" caption="重现清单 12-23 中的 `Config::build` 函数">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

当时，我们说过不必担心低效的 `clone` 调用，因为以后会将其移除。现在就是时候了！

我们在这里需要 `clone`，因为 `String` 元素构成的切片位于参数 `args` 中，但 `build` 函数并不拥有 `args`。为了返回一个 `Config` 实例的所有权，我们必须克隆 `query` 和 `file_path` 字段中的值，这些字段属于 `Config`，这样 `Config` 实例才能拥有这些值。

借助我们对迭代器的新知识，我们可以修改 `build` 函数，让它获取一个迭代器的所有权作为参数，而不是借用切片。我们将使用迭代器的功能，而不是检查切片长度并索引特定位置的代码。这样可以更清楚地表明 `Config::build` 函数正在做什么，因为迭代器会访问这些值。

一旦 `Config::build` 获取了迭代器的所有权，不再使用借用的索引操作，我们就可以将迭代器中的 `String` 值移动到 `Config` 中，而不是调用 `clone` 并进行新的分配。

#### 直接使用返回的迭代器

请打开 I/O 项目的 _src/main.rs_ 文件，其内容应该如下：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

我们首先将清单 12-24 中 `main` 函数的开头修改为清单 13-18 中的代码，这次代码使用了迭代器。在我们同时更新 `Config::build` 之前，这段代码无法编译。

<Listing number="13-18" file-name="src/main.rs" caption="将 `env::args` 的返回值传递给 `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

`env::args` 函数返回一个迭代器！我们不再将迭代器的值收集到向量中，然后把切片传递给 `Config::build`，而是现在直接将 `env::args` 返回的迭代器的所有权传递给 `Config::build`。

接下来，我们需要更新 `Config::build` 的定义。让我们将 `Config::build` 的签名修改为清单 13-19 所示的样子。由于还需要更新函数体，这段代码仍然无法编译。

<Listing number="13-19" file-name="src/main.rs" caption="更新 `Config::build` 的签名，使其接受一个迭代器">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

标准库中 `env::args` 函数的文档显示，它返回的迭代器类型是 `std::env::Args`，该类型实现了 `Iterator` trait，并返回 `String` 值。

我们更新了 `Config::build` 函数的签名，使参数 `args` 具有带有 trait bound `impl Iterator<Item =
String>` 的泛型类型，而不是 `&[String]`。我们在第 10 章的[“将 trait 用作参数”][impl-trait]<!-- ignore -->
部分中讨论过 `impl Trait` 语法的这种用法，这意味着 `args` 可以是任何实现
`Iterator` trait 并返回 `String` 项的类型。

由于我们正在获取 `args` 的所有权，并且会通过遍历它来修改 `args`，因此可以添加 `mut` 关键字到 `args` 参数的声明中，使其可变。

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### 使用 `Iterator` trait 方法

接下来，我们来修复 `Config::build` 的函数体。由于 `args` 实现了 `Iterator` trait，我们知道可以对它调用 `next` 方法！清单 13-20 将清单 12-23 中的代码更新为使用 `next` 方法。

<Listing number="13-20" file-name="src/main.rs" caption="修改 `Config::build` 的函数体以使用迭代器方法">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

请记住，`env::args` 返回值中的第一个值是程序名称。我们想忽略它并获取下一个值，因此首先调用 `next`，不处理返回值。然后调用 `next`，获取要放入 `query` 字段（该字段属于 `Config`）的值。如果 `next` 返回 `Some`，我们使用 `match` 提取该值。如果它返回 `None`，就意味着提供的参数不够，我们提前返回一个 `Err` 值。对于 `file_path` 值，我们也进行相同的操作。

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### 使用迭代器适配器让代码更清晰

我们还可以利用 I/O 项目的 `search` 函数中的迭代器。这里的清单 13-21 重现了它在清单 12-19 中的实现。

<Listing number="13-21" file-name="src/lib.rs" caption="清单 12-19 中 `search` 函数的实现">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

我们可以使用迭代器适配器方法，以更简洁的方式编写这段代码。这样还可以避免使用可变的中间 `results` 向量。函数式编程风格倾向于尽量减少可变状态，以使代码更清晰。移除可变状态可能为未来的改进创造条件，使搜索可以并行进行，因为我们不必管理对 `results` 向量的并发访问。清单 13-22 展示了这一修改。

<Listing number="13-22" file-name="src/lib.rs" caption="在 `search` 函数的实现中使用迭代器适配器方法">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

回顾一下，`search` 函数的作用是返回 `contents` 中包含 `query` 的所有行。与清单 13-16 中的 `filter` 示例类似，这段代码使用 `filter` 适配器，只保留 `line.contains(query)` 返回 `true` 的行。然后，我们使用 `collect` 将匹配的行收集到另一个向量中。简单多了！你也可以对 `search_case_insensitive` 函数进行相同的修改，使用迭代器方法。

作为进一步的改进，可以从 `search` 函数返回一个迭代器：移除 `collect` 调用，并将返回类型改为 `impl
Iterator<Item = &'a str>`，这样该函数就会成为一个迭代器适配器。请注意，你还需要更新测试！在进行这项修改之前和之后，使用 `minigrep` 工具搜索一个大文件，观察行为上的差异。在修改之前，程序要等到收集完所有结果后才会打印任何结果；而修改之后，每找到一行匹配的行就会打印结果，因为 `for` 循环所在的 `run` 函数可以利用迭代器的惰性。

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### 在循环和迭代器之间做出选择

接下来合理的问题是：在你自己的代码中，应该选择哪种风格，以及为什么：清单 13-21 中的原始实现，还是清单 13-22 中使用迭代器的版本（假设我们在返回结果前收集所有结果，而不是返回迭代器）。大多数 Rust 程序员更喜欢使用迭代器风格。起初这种风格有点难掌握，但一旦你熟悉了各种迭代器适配器及其作用，迭代器就会更容易理解。代码不再纠结于各种循环细节和创建新向量，而是聚焦于循环的高级目标。这种方式抽象掉了一些常见代码，因此更容易看出这段代码中特有的概念，例如迭代器中的每个元素都必须通过的过滤条件。

但是，这两个实现真的等价吗？直觉上可能会认为，较低层次的循环会更快。让我们来谈谈性能。

[impl-trait]: ch10-02-traits.html#traits-as-parameters
