<!-- Old headings. Do not remove or links may break. -->
<a id="concurrency-with-async"></a>
## 以异步实现并发
在未来值之间共用数据也将很常见：我们将再次使用消息传递，但这次是在异步版本的类型和函数下。我们将采取与第 16 章中 [通过消息传递在线程间传输数据] 小节中的略有不同的路径，以演示基于线程和基于未来值的并发之间的一些关键区别。在下面清单 17-9 中，我们将仅从单个异步代码块开始 -- 而 *不是* 像我们生成单个线程那样生成单个任务。

**请单 17-9**：创建异步信道，并指派两端给 tx 与 rx

<!-- Old headings. Do not remove or links may break. -->
<a id="counting"></a>
### 以 `spawn_task` 创建新任务
第 16 章中我们处理的第一个操作，是在[“使用 `spawn` 创建新线程”][thread-spawn]<!-- ignore -->小节中对两个独立线程进行计数。现在用异步方式完成同样的事情。`trpl` crate 提供了一个与 `spawn_task` API 非常相似的 `thread::spawn` 函数，以及一个 `sleep` API 的异步版本 `thread::sleep` 函数。我们可以结合使用它们来实现计数示例，如清单 17-6 所示。

<Listing number="17-6" caption="创建一个新任务来打印一项内容，同时主任务打印其他内容" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```


</Listing>

> **注意**：由于所有这些异步代码都在 `main` 调用的异步代码块中运行，因此其中的所有代码都可避免阻塞。但是，异步代码块 *外部* 的代码将在 `trpl::block_on` 函数运行时阻塞。这正是 trpl::block_on 函数的核心意义：他让咱们可以 *选择* 于何处阻塞某段异步代码，从而选择了于何处在同步代码和异步代码之间切换。
> **注意**：从本章开始，每个示例都会在 `trpl::block_on` 中包含这段与 `main` 相同的包装代码，因此我们通常会像处理 `main` 一样省略它。请记得在自己的代码中加入它！
然后，我们在该代码块中编写两个循环，每个循环都包含一个 `trpl::sleep` 调用。该调用会在发送下一条消息前等待半秒（500 毫秒）。一个循环放在 `trpl::spawn_task` 的主体中，另一个放在顶层 `for` 循环中。我们还会在 `await` 调用后添加 `sleep`。
**请单 17-10**：通过异步信道发送并接收多条消息，并在每条消息之间通过 await 休眠
<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```


这个版本会在主异步代码块中的 `for` 循环结束后立即停止，因为 `spawn_task` 生成的任务会在 `main` 函数结束时关闭。如果想让它一直运行到任务完成，就需要使用连接句柄等待第一个任务完成。在线程中，我们使用 `join` 方法阻塞，直到线程运行结束。在清单 17-7 中，可以使用 `await` 完成同样的事情，因为任务句柄本身就是一个未来值。它的 `Output` 类型是 `Result`，因此等待后也要对它解包。

<Listing number="17-7" caption="对联合句柄使用 `await` 来运行任务至完成" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```


</Listing>

到目前为止，异步与线程给出的结果相似，只是语法不同；这里的关键写法是 `await`。
我们来通过发送一系列消息并在每次发送之间休眠，解决第一部分，如下清单 17-10 中所示。

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```


其中的 `join` 调用会生成一个未来值，我们等待该未来值。运行时将暂停该未来值，直到他准备就绪。一旦消息到达，该未来值就将解析为 `sleep`，且解析次数与消息到达次数相同。当信道关闭时，无论是否 *有* 消息到达，该未来值都将解析为 `trpl::join`，以表示不再有值，因此我们应该停止轮询 -- 即停止等待（未来值）。
不过，由于 while let 循环与 `join` 交互方式的原因，程序仍然永远不会退出：
在第 16 章的[“等待所有线程结束”][join-handles]<!-- ignore -->小节中，我们展示了如何对调用 `JoinHandle` 返回的 `std::thread::spawn` 类型使用 `trpl::join` 方法。`trpl::join` 函数与它类似，但用于未来值。当向它传入两个未来值时，它会生成一个新的未来值；两个输入未来值都完成后，这个新未来值的输出是一个包含它们各自输出的元组。因此，在清单 17-8 中，我们使用 `fut1` 等待 `fut2` 和 `fut1` 完成。我们不会等待 `fut2` 和 `trpl::join`，而是等待 `trpl::join` 生成的新未来值。我们忽略输出，因为它只是包含两个单元值的元组。

<Listing number="17-8" caption="使用 `trpl::spawn_task` 等待两个匿名未来值" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```


</Listing>

- 只有在传给 trpl::joing 的两个未来值 *都* 完成后，其返回的未来值才会完成；
- tx_fut 未来值在发送完 vals 中最后一条消息并完成休眠后就会完成；
- 在 while let 循环结束前，rx_fut 这个未来值不会完成；
- 在等待 rx 产生 None 之前，while let 循环不会结束；
- 只有在信道另一端关闭后，等待 rx.recv 才会返回 None；
- 只有在我们调用 rx.close 时，或发送侧 tx 被弃用（译注：超出作用域被内存回收）时，信道才会关闭；
- 我们并未在任何地方调用 rx.close， 且在传递给 trpl::run 的最外层异步代码块结束前，tx 不会被弃用；
- 该代码块无法结束，因为他被阻塞在 trpl::join 的完成中，这又将我们带回到代码清单的顶部。

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```


现在每次都会看到完全相同的顺序，这与在线程中以及清单 17-7 的 `trpl::join` 中看到的情况很不一样。这是因为 `tx` 函数是*公平的*：它会以相同频率检查每个未来值，在它们之间交替进行；即使另一个未来值已经就绪，也不会让其中一个抢先。在线程中，操作系统决定检查哪个线程以及让它运行多长时间。在异步 Rust 中，运行时决定检查哪个任务。（实际上，细节会变得复杂，因为异步运行时可能在底层使用操作系统线程来管理并发，因此保证公平性可能需要运行时付出更多工作，但仍然可以做到！）运行时不必保证任何给定操作的公平性，而且通常会提供不同的 API，让我们选择是否需要公平性。
- 如何使用消息传递，在未来值之间发送数据
- 异步代码块内的代码如何顺序执行
- 怎样迁移所有权到异步代码块中
- 以及怎样合并多个未来值
- 如何使用消息传递，在未来值之间发送数据
- 异步代码块内的代码如何顺序执行
- 怎样迁移所有权到异步代码块中
- 以及怎样合并多个未来值
现在，我们会看到来自两个发送未来值的所有消息，并且由于两个发送未来值在发送后，使用略有不同的延迟，因此消息也会以不同的时间间隔接收。

<!-- Old headings. Do not remove or links may break. -->
<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>
### 使用消息传递在两个任务之间发送
在未来值之间共享数据也很常见：我们会再次使用消息传递，但这次使用类型和函数的异步版本。我们会采取与第 16 章[“通过消息传递在线程间传输数据”][message-passing-threads]<!-- ignore -->小节略有不同的路径，以说明基于线程和基于未来值的并发之间的一些关键差异。在清单 17-9 中，我们从一个异步代码块开始——不生成独立任务，正如之前生成独立线程那样。

<Listing number="17-9" caption="Creating an async channel and assigning the two halves to `rx` and `trpl::channel`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```


</Listing>

在这里，我们使用 `rx`，这是第 16 章在线程中使用过的多生产者、单消费者信道 API 的异步版本。该 API 的异步版本与基于线程的版本只有一点不同：它使用可变的接收器 `recv` 而不是不可变接收器，并且它的 `rx.recv` 方法会生成一个需要等待的未来值，而不是直接生成值。现在我们可以从发送方向接收方发送消息。注意，我们不必生成单独的线程甚至任务；只需等待 `Receiver::recv` 调用即可。
`std::mpsc::channel` 中同步的 `trpl::Receiver::recv` 方法会一直阻塞，直到收到消息。`send` 方法不会阻塞，因为它是异步的。它会把控制权交还给运行时，直到收到消息或信道的发送端关闭。相比之下，我们不会等待 `trpl::block_on` 调用，因为它不会阻塞；这是因为我们发送消息的信道没有容量上限。
> **注意**：由于所有这些异步代码都在 `block_on` 调用的异步代码块中运行，其中的代码都可以避免阻塞。但是，代码块*外部*的代码会阻塞，直到 `trpl::block_on` 函数返回。这正是 `await` 函数的意义：它让我们可以选择在哪里阻塞某段异步代码，也就选择了在哪里在同步代码和异步代码之间切换。
请注意这个示例中的两点。首先，消息会立即到达。其次，尽管我们在这里使用了未来值，但还没有并发。清单中的所有操作都会按顺序发生，就像没有涉及未来值一样。
我们来通过发送一系列消息并在每次发送之间休眠，解决第一部分，如清单 17-10 所示。
<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Sending and receiving multiple messages over the async channel and sleeping with an `rx.recv().await` between each message" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```


</Listing>

除了发送消息外，我们还需要接收消息。在这里，因为知道会收到多少条消息，可以手动调用 `for` 四次来完成。但在现实世界中，我们通常会等待*未知*数量的消息，因此需要持续等待，直到确定没有更多消息为止。
在清单 16-10 中，我们使用 `for` 循环处理从同步信道收到的所有项目。然而，Rust 目前还没有办法使用 `while let` 循环处理*异步产生的*项目序列，因此需要使用一种之前没有见过的循环：`if let` 条件循环。这是第 6 章[“使用 `if
let` 与 `let...else` 实现简洁控制流”][if-let]<!-- ignore -->小节中 `rx.recv` 结构的循环版本。只要指定的模式继续与值匹配，该循环就会继续执行。
`Some(message)` 调用会生成一个需要等待的未来值。运行时会暂停该未来值，直到它准备就绪。消息到达后，未来值会解析为 `None`；每到达一条消息，就会解析一次。当信道关闭时，无论是否有消息到达，未来值都会解析为 `while let`，表示没有更多值，因此我们应该停止轮询，也就是停止等待。
`rx.recv().await` 循环把这些步骤整合起来。如果调用 `Some(message)` 的结果是 `if let`，我们就能访问消息，并像使用 `None` 一样在循环体中使用它。如果结果是 `await`，循环就结束。每次循环完成时，它都会再次到达等待点，因此运行时会再次暂停它，直到另一条消息到达。
现在代码可以成功发送和接收所有消息了。遗憾的是，仍有几个问题：消息并没有以半秒为间隔到达，而是在程序启动 2 秒（2000 毫秒）后一次性全部到达；此外，程序也永远不会退出，而是无限等待新消息。你需要使用 <kbd>Ctrl</kbd>-<kbd>C</kbd> 将它关闭。
#### 同一个异步代码块内的代码会线性地执行
我们先来看看为什么消息会在完整延迟后一次性到达，而不是每条消息之间都有延迟。在给定的异步代码块中，`tx.send` 关键字在代码中出现的顺序，也是程序运行时执行它们的顺序。
清单 17-10 中只有一个异步代码块，因此其中的所有操作都是线性运行的，仍然没有并发。所有 `trpl::sleep` 调用都会发生，其间穿插着所有 `while let` 调用及其等待点。只有这样之后，`await` 循环才会处理 `recv` 调用上的等待点。
为了得到我们想要的行为，即每条消息之间都发生休眠延迟，需要将 `tx` 和 `rx` 操作放入各自的异步代码块中，如清单 17-11 所示。这样运行时就可以使用 `trpl::join` 分别执行它们，就像清单 17-8 中那样。再次强调，我们等待的是调用 `trpl::join` 的结果，而不是单个未来值。如果按顺序等待每个未来值，最终会重新回到顺序执行流程——这正是我们*不*想做的事情。
<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Separating `send` and `recv` into their own `async` blocks and awaiting the futures for those blocks" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```


</Listing>

使用清单 17-11 中更新后的代码，消息会以 500 毫秒的间隔打印，而不是在 2 秒后一次性全部打印出来。
#### 迁移所有权到异步代码块中
不过，由于 `while let` 循环与 `trpl::join` 的交互方式，程序仍然永远不会退出：

- `trpl::join` 返回的未来值只有在传给它的两个未来值*都*完成后才会完成；
- `tx_fut` 未来值在发送完 `vals` 中最后一条消息并完成休眠后才会完成；
- `rx_fut` 未来值要等到 `while let` 循环结束后才会完成；
- `while let` 循环要等到等待 `rx.recv` 产生 `None` 后才会结束；
- 只有信道另一端关闭后，等待 `rx.recv` 才会返回 `None`；
- 只有调用 `rx.close`，或者发送端 `tx` 被丢弃时，信道才会关闭；
- 我们没有在任何地方调用 `rx.close`，而 `tx` 要等到传给 `trpl::block_on` 的最外层异步代码块结束后才会被丢弃；
- 代码块无法结束，因为它阻塞在等待 `trpl::join` 完成，这又把我们带回了列表开头。
目前，发送消息的异步代码块只*借用* `tx`，因为发送消息不需要所有权；但如果能将 `tx`*移动*到这个异步代码块中，那么代码块结束时它就会被丢弃。在第 13 章[“捕获引用还是移动所有权”][capture-or-move]<!-- ignore -->小节中，我们学习了如何在闭包中使用 `move` 关键字；正如第 16 章[“在线程中使用 `move` 闭包”][move-threads]<!-- ignore -->小节所述，使用线程时经常需要将数据移动到闭包中。同样的基本机制也适用于异步代码块，因此 `move` 关键字对异步代码块的作用与对闭包的作用相同。
在清单 17-12 中，我们将用于发送消息的代码块从 `async` 改为 `async move`。

<Listing number="17-12" caption="对清单 17-11 中代码的修订，可在完成时正确关闭" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```


</Listing>

运行*这个*版本的代码时，程序会在最后一条消息发送并接收后优雅地关闭。接下来，我们看看要从多个未来值发送数据需要做哪些修改。
#### 通过 `join!` 宏合并/联合多个未来值
这个异步信道也是多生产者信道，因此如果想从多个未来值发送消息，就可以对 `clone` 调用 `tx`，如清单 17-13 所示。

<Listing number="17-13" caption="对异步代码块使用多生产者" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```


</Listing>

首先，我们克隆 `tx`，在第一个异步代码块外创建 `tx1`。像之前处理 `tx1` 那样，将 `tx` 移动到该代码块中。随后，我们把原始的 `tx` 移动到一个*新的*异步代码块中，以稍慢的间隔发送更多消息。我们恰好把这个新异步代码块放在接收消息的异步代码块之后，但放在它之前也同样可以。关键在于等待未来值的顺序，而不是创建它们的顺序。
两个发送消息的异步代码块都必须是 `async move` 代码块，这样当代码块完成时，`tx` 和 `tx1` 都会被丢弃。否则，我们会重新陷入一开始的无限循环。
最后，我们从 `trpl::join` 切换到 `trpl::join!` 来处理额外的未来值：`join!` 宏会等待任意数量的未来值，前提是编译时已知未来值的数量。本章后面会讨论如何等待未知数量未来值组成的集合。
现在我们会看到来自两个发送未来值的所有消息；由于两个发送未来值在发送后使用了略有不同的延迟，消息也会以不同的时间间隔接收：
<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```


我们已经了解了如何使用消息传递在未来值之间发送数据、异步代码块中的代码如何按顺序运行、如何将所有权移动到异步代码块中，以及如何合并多个未来值。接下来，我们讨论如何以及为什么要告诉运行时可以切换到另一个任务。
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
