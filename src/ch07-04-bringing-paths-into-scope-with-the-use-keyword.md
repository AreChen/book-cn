## 以 `use` 关键字带入路径到作用域

必须写出调用函数的路径可能会感到不便且重复。在 [清单 7-7] 中，无论我们选择 `add_to_waitlist` 函数的绝对路径还是相对路径，每次我们想要调用 `add_to_waitlist` 时，我们都必须还要指定 `front_of_house` 和 `hosting`。幸运的是，有一种简化这一过程的方式：我们可以 `use` 关键字创建路径的快捷方式一次，然后在作用域中的其他地方使用较短的名字。

在下面清单 7-11 中，我们将 `crate::front_of_house::hosting` 模组带入 `eat_at_restaurant` 函数的作用域，这样我们只需指定 `hosting::add_to_waitlist` 即可在 `add_to_waitlist` 中调用 `eat_at_restaurant` 函数。

<Listing number="7-11" file-name="src/lib.rs" caption="以 `use` 关键字带入模组到作用域">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

在作用域中添加 `use` 与路径，类似于在文件系统中创建符号链接。通过在代码箱根处添加 `use crate::front_of_house::hosting`，`hosting` 现在便是该作用域中的有效名字，就像 `hosting` 模组已在代码箱根处定义一样。与任何其他路径一样，以 `use` 关键字带入作用域的路径也会检查隐私。

请注意，`use` 只会针对 `use` 发生之处的作用域创建快捷方式。下面清单 7-12 迁移 `eat_at_restaurant` 函数到一个名为 `customer` 的新子模组中，该子模组是个与 `use` 语句不同的作用域，因此该函数体将不编译。

<Listing number="7-12" file-name="src/lib.rs" caption="`use` 语句仅应用于其所在的作用域">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

编译器错误表明该快捷方式在 `customer` 模组内不再适用：

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

请注意，还有一条告警，表明其中的 `use` 在其作用域中不在被用到！要修复这个问题，也要迁移这个 `use` 语句到 `customer` 模组中，或者在 `super::hosting` 子模组内以 `customer` 引用父模组中的该快捷方式。

### 创建惯用的 `use` 路径

在 [清单 7-11] 中，咱们可能想知道为什么我们指定了 `use
crate::front_of_house::hosting`，然后在 `hosting::add_to_waitlist` 中调用 `eat_at_restaurant`，而不是指定 `use` 函数的完整 `add_to_waitlist` 路径，如下面清单 7-13 中那样。

<Listing number="7-13" file-name="src/lib.rs" caption="以 `add_to_waitlist` 带入 `use` 到作用域，这属于非惯用的">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

尽管清单 7-11 和清单 7-13 都完成了同一任务，但清单 7-11 是以 `use` 带入函数到作用域的惯用方式。以 `use` 带入函数的父模到作用域意味着我们在调用函数时必须指定父模组。在调用函数时指定父模组可以清楚地表明该函数不属于本地定义的，同时仍然最大限度地减少完整路径的重复。清单 7-13 中的代码在 `add_to_waitlist` 于何处定义方面不清楚。

另一方面，在以 `use` 关键字引入结构体、枚举及其他项目时，指定完整路径是惯用的。下面清单 7-14 展示了带入标准库的 `HashMap` 结构体到二进制代码箱的作用域的惯用方式。

<Listing number="7-14" file-name="src/main.rs" caption="以惯用方式带入 `HashMap` 到作用域">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

这个习惯用法背后没有什么强有力的理由：他只是已经出现的约定，人们已经习惯了以这种方式阅读和编写 Rust 代码。

这种习惯用法的例外是，当我们以 `use` 语句带入两个同名的项目到作用域时，因为 Rust 不允许这样做。下面清单 7-15 展示了如何带入两种有着同一名字但不同父模组的 `Result` 类型到作用域，以及如何引用他们。

<Listing number="7-15" file-name="src/lib.rs" caption="带入两个有着相同名字的类型到同一作用域必须用到他们的父模组">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

正如咱们所见，使用父模组区分了两种 `Result` 类型。相反，若我们指定了 `use std::fmt::Result` 和 `use std::io::Result`，我们就会在同一作用域中有两个 `Result` 类型，并且当我们使用 `Result` 时，Rust 将不清楚我们指的是哪个。

### 以 `as` 关键字提供新的名字

对于以 `use` 带入两种同名类型到同一作用域的问题，还有另一种解决方案：在路径后，我们可以为类型指定 `as` 及一个新的本地名字，或 *别名，alias*。下面清单 7-16 展示了编写清单 7-15 中代码的另一种方式，通过使用 `Result` 重命名两种 `as` 类型中之一。

<Listing number="7-16" file-name="src/lib.rs" caption="当带入类型到作用域时以 `as` 关键字重命名类型">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

在第二个 `use` 语句中，针对 `IoResult` 类型我们选择了新的名字 `std::io::Result`，这不会与我们同样带入作用域的 `Result` 中的 `std::fmt` 冲突。清单 7-15 和清单 7-16 均被视为惯用的，因此选择取决于咱们！

### 以 `pub use` 再导出名字

当我们以 `use` 关键字带入名字到作用域后，该名字对于我们将其导入的作用域是私有的。为了该作用域外部的代码能够引用这个名字，就好像他已在该作用域中定义那样，我们可以结合 `pub` 与 `use`。这项技巧称为 *再导出，re-exporting*，因为我们在带入项目到作用域的同时，还构造该项目为可供其他人带入他们的作用域。

下面清单 7-17 展示 [清单 7-11] 中的代码，其中根模组中的 `use` 已改为 `pub use`。

<Listing number="7-17" file-name="src/lib.rs" caption="以 `pub use` 在新的作用域中构造项目为可供任何代码使用">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

在这一修改前，外部代码将必须通过使用路径 `add_to_waitlist` 路径调用 `restaurant::front_of_house::hosting::add_to_waitlist()` 函数，这还需要 `front_of_house` 模组标记为 `pub`。现在，这个 `pub
use` 已重导出了根模组中的 `hosting` 模组，外部代码便可使用路径 `restaurant::hosting::add_to_waitlist()`。

当咱们代码的内部结构不同于与调用咱们代码的程序员，对这一领域的理解方式时，重导出非常有用。例如，在这个餐厅比喻中，经营餐厅的人考虑的是 “前厅” 和 “后厨”。但光顾餐厅的顾客可能不会从这些方面考虑餐厅的各个部分。在 `pub
use` 下，我们可以一种结构编写咱们的代码，而暴露另一种结构。这样做使我们的库对在这个库上工作及调用库的程序员，都能保持组织良好。我们将在第 14 章中的 [“导出便利的公开 API”] 小节中，探讨 `pub use` 的另一个示例，以及他如何影响咱们的代码箱文档。

### 使用外部包

在第 2 章中，我们编写了个猜数游戏项目，使用了一个名为 `rand` 的外部包来获取随机数。为了在咱们的项目中使用 `rand`，我们添加了下面这行到 Cargo.toml：



<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

在 Cargo.toml 添加 `rand` 为依赖项，告诉 Cargo 从 [crates.io](https://crates.io/) 下载 `rand` 包及任何依赖项，而使 `rand` 对咱们的项目可用。

然后，为了带入 `rand` 的定义到咱们包的作用域，我们添加了以这个代码箱名字 `use` 开头的 `rand` 行，并列出了咱们打算带入作用域的项目。回顾在第 2 章中的 [“生成随机数”] 小节中，我们带入了 `rand::prelude` 这个特质到作用域并调用了 `rand::rng` 函数：

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Rust 社区的成员已在 [crates.io](https://crates.io/) 处提供了许多包，而拉取其中任何包到咱们的包中都涉及这些同样步骤：在咱们包的 Cargo.toml 文件中列出他们，并使用 `use` 带入他们代码箱中的项目到作用域。

请注意，标准 `std` 库同样属于咱们包外部的代码箱。因为标准库是随 Rust 语言一起提供的，所以我们不需要修改 Cargo.toml 来包含 `std`。但我们确实需要以 `use` 引用他，来带入其中的项目到咱们包的作用域。例如，对于 `HashMap` 我们将使用下面这行：

```rust
use std::collections::HashMap;
```

这是个以 `std`，即标准库代码箱名字，开头的绝对路径。



<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### 使用嵌套路径清理 `use` 列表

当我们正使用定义在同一代码箱或同一模组中的多个项目时，那么在每个项目自己的行上列出他们就会占用咱们文件中的大量垂直空间。例如，我们在猜数游戏处的 [清单 2-4] 中有的这两条 `use` 语句，会带入 `std` 中的项目到作用域：

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

相反，我们可以使用嵌套路径于一行中带入同样的项目到作用域。通过指定路径的共同部分，后跟两个冒号，然后用花括号括起一个路径不同部分的列表，如下清单 7-18 中所示。

<Listing number="7-18" file-name="src/main.rs" caption="指定嵌套路径以带入有着同一前缀的多个项目到作用域">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

在较大的程序中，使用嵌套路径带入同一代码箱或同一模组中的许多项目到作用域，可大大减少所需的单独 `use` 语句数量！

我们可在路径的任何级别使用嵌套路径，这在组合两条共用子路径的 `use` 语句时非常有用。例如，下面清单 7-19 显示了两条 `use` 语句：一个带入 `std::io` 到作用域，另一个带入 `std::io::Write` 到作用域。

<Listing number="7-19" file-name="src/lib.rs" caption="两条 `use` 语句，其中一条是另一条的子路径">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

这两条路径的共同部分是 `std::io`，而这正是完整的第一条路径。要将这两条路径合并为一条 `use` 语句，我们可在嵌套路径中使用 `self`，如下清单 7-20 中所示。

<Listing number="7-20" file-name="src/lib.rs" caption="合并清单 7-19 中的路径为一条 `use` 语句">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

这一行会带入 `std::io` 与 `std::io::Write` 到作用域。



<a id="the-glob-operator"></a>

### 以全局运算符导入项目

当我们打算带入定义在路径下的 *所有* 公开项目到作用域时，我们可以指定该路径，后跟 `*` 这个全局运算符：

```rust
use std::collections::*;
```

这条 `use` 语句会带入定义在 `std::collections` 下的所有公开项目到当前作用域。使用全局运算符时要小心！全局会使区分哪些名字在作用域中以及程序中用到的名字于何处定义变得更难。此外，当依赖项修改了其定义时，咱们已导入的内容也会改变，例如，当依赖项添加了带有与同一作用域下咱们的某个定义同样名字的定义，那么在咱们更新依赖项后，这可能导致编译器错误。

全局运算符通常会在测试时使用，以带入所有被测试内容到 `tests` 模块；我们将在第 11 章中的 [“怎样编写测试”](../std/prelude/index.html#other-preludes) 小节中讨论这点。全局运算符有时也用作前奏模式，the prelude pattern，的一部分：有关该模式的更多信息，请参阅 [标准库文档]。





<!-- ignore -->

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<!-- ignore -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- ignore -->

<!-- ignore -->

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
