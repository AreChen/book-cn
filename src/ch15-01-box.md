## 使用 `Box<T>` 指向堆上数据

最简单的灵巧指针是 *匣子* ，其类型写为 `Box<T>`。匣子允许咱们存储数据于堆上，而非栈上。留在栈上的只是指向堆数据的指针。请参考 第 4 章 回顾栈和堆之间的区别。

除了在堆上而不是栈上存储他们的数据外，匣子数据结构并无性能开销。但他们也没有太多额外的能力。咱们将在以下这些情况下经常使用他们：

- 当咱们有个在编译时无法得知其大小的类型，而打算在需要精确大小的上下文中，使用这种类型的值时；
- 当咱们有着大量数据，而打算转移所有权，但要确保转移时数据不会被拷贝时；
- 当咱们打算拥有某个值，且只关心他是否实现特定特质，而非属于某种特定类型时。

我们将在 [“Enabling Recursive Types with
Boxes”](#enabling-recursive-types-with-boxes) 中演示第一种情况。在第二种情形下，转移大量数据的所有权会耗时很长，因为数据会在栈上来回拷贝。为了提升这种情况下的性能，我们可以存储大量数据于堆上的一个匣子中。然后，只有少量的指针数据在栈上来回拷贝，而他引用的数据保留在堆上的一处。第三种情况称为 *特质对象*，第 18 中的 [“Using Trait Objects to Abstract over Shared
Behavior”][trait-objects] 专门讨论这一主题。因此，咱们在这里学到的内容将在那个小节中再次应用！ <!-- ignore --> <!-- ignore -->

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### 在堆上存储数据

在讨论 `Box<T>` 的堆存储用例前，我们将介绍这一语法，以及怎样与 `Box<T>` 内存储的值交互。

下面清单 15-1 展示了怎样使用匣子在堆上存储 `i32` 的值：

<Listing number="15-1" file-name="src/main.rs" caption="Storing an `i32` value on the heap using a box">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

我们定义变量 `b` 为有着指向值 `Box` 的一个 `5` 值，而值 `b = 5` 分配在堆上。这个程序将打印 `b`；在这种情况下，我们可以访问匣子中的数据，就像我们访问栈上的这一数据一样。与任何自有值一样，当匣子超出作用域时，正如 `main` 在 main 结束处所做的那样，他将被解除内存分配（释放）。解除内存分配会针对匣子（存储在栈上）和他指向的数据（存储在堆上）同时发生。

在堆上放置单个值并不是很有用，因此咱们不会经常以这种方式单独使用匣子。在大多数情况下，让 i32 这样的值处于他们默认存储所在的栈上更为合适。我们来看看一种情形，其中匣子允许我们定义一些，在没有匣子数据结构时我们不被允许定义的类型。 `i32`

<a id="enabling-recursive-types-with-boxes"></a>

### 通过匣子数据结构得到递归类型

*递归类型* 的值，可以将同一类型的另一个值作为自身的一部分。递归类型会带来一个问题，因为 Rust 需要在编译时知道类型占用了多少空间。然而，递归类型的值的嵌套理论上可以无限地延续，因此 Rust 无法知道该值需要多少空间。由于匣子有着已知大小，我们可以通过在递归类型定义中插入匣子来得到递归类型。

作为递归类型的示例，我们来探讨一下 *构造列表，cons list*（the *cons list*）。这是一种常见于函数式编程语言中的数据类型。除了递归外，我们将定义的构造列表类型很简单；因此，当咱们遇到涉及递归类型的更复杂的情况时，我们将使用的示例中的概念将很有用。

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### 理解构造列表

所谓 *构造列表*，是 Lisp 编程语言及其方言中的数据结构，由嵌套对构成，是 Lisp 版本的链表。他的名称来自 Lisp 中的 `cons` 函数（*construct function* 的缩写），该函数会根据他的两个参数构造一个新的对。通过对由一个值和另一个对组成的对调用 `cons`，我们可以构造由递归对组成的构造列表。

例如，下面是个构造列表的伪代码表示，包含列表 `1, 2, 3`，其中每个位于括号中：

```text
(1, (2, (3, Nil)))
```

构造列表中的每个项目都包含两个元素：当前项目的值和下一个项目的值。列表中的最后一个项目仅包含一个名为 `Nil` 的值，而没有下一项目。构造列表是通过递归调用 `cons` 函数产生的。表示递归基础情形的规范名称是 `Nil`。请注意，这与第 6 章中讨论的 “null” 或 “nil” 概念不同，后者属于无效或不存在的值。

构造列表不是 Rust 中的常用数据结构。大多数时候，当咱们在 Rust 中有个项目列表时，使用 `Vec<T>` 是种更好的选择。在其他时间，更复杂的递归数据类型在各种情况下 *都* 很有用，但从这一章中的构造列表开始，我们可以探讨匣子数据结构，怎样让我们不受干扰地定义递归数据类型。

下面清单 15-2 包含用于构造列表的枚举定义。请注意，这段代码还不会编译，因为其中的 `List` 类型没有已知的大小，我们将演示这点。

<Listing number="15-2" file-name="src/main.rs" caption="The first attempt at defining an enum to represent a cons list data structure of `i32` values">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> **注意**：我们正在出于这个示例的目的，实现一个仅包含 `i32` 值的构造列表。正如我们在第 10 章中讨论的那样，我们本可以使用泛型来实现，定义一种可以存储任何类型值的构造列表。

使用这个 `List` 类型来存储列表 `1, 2, 3`，将看起来像下面清单 15-3 中的代码：

<Listing number="15-3" file-name="src/main.rs" caption="Using the `List` enum to store the list `1, 2, 3`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

其中第一个 `Cons` 包含 `1` 和另一个 `List` 值。这个 `List` 值是另一个 `Cons` 值，其中包含 `2` 与另一个 `List`。这个 `List` 值又是另一个 `Cons` 值，其中包含 `3` 和一个 `List` 值，该值最终为 `Nil`，表示列表结束的非地归变种。

当我们尝试编译清单 15-3 中的代码时，我们会得到下面清单 15-4 中所示的报错：

<Listing number="15-4" caption="The error we get when attempting to define a recursive enum">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

报错显示这种类型“有着无限大小，has infinite size”。原因是咱们以递归的变种定义了 `List`：他直接包含本身的另一个值。因此，Rust 无法计算出存储 `List` 值需要多少空间。我们来分析一下为什么我们会得到这个报错。首先，我们将看看，Rust 如何决定存储非递归类型需要多少空间。

#### 计算非递归类型的大小

回顾咱们在第 6 章中讨论枚举定义时，在 清单 6-2 中定义的 `Message` 枚举：

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

为了确定为 `Message` 值分配多少空间，Rust 会遍历每个变种，以发现哪个变种需要最多的空间。Rust 发现 `Message::Quit` 不需要任何空间，`Message::Move` 需要足够的空间来存储两个 `i32` 值，以此类推。由于只有一个变种会被用到，因此 `Message` 值所需的最大内存空间，便是存储最大变种将占用的空间。

与 Rust 尝试确定像是清单 15-2 中的 `List` 枚举，这样的递归类型需要多少空间时的情况对比这一过程。编译器首先查看 `Cons` 变种，他包含一个 `i32` 类型的值和一个 `List` 类型的值。因此，`Cons` 需要的空间量等于 `i32` 的大小加上 `List` 的大小。为了计算出 `List` 类型需要多少内存，编译器会从 `Cons` 变种开始查看变种。 `Cons` 变种包含一个 `i32` 类型的值和一个 `List` 类型的值，而这个过程会无限地继续下去，如图 15-1 中所示。

由无限个 Cons 变种构成的无限 List

**图 15-1**：由无限个 `List` 变种构成的无限 `Cons`

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### 获得已知大小的递归类型

因为 Rust 无法计算出要为递归定义的类型分配多少空间，所以编译器给出了带有下面这个有用的建议的报错：

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

在这个建议中，*indirection* 意味着我们不应直接存储值，而应修改数据结构为通过存储指向值的指针间接存储值。

因为 `Box<T>` 是个指针，Rust 总是知道 `Box<T>` 需要多少空间：指针的大小不会根据他指向的数据量而改变。这意味着我们可以放置一个 `Box<T>` 在 `Cons` 变种内，而不是直接放置另一个 `List` 值。`Box<T>` 将指向下一个 `List` 值，该值将在堆上而不是在 `Cons` 变种内。从概念上讲，我们仍然有个列表，他是以包含其他列表的列表创建的，但这种实现方式现在更像是彼此相邻地放置项目，而非嵌套在彼此之中。

我们可以把清单 15-2 中 `List` 枚举的定义，以及清单 15-3 中 `List` 的用法，修改为下面清单 15-5 中的代码，这段代码将编译。

<Listing number="15-5" file-name="src/main.rs" caption="The definition of `List` that uses `Box<T>` in order to have a known size">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

`Cons` 变种需要一个 `i32` 的大小，加上存储匣子指针数据的空间。`Nil` 变种不存储值，因此他需要比 `Cons` 变种更少的栈上空间。现在我们知道，任何 `List` 值都会占用一个 `i32` 的大小加上一个匣子的指针数据的大小。通过使用匣子，我们打破了无限的递归链，因此编译器可以计算出存储 `List` 值所需的内存大小。下图 15-2 展示了 `Cons` 变种现在的样子：

不是无限大小的 List，因为 Cons 包含一个 Box

**图 15-02**：不是无限大小的 `List`，因为 `Cons` 包含一个 `Box`

匣子数据结构仅提供间接性和堆分配；他们不具备任何别的特殊能力，就像我们在其他灵巧指针类型中看到的那样。他们也没有这些特殊能力带来的性能开销，因此在像构造列表这样的，其中间接性是我们唯一需要的特性的情况下会非常有用。我们将在第 18 中，讨论匣子数据结构的更多用例。

`Box<T>` 类型属于灵巧指针，因为他实现了 `Deref` 特质，该特质允许 `Box<T>` 值可以像引用一样对待。当 `Box<T>` 值超出作用域时，由于 `Drop` 特质的实现，匣子指向的堆数据也会被清理。对于我们将在这一章其余部分中讨论的其他灵巧指针提供的功能，这两个特质将更加重要。我们来更详细地探讨这两个特质。

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
