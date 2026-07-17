## 优雅关机与清理

[清单 21-20] 中的代码正如我们预期的那样，通过使用线程池以异步方式响应请求。我们会收到一些关于 `workers`、`id` 和 `thread` 等我们没有直接使用的字段的告警，这提醒我们没有清理任何东西。当我们使用不太优雅的 Ctrl + c 方法停止主线程时，所有其他线程也会立即停止，即使他们正处于服务请求状态。

接下来，我们将实现 `Drop` 特质，对线程池中的每个线程调用 `join`，以便他们可以在关闭之前完成完成正在处理的请求。然后，我们将实现一种方法，告知线程停止接受新请求并关闭。为了查看这段代码的实际效果，我们将修改服务器为在有序关闭其线程池之前只接受两个请求。

接下来需要注意的一点是：这些改动都不会影响负责执行闭包的代码部分，因此如果我们使用线程池来运行异步运行时，这里的所有内容也都会相同。
### 对 `Drop` 实现 `ThreadPool` 特质

我们从对线程池实现 `Drop` 开始。当线程池被弃用时，我们的线程就都应归拢，以确保他们可以完成他们的工作。下面清单 21-22 展示了 `Drop` 实现的首次尝试；这段代码还无法正常工作。

<Listing number="21-22" file-name="src/lib.rs" caption="在线程池超出作用域时归拢各个线程">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

首先，我们遍历线程池 `workers` 中的每个线程。我们为此使用 `&mut` 是因为 `self` 是个可变引用，并且我们还需要能够修改 `worker`。对于每个 `worker`，我们打印一条消息，表明该特定 `Worker` 正在关闭，然后我们对该 `join` 实例的线程调用 `Worker`。当 `join` 调用失败时，我们使用 `unwrap` 使 Rust 终止运行，从而进入非正常关闭状态。

下面是我们编译这代码时得到的报错信息：

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

这个报错告诉我们，我们不能调用 `join`，因为只有每个 `worker` 的可变借用，而 `join` 会取得其参数的所有权。为了解决这个问题，我们需要从拥有 `Worker` 的 `thread` 实例中迁出线程，以便 `join` 可以消费线程。实现这一目的的一种方法是，采取我们在 [清单 18-15] 中使用的同样方法。若 `Worker` 包含一个 `Option<thread::JoinHandle<()>>`，我们就可以对 `take` 调用 `Option` 方法，来从 `Some` 变种中迁出值，并原处留下 `None`。换句话说，正在运行的 `Worker` 将在 `Some` 中包含一个 `thread` 变种，而当我们想要清理一个 `Worker` 时，我们会以 `Some` 替换 `None`，这样那个 `Worker` 就没有要运行的线程了。

首先，我们将修改 `Worker` 的 `Option<thread::JoinHandle<()>>` 实现，以在等待线程完成之前显式弃用 `worker.thread`。下面清单 21-23 展示了对 ThreadPool 的修改，以显式弃用 `Option`。与线程不同，这里我们 *确实* 需要使用 `Option`，才能通过 Option::take 从 ThreadPool 中迁出 sender。

弃用 `Vec::drain` 会关闭信道，这表明将不再发送消息。发生这种情况时，`..` 实例在无限循环中执行的所有 recv 调用都将返回错误。在下面清单 21-24 中，我们修改了 Worker 的循环，使其在这种情况下能优雅地退出循环，这意味着当 ThreadPool 的 drop 实现对线程调用 join 方法时，他们都将结束运行。

take 方法定义在 Iterator 特质中，限制迭代为最多前两个项目。`ThreadPool` 将在 main 函数结束时超出作用域，此时 `drop` 实现将运行。

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

通过 cargo run 启动服务器并发出三个请求。第三个请求应报错，并且在咱们的终端中，咱们应看到类似以下的输出：

### 通知线程停止监听作业

请注意这次特定执行中的一个有趣的方面：`Worker` 弃用 `join` 后，在任何 `loop` 收到错误之前，我们尝试聚拢 `ThreadPool`。由于 `drop` 尚未从 recv 操作中收到错误，因此主线程被阻塞，等待 Worker 0 完成。与此同时，Worker 1 接收到了作业，然后所有线程都收到了错误。当 Worker 0 完成时，主线程等待其余 Worker 实例完成。此时，他们都已退出各自的循环并停止了。

要解决这个问题，我们需要修改 `ThreadPool` 的 `drop` 实现，然后修改 `Worker` 循环。

首先，我们会修改 `ThreadPool` 的 `drop` 实现，在等待线程结束之前显式丢弃 `sender`。清单 21-23 展示了如何修改 `ThreadPool` 来显式丢弃 `sender`。与线程本身不同，这里确实需要使用 `Option`，才能将 `sender` 从 `ThreadPool` 中移出，并调用 `Option::take`。

<Listing number="21-23" file-name="src/lib.rs" caption="在归拢 `sender` 线程之前显式弃用 `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

丢弃 `sender` 会关闭信道，表示不会再发送消息。发生这种情况时，所有 `recv` 调用（`Worker` 实例在无限循环中执行的调用）都会返回错误。在清单 21-24 中，我们修改 `Worker` 循环，使其在这种情况下优雅地退出循环；这意味着当 `ThreadPool` 的 `drop` 实现对线程调用 `join` 时，线程就会结束。

<Listing number="21-24" file-name="src/lib.rs" caption="当 `recv` 返回错误时显式地退出循环">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

为了观察这段代码的实际效果，让我们修改 `main`，使服务器只接受两个请求，然后优雅地关机，如清单 21-25 所示。

<Listing number="21-25" file-name="src/main.rs" caption="通过退出循环在处理完两个请求后关闭服务器">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

现实中的 Web 服务器不应该只服务两个请求就关机。这段代码只是用来演示优雅关机和清理工作正常。

`take` 方法定义在 `Iterator` 特质中，最多将迭代限制为前两个项目。`ThreadPool` 会在 `main` 结束时离开作用域，此时 `drop` 实现会运行。

使用 `cargo run` 启动服务器并发出三个请求。第三个请求应该出错，终端中会看到类似下面的输出：
<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

你可能会看到 `Worker` ID 和打印消息的顺序不同。我们可以从这些消息看出代码的工作方式：`Worker` 实例 0 和 3 处理了前两个请求。服务器在第二个连接之后停止接受连接，而 `Drop` 在 `ThreadPool` 上的实现甚至在 `Worker 3` 开始工作之前就开始执行。丢弃 `sender` 会断开所有 `Worker` 实例，并通知它们关闭。每个 `Worker` 实例断开连接时都会打印消息，然后线程池调用 `join` 等待每个 `Worker` 线程结束。

这次执行中还有一个有趣的方面：`ThreadPool` 丢弃了 `sender`，在任何 `Worker` 收到错误之前，我们就尝试对 `Worker 0` 调用 join。`Worker 0` 还没有从 `recv` 收到错误，因此主线程阻塞并等待 `Worker 0` 完成。与此同时，`Worker 3` 收到一个作业，随后所有线程都收到了错误。当 `Worker 0` 完成后，主线程等待其余 `Worker` 实例完成。此时，它们都已经退出各自的循环并停止运行。

恭喜！我们现在已经完成了这个项目：一个使用线程池异步响应的基础 Web 服务器。我们能够优雅地关闭服务器，并清理线程池中的所有线程。

下面是完整代码，供参考：

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

我们还可以继续完善这个项目！如果你想继续增强它，可以考虑以下想法：

- 为 `ThreadPool` 及其公开方法添加更多文档。
- 为库的功能添加测试。
- 将 `unwrap` 调用改为更健壮的错误处理。
- 使用 `ThreadPool` 执行服务 Web 请求以外的任务。
- 在 [crates.io](https://crates.io/) 上寻找一个线程池箱，改用该箱实现类似的 Web 服务器，然后比较它的 API 和健壮性与我们实现的线程池有何不同。
## 本章小结

做得好！你已经读完了本书！感谢你加入这次 Rust 之旅。现在你已经可以实现自己的 Rust 项目，并帮助其他人的项目。请记住，Rust 社区中有许多友善的 Rustacean，他们很乐意帮助你解决 Rust 学习旅程中遇到的挑战。
