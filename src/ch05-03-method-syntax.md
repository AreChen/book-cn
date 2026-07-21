<a id="methods"></a>

## 方法

方法与函数类似：我们使用 `fn` 关键字和名称声明方法；方法可以有参数和返回值，
并包含从其他位置调用该方法时运行的代码。与函数不同，方法定义在结构体（或枚举
或特质对象）的上下文中，我们分别会在[第 6 章][enums]<!-- ignore -->和[第
18 章][trait-objects]<!-- ignore -->介绍枚举和特质对象；方法的第一个参数始终是
`self`，表示调用该方法的结构体实例。

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

<a id="method-syntax"></a>

### 方法语法

`area` 函数接收一个 `Rectangle` 实例作为参数；让我们把这个 `area` 函数改为定义在
`Rectangle` 结构体上的方法，如示例 5-13 所示。

<Listing number="5-13" file-name="src/main.rs" caption="定义 `area` 方法（位于 `Rectangle` 结构体上）">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

为了在 `Rectangle` 的上下文中定义这个函数，我们先开始一个 `impl`（实现）
`Rectangle` 代码块。这个 `impl` 块中的所有内容都与 `Rectangle` 类型相关联。然后，
我们把 `area` 函数移到 `impl` 的花括号中，并将签名中第一个（在本例中也是唯一的）
参数以及函数体中的对应部分改为 `self`。在 `main` 中，原来调用 `area` 函数并传入
`rect1` 作为参数，现在可以使用_方法语法_在实例上调用 `area` 方法；这个实例是
`Rectangle` 类型。
方法语法跟在实例后面：添加一个点，后面接方法名称、圆括号和任何参数。

在 `area` 的签名中，我们使用 `&self`，而不是 `rectangle: &Rectangle`。`&self`
实际上是 `self: &Self` 的缩写。在 `impl` 块中，类型 `Self` 是该 `impl` 块所针对
类型的别名。方法的第一个参数必须是名为 `self`、类型为 `Self` 的参数，因此 Rust
允许我们在第一个参数位置只使用名称 `self` 来缩写它。注意，仍然需要使用 `&` 来修饰
`self` 简写，以表示该方法借用 `Self` 实例，就像在 `rectangle: &Rectangle` 中一样。
方法可以取得 `self` 的所有权，可以像这里一样不可变地借用 `self`，也可以可变地借用
`self`，就像它们可以借用任何其他参数一样。

我们在这里选择 `&self`，原因与函数版本中使用 `&Rectangle` 相同：不想取得所有权，
只想读取结构体中的数据，而不是写入。如果想在方法执行过程中修改调用该方法的实例，
就会使用 `&mut self` 作为第一个参数。仅使用 `self` 作为第一个参数来取得实例所有权
的方法很少见；通常，只有当方法会将 `self` 转换为其他东西，并且希望阻止调用者在
转换后使用原始实例时，才会采用这种技术。

使用方法而不是函数的主要原因是组织代码，除此之外它还提供方法语法，并且不必在
每个方法的签名中重复 `self` 的类型。我们把对某种类型的实例可以执行的所有操作
放在一个 `impl` 块中，而不是让代码的未来用户在我们提供的库的各个位置搜索
`Rectangle` 的功能。

注意，可以让方法与结构体字段同名。例如，可以在 `Rectangle` 上定义名为 `width`
的方法：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

这里，我们让 `width` 方法返回 `true`（当实例的 `width` 字段值大于 `0` 时），否则
返回 `false`（当该值为 `0` 时）：在同名方法中可以出于任何目的使用字段。在 `main` 中，当
`rect1.width` 后面跟着圆括号时，Rust 知道我们指的是 `width` 方法；不使用圆括号时，
Rust 知道我们指的是 `width` 字段。

通常（但并非总是如此），当方法与字段同名时，我们希望它只返回字段中的值而不做
其他事情。这样的方法称为_获取器_，Rust 不会像某些其他语言那样为结构体字段自动
实现获取器。获取器很有用，因为可以将字段设为私有、将方法设为公开，从而把对该
字段的只读访问作为类型公开 API 的一部分。我们将在[第
7 章][public]<!-- ignore -->讨论公开和私有的含义，以及如何将字段或方法指定为公开
或私有。

<a id="wheres-the---operator"></a>

> ### `->` 运算符在哪里？
>
> 在 C 和 C++ 中，调用方法使用两种不同的运算符：直接在对象上调用方法时使用
> `.`；在指向对象的指针上调用方法并需要先解引用指针时使用 `->`。换句话说，如果
> `object` 是指针，`object->something()` 与 `(*object).something()` 类似。
>
> Rust 没有与 `->` 等价的运算符；相反，Rust 有一项称为_自动引用与解引用_的特性。
> 调用方法是 Rust 中少数具有这种行为的地方之一。
>
> 下面是它的工作原理：使用 `object.something()` 调用方法时，Rust 会自动添加 `&`、
> `&mut` 或 `*`，使 `object` 与方法的签名匹配。换句话说，下面两种写法相同：
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> 第一种写法看起来简洁得多。这种自动引用行为之所以有效，是因为方法有明确的
> 接收者，即 `self` 的类型。给定接收者和方法名称，Rust 可以明确判断方法是在读取
>（`&self`）、修改（`&mut self`）还是消耗（`self`）。Rust 让方法接收者的借用
> 隐式发生，是所有权在实践中易于使用的重要原因。

### 带有更多参数的方法

让我们通过在 `Rectangle` 结构体上实现第二个方法来练习使用方法。这次，我们希望
一个 `Rectangle` 实例接收另一个 `Rectangle` 实例；如果它可以
完全容纳，就返回 `true`；这个第二个 `Rectangle` 应位于 `self`（第一个 `Rectangle`）
中；否则返回 `false`。
也就是说，一旦定义了 `can_hold` 方法，就希望能够编写示例 5-14 中所示的程序。

<Listing number="5-14" file-name="src/main.rs" caption="使用尚未编写的 `can_hold` 方法">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

预期输出如下，因为 `rect2` 的两个尺寸都小于 `rect1` 的尺寸，而 `rect3` 比
`rect1` 更宽：

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

我们知道要定义一个方法，所以它会位于 `impl Rectangle` 块中。方法名是
`can_hold`，它会接收另一个 `Rectangle` 的不可变借用作为参数。通过查看调用方法的
代码，可以确定参数的类型：`rect1.can_hold(&rect2)` 传入 `&rect2`，它是对
`rect2`（一个 `Rectangle` 实例）的不可变借用。这很合理，因为我们只需要读取
`rect2`（而不是写入它；写入就需要可变借用），并且希望 `main` 保留 `rect2` 的所有权，
以便在调用 `can_hold` 方法后再次使用它。`can_hold` 的返回值是布尔值，实现会分别
检查 `self` 的宽度和高度是否大于另一个 `Rectangle` 的宽度和高度。让我们将新的
`can_hold` 方法添加到示例 5-13 的 `impl` 块中，如示例 5-15 所示。

<Listing number="5-15" file-name="src/main.rs" caption="实现 `can_hold` 方法（作用于 `Rectangle`，接收另一个 `Rectangle` 实例作为参数）">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

使用示例 5-14 中的 `main` 函数运行这段代码时，会得到期望的输出。方法可以在
`self` 参数之后将多个参数添加到签名中，这些参数的工作方式与函数参数相同。

### 关联函数

`impl` 块中定义的所有函数都称为_关联函数_，因为它们与 `impl` 后命名的类型相关联。
我们可以定义第一个参数不是 `self` 的关联函数（因而它们不是方法），因为它们不需要
使用该类型的实例。我们已经使用过这样一个函数：`String::from` 函数，定义在
`String` 类型上。

不是方法的关联函数通常用于构造函数，它们会返回结构体的新实例。这些函数通常叫作
`new`，但 `new` 不是特殊名称，也没有内置在语言中。例如，可以提供一个名为 `square`
的关联函数，它接收一个尺寸参数，并将该参数同时用作宽度和高度，从而更容易创建
正方形 `Rectangle`，而不必两次指定同一个值：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

返回类型和函数体中的 `Self` 关键字，是 `impl` 关键字之后出现的类型的别名，在本例
中就是 `Rectangle`。

要调用这个关联函数，需要对结构体名称使用 `::` 语法；`let sq = Rectangle::square(3);`
就是一个例子。这个函数位于结构体的命名空间中：`::` 语法既用于关联函数，也用于
模块创建的命名空间。我们将在[第 7 章][modules]<!-- ignore -->讨论模块。

### 多个 `impl` 块

每个结构体都可以有多个 `impl` 块。例如，示例 5-15 等价于示例 5-16 中的代码，
后者将每个方法放在自己的 `impl` 块中。

<Listing number="5-16" caption="使用多个 `impl` 块重写示例 5-15">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

在这里没有理由将这些方法拆分到多个 `impl` 块中，但这是有效的语法。我们会在第
10 章讨论泛型类型和特质时，看到多个 `impl` 块有用的情况。

## 总结

结构体让你可以创建对自身领域有意义的自定义类型。使用结构体可以将相关的数据片段
连接起来，并为每个片段命名，使代码清晰。在 `impl` 块中，可以定义与类型相关的
函数；方法是关联函数的一种，可以指定结构体实例具有的行为。

但结构体并不是创建自定义类型的唯一方式：接下来看看 Rust 的枚举功能，为工具箱
再增加一种工具。

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
