## 模式语法

在这一小节中，我们汇总所有模式方面的有效语法，并讨论咱们可能打算使用每种语法的原因和时机。

### 匹配字面值

正如咱们在第 6 章中看到的，咱们可以直接将模式与字面值匹配。下面的代码给出了一些示例：

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

这段代码会打印 `one`，因为 `x` 中的值为 `1`。当咱们希望代码在其获取到某个特定具体值时执行某项操作时，这种语法非常有用。

### 匹配命名变量

命名变量属于匹配任何值的不可证伪模式，我们在本书中已经多次使用他们。但是，当咱们在 `match`、`if let` 或 `while let` 表达式中使用命名变量时，会存在一定的复杂性。由于这三类表达式都会开启新的作用域，因此作为这些表达式内的模式一部分而声明的变量，会像所有变量一样，遮蔽这些结构外部同名的变量。在下面清单 19-11 中，我们通过 `x` 声明了一个名为 `Some(5)` 的变量，以及有着值 `y` 的变量 `10`。然后，我们对值 `match` 上创建一个 `x` 表达式。请仔细观察匹配支臂中的模式及末尾的 `println!`，并在运行这段代码或继续阅读前，尝试弄清楚这段代码将打印什么。

<Listing number="19-11" file-name="src/main.rs" caption="A `match` expression with an arm that introduces a new variable which shadows an existing variable `y`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

我们来逐步分析这个 `match` 表达式运行时会发生什么。第一个匹配支臂中的模式未匹配 `x` 中的定义值，因此代码继续。

第二个匹配支臂中的模式引入了一个名为 `y` 新变量，该变量将匹配 `Some` 值内部的任何值。由于我们处于 `match` 表达式内部的新作用域中，因此这是个新的 `y` 变量，而不是我们在开头声明的值为 `y` 的 `10`。这个新的 `y` 绑定将匹配 `Some` 内的任何值，这正是我们在 `x` 中的值。因此，这个新的 `y` 绑定到 `Some` 中 `x` 的内层值。该值为 `5`，因此这一支臂的表达式执行，并打印 `Matched, y = 5`。

当 `x` 为 `None` 值而不是 `Some(5)` 时，前两个支臂中的模式都不会匹配，因此该值
将与下划线匹配。我们没有在下划线支臂的模式中引入 `x` 变量，所以表达式中的 `x`
仍然是没有被遮蔽的外层 `x`。在这种假设的情况下，`match` 会打印 `Default case,
x = None`。

当 `match` 表达式执行完毕后，他的作用域结束，而内层的 `y` 的作用域也结束。最后的 `println!` 产生 `at the end: x = Some(5), y = 10`。

要创建一个比较外层的 `match` 和 `x` 值的 `y` 表达式，而非引入一个会遮蔽现有变量 `y` 的新变量，我们需要改用匹配卫语句条件，a match guard conditional。我们稍后将在 [“Adding Conditionals with Match
Guards”](#adding-conditionals-with-match-guards) 小节，讨论到匹配卫语句问题。 <!-- ignore -->

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### 匹配多个模式

在 `match` 表达式中，咱们可以使用 `|` 语法，即模式 *或* 运算符，匹配多个模式。例如，在下面的代码中，我们将 `x` 的值与匹配支臂匹配，其中第一个支臂有着一个 *或* 选项，这意味着当 `x` 的值匹配该支臂中的任何一个值时，这一支臂的代码将运行：

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

这段代码打印 `one or two`。

### 通过 `..=` 匹配值范围

`..=` 语法允许我们匹配包含起始值和结束值的范围匹配。在下面的代码中，当模式匹配给定范围内的任意值时，该支臂将执行：

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

如果 `x` 为 `1`、`2`、`3`、`4` 或 `5`，第一条支臂将匹配。相比使用 `|` 运算符来表达
相同想法，这种语法对多个匹配值更方便；如果使用 `|`，我们就必须指定 `1 | 2 |
3 | 4 | 5`。指定范围要简短得多，尤其是当我们想要匹配 1 到 1000 之间的任何数字时！

编译器会在编译时检查范围是否为空，而由于 Rust 仅能判断 `char` 和数值类型的范围是否为空，因此范围仅允许带有数值或 `char` 值。

下面是个使用 `char` 值范围的示例：

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust 能判断 `'c'` 位于第一个模式的范围内，并打印 `early
ASCII letter`。

### 解构以拆分值

我们还可以使用模式来解构结构体、枚举和元组，从而使用这些值的不同部分。我们来逐一分析这些值。

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### 结构体

下面清单 19-12 展示了个具有两个字段 `Point` 和 `x` 的 `y` 结构体，我们可以与 `let` 语句一起使用模式拆解他。

<Listing number="19-12" file-name="src/main.rs" caption="Destructuring a struct’s fields into separate variables">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

这段代码创建了变量 `a` 和 `b`，匹配结构体 `x` 中的 `y` 与 `p` 字段的值。这个示例表明，模式中的变量名字不必与结构体的字段名字一致。但是，通常会将变量名字与字段名字保持一致，以便更容易记住哪些变量来自哪个字段。由于这种常见用法，并且写下 `let Point { x: x, y: y } = p;` 会包含大量重复，Rust 为匹配结构体字段的模式提供了一种简写形式：咱们只需列出结构体字段的名字，从该模式创建的变量就会具有同样的名字。下面清单 19-13 的行为与清单 19-12 中的代码相同，但在 `let` 模式中创建的变量是 `x` 和 `y`，而不是 `a` 与 `b`。

<Listing number="19-13" file-name="src/main.rs" caption="Destructuring struct fields using struct field shorthand">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

这段代码创建了变量 `x` 与 `y`，匹配变量 `x` 中的字段 `y` 和 `p`。结果是变量 `x` 与 `y` 包含结构体 `p` 中的值。

我们还可以作为结构体模式一部分的字面值解构，而无需为所有字段都创建变量。这样做允许在创建变量解构其他字段的同时，针对特定值测试某些字段。

在下面清单 19-14 中，我们有个 `match` 表达式，将 `Point` 值分为三种情形： `x` `y = 0` `y` `x = 0`

<Listing number="19-14" file-name="src/main.rs" caption="Destructuring and matching literal values in one pattern">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

- 直接位于 `x` 轴上的点（当 `y` 时为真）、
- 位于 `0` 轴上的点，
- 或不在任一轴上的点。 `x`

第一条支臂通过指定当 `y` 字段的值匹配字面值 `x` 时匹配，而将匹配位于 `0` 轴上的任意点。该模式仍会创建一个 `y` 变量，我们可以在这一支臂的代码中使用。 `y` `Point` `x` `y`

同样地，第二条支臂通过指定当 `p` 字段的值为 `x` 时该字段匹配，从而匹配位于 `0` 轴上的任意点，并为 `On the y axis at 7` 字段创建变量 y。第三条支臂未指定任何字面值，因此他匹配任何其他 Point，并为 x 与 y 字段创建变量。

在这个示例中，由于 `match` 包含 `Point { x: 0, y: 0 }`，因此值 `x` 与第二条支臂匹配，所以这段代码将打印 `y`. `On the x axis at 0`

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### 枚举

我们在本书中解构过枚举（比如，第 6 章中的 清单 6-5），但我们还没有明确讨论解构枚举的模式，与枚举中存储的数据的定义方式相对应。例如，在下面清单 19-15 中，我们使用 清单 6-2 中的 `Message` 枚举，并编写了个有着模式的 `match` 表达式，将解构每个内层值。

<Listing number="19-15" file-name="src/main.rs" caption="Destructuring enum variants that hold different kinds of values">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

这段代码将打印 `Change color to red 0, green 160, and blue 255`。请尝试修改 `msg` 的值，看看其他支臂中的代码运行。

对于没有任何数据的枚举变种，比如 `Message::Quit`，我们无法进一步解构该值。我们只能匹配字面量的 `Message::Quit` 值，并且这一模式中没有变量。

对于类似结构体的枚举变种，比如 `Message::Move`，我们可以使用与我们对结构体指定的类似模式。在变种名字之后，我们放置了一对花括号，然后通过变量列出字段，以便我们分解各个部分已在这一支臂的代码中使用。这里我们使用了与清单 19-13 中一样的简写形式。

对于类似元组的枚举变种，比如包含一个元素的元组的 `Message::Write` 和包含三个元素的元组的 `Message::ChangeColor`，该模式与我们用于匹配元组的模式类似。模式中的变量数量必须要与我们要匹配的变种中的元素数量一致。

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### 嵌套结构体与枚举

到目前为止，我们的示例都只匹配了一层深度的结构体与枚举，但匹配也可以用于嵌套项目！例如，我们可以重构清单 19-15 中的代码，以支持 `ChangeColor` 消息中的 RGB 与 HSV 颜色，如下清单 19-16 中所示。

<Listing number="19-16" caption="Matching on nested enums">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

`match` 表达式中第一个支臂的模式，匹配包含 `Message::ChangeColor` 变种的 `Color::Rgb` 枚举变种；然后，该模式会绑定到三个内部 `i32` 值。第二支臂的模式同样匹配 `Message::ChangeColor` 枚举变种，但内部枚举匹配的是 `Color::Hsv`。即使涉及两个枚举，我们也可以在一个 `match` 表达式中指定这些复杂条件。

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### 结构体和元组

咱们可以更复杂的方式混合、匹配并嵌套解构模式。以下示例展示了一个复杂的解构，其中我们将结构体与元组嵌套在元组内，并解构出所有原始值：

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

这段代码让我们可以将复杂类型分解为各个组成部分，从而我们可以单独使用我们感兴趣的值。

对模式解构是一种彼此分开地使用值的部分的便捷方式，例如结构体中每个字段中的值。

### 忽略模式中的值

咱们已经看到，有时为了获得全包模式，而忽略模式中的值很有用，比如在 `match` 的最后支臂中，全包模式实际上不执行任何操作，但确实考虑了所有剩余的可能值。忽略模式中整个值或部分值的方式有几种：使 `_` `_` `..`

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### 通过 `_` 忽略整个值

我们已将下划线作为通配符模式使用过，他将匹配任何值但不会绑定到该值。这作为 `match` 表达式中的最后一个支臂尤为有用，但我们也可在任何模式中使用他，包括函数参数，如下清单 19-17 中所示。

<Listing number="19-17" file-name="src/main.rs" caption="Using `_` in a function signature">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

这段代码将完全忽略作为第一个参数传递的值 `3`，并将打印 `This code only uses the y parameter: 4`。

在大多数情况下，当咱们不需要某个特定的函数参数时，咱们会修改函数签名，使其不包含未使用的参数。忽略函数参数在某些情况下特别有用，例如，当咱们实现某个特质时，咱们需要特定的类型签名，而实现中的函数体并不需要其中某个参数。忽略函数参数后，咱们可以避免收到关于未使用的函数参数的编译器告警。

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### 通过嵌套的 `_` 忽略值的部分

我们还可以在另一个模式内使用 `_`，来仅忽略值的一部分，例如，当我们仅希望测试值的一部分，而在我们打算运行的相应代码中未用到其他部分时。下面清单 19-18 展示了负责管理某种设置值的代码。业务要求为，不应允许用户覆盖设置的现有自定义设置，但允许用户取消该设置，并在当前未设置时为其赋予新值。

<Listing number="19-18" caption="Using an underscore within patterns that match `Some` variants when we don’t need to use the value inside the `Some`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

这段代码将打印 `Can't overwrite an existing customized value`，及随后的 `setting is Some(5)`。在第一个匹配支臂中，我们无需匹配或使用任一 `Some` 变种内的值，但我们确实需要测试 `setting_value` 和 `new_setting_value` 均为 `Some` 变种时的情形。在这一情形下，我们打印不修改 `setting_value` 的原因，并且他不会被更改。

在第二个支臂中以 `setting_value` 模式表示的所有其他情形下（当 `new_setting_value` 或 `None` 为 `_` 时），我们希望允许 `new_setting_value` 成为 `setting_value`。

我们还可以在一个模式中的多个位置，使用下划线来忽略特定值。下面清单 19-19 展示了忽略五个项目的元组中，第二和第四个值的示例。

<Listing number="19-19" caption="Ignoring multiple parts of a tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

这段代码将打印 `Some numbers: 2, 8, 32`，而值 `4` 与 `16` 将被忽略。

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### 通过 `_` 开头的变量名字，忽略未使用变量

当咱们创建一个变量但未在任何地方使用他时，Rust 通常会发出告警，因为未使用变量可能是个 bug。然而，有时创建一个咱们使用的变量是很有用的，比如当咱们正在构造原型或刚刚开始一个项目时。在这种情况下，咱们可以通过让变量以下划线开头，告诉 Rust 不要对这个使用的变量发出告警。在下面清单 19-20 中，我们创建了两个未使用的变量，但编译此代码时，我们应该只会收到关于其中一个变量的告警。

<Listing number="19-20" file-name="src/main.rs" caption="Starting a variable name with an underscore to avoid getting unused variable warnings">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

在这里，我们会得到关于未用到变量 `y` 的告警，但不会收到关于未使用 `_x` 的告警。

请注意，仅使用 `_` 和使用以下划线开头的名字之间存在细微差别。语法 `_x` 仍会绑定值到变量，而 `_` 则完全不会绑定。为了展示这种区别很重要的情形，下面清单 19-21 将为我们提供一个报错。

<Listing number="19-21" caption="An unused variable starting with an underscore still binds the value, which might take ownership of the value.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

我们将收到报错，因为 `s` 值仍将被迁移到 `_s` 中，这会阻止我们再次使用 `s`。然而，单独使用下划线本身并不会绑定到值。下面清单 19-22 将无任何报错地编译，因为`s` 不会迁移到 `_` 中。

<Listing number="19-22" caption="Using an underscore does not bind the value.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

这段代码正常运行，因为我们从未绑定 `s` 到任何变量；他未被迁移。

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### 通过 `..` 忽略值的剩余部分

对于包含多个部分的值，我们可以使用 `..` 语法，来使用特定部分而忽略其余部分，从而避免需要为每个忽略的值逐一列出下划线。`..` 模式会忽略我们在模式的剩余部分中未曾显式匹配的任何部分。在下面清单 19-23 中，我们有个 `Point` 结构体，保存三维空间中的坐标。在 `match` 表达式中，我们只打算对 `x` 坐标操作，而忽略 `y` 与 `z` 字段中的值。

<Listing number="19-23" caption="Ignoring all fields of a `Point` except for `x` by using `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

我们列出值 `x`，然后仅包含 `..` 模式。这比列出 `y: _` 和 `z: _` 更快，特别是当我们在处理包含大量字段的结构体，而只有一两个字段是相关的时。

语法 `..` 将扩展为所需数量的值。下面清单 19-24 展示了怎样对元组使用 `..`。

<Listing number="19-24" file-name="src/main.rs" caption="Matching only the first and last values in a tuple and ignoring all other values">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

在这段代码中，第一个和最后一个值分别与 `first` 和 `last` 匹配。`..` 将匹配并忽略中间的所有值。

不过，使用 `..` 必须没有歧义。当不清楚哪些值要匹配，哪些值应该被忽略时，Rust 将给予我们一个报错。下面清单 19-25 展示了 `..` 歧义用法的示例，因此他不会编译。

<Listing number="19-25" file-name="src/main.rs" caption="An attempt to use `..` in an ambiguous way">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

当我们编译这个示例时，我们会得到下面这个报错：

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rust 不可能确定出在将某个值与 `second` 匹配之前，应忽略元组中的多少个值，以及之后还应忽略多少个值。这段代码可能意味着我们想要忽略 `2`，将 `second` 与 `4` 绑定，然后忽略 `8`、`16` 和 `32`；或者我们想要忽略 `2` 和 `4`，将 `second` 与 `8` 绑定，然后忽略 `16` 和 `32`；等等。变量名 `second` 对 Rust 而言并无特殊含义，所以我们会得到一个编译器报错，因为在像这样在两个地方使用 `..` 是不明确的。

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

<a id="adding-conditionals-with-match-guards"></a>

### 匹配卫语句下的额外条件

所谓 *匹配卫语句，match guard*，属于额外的 `if` 条件，指定于 `match` 支臂之后，他也必须匹配，该支臂才能被选中。对于表达比单独模式所允许的更复杂的概念，匹配卫语句非常有用。但请注意，他们仅可在 `match` 表达式中使用，而不能用于 `if let` 或 `while let` 表达式。

这种条件可以使用模式中创建的变量。下面清单 19-26 展示了一个 `match` 表达式，其中第一个支臂有着模式 `Some(x)`，并且还有着 `if x % 2 == 0` 的匹配卫语句（当数字为偶数时该条件将为 `true` ）。

<Listing number="19-26" caption="Adding a match guard to a pattern">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

这个示例将打印 `The number 4 is even`。当 `num` 与第一个支臂中的模式比较时，他会匹配，因为 `Some(4)` 匹配 `Some(x)`。然后，匹配卫语句会检查 `x` 除以 2 的余数是否等于 0，由于结果为 0，因此第一个支臂被选中。

若 `num` 改为 `Some(5)`，那么第一个支臂中的匹配卫语句将为 `false`，因为 5 除以 2 的余数为 1，不等于 0。此时 Rust 将转到第二个支臂，该支臂会匹配，因为他没有匹配卫语句，而因此会匹配任何 `Some` 变种。

由于无法在支臂内部表达 `if x % 2 == 0` 这一条件，因此匹配卫语句给予了我们表达这种逻辑的能力。这种额外表达能力的的缺点在于，当涉及匹配卫语句时，编译器不会尝试检查是否穷尽。

在讨论 清单 19-11 时，我们提到可以使用匹配卫语句来解决模式遮蔽问题，pattern-shadowing problem。回顾以下，我们在 `match` 表达式中的模式内部创建了一个新变量，而不是使用 `match` 外部的变量。这个新变量意味着我们无法测试外层变量的值。下面清单 19-27 展示了我们可以怎样使用匹配卫语句解决这个问题。

<Listing number="19-27" file-name="src/main.rs" caption="Using a match guard to test for equality with an outer variable">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

这段代码现在将打印 `Default case, x = Some(5)`。第二个匹配支臂中的模式不会引入将遮蔽外层的 `y` 的新变量 `y`，这意味着我们可以在匹配卫语句中使用外层的 `y`。我们没有将模式指定为 `Some(y)`，这将遮蔽外层的 `y`，而是指定 `Some(n)`。这会创建一个新变量 `n`，他不会遮蔽任何变量，因为 `n` 外部没有变量 `match`。

匹配卫语句 `if n == y` 不是个模式，因此不会引入新变量。这个 `y` *是* 外层的 `y`，而不是一个会遮蔽他的新的 `y`，我们可以通过比较 `y` 和 `n`，查找与外层 `y` 具有相同的值。

咱们还可在匹配卫语句中使用 *或* 运算符 `|`，来指定多个模式；匹配卫语句条件将应用与所有模式。下面清单 19-28 展示了使用 `|` 的模式与匹配卫语句组合时的优先级。这个示例的重要部分是，`if y` 匹配卫语句会应用于 `4`、`5` *和* `6`，尽管看起来 `if y` 只会应用到 `6`。

<Listing number="19-28" caption="Combining multiple patterns with a match guard">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

匹配条件指出，只有当 `x` 的值等于 `4`、`5` 或 `6`， *且* `y` 为 `true` 时，这个支臂才会匹配。当这段代码运行时，由于 `x` 为 `4`，第一个支臂的模式会匹配，但匹配卫卫语句的 `if y` 为`false`，从而第一个支臂未被选中。代码会转到第二个支臂，他确实匹配，进而这个程序打印 `no`。原因是 `if` 条件会应用到整个模式 `4 | 5 | 6`，而不仅仅是最后一个值 `6`。换句话说，匹配卫语句相对于模式的优先级的行为如下：

```text
(4 | 5 | 6) if y => ...
```

而不是这样：

```text
4 | 5 | (6 if y) => ...
```

运行代码后，优先级行为显而易见：若匹配卫语句仅应用于使用 `|` 运算符指定的值列表中的最后一个值，那么该支臂就会匹配，进而这个程序就会打印 `yes`。

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### 使用 `@` 绑定

*地址* 运算符 `@` 让我们可以在对某个值进行模式匹配测试的同时，创建一个保存值的变量。在下面清单 19-29 中，我们打算测试 `Message::Hello` 的 `id` 字段，是否范围 `3..=7` 内。我们还希望绑定该值到变量 `id`，以便在与该支臂相关的代码中使用他。

<Listing number="19-29" caption="Using `@` to bind to a value in a pattern while also testing it">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

这个示例将打印 `Found an id in range: 5`。通过在范围 `id @` 之前指定 `3..=7`，我们将于名为 `id` 的变量中，捕获匹配该范围匹配的任何值，同时测试该值是否匹配该范围模式。

在第二个支臂中，我们仅在模式中指定了一个范围，与该支臂关联的代码没有包含 `id` 字段实际值的变量。`id` 字段的值可能是 10、11 或 12，但与该模式相关的代码并不知道具体是哪个值。由于我们没有保存 `id` 值在变量中，因此模式代码无法使用 `id` 字段的值。

在最后一个支臂中，虽然我们指定了一个不带范围的变量，但在该支臂的代码中，我们确实可以通过一个名为 `id` 的变量使用该值。原因在于我们使用了结构体字段的简写语法，the struct field shorthand syntax。但与前两个支臂不同，我们在这个支臂中并未对`id` 字段应用任何测试：任何值都会匹配这个模式。

使用 `@` 让我们可以在同一个模式中测试值并保存其到变量中。

## 本章小结

Rust 的模式在区分不同类别的数据方面非常有用。当在 `match` 表达式中使用时，Rust 就会确保咱们的模式涵盖所有可能的值，否则程序将无法编译。`let` 语句和函数参数中的模式，使这些结构更为有用，可以将值解构为更小的部分，并将这些部分赋值给变量。我们可以创建简单或复杂的模式来满足我们的需求。

接下来，在本书的倒数第二章中，我们将探讨 Rust 各种特性的一些高级方面。
