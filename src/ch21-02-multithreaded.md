<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>
## 从单线程服务器到多线程服务器
目前，服务器将依次处理每个请求，这意味着在第一个连接处理完毕之前，他不会处理第二个连接。当服务器收到越来越多的请求时，这种串行执行将越来越不理想。当服务器收到一个需要很长时间处理的请求时，后续请求就必须等该该请求处理完毕，即使这些新请求可被快速处理。我们需要解决这个问题，但首选我们将看看实际操作中的问题。

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>
### 模拟慢速请求
我们将探讨处理慢速请求会怎样影响向当前服务器发出的其他请求。下面清单 21-10 实现了通过模拟慢速响应来处理对 /sleep 的请求，这将导致服务器在响应之前休眠 5 秒钟。

<Listing number="21-10" file-name="src/main.rs" caption="通过休眠 5 秒来模拟慢速请求">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```


</Listing>

现在我们有三种情况，于是已从 `if` 切换为 `match`。我们需要显式地对 `request_line` 的一个切片匹配，以与字符串字面值模式匹配；`match` 不会像相等比较方式那样，执行自动引用和解引用。

第一个支臂与 [清单 21-9] 中的 `if` 代码块相同。第二个支臂匹配到 /sleep 的请求。收到该请求后，服务器将在渲染成功 HTML 页面之前休眠 5 秒。第三个支臂与清单 21-9 中的 `else` 代码块相同。

咱们可以看到我们的服务器是多么的原始：真正的库将以更简洁的方式处理多个请求的识别！

他编译了！但请注意，当咱们尝试运行 `cargo run` 并在浏览器中发出请求时，咱们将看到浏览器中看到在本章开头曾看到的那些报错。我们的库实际上还没有调用传递给 `sleep` 的闭包！

> **注意**：关于像 Haskell 和 Rust 这样有着严格编译器的语言，咱们或许听说过一种说法，即 “当代码编译时，他就会运行。” 但这种说法并非放之四海而皆准。我们的项目编译了，但他什么也没做！若我们正在构建一个真实且完整的项目，那么现在正是开始编写单元测试的好时机，以验证代码不仅会编译，*还* 有着我们想要的行为。

### 通过线程池提升吞吐量
请思考：若我们即将执行一个未来值而不是闭包，这里会有什么不同？

我们没有对 new 和 execute 的参数执行任何操作。我们来以我们希望的行为实现这两个函数的主体。首先，我们来思考一下 new。之前我们为 size 参数选择了无符号类型，因为线程数为负的线程池没有意义。然而，有着零个线程的线程池也没有意义，但零是完全有效的 usize。在返回 ThreadPool 实例之前，我们将添加检查 size 是否大于零的代码，在返回一个 ThreadPool 实例前，添加检查 size 大于零的代码，并当程序通过使用 assert! 宏收到零时让程序终止运行，如下清单 21-13 中所示。

我们还通过 [文档注释] 为我们的 `N` 添加了一些文档。请注意，我们遵循了良好的文档实践，添加了一个小节，之处我们的函数可能会终止运行的情况，正如第 14 章中所讨论的那样。请尝试运行 `N` 并点击 ThreadPool 结构体，看看为 new 生成的文档是什么样的！

与其像这里这样添加 assert! 宏，我们也可以改 new 为 build，并像在 [清单 12-9] 中 I/O 项目中的 Config::build 那样返回一个 Result。但我们已经决定在这种情况下，尝试创建一个没有任何线程的线程池应该是不可恢复的错误。若咱们感兴趣，那就编写一个有着以下签名的名为 build 的函数，与 new 函数比较：

在开始实现线程池之前，我们先讨论使用线程池应该是什么样子。设计代码时，先编写客户端接口有助于引导设计。应按照希望调用代码的方式编写 API，然后在这个结构中实现功能，而不是先实现功能再设计公开 API。
与第 12 章项目中使用测试驱动开发类似，这里我们将使用编译器驱动开发。我们先编写调用所需函数的代码，再查看编译器错误，以确定下一步应该做什么修改才能让代码运行。不过在此之前，我们先看看一种不会作为起点采用的技术。
<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>
#### 为每个请求生成一个线程
首先，我们来看看如果为每个连接创建一个新线程，代码可能是什么样子。正如前面提到的，由于可能生成无限数量的线程，这不是最终方案，但它是先构建一个可运行多线程服务器的起点。然后我们会加入线程池作为改进，这样比较两种方案也更容易。清单 21-11 展示了对 `main` 的修改，以便在 `for` 循环中为每个流生成一个新线程。

<Listing number="21-11" file-name="src/main.rs" caption="为每个流都生成一个新线程">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```


</Listing>

现在我们有一种方法知道，我们有要存储在池中的有效线程数量，我们可以创建这些线程并在 ThreadPool 结构体中存储他们。但我们要怎样 “存储” 线程呢？我们再看看 `thread::spawn` 的签名：

spawn 函数返回一个 JoinHandle&lt;T>，其中 T 是闭包返回的类型。我们也来尝试使用 JoinHandle，看看会发生什么。在我们的情形下，传递给线程池的闭包将处理连接，并且不返回任何值，因此 T 将是单元值类型 ()。

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>
#### 创建有限数量的线程
接下来我们将解决的问题是，给予到 `ThreadPool` 的闭包不执行任何操作。目前，我们在 `thread::spawn` 方法中得到了打算执行的闭包。但在创建 ThreadPool 期间创建每个 Worker 时，我们需要给予 thread::spawn 一个要运行的闭包。

<Listing number="21-12" file-name="src/main.rs" caption="我们的理想 `ThreadPool` 接口">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```


</Listing>

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```


我们使用 `ThreadPool::new` 创建一个线程池，线程数量可配置，这里设为 4。然后在 `for` 循环中，`pool.execute` 的接口与 `thread::spawn` 类似：它接收一个闭包，线程池应为每个流运行这个闭包。我们需要实现 `pool.execute`，让它接收闭包并交给线程池中的某个线程运行。这段代码目前还无法编译，但我们会先尝试，让编译器指导我们如何修复它。
<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>
#### 使用编译器驱动开发构建 `ThreadPool`
在 `cargo check` 中，我们创建新通道，并让线程池包含发送器。这段代码将成功编译。

很好！这个错误告诉我们需要一个 `ThreadPool` 类型或模块，所以现在就来构建它。`ThreadPool` 的实现将独立于 Web 服务器执行的工作类型。因此，我们把 `hello` crate 从二进制 crate 切换为库 crate，用来保存 `ThreadPool` 的实现。切换为库 crate 后，还可以把这个独立的线程池库用于任何需要线程池的工作，而不只是处理 Web 请求。
我们进行了一些小而直接的修改：我们传递接收器到 `ThreadPool` 中，然后在闭包内使用他。

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```


</Listing>

我们进行了一些小而直接的修改：我们传递接收器到 `ThreadPool` 中，然后在闭包内使用他。

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```


</Listing>

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```


当我们尝试检查这段代码时，会得到下面这样的报错：

这个错误表明，接下来需要为 `new` 创建一个名为 `ThreadPool` 的关联函数。我们还知道，`new` 需要有一个能接收 `4` 作为参数的形参，并且应该返回一个 `ThreadPool` 实例。我们来实现一个具备这些特征的最简单 `new` 函数：

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```


</Listing>

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```


回顾第 16 章中讨论的线程安全的灵巧指针：为了在多个线程之间共用所有权并允许实现线程修改值，我们需要使用 `usize`。`size` 类型将允许多个 `4` 实例都拥有 `usize`，而 Mutex 将确保一次只有一个 worker 获取一项接收器中的作业。下面清单 21-18 展示了我们需要进行的修改。
回顾第 16 章中讨论的线程安全的灵巧指针：为了在多个线程之间共用所有权并允许实现线程修改值，我们需要使用 Arc&lt;Mutex&lt;T>>。Arc 类型将允许多个 Worker 实例都拥有 receiver，而 Mutex 将确保一次只有一个 worker 获取一项接收器中的作业。下面清单 21-18 展示了我们需要进行的修改。
最后，我们来对 `execute` 实现 `ThreadPool` 方法。我们还将把 `thread::spawn` 从结构体修改为特质对象的类型别名，包含 `execute` 接收的闭包类型。正如第 20 章中 [类型同义词和类型别名](#creating-a-finite-number-of-threads) 小节中讨论的，类型别名允许我们使长类型变短以方便使用。请看下面清单 21-19.
我们将定义 `execute` 上的 `ThreadPool` 方法，使其接收一个闭包作为参数。回顾第 13 章[“从闭包中移出捕获的值”][moving-out-of-closures]小节，我们可以使用三种不同的特质来接收闭包作为参数：`Fn`、`FnMut` 和 `FnOnce`。这里需要决定使用哪一种闭包。我们知道最终会实现与标准库 `thread::spawn` 类似的功能，因此可以查看 `thread::spawn` 签名对参数施加了哪些边界。文档展示了如下定义：

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```


这里关心的是 `F` 类型参数；`T` 类型参数与返回值有关，我们不关心它。可以看到，`spawn` 使用 `FnOnce` 作为 `F` 的特质边界。这可能也是我们想要的，因为最终会把从 `execute` 获得的参数传给 `spawn`。我们更有把握使用 `FnOnce`，因为运行请求的线程只会执行该请求的闭包一次，这正好对应 `Once` 中的 `FnOnce`。
`F` 类型参数还具有 `Send` 特质边界和 `'static` 生命周期边界，这在我们的场景中很有用：需要使用 `Send` 将闭包从一个线程传递到另一个线程，而使用 `'static` 是因为不知道线程执行需要多长时间。我们来在 `execute` 上创建一个带有这些边界、接收 `ThreadPool` 类型泛型参数的 `F` 方法：

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```


</Listing>

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```


在这里，我们首选对 `()` 调用 `FnOnce` 来获取互斥量，然后调用 `FnOnce` 来对任何错误终止运行。当互斥量处于 *中毒* 状态时，则获取锁可能失败，这种情况会在某个其他线于持有锁期间终止运行，而非释放锁时发生。在这种情况下，调用 `()` 来让这个线程终止运行，便是要采取的正确操作。咱们可以修改这个 unwrap 为带有对咱们有意义的报错信息的 expect。
在这里，我们首选对 `execute` 调用 lock 来获取互斥量，然后调用 unwrap 来对任何错误终止运行。当互斥量处于 *中毒* 状态时，则获取锁可能失败，这种情况会在某个其他线于持有锁期间终止运行，而非释放锁时发生。在这种情况下，调用 unrap 来让这个线程终止运行，便是要采取的正确操作。咱们可以修改这个 unwrap 为带有对咱们有意义的报错信息的 expect。

它可以编译！但请注意，如果尝试运行 `cargo run` 并在浏览器中发出请求，就会看到本章开头在浏览器中看到的那些错误。我们的库实际上还没有调用传给 `execute` 的闭包！
成功了！我们现在有了个能够异步执行连接的线程池。创建的线程永远不会超过四个，因此当服务器收到大量请求时，系统也不会过载。当我们发出到 /sleep 的请求时，服务器将能够通过让另一个线程运行其他请求而服务这些请求。
成功了！我们现在有了个能够异步执行连接的线程池。创建的线程永远不会超过四个，因此当服务器收到大量请求时，系统也不会过载。当我们发出到 /sleep 的请求时，服务器将能够通过让另一个线程运行其他请求而服务这些请求。
#### 验证 `new` 中的线程数量
我们还没有对 `new` 和 `execute` 的参数做任何处理。现在按照期望的行为实现这两个函数的主体。先思考 `new`：之前为 `size` 参数选择无符号类型，是因为负数线程数的线程池没有意义。然而，零个线程的线程池也没有意义，尽管 0 是有效的 `usize`。如清单 21-13 所示，在返回 `size` 实例之前添加代码检查 `ThreadPool` 是否大于零，并在收到零时使用 `assert!` 宏让程序恐慌。

<Listing number="21-13" file-name="src/lib.rs" caption="实现 `ThreadPool::new` 为当 `size` 为零时终止运行">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```


</Listing>

我们还通过文档注释为 `ThreadPool` 添加了一些文档。请注意，我们遵循了良好的文档实践，添加了一个小节说明函数可能发生恐慌的情况，正如第 14 章所讨论的那样。尝试运行 `cargo doc --open` 并点击 `ThreadPool` 结构体，看看为 `new` 生成的文档是什么样的！
我们也可以像这里一样添加 `assert!` 宏，或者把 `new` 改为 `build`，并像 I/O 项目清单 12-9 中对 `Result` 所做的那样返回 `Config::build`。但在这个例子中，我们决定尝试创建一个没有任何线程的线程池应该是不可恢复的错误。如果想挑战一下，可以编写一个名为 `build`、签名如下的函数，并与 `new` 函数比较：

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```


#### 创建空间来存储线程
现在我们已经有办法确认线程数量有效，可以创建这些线程，并在返回结构体前将它们存储到 `ThreadPool` 结构体中。但要怎样“存储”线程呢？我们再看看 `thread::spawn` 的签名：

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```


`spawn` 函数返回一个 `JoinHandle<T>`，其中 `T` 是闭包返回的类型。我们也尝试使用 `JoinHandle`，看看会发生什么。在我们的例子中，传给线程池的闭包会处理连接而不返回任何值，因此 `T` 是单元类型 `()`。
清单 21-14 中的代码可以编译，但目前还不会创建任何线程。我们修改了 `ThreadPool` 的定义，使其保存一个 `thread::JoinHandle<()>` 实例的矢量，将矢量初始化为容量为 `size`，设置一个 `for` 循环来运行创建线程的代码，并返回一个包含这些线程的 `ThreadPool` 实例。

<Listing number="21-14" file-name="src/lib.rs" caption="为 `ThreadPool` 创建一个用于保存线程的矢量值">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```


</Listing>

我们在库 crate 中将 `std::thread` 引入作用域，因为使用 `thread::JoinHandle` 作为 `ThreadPool` 矢量中项目的类型。
收到有效的大小后，`ThreadPool` 会创建一个可以容纳 `size` 个项目的新矢量。`with_capacity` 函数与 `Vec::new` 完成相同任务，但有一个重要区别：它会预先为矢量分配空间。因为我们知道矢量需要存储 `size` 个元素，提前分配比使用会随着插入元素而调整大小的 `Vec::new` 略高效。
再次运行 `cargo check` 时，应该就能成功。
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>
#### 发送 `ThreadPool` 中的代码到线程
我们在清单 21-14 的 `for` 循环中留下了关于创建线程的注释。这里来看看实际如何创建线程。标准库提供 `thread::spawn` 作为创建线程的方式，而 `thread::spawn` 希望在线程创建后立即获得线程应该运行的代码。然而，在我们的例子中，我们希望先创建线程，让它们*等待*稍后发送的代码。标准库的线程实现没有提供这种能力，因此必须手动实现。
我们将在 `ThreadPool` 和线程之间引入一种管理这种新行为的数据结构。把这个数据结构称为 *Worker*，这是线程池实现中常用的术语。`Worker` 会获取需要运行的代码，并在线程中运行这些代码。
可以把它想成餐厅厨房里的工作人员：他们会等待顾客订单到来，然后负责接收并完成这些订单。
线程池不再存储 `JoinHandle<()>` 实例的矢量，而是存储 `Worker` 结构体的实例。每个 `Worker` 都会存储一个 `JoinHandle<()>` 实例。然后，我们会在 `Worker` 上实现一个方法，接收要运行的闭包代码，并将它发送到已经运行的线程执行。我们还会给每个 `Worker` 一个 `id`，这样在记录日志或调试时，就能区分池中的不同 `Worker` 实例。
创建 `ThreadPool` 时会经过以下流程。按这种方式设置好 `Worker` 后，我们再实现将闭包发送到线程的代码：

1. 定义一个 `Worker` 结构体，包含 `id` 和 `JoinHandle<()>`。
2. 修改 `ThreadPool`，让它保存一个 `Worker` 实例的矢量。
3. 定义一个 `Worker::new` 函数，接收一个 `id` 数字，返回一个包含该 `Worker` 和由空闭包生成的线程的 `id` 实例。
4. 在 `ThreadPool::new` 中使用 `for` 循环计数器生成 `id`，使用该 `Worker` 创建新的 `id`，并将 `Worker` 存入矢量。

如果愿意接受挑战，可以先尝试自己实现这些修改，再查看清单 21-15 中的代码。
准备好了吗？下面是清单 21-15 中一种实现上述修改的方法。

<Listing number="21-15" file-name="src/lib.rs" caption="修改 `ThreadPool` 为包含 `Worker` 实例，而非直接包含线程">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```


</Listing>

我们把 `ThreadPool` 的字段名从 `threads` 改为 `workers`，因为它现在保存的是 `Worker` 实例，而不是 `JoinHandle<()>` 实例。我们使用 `for` 循环中的计数器作为 `Worker::new` 的参数，并把每个新 `Worker` 存入名为 `workers` 的矢量。
外部代码（例如 _src/main.rs_ 中的服务器）不需要知道 `Worker` 内使用 `ThreadPool` 结构体的实现细节，因此我们将 `Worker` 结构体及其 `new` 函数设为私有。`Worker::new` 使用传入的 `id`，并保存一个通过空闭包生成新线程得到的 `JoinHandle<()>` 实例。
> **注意**：如果操作系统因系统资源不足而无法创建线程，`thread::spawn` 会引发恐慌。这会导致整个服务器恐慌，即使部分线程可能已经创建成功。为简单起见，这种行为在示例中是可以接受的；但在生产环境的线程池实现中，可能更希望使用 [`std::thread::Builder`][builder] 及其返回 `spawn` 的 [`Result`][builder-spawn] 方法。
这段代码可以编译，并会存储作为参数传给 `Worker` 的数量个 `ThreadPool::new` 实例。但我们*仍然*没有处理从 `execute` 得到的闭包。接下来看看如何做到这一点。
#### 通过信道发送请求到线程
接下来要解决的问题是，传给 `thread::spawn` 的闭包什么也不做。目前，我们在 `execute` 方法中得到想要执行的闭包。但在创建 `thread::spawn` 时为每个 `Worker` 创建线程，还需要给 `ThreadPool` 一个要运行的闭包。
我们希望刚刚创建的 `Worker` 结构体从 `ThreadPool` 持有的队列中获取要运行的代码，并将这些代码发送给自己的线程运行。
第 16 章学习过的信道——一种在两个线程之间通信的简单方式——非常适合这个用例。我们使用信道作为作业队列，`execute` 将作业从 `ThreadPool` 发送到 `Worker` 实例，由 `ThreadPool` 将作业发送给自己的线程。计划如下：

1. `Worker` 创建信道并保存发送器。
2. 每个 `Job` 保存接收器。
3. 创建一个新的 `execute` 结构体，用来保存希望通过信道发送的闭包。
4. `Worker` 方法通过发送器发送它想执行的作业。
5. `ThreadPool::new` 在线程中循环读取接收器，并执行收到的作业闭包。

先在 `ThreadPool` 中创建信道并将发送器保存在 `Job` 实例中，如清单 21-16 所示。`ThreadPool` 结构体目前不包含任何内容，但它会成为通过信道发送的项目类型。

<Listing number="21-16" file-name="src/lib.rs" caption="修改 `Job` 为存储传输 `ThreadPool::new` 实例的信道的发送器">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```


</Listing>

在 `Worker` 中，我们创建新信道，并让线程池保存发送器。这段代码可以成功编译。
接下来，在线程池创建信道时，尝试把信道接收器传给每个 `Worker`。我们知道要在线程池生成的线程中使用接收器，因此会在闭包中引用 `receiver` 参数。清单 21-17 中的代码还不能完全编译。

<Listing number="21-17" file-name="src/lib.rs" caption="传递 receiver 给每个 `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```


</Listing>

我们做了一些简单直接的修改：把接收器传给 `Worker::new`，然后在闭包中使用它。
当我们尝试检查这段代码时，会得到下面这个错误：

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```


这段代码试图把 `receiver` 传给多个 `Worker` 实例。这行不通，正如第 16 章所述：Rust 提供的信道实现是多*生产者*、单*消费者*。这意味着不能简单地克隆信道的消费端来修复代码。我们也不希望把一条消息发送给多个消费者；我们需要一条消息列表和多个 `Worker` 实例，让每条消息只处理一次。
此外，从信道队列中取出作业需要修改 `receiver`，因此线程需要一种安全的方式来共享和修改 `receiver`；否则可能产生竞争条件（第 16 章介绍过）。
回顾第 16 章讨论的线程安全智能指针：要在多个线程之间共享所有权并允许线程修改值，需要使用 `Arc<Mutex<T>>`。`Arc` 类型允许多个 `Worker` 实例拥有接收器，而 `Mutex` 确保同一时刻只有一个 `Worker` 从接收器中获取作业。清单 21-18 展示了需要进行的修改。

<Listing number="21-18" file-name="src/lib.rs" caption="使用 `Worker` 和 `Arc` 在 `Mutex` 实例间共用接收器">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```


</Listing>

在 `ThreadPool::new` 中，我们把接收器放入 `Arc` 和 `Mutex`。对于每个新的 `Worker`，都克隆 `Arc` 以增加引用计数，使 `Worker` 实例能够共享接收器的所有权。
做出这些修改后，代码可以编译了！我们快成功了！
#### 实现 `execute` 方法
最后，我们来实现 `execute` 上的 `ThreadPool` 方法。还要把 `Job` 从结构体改为特质对象的类型别名，用来保存 `execute` 接收的闭包类型。正如第 20 章[“类型同义词和类型别名”][type-aliases]小节所述，类型别名可以缩短很长的类型，方便使用。请看清单 21-19。

<Listing number="21-19" file-name="src/lib.rs" caption="为包含每个闭包的 `Job` 创建 `Box` 类型的别名，然后发送作业到信道">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```


</Listing>

使用从 `Job` 中得到的闭包创建新的 `execute` 实例后，我们将该作业发送到信道的发送端。为处理发送失败的情况，我们对 `unwrap` 调用 `send`。例如，如果停止所有线程的执行，接收端就会停止接收新消息，可能发生发送失败。目前我们还无法停止线程执行：只要线程池存在，线程就会继续运行。使用 `unwrap` 是因为我们知道失败情况不会发生，但编译器不知道这一点。
但还没有完全搞定！在 `Worker` 中，传给 `thread::spawn` 的闭包仍然只是*引用*信道的接收端。相反，我们需要让闭包无限循环，向信道接收端请求作业，并在获得作业后运行它。按照清单 21-20 对 `Worker::new` 做出修改。

<Listing number="21-20" file-name="src/lib.rs" caption="在 `Worker` 实例的线程中接收并执行作业">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```


</Listing>

这里首先对 `lock` 调用 `receiver` 获取互斥量，然后调用 `unwrap` 在发生错误时引发恐慌。如果互斥量处于*中毒*状态，获取锁可能失败；当其他线程持有锁时发生恐慌而没有释放锁，就会出现这种情况。在这种情形下，调用 `unwrap` 让该线程恐慌是正确的做法。也可以将这个 `unwrap` 改为带有有意义错误消息的 `expect`。
如果成功获取互斥量的锁，就调用 `recv` 从信道接收一个 `Job`。最后一个 `unwrap` 同样会跳过这里可能发生的错误；例如，持有发送器的线程已经关闭，这与接收器关闭时 `send` 方法返回 `Err` 类似。
`recv` 调用会阻塞，因此如果暂时没有作业，当前线程会等待，直到作业可用。`Mutex<T>` 确保同一时刻只有一个 `Worker` 线程尝试请求作业。
我们的线程池现在已经可以工作了！运行 `cargo run`，然后发出一些请求：
现在是停下来思考一下的好时机，若我们针对要完成的工作，使用未来值而不是闭包，那么清单 21-18、21-19 和 21-20 中的代码会有什么不同。哪些类型会发生变化？方法签名会有什么不同，如果有的话？代码的哪些部分会保持不变？

在了解了第 17 章和第 19 章中的 `while let` 循环之后，咱们可能想知道，为什么我们没有编写如同清单 21-21 中所示的 `Worker` 线程代码。


```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```


<Listing number="21-21" file-name="src/lib.rs" caption="使用 `Worker::new` 的 `while let` 替代实现">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```


</Listing>

这段代码可以编译并运行，但不会产生所需的线程行为：慢速请求仍将导致其他请求等待处理。原因有些微妙：`Mutex` 结构体没有公开的 `unlock` 方法，因为锁的所有权基于 `MutexGuard<T>` 方法返回的 `LockResult<MutexGuard<T>>` 内 `lock` 的生命周期。在编译时，借用检查器就会强制执行这样的规则：除非我们持有锁，否则无法访问由 `Mutex` 保护的资源。然而，当我们没有注意到 `MutexGuard<T>` 的生命周期时，这种实现也会导致锁被持有的时间超过预期。
清单 21-20 中使用 `let job =
receiver.lock().unwrap().recv().unwrap();` 的代码之所以有效，是因为使用 `let` 时，等号右侧表达式中的临时值会在 `let` 语句结束时立即丢弃。然而，`while
let`（以及 `if let` 和 `match`）不会在关联代码块结束前丢弃临时值。在清单 21-21 中，锁会在调用 `job()` 的整个期间保持持有，这意味着其他 `Worker` 实例无法接收作业。
[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
<!-- Old headings. Do not remove or links may break. -->
<!-- Old headings. Do not remove or links may break. -->
<!-- Old headings. Do not remove or links may break. -->
<!-- Old headings. Do not remove or links may break. -->
<!-- Old headings. Do not remove or links may break. -->
<!--
ignore -->
<!-- ignore -->
<!-- ignore -->
<!-- Old headings. Do not remove or links may break. -->
<!-- ignore -->
<!-- ignore -->
<!-- ignore -->

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->
