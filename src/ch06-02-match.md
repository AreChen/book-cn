<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## `match` 控制流结构

Rust 有一种非常强大的控制流构造，称为 `match`。它允许你将值与一系列模式
比较，然后根据匹配的模式执行代码。模式可以由字面值、变量名、通配符等
组成；[第 19 章][ch19-00-patterns]<!-- ignore --> 会介绍所有不同种类的
模式及其作用。`match` 的强大之处在于模式的表达能力，以及编译器会确认
所有可能的情况都得到处理。

可以把 `match` 表达式想象成分拣硬币的机器：硬币沿着带有不同大小孔洞的
轨道滑下，每枚硬币都会从遇到的第一个能容纳它的孔洞掉下去。同样，值会
依次经过 `match` 中的每个模式，在第一个“适合”该值的模式处，值会进入
关联的代码块，在执行时使用。

说到硬币，就用硬币作为 `match` 的例子吧！可以编写一个函数，接收一枚
未知的美国硬币，以类似分拣机器的方式判断它是哪种硬币，并返回以美分表示
的价值，如示例 6-3 所示。

<Listing number="6-3" caption="以枚举变体作为模式的枚举和 `match` 表达式">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

分解一下 `match` 函数中的 `value_in_cents`。首先写出 `match` 关键字，
后跟一个表达式，这里是值 `coin`。这看起来与 `if` 使用的条件表达式很像，
但有一个很大的区别：`if` 的条件必须求值得到布尔值，而这里可以是任意
类型。本例中 `coin` 的类型是第一行定义的 `Coin` 枚举。

接下来是 `match` 分支。一个分支有两部分：模式和一些代码。这里第一个
分支的模式是值 `Coin::Penny`，然后使用 `=>` 运算符分隔模式和要运行的
代码。本例中的代码只是值 `1`。每个分支之间用逗号分隔。

执行 `match` 表达式时，会按顺序将结果值与每个分支的模式比较。如果模式
匹配该值，就执行与模式关联的代码。如果模式不匹配，就像硬币分拣机器一样
继续执行下一个分支。可以根据需要使用任意数量的分支：在示例 6-3 中，
`match` 有四个分支。

每个分支关联的代码都是表达式，匹配分支中表达式的结果值就是整个 `match`
表达式返回的值。

如果 match 分支代码很短，通常不使用花括号，就像示例 6-3 中每个分支
只返回一个值。若想在分支中运行多行代码，必须使用花括号，此时分支后的
逗号可以省略。例如，下面的代码每次使用 `Coin::Penny` 调用方法时都会
打印“Lucky penny!”，但仍返回代码块的最后一个值 `1`：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### 与值绑定的模式

match 分支的另一个有用功能是，可以绑定与模式匹配的值的各个部分。这
就是从枚举变体中提取值的方式。

例如，修改一个枚举变体，让它在内部保存数据。1999 年至 2008 年间，美国
铸造了 25 美分硬币，一面为 50 个州分别设计了不同图案。其他硬币没有州
图案，因此只有 25 美分硬币具有这个额外值。可以修改 `enum` 变体，
让它包含一个存储在其中的 `Quarter` 值，将这一信息加入 `UsState`，如示例
6-4 所示。

<Listing number="6-4" caption="`Coin` 变体也保存 `Quarter` 值的 `UsState` 枚举">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

假设有位朋友想收集全部 50 种州 25 美分硬币。分拣零钱的硬币类型时，也
打印每枚 25 美分硬币关联的州名；如果朋友还没有这枚，就可以将它加入收藏。

在这段代码的 match 表达式中，我们将名为 `state` 的变量添加到匹配
`Coin::Quarter` 变体值的模式中。匹配 `Coin::Quarter` 时，`state` 变量会
绑定到这枚 25 美分硬币的州值。然后就可以在该分支的代码中使用 `state`，
如下所示：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

如果调用 `value_in_cents(Coin::Quarter(UsState::Alaska))`，`coin` 就是
`Coin::Quarter(UsState::Alaska)`。将该值与每个 match 分支比较时，直到
`Coin::Quarter(state)` 才会匹配。此时，`state` 的绑定值是 `UsState::Alaska`。
随后可以在 `println!` 表达式中使用这个绑定，从 `Coin` 枚举的 `Quarter`
变体中取出内部州值。

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### `Option<T>` 的 `match` 模式

上一节使用 `T` 时，我们想从 `Some` 情况中取出内部的 `Option<T>` 值；也
可以像处理 `Option<T>` 枚举一样使用 `match` 处理 `Coin`！这里不比较
硬币，而是比较 `Option<T>` 的变体，但 `match` 表达式的工作方式不变。

假设想编写一个接收 `Option<i32>` 的函数，如果其中有值，就给该值加 1。
如果其中没有值，函数应返回 `None`，而不尝试执行任何操作。

借助 `match`，这个函数很容易编写，如示例 6-5 所示。

<Listing number="6-5" caption="对 `match` 使用 `Option<i32>` 表达式的函数">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

更详细地看看第一次执行 `plus_one`。调用 `plus_one(five)` 时，函数体中的变量
`x` 属于 `plus_one`，其值为 `Some(5)`。然后将它与每个 match 分支比较：

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

`Some(5)` 值不匹配 `None` 模式，因此继续下一个分支：

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

`Some(5)` 匹配 `Some(i)` 吗？匹配！它们是相同的变体。`i` 会绑定到 `Some`
中包含的值，因此 `i` 得到值 `5`。接着执行该 match 分支中的代码，给 `i` 的值
加 1，并创建一个新的 `Some` 值，其中包含总值 `6`。

现在考虑示例 6-5 中第二次调用 `plus_one` 的情况，此时 `x` 是 `None`。
进入 `match`，与第一个分支比较：

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

匹配！没有值可以相加，因此程序停止，并返回 `None` 右侧的 `=>` 值。由于
第一个分支已经匹配，不会再比较其他分支。

组合使用 `match` 和枚举在很多情况下都很有用。你会在 Rust 代码中经常看
到这种模式：对枚举使用 `match`，将变量绑定到其中的数据，然后根据数据
执行代码。起初可能有些棘手，但习惯后，你会希望所有语言都有这个功能。
它一直深受用户喜爱。

### 匹配属于穷举性的

还需讨论 `match` 表达式的另一个方面：分支的模式必须涵盖所有可能性。
看看下面这个版本的 `plus_one` 函数，它有一个 bug，无法编译：

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```


我们没有处理 `None` 的情况，因此这段代码会造成 bug。幸运的是，这是
Rust 能够捕获的 bug。尝试编译这段代码时，会得到下面的错误：

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust 知道我们没有覆盖所有可能情况，甚至知道遗漏了哪种模式！Rust 中的
匹配是*穷举性的*：为了让代码有效，必须穷尽所有可能性。特别是对于
`Option<T>`，Rust 强制我们显式处理 `None`，从而保护我们免受拥有空值却
假定拥有值的影响，也使前面讨论的数十亿美元错误不可能发生。

### 全包模式与 `_` 占位符

使用枚举，我们还可以对少数特定值采取特殊操作，而对所有其他值采取一种默认操作。设想我们正在实现一个游戏：当玩家掷出 3 点时，角色不移动，而会得到一顶漂亮的新帽子；当掷出 7 点时，角色会失去一顶漂亮的帽子；对于所有其他点数，角色都会在棋盘上移动相应数量的格子。下面是实现这一逻辑的 `match` 表达式，其中骰子的结果被硬编码，而不是随机生成的；其他操作都用没有函数体的函数表示，因为实现这些操作超出了本示例的范围：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```


对于前两个分支，模式是字面值 `3` 和 `7`。对于覆盖所有其他可能值的最后一个分支，模式是我们选择命名为 `other` 的变量。针对 `other` 分支运行的代码会使用这个变量：将它传递给 `move_player` 函数。

即使我们尚未列出 `u8` 的所有可能值，这段代码也会编译，因为最后一个模式会匹配所有未特别列出的值。这种全包模式满足 `match` 表达式必须穷尽所有情况的要求。请注意，我们必须把全包分支放在最后，因为模式是按顺序匹配的。若将全包分支放在前面，其他分支将永远不会运行，因此当我们在全包分支后添加分支时，Rust 会向我们发出警告！

Rust 还提供了一种模式，适用于我们想要匹配所有情况、但又不打算*使用*全包模式所匹配的值时：`_` 是一种特殊模式，它匹配任何值但不会绑定到该值。这告诉 Rust 我们不会使用这个值，因此 Rust 不会针对未使用的变量向我们发出警告。

我们再改变一次游戏规则：现在，当玩家掷出 3 或 7 以外的任何点数时，必须再投一次。我们不再需要使用全包模式匹配的值，因此修改代码，使用 `_` 而不是名为 `other` 的变量：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

这个示例同样满足穷举要求，因为我们在最后一个分支中明确忽略了所有其他值；没有任何情况被遗漏。

最后，我们再改变一次游戏规则：如果玩家掷出的不是 3 或 7，那么这一回合不发生任何其他事情。我们可以使用单元值（也就是在[“元组类型”][tuples]<!-- ignore -->一节中提到的空元组类型）作为 `_` 分支对应的代码来表达这一点：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

这里，我们明确告诉 Rust：对于不匹配前面分支中任何模式的其他值，我们不会使用它，也不希望在这种情况下运行任何代码。

关于模式和匹配的更多内容，我们将在[第 19 章][ch19-00-patterns]<!-- ignore -->介绍。现在，我们继续学习 `if let` 语法；在 `match` 表达式显得有些冗长的情况下，它会很有用。

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
