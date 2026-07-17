<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## 流：序列中的未来值

回顾在这一章早先 [“Message Passing”][17-02-messages] 小节中，我们对异步信道使用接收器的方式。异步的 `recv` 方法会随着时间推移生成项目序列。这属于一种称为 *流* 的更通用模式的实例。许多概念都自然地以流的形式呈现：项目以队列形式变得可用、当完整数据集相对计算机内存过大而从文件系统中增量提取的数据块，或是随时间推移通过网络到达的数据。由于流属于未来值，我们可以像使用任何其他类型的未来值一样使用他们，并以有趣的方式组合他们。例如，我们可以批量处理事件以避免触发过多的网络调用，可以对长时间运行的操作序列设置超时，或者对用户接口事件限流，以避免执行不必要的工作。 <!-- ignore -->

我们在第 13 章中 [“The Iterator Trait and the `next` Method”][iterator-trait] 小节研究迭代器时，曾见到过条目序列，但迭代器与异步信道接收器之间有两个区别。第一个区别是时间：迭代器是同步的，而信道接收器是异步的。第二个区别是 API。在直接使用 `Iterator` 时，我们调用他的同步的 `next` 方法。而特别是对于 `trpl::Receiver` 流，我们调用他的异步的 `recv` 方法。除此之外，这些 API 感觉非常相似，而这种相似性并非偶然。流就像迭代的异步形式。尽管 `trpl::Receiver` 专门等待接收消息，而通用的流 API 则范围更广：他以 `Iterator` 的方式提供下一项目，但以异步方式。 <!--
ignore -->

Rust 中迭代器与流之间的相似性，意味着我们实际上可以从任何迭代器创建流。与迭代器一样，我们通过调用流的 `next` 方法然后等待输出来使用流，如下清单 17-30 中所示，其尚不会编译。

<Listing number="17-21" caption="Creating a stream from an iterator and printing its values" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

我们以一个数字数组开始，将其转换为迭代器，然后调用 `map` 将所有值翻倍。然后我们使用 `trpl::stream_from_iter` 函数转换该迭代器为流。接下来，我们以 `while let` 循环在该流中的项目到达时遍历他们。

不幸的是，当我们尝试运行代码时，他不会编译，而是报告没有可用的 `next` 方法：

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

正如这一输出所解释的，编译器报错的原因是，我们需要作用域中的正确特质，才能使用 `next` 方法。根据我们到目前为止的讨论，咱们可能会合理地认为该特质是 `Stream`，但他实际上是 `StreamExt`。`Ext` 是 *extension* 的缩写，属于 Rust 社区中用于以一个特质扩展另一特质的常见模式。

`Stream` 特质定义了一个底层接口，其有效地结合了 `Iterator` 和 `Future` 特质。`StreamExt` 在 `Stream` 之上提供了一组更高层次的 API，包括 `next` 方法以及类似于 `Iterator` 特质提供的其他实用方法。`Stream` 和 `StreamExt` 目前均尚不属于 Rust 标准库的一部分，但大多数生态系统代码箱都使用类似的定义。

这一编译器报错的解决方法是，添加一个 `use` 的 `trpl::StreamExt` 语句，如下清单 17-22 中所示。

<Listing number="17-22" caption="Successfully using an iterator as the basis for a stream" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

在本章末尾，我们将对 `StreamExt` 与 StreamExt 两个特质进行更详细的解释，但现在咱们只需知道，Stream 特质定义了个可有效地结合 Iterator 与 Future 特质的底层接口。而 StreamExt 则在 Stream 之上，提供了一组更高级别的 API，包括 next 方法以及与由 Iterator 特质所提供的类似其他工具方法。Stream 与 StreamExt 还不是 Rust 标准库的一部分，但大多数生态代码箱，都使用了这同样的定义。

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
