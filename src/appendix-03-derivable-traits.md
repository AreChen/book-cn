## 附录 C：派生特质

在这本书的不同地方，我们都讨论了 `derive` 属性，咱们可以用于结构体或枚举的定义。`derive` 属性将生成代码，对咱们以 `derive` 语法注解的类型，以某个特质的默认实现该特质。

在这个附录中，我们提供了对标准库中，所有可与  `derive` 一起使用的特质的参考。每个小节涵盖都会介绍：

- 派生这个特质将启用哪些运算符和方法；
- `derive` 会执行该特质所提供的何种实现；
- 实现该特质对类型意味着什么；
- 允许及不允许咱们实现该特质的条件；
- 需要该特质的操作示例。

当咱们想要与 `derive` 属性提供的不同行为时，请查阅每种特质的 [标准库文档](../std/index.html)，了解有关如何手动实现他们的详细信息。
这个附录中提供的派生特质列表并不全面：库可以针对自己的特质实现 `derive`，构造咱们可以真正开放式地与 derive 一起使用的特质列表。实现 derive 涉及使用过程宏，这在第 20 章的 [自定义 derive 宏] 小节中介绍过。

无法派生的特质的一个示例是 `Display`，他为最终用户处理格式化。咱们应该始终考虑向最终用户展示类型时的适当方式。最终用户应该被允许看类型的哪些部分？他们会发现哪些部分是相关的？哪种数据格式对他们来说最相关？Rust 编译器没有这种洞察力，因此无法为咱们提供适当的默认行为。
这个附录中提供的派生特质列表并不全面：库可以针对自己的特质实现 `derive`，构造咱们可以真正开放式地与 `derive` 一起使用的特质列表。实现 `derive` 涉及使用过程宏，这在第 20 章的 [自定义 `derive` 宏] 小节中介绍过。
### 用于程序员输出的 `Debug`

`Debug` 特质支持以格式字符串形式的调试输出，咱们可以通过在 `:?` 占位符内添加 `{}` 表示。

`Debug` 特质允许咱们出于调试目的，打印某种类型的实例，这样咱们和该类型的其他程序员就可以在程序执行的特定点检查该实例。

例如，在使用 `Debug` 宏下，`assert_eq!` 特质就是必需的，因为该宏需要能够比较两个类型实例的相等性。

### 用于相等比较的 `PartialEq` 和 `Eq`

`PartialEq` 特质没有方法。其目的是表明，对于其注解的类型的每个值，该值都等于其自身。`==` 特质只能应用于同时实现 `!=` 的类型，尽管并非所有实现 PartialEq 的类型都可以实现 Eq。浮点数类型就是一个示例：浮点数的实现规定，两个非数字，the not-a-number, NaN，值的实例彼此不相等。

`PartialEq` 特质允许咱们出于排序目的比较某种类型的实例。实现 `eq` 的类型可以与 <、>、<= 及 >= 等运算符一起使用。咱们只能对那些同时实现 `PartialEq` 的类型应用 PartialOrd 特质。

`PartialEq` 特质让咱们知道对于其注解类型的任意两个值，是否存在有效的顺序。Ord 特质实现 cmp 方法，该方法返回一个 Ordering 类型，而非 Option&lt;Ordering>，因为有效的排序始终是可能的。咱们只能对同时实现 PartialOrd 及 Eq (且 Eq 需要 `assert_eq!`) 的类型应用 Ord 特质。当对结构体和枚举派生时，cmp 的行为方式与 PartialOrd 中的 partial_cmp 的派生实现相同。

`Eq` 特质没有方法。它的作用是表明，对于标注类型的每个值，该值都等于自身。`Eq` 特质只能用于同时实现 `PartialEq` 的类型，尽管并非所有实现 `PartialEq` 的类型都能实现 `Eq`。一个例子是浮点数类型：浮点数的实现规定，两个非数字（`NaN`）值的实例彼此不相等。

当需要 `Eq` 特质时，例如将它用于 `HashMap<K, V>` 的键，使 `HashMap<K, V>` 能判断两个键是否相同。
### 用于排序比较的 `PartialOrd` 和 `Ord`

`PartialOrd` 特质允许你出于排序目的比较某种类型的实例。实现 `PartialOrd` 的类型可以使用 `<`、`>`、`<=` 和 `>=` 运算符。你只能将 `PartialOrd` 应用于同时实现 `PartialEq` 的类型。

派生 `PartialOrd` 会实现 `partial_cmp` 方法；当给定值无法产生顺序时，该方法返回 `Option<Ordering>`，其值为 `None`。一个无法产生顺序的例子是浮点数 `NaN` 值，尽管该类型的大多数值都可以比较。对任意浮点数调用 `partial_cmp` 时，如果该值是 `NaN`，就会返回 `None`。

在结构体上派生时，`PartialOrd` 会按照字段在结构体定义中出现的顺序，逐个比较两个实例的字段值。在枚举上派生时，枚举定义中较早声明的变体小于较晚列出的变体。

`PartialOrd` 的一个使用示例是 `gen_range` 方法，它来自 `rand` 箱，会根据范围表达式生成指定范围内的随机值。

`Ord` 特质让你可以确定，标注类型的任意两个值之间都存在有效的顺序。`Ord` 特质实现 `cmp` 方法，该方法返回 `Ordering`，而不是 `Option<Ordering>`，因为有效顺序总是存在的。你只能将 `Ord` 应用于同时实现 `PartialOrd` 和 `Eq` 的类型（而 `Eq` 要求实现 `PartialEq`）。在结构体和枚举上派生时，`cmp` 的行为与 `partial_cmp` 在 `PartialOrd` 中的派生实现相同。
需要 `Ord` 的一个示例是在 `BTreeSet<T>` 中存储值时，这是一种根据值的排序顺序存储数据的数据结构。
### 用于复制值的 `Clone` 和 `Copy`

`Clone` 特质允许咱们显式地创建值的深拷贝，而复制过程可能涉及运行任意代码和拷贝堆数据。有关 `Clone` 的更多信息，请参阅第 4 章中 [变量与数据相互作用：克隆] 小节。

派生 `Clone` 会实现 `clone` 方法，当该方法针对整个类型实现时，会对该类型的每个部分调用 `clone`。这意味着类型中的所有字段或这，也必须实现 `Clone` 才能派生 `Clone`。

需要 `Clone` 的一个示例是对切片调用 `to_vec` 方法。切片并不拥有其包含的类型实例，但 `to_vec` 返回的矢量值需要拥有其实例，因此 `to_vec` 会对每个项目调用 `clone`。因此，切片中存储的类型必须实现 `Clone`。

`Copy` 特质允许咱们仅通过拷贝存储在栈上的二进制位来复制值；无需任意代码。有关 `Copy` 的更多信息，请参阅第 4 章中 [唯栈数据：拷贝] 小节。

`Copy` 特质未定义任何方法，以防止程序员重载这些方法，从而避免违反 “不运行任意代码” 这一假设。这样一来，所有程序员都可以假设拷贝值会非常快。

只要一个类型的所有组成部分都实现了 `Copy`，就可以为它派生 `Copy`。实现 `Copy` 的类型也必须实现 `Clone`，因为实现 `Copy` 的类型拥有一个简单的 `Clone` 实现，该实现执行与 `Copy` 相同的任务。

通常不需要 `Copy` 特质；实现 `Copy` 的类型可以使用优化，因此不必调用 `clone`，代码也更加简洁。

通过 `Copy` 能实现的操作，也都可以通过 `Clone` 完成，但代码可能会更慢，或者必须在某些地方使用 `clone`。

### 用于映射值到固定大小值的 `Hash`

`Hash` 特质允许咱们取任意大小的类型的示例，并使用哈希函数映射该示例到固定大小的值。派生 `Hash` 会实现 `hash` 方法。`hash` 方法的派生实现，会组合对该类型的每个部分调用 `hash` 的结果，这就意味所有字段或这也必须实现 `Hash` 才能派生 `Hash`。

需要 `Hash` 的一个示例是，在 `HashMap<K, V>` 中存储键以高效地存储数据。

### 用于默认值的 `Default`

`Default` 特质允许咱们创建某种类型的默认值。派生 `Default` 会实现 `default` 函数。`default` 函数的派生实现会对类型的各个部分调用 `default` 函数，这意味类型中的所有字段或者也必须实现 `Default`，才能派生 `Default`。

`Default::default` 函数通常与第 5 章中 [通过结构体更新语法创建实例] 小节中讨论的结构体更新语法结合使用。咱们可以自定义结构体的几个字段，然后使用 `..Default::default()`，为其余字段设置并使用默认值。

例如，当咱们对 `Default` 实例使用 `unwrap_or_default` 方法时，`Option<T>` 特质就是必需的。当 `Option<T>` 为 `None` 时，方法 `unwrap_or_default` 将返回 `Default::default` 针对存储在 `T` 中的类型 `Option<T>` 的结果。

<!-- ignore -->

<!-- ignore -->

<!-- ignore -->

<!-- ignore -->

<!--
ignore -->

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
