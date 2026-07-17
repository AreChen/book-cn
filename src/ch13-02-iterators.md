## 以迭代器处理一系列项目
迭代器模式允许咱们依次对一系列项目执行某些任务。所谓迭代器，负责遍历每个项目以及判断序列何时结束的逻辑。当咱们使用迭代器时，咱们不必自己重新实现该逻辑。

还要注意，我们从调用 `v1` 获取的值，属于对矢量中的值的不可变引用。`iter` 方法会生成一个对不可变引用的迭代器。当我们打算创建一个会取得 `Vec<T>` 的所有权并返回自有的值时，我们可以调用 into_iter 而不是 iter。同样的，当我们打算遍历可变引用时，可以调用 iter_mut 而不是 iter。

<Listing number="13-10" file-name="src/main.rs" caption="创建迭代器">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```


</Listing>

我们不允许在调用 `v1_iter` 之后再使用 `for`，因为 sum 取我们对其调用他的迭代器的所有权。
在清单 13-11 的示例中，我们将迭代器的创建与 `for` 循环中的使用分开。当使用 `for` 中的迭代器调用 `v1_iter` 循环时，迭代器中的每个元素都会在循环的一次迭代中使用，并打印出每个值。

<Listing number="13-11" file-name="src/main.rs" caption="在 `for` 循环中使用迭代器">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```


</Listing>

在没有标准库提供迭代器的语言中，我们通常需要从索引为 0 的变量开始，使用这个变量索引矢量来获取值，然后在循环中递增变量，直到它达到矢量中的项目总数，才能编写相同的功能。
迭代器为我们处理了所有这些逻辑，减少了可能出错的重复代码。迭代器让我们可以更灵活地对许多不同类型的序列使用相同的逻辑，而不仅仅是可以像矢量一样进行索引的数据结构。下面来看看迭代器是如何做到这一点的。
### `Iterator` 特质与 `next` 方法
所有迭代器都实现标准库定义的 `Iterator` 特质。特质的定义如下：

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```


请注意，这个定义使用了一些新语法：`type Item` 与 `Self::Item`，它们定义了这个特质下的关联类型。我们将在第 20 章中深入探讨关联类型。目前只需知道，实现 `Iterator` 特质需要同时定义一个 `Item` 类型，而这个 `Item` 类型会用于 `next` 方法的返回类型中。换言之，`Item` 类型将是迭代器返回的类型。
`Iterator` 特质只要求实现者定义一个方法：`next` 方法。它每次返回迭代器中的一个项目，并将其包装在 `Some` 中；迭代结束时返回 `None`。
我们可以直接在迭代器上调用 `next` 方法；清单 13-12 演示了对从矢量创建的迭代器反复调用 `next` 时会返回哪些值。

<Listing number="13-12" file-name="src/lib.rs" caption="对迭代器调用 `next` 方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```


</Listing>

请注意，我们需要将 `v1_iter` 设为可变：调用迭代器上的 `next` 方法会改变迭代器的内部状态，迭代器用它来跟踪自己在序列中的位置。换句话说，这段代码会“消费”迭代器，也就是用尽迭代器。每次调用 `next` 都会取走迭代器中的一个项目。当我们使用 `v1_iter` 循环时，不需要将 `for` 设为可变，因为循环取得了 `v1_iter` 的所有权，并在幕后将它设为可变。
还要注意，我们从调用 `next` 得到的值，是对矢量中值的不可变引用。`iter` 方法会生成一个遍历不可变引用的迭代器。如果想创建一个取得 `v1` 所有权并返回自有值的迭代器，可以调用 `into_iter` 而不是 `iter`。同样，如果想遍历可变引用，可以调用 `iter_mut` 而不是 `iter`。
### 消费迭代器的方法
`Iterator` 特质有许多由标准库提供默认实现的方法；可以查阅标准库 API 文档中的 `Iterator` 特质来了解这些方法。其中一些方法会在定义中调用 `next`，这就是实现 `next` 特质时必须实现 `Iterator` 方法的原因。
调用 `next` 的方法称为“消费适配器”，因为调用它们会耗尽迭代器。一个例子是 `sum` 方法：它取得迭代器的所有权，并通过反复调用 `next` 遍历项目，从而消费迭代器。遍历过程中，它会把每个项目加到运行总和中，并在迭代完成后返回总和。清单 13-13 中有一个测试，演示了 `sum` 方法的用法。

<Listing number="13-13" file-name="src/lib.rs" caption="调用 `sum` 方法获取迭代器中所有项目的总和">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```


</Listing>

调用 `v1_iter` 后不允许再使用 `sum`，因为 `sum` 会取得我们调用它的迭代器的所有权。
### 产生其他迭代器的方法
所谓迭代器适配器，是定义在 `Iterator` 特质中的方法，它们不会消费迭代器。相反，它们会通过改变原始迭代器的某些方面来生成不同的迭代器。
清单 13-14 展示了调用迭代器适配器方法 `map` 的示例。该方法接收一个闭包，在遍历迭代器项目时对每个项目调用这个闭包。`map` 方法返回一个生成修改后项目的新迭代器。此处的闭包会创建一个新迭代器，使矢量中的每个项目都增加 1。

<Listing number="13-14" file-name="src/main.rs" caption="调用迭代器适配器 `map` 来创建新的迭代器">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```


</Listing>

但是，这段代码会产生一条警告：

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```


清单 13-14 中的代码没有执行任何操作；我们指定的闭包从未被调用。警告提醒了我们原因：迭代器适配器是惰性的，因此这里需要消费迭代器。
闭包捕获环境中的 `collect` 参数，并与每双鞋子比较该值，仅保留指定尺码的鞋子。最后，调用 `env::args` 方法收集将调整后的迭代器返回的值，到一个该函数返回的矢量中。
在清单 13-15 中，我们将遍历调用 `map` 返回的迭代器所得到的结果收集到一个矢量中。这个矢量最终会包含原矢量中的每个项目，并且每个项目都增加 1。

<Listing number="13-15" file-name="src/main.rs" caption="调用 `map` 方法创建一个新的迭代器，然后调用 `collect` 方法消费新的迭代器并创建一个矢量值">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```


</Listing>

由于 `map` 接收一个闭包，因此可以指定想对每个项目执行的任意操作。这很好地展示了闭包如何让我们在复用 `Iterator` 特质提供的迭代行为的同时，自定义部分行为。
我们可以链式调用多个迭代器适配器，以可读的方式执行复杂操作。但由于所有迭代器都是惰性的，因此必须调用某个消费适配器方法，才能得到调用迭代器适配器的结果。
<!-- Old headings. Do not remove or links may break. -->
<a id="using-closures-that-capture-their-environment"></a>
### 捕获环境的闭包
许多迭代器适配器会接收闭包作为参数，而我们通常指定给迭代器适配器的闭包会捕获它们的环境。
在这个示例中，我们将使用接收闭包的 `filter` 方法。闭包从迭代器中取得一个项目并返回 `bool`。如果闭包返回 `true`，该值就会包含在 `filter` 生成的迭代器中；如果闭包返回 `false`，该值就不会被包含。
在清单 13-16 中，我们使用一个捕获环境中 `filter` 变量的闭包调用 `shoe_size`，遍历 `Shoe` 结构体实例的集合。它只会返回指定尺码的鞋子。

<Listing number="13-16" file-name="src/lib.rs" caption="以一个捕获 `filter` 的闭包使用 `shoe_size` 方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```


</Listing>

测试表明，当我们调用 `shoes_in_size` 时，返回的只有与指定的值相同尺码的鞋子。

在 `shoes_in_size` 的主体中，我们调用 `into_iter` 来创建一个取得矢量所有权的迭代器。然后调用 `filter`，将该迭代器调整为一个新迭代器，只包含闭包返回 `true` 的元素。
闭包从环境中捕获 `shoe_size` 参数，并将该值与每双鞋的尺码比较，只保留指定尺码的鞋子。最后，调用 `collect` 将调整后迭代器返回的值收集到函数返回的矢量中。
测试表明，调用 `shoes_in_size` 时，返回的只有与指定值尺码相同的鞋子。
