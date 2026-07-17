## 控制测试的运行方式

正如 `cargo run` 会编译代码并运行生成的二进制文件一样，`cargo test` 会在测试模式下编译代码，
并运行生成的测试二进制文件。`cargo test` 生成的二进制文件默认会并行运行所有测试，并捕获测试
运行期间生成的输出，从而不显示这些输出，让我们更容易阅读与测试结果有关的内容。不过，我们
可以指定命令行选项来改变这一默认行为。

有些命令行选项传给 `cargo test`，另一些传给生成的测试二进制文件。为区分这两类参数，先列出
传给 `cargo test` 的参数，接着写分隔符 `--`，然后列出传给测试二进制文件的参数。运行 `cargo test --help` 可显示可用于 `cargo test` 的选项；运行 `cargo test -- --help` 可显示分隔符之后可用
的选项。这些选项也记录在 _`rustc` 手册_ 的[“测试”一节][tests]中。



### 并行或依次运行测试

运行多个测试时，默认情况下它们会使用线程并行运行，因此完成得更快，我们也能更早得到反馈。由于
测试同时运行，必须确保它们彼此不依赖，也不依赖任何共享状态，包括共享环境，例如当前工作目录
或环境变量。

例如，假设每个测试都会运行一些代码，在磁盘上创建名为 _test-output.txt_ 的文件，并向其中写入
一些数据。然后，每个测试都会读取该文件中的数据，并断言文件包含一个特定值，而且每个测试所
要求的值都不同。由于测试同时运行，一个测试可能会在另一个测试写入和读取文件之间覆盖该文件。
这样，第二个测试就会失败，但原因不是代码有误，而是测试在并行运行时相互干扰。一种解决方案是
确保每个测试写入不同的文件；另一种是让测试一次只运行一个。

如果不希望并行运行测试，或者希望更细致地控制使用的线程数，可以将 `--test-threads` 标志以及
希望使用的线程数传给测试二进制文件。请看下面的示例：

```console
$ cargo test -- --test-threads=1
```

我们将测试线程数设为 `1`，告诉程序不要使用并行。使用单个线程运行测试会比并行运行更耗时，但
如果测试共享状态，它们就不会互相干扰。

### 显示函数输出

默认情况下，测试通过时，Rust 的测试库会捕获打印到标准输出的所有内容。例如，如果我们在测试中
调用 `println!` 且测试通过，就不会在终端中看到 `println!` 的输出；只会看到表明测试通过的那一行。
如果测试失败，就会在其余失败消息中看到打印到标准输出的内容。

例如，清单 11-10 包含一个简单的函数，它会打印参数的值并返回 10；此外还有一个通过的测试和
一个失败的测试。

<Listing number="11-10" file-name="src/lib.rs" caption="调用 `println!` 的函数的测试">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

当我们用 `cargo test` 运行这些测试时，会看到如下输出：

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

注意，这段输出中没有出现 `I got the value 4`，它是在通过的测试运行时打印的。该输出已被捕获。
失败测试的输出 `I got the value 8` 出现在测试摘要输出的一节中，该节还显示了测试失败的原因。

如果也想看到通过测试打印的值，可以通过 `--show-output` 告诉 Rust 同时显示成功测试的输出：

```console
$ cargo test -- --show-output
```

再次使用 `--show-output` 标志运行清单 11-10 中的测试时，我们会看到如下输出：

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### 按名称运行测试子集

完整运行测试套件有时会花费很长时间。如果你正在处理某个特定部分的代码，可能只想运行与该代码
相关的测试。可以将要运行的测试名称作为参数传给 `cargo test`，从而选择要运行的测试。

为了演示如何运行测试子集，我们先为 `add_two` 函数创建三个测试，如清单 11-11 所示，然后选择
要运行的测试。

<Listing number="11-11" file-name="src/lib.rs" caption="名称各不相同的三个测试">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

如果像之前一样不传参数运行测试，所有测试都会并行运行：

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### 运行单个测试

可以将任意测试函数的名称传给 `cargo test`，从而只运行该测试：

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

只有名称为 `one_hundred` 的测试运行了；另外两个测试的名称与它不匹配。测试输出在末尾显示
`2 filtered out`，告诉我们还有更多测试没有运行。

不能用这种方式指定多个测试名称；传给 `cargo test` 的值只有第一个会生效。不过，有办法运行
多个测试。

#### 通过筛选运行多个测试

可以指定测试名称的一部分，名称包含该部分的测试都会运行。例如，我们有两个测试名称包含 `add`，
因此可以运行 `cargo test add` 来运行这两个测试：

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

这条命令运行了名称中包含 `add` 的所有测试，并筛掉了名为 `one_hundred` 的测试。还要注意，测试
所在的模块会成为测试名称的一部分，因此可以按模块名称进行筛选，以运行该模块中的所有测试。

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### 除非明确要求，否则忽略测试

有时，少数特定测试执行起来非常耗时，因此你可能希望在大多数运行 `cargo test` 的时候将它们排除。
与其把所有想运行的测试都列为参数，不如给这些耗时测试加上 `ignore` 属性来排除它们，如下所示：

<span class="filename">文件名： src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

在 `#[test]` 后面添加 `#[ignore]` 行，标记要排除的测试。现在运行测试时，`it_works` 会运行，
但 `expensive_test` 不会：

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

`expensive_test` 函数会列为 `ignored`。如果只想运行被忽略的测试，可以使用 `cargo test -- --ignored`：

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

通过控制运行哪些测试，可以让 `cargo test` 的结果快速返回。当你认为适合检查 `ignored` 测试的结果
且有时间等待时，可以运行 `cargo test -- --ignored`。如果想运行所有测试，无论是否被忽略，都可以
运行 `cargo test -- --include-ignored`。

[tests]: https://doc.rust-lang.org/rustc/tests/index.html
