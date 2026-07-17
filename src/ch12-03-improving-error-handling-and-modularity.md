## 重构以改进模块化和错误处理

为了改进程序，我们要解决四个与程序结构和潜在错误处理方式有关的问题。首先，我们的 `main` 函数现在执行两项任务：解析参数和读取文件。随着程序增长，`main` 函数处理的独立任务会越来越多。函数承担的职责越多，就越难理解，也越难测试；如果要修改其中一部分，还更容易破坏其他部分。最好将功能分离，让每个函数只负责一项任务。

这个问题也与第二个问题有关：虽然 `query` 和 `file_path` 是程序的配置变量，但 `contents` 这样的变量用于执行程序逻辑。`main` 越长，我们就需要将越多变量引入作用域；作用域中的变量越多，就越难追踪每个变量的用途。最好把配置变量组合到一个结构体中，让它们的用途更加清晰。

第三个问题是，我们使用 `expect` 在读取文件失败时打印错误消息，但这条错误消息只会打印 `Should have been
able to read the file`。读取文件可能因多种原因失败：例如文件可能不存在，或者我们没有打开它的权限。现在无论具体情况如何，我们都会对所有错误打印同一条消息，这无法向用户提供任何信息！

第四个问题是，我们使用 `expect` 处理错误；如果用户运行程序时没有指定足够的参数，就会得到 Rust 的 `index out of bounds` 错误，而这没有清楚地解释问题。如果所有错误处理代码都集中在一个地方，未来的维护者在需要修改错误处理逻辑时就只需查阅一处代码，那会更好。把所有错误处理代码放在一起，还能确保我们打印的消息对最终用户有意义。

让我们通过重构项目来解决这四个问题。

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### 分离二进制项目中的关注点

在许多二进制项目中，把多个任务的职责都分配给 `main` 函数是很常见的组织问题。因此，许多 Rust 程序员发现，当 `main` 函数开始变大时，拆分二进制程序中的不同关注点很有用。这个过程包含以下步骤：

- 将程序拆分为 _main.rs_ 文件和 _lib.rs_ 文件，并将程序逻辑移到 _lib.rs_ 中。
- 只要命令行解析逻辑还比较小，就可以保留在 `main` 函数中。
- 当命令行解析逻辑开始变得复杂时，就把它从 `main` 函数提取到其他函数或类型中。

经过这个过程后，`main` 函数保留的职责应当局限于以下内容：

- 使用参数值调用命令行解析逻辑
- 设置其他配置
- 调用 _lib.rs_ 中的 `run` 函数
- 处理 `run` 返回的错误

这种模式的核心是分离关注点：_main.rs_ 负责运行程序，_lib.rs_ 负责当前任务的全部逻辑。由于不能直接测试 `main` 函数，这种结构把程序逻辑移出 `main` 后，就能测试程序的所有逻辑。留在 `main` 函数中的代码会足够小，可以通过阅读来验证其正确性。让我们遵循这个过程重新组织程序。

#### 提取参数解析器

我们要把解析参数的功能提取到一个由 `main` 调用的函数中。清单 12-5 展示了 `main` 函数的新开头，它会调用我们将在 _src/main.rs_ 中定义的新函数 `parse_config`。

<Listing number="12-5" file-name="src/main.rs" caption="从 `parse_config` 中提取 `main` 函数">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

我们仍然把命令行参数收集到向量中，但不再在 `query` 函数中把索引 1 处的参数值赋给变量 `file_path`、把索引 2 处的参数值赋给变量 `main`，而是把整个向量传给 `parse_config` 函数。`parse_config` 函数负责确定每个参数应放入哪个变量，并把这些值传回 `main`。我们仍在 `query` 中创建 `file_path` 和 `main` 变量，但 `main` 不再负责确定命令行参数与变量之间的对应关系。

对于这个小程序来说，这次改动看起来可能有些过度，但我们正在以小步、渐进的方式进行重构。完成改动后，再次运行程序，确认参数解析仍然正常。经常检查进度是个好习惯，有助于在问题出现时找出原因。

#### 组合配置值

我们还可以再迈出一小步，进一步改进 `parse_config` 函数。目前我们返回一个元组，但紧接着又立即把元组拆成各个部分。这说明我们可能还没有找到正确的抽象。

另一个表明仍有改进空间的地方是 `config` 中的 `parse_config` 部分，它暗示我们返回的两个值彼此相关，并且都是一个配置值的一部分。目前，除了把两个值组合成元组，我们没有在数据结构中表达这种含义；接下来会把两个值放进一个结构体，并为结构体字段取有意义的名字。这样，未来维护这段代码的人就更容易理解不同值之间的关系及其用途。

清单 12-6 展示了对 `parse_config` 函数的改进。

<Listing number="12-6" file-name="src/main.rs" caption="重构 `parse_config` 以返回 `Config` 结构体实例">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

我们添加了一个名为 `Config` 的结构体，并为它定义了名为 `query` 和 `file_path` 的字段。现在，`parse_config` 的签名表明它返回一个 `Config` 值。在 `parse_config` 的函数体中，我们原本返回引用 `String` 中 `args` 值的字符串切片；现在则将 `Config` 定义为包含拥有所有权的 `String` 值。`args` 中的 `main` 变量拥有参数值，只允许 `parse_config` 函数借用这些值；这意味着如果 `Config` 试图取得 `args` 中值的所有权，就会违反 Rust 的借用规则。

我们有多种方式管理 `String` 数据；最简单但效率略低的方法，是对这些值调用 `clone` 方法。这会完整复制数据，让 `Config` 实例拥有副本，相比存储字符串数据的引用会消耗更多时间和内存。不过，克隆数据也让代码非常直接，因为我们不必管理引用的生命周期；在这种情况下，牺牲一点性能换取简单性是值得的权衡。

> ### 使用 `clone` 的权衡
>
> 许多 Rustacean 会因为 `clone` 的运行时成本而倾向于避免用它解决所有权问题。在[第 13 章][ch13]<!-- ignore -->中，你会学习如何在这类情况下使用更高效的方法。不过现在，复制几个字符串来继续推进完全没问题，因为这些复制只会发生一次，而且文件路径和查询字符串都很小。与其第一次实现就尝试过度优化代码，不如先拥有一个稍微低效但能正常工作的程序。随着 Rust 经验增加，从最高效的解决方案开始会更容易；但现在，调用 `clone` 完全可以接受。

我们更新了 `main`，把 `Config` 返回的 `parse_config` 实例放入名为 `config` 的变量中；同时更新了原来使用独立 `query` 和 `file_path` 变量的代码，使其改用 `Config` 结构体中的字段。

现在，代码更清楚地表达了 `query` 和 `file_path` 彼此相关，并且它们的用途是配置程序的工作方式。任何使用这些值的代码，都知道应该在 `config` 实例中按用途命名的字段里找到它们。

#### 为 `Config` 创建构造函数

到目前为止，我们已经把负责解析命令行参数的逻辑从 `main` 提取出来，并放入 `parse_config` 函数。这让我们看出 `query` 和 `file_path` 两个值彼此相关，而这种关系应该在代码中表达出来。于是，我们添加了 `Config` 结构体，为 `query` 和 `file_path` 的共同用途提供名称，并让 `parse_config` 函数能够以结构体字段名的形式返回这些值的名称。

既然 `parse_config` 函数的用途是创建 `Config` 实例，我们就可以把 `parse_config` 从普通函数改成一个与 `new` 结构体关联、名为 `Config` 的函数。这样会让代码更符合惯用写法。我们可以通过调用 `String` 创建标准库类型（例如 `String::new`）的实例。同样，把 `parse_config` 改成与 `new` 关联的 `Config` 函数后，就能通过调用 `Config` 创建 `Config::new` 实例。清单 12-7 展示了需要进行的修改。

<Listing number="12-7" file-name="src/main.rs" caption="将 `parse_config` 改为 `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

我们更新了 `main`，把原来调用 `parse_config` 的地方改为调用 `Config::new`。我们还将 `parse_config` 改名为 `new`，并把它移入 `impl` 块中，使 `new` 函数与 `Config` 关联。再次编译这段代码，确认它能正常工作。

### 修复错误处理

现在来修复错误处理。回想一下，如果 `args` 向量包含的项目少于三个，尝试访问索引 1 或索引 2 处的值就会导致程序 panic。尝试不带任何参数运行程序，结果会如下所示：

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

其中的 `index out of bounds: the len is 1 but the index is 1` 是面向程序员的错误消息。它无法帮助最终用户理解应该怎么做。现在就来修复它。

#### 改进错误消息

在清单 12-8 中，我们在 `new` 函数中添加检查，在访问索引 1 和索引 2 之前验证切片长度是否足够。如果切片长度不够，程序就会 panic 并显示更好的错误消息。

<Listing number="12-8" file-name="src/main.rs" caption="添加检查参数数量的代码">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

这段代码类似于[我们在清单 9-13 中编写的 `Guess::new` 函数][ch9-custom-types]<!-- ignore -->：当 `panic!` 参数超出有效值范围时，我们调用 `value`。这里不检查值的范围，而是检查 `args` 的长度至少为 `3`，这样函数的其余部分就可以假定这个条件已经满足。如果 `args` 少于三个项目，这个条件就为 `true`，我们会调用 `panic!` 宏立即结束程序。

在 `new` 中添加这几行代码后，再次不带参数运行程序，看看现在的错误是什么样：

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

这个输出更好了：现在有了一条合理的错误消息。不过，其中还有一些我们不希望提供给用户的多余信息。也许清单 9-13 使用的技术并不适合这里：正如[第 9 章所讨论的][ch9-error-guidelines]<!-- ignore -->，调用 `panic!` 更适合处理编程问题，而不是使用问题。相反，我们会使用在第 9 章学到的另一种技术——[返回 `Result`][ch9-result]<!-- ignore -->，用它表示成功或错误。

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### 返回 `Result` 而不是调用 `panic!`

我们可以改为返回一个 `Result` 值：成功时包含 `Config` 实例，出错时描述问题。我们还会把函数名从 `new` 改为 `build`，因为许多程序员会认为 `new` 函数不应失败。当 `Config::build` 向 `main` 传递结果时，我们可以使用 `Result` 类型发出出现问题的信号。然后，修改 `main`，把 `Err` 变体转换为对用户更实用的错误消息，同时避免 `thread
'main'` 调用带来的 `RUST_BACKTRACE` 和 `panic!` 等周边文本。

清单 12-9 展示了现在称为 `Config::build` 的函数需要对返回值所做的修改，以及让函数返回 `Result` 所需的函数体。注意，在更新 `main` 之前这段代码不会编译；我们会在下一个清单中完成更新。

<Listing number="12-9" file-name="src/main.rs" caption="从 `Result` 返回 `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

我们的 `build` 函数在成功时返回包含 `Result` 实例的 `Config`，在出错时返回字符串字面量。错误值始终是具有 `'static` 生命周期的字符串字面量。

我们对函数体做了两处修改：用户没有传入足够参数时，不再调用 `panic!`，而是返回 `Err` 值；同时把返回的 `Config` 值包装在 `Ok` 中。这些修改使函数符合新的类型签名。

从 `Err` 返回 `Config::build` 值后，`main` 函数就能处理 `Result` 函数返回的 `build`，并在出错时更干净地退出进程。

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### 调用 `Config::build` 并处理错误

为了处理错误情况并打印用户友好的消息，需要更新 `main` 来处理 `Result` 返回的 `Config::build`，如清单 12-10 所示。我们还会不再依靠 `panic!` 让命令行工具以非零错误代码退出，而是手动实现这一点。非零退出状态是一种约定，用来向调用我们程序的进程表明程序以错误状态退出。

<Listing number="12-10" file-name="src/main.rs" caption="构建 `Config` 失败时以错误代码退出">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

在这个清单中，我们使用了一个尚未详细介绍的方法：标准库为 `unwrap_or_else` 定义的 `Result<T, E>`。使用 `unwrap_or_else` 可以定义自定义的、非 `panic!` 错误处理。如果 `Result` 是 `Ok` 值，这个方法的行为类似于 `unwrap`：返回 `Ok` 包装的内部值。但如果值是 `Err`，这个方法会调用闭包中的代码；闭包是我们定义并作为参数传给 `unwrap_or_else` 的匿名函数。[第 13 章][ch13]<!-- ignore -->会更详细地介绍闭包。现在只需知道，`unwrap_or_else` 会把 `Err` 的内部值传给闭包中出现在竖线之间的 `"not enough arguments"` 参数。本例中，这个内部值就是我们在清单 12-9 中添加的静态字符串 `err`。闭包运行时就可以使用 `err` 值。

我们添加了一行新的 `use`，把标准库中的 `process` 引入作用域。错误情况下运行的闭包只有两行代码：打印 `err` 值，然后调用 `process::exit`。`process::exit` 函数会立即停止程序，并返回传入的数字作为退出状态代码。这类似于清单 12-8 中基于 `panic!` 的处理方式，但不再产生所有额外输出。试试看：

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

很好！这个输出对用户友好得多。

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### 从 `main` 中提取逻辑

现在配置解析已经重构完毕，接下来处理程序逻辑。正如[“分离二进制项目中的关注点”](#separation-of-concerns-for-binary-projects)<!-- ignore -->一节所说，我们会提取一个名为 `run` 的函数，用来保存当前 `main` 函数中与设置配置或处理错误无关的全部逻辑。完成后，`main` 函数会简洁且易于通过检查验证，我们也能为其他所有逻辑编写测试。

清单 12-11 展示了提取 `run` 函数这一小步渐进式改进。

<Listing number="12-11" file-name="src/main.rs" caption="提取包含其余程序逻辑的 `run` 函数">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

现在，`run` 函数包含 `main` 中从读取文件开始的所有剩余逻辑。`run` 函数接收 `Config` 实例作为参数。

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### 从 `run` 返回错误

将剩余程序逻辑分离到 `run` 函数后，我们可以像在清单 12-9 中处理 `Config::build` 那样改进错误处理。出现问题时，`expect` 函数不再调用 `run` 让程序 panic，而是返回 `Result<T, E>`。这样就能以用户友好的方式，把更多错误处理逻辑集中到 `main` 中。清单 12-12 展示了需要对 `run` 的签名和函数体所做的修改。

<Listing number="12-12" file-name="src/main.rs" caption="修改 `run` 函数以返回 `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

这里做了三处重要修改。首先，我们把 `run` 函数的返回类型改为 `Result<(), Box<dyn Error>>`。这个函数之前返回单元类型 `()`，现在仍将它作为 `Ok` 情况下返回的值。

对于错误类型，我们使用 trait 对象 `Box<dyn Error>`（并在顶部用 `std::error::Error` 语句将 `use` 引入作用域）。[第 18 章][ch18]<!-- ignore -->会介绍 trait 对象。现在只需知道，`Box<dyn Error>` 表示函数会返回实现了 `Error` trait 的类型，但不必指定返回值的具体类型。这让我们可以灵活地在不同错误情况下返回不同类型的错误值。关键字 `dyn` 是 _dynamic_ 的缩写。

其次，正如[第 9 章][ch9-question-mark]<!-- ignore -->所讨论的，我们移除了对 `expect` 的调用，改用 `?` 运算符。发生错误时，`panic!` 不会调用 `?`，而是从当前函数返回错误值，让调用者处理。

第三，`run` 函数现在会在成功时返回 `Ok` 值。我们在签名中将 `run` 函数的成功类型声明为 `()`，因此需要把单元类型值包装到 `Ok` 中。`Ok(())` 这样的语法初看可能有些奇怪，但这样使用 `()` 是惯用的写法，用来表示调用 `run` 只是为了它的副作用；它不会返回我们需要的值。

运行这段代码时，它会编译成功，但会显示一条警告：

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust 告诉我们，代码忽略了 `Result` 值，而 `Result` 值可能表示发生了错误。但我们没有检查是否发生错误，编译器提醒我们这里可能应该有一些错误处理代码！现在就来解决这个问题。

#### 在 `run` 中处理 `main` 返回的错误

我们会使用与清单 12-10 中处理 `Config::build` 类似的技术检查并处理错误，但有一点不同：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

我们使用 `if let` 而不是 `unwrap_or_else` 来检查 `run` 是否返回 `Err` 值，并在返回 Err 时调用 `process::exit(1)`。`run` 函数不会返回一个我们想要 `unwrap` 的值，就像 `Config::build` 返回的那样；该函数会返回 `Config` 实例。因为 `run` 在成功时返回 `()`，我们只关心检测错误，所以不需要让 `unwrap_or_else` 返回解包后的值，因为那个值只会是 `()`。

在这两种情况下，`if let` 和 `unwrap_or_else` 的函数体相同：打印错误并退出。

### 将代码拆分到库 crate 中

目前我们的 `minigrep` 项目进展不错！现在把 _src/main.rs_ 文件拆分开，将一部分代码放入 _src/lib.rs_ 文件。这样既能测试代码，也能让 _src/main.rs_ 的职责更少。

我们把负责搜索文本的代码定义在 _src/lib.rs_ 而不是 _src/main.rs_ 中。这样，我们（或其他使用 `minigrep` 库的人）就能在比 `minigrep` 二进制程序更多的上下文中调用搜索函数。

首先，按照清单 12-13 所示，在 _src/lib.rs_ 中定义 `search` 函数签名，并让函数体调用 `unimplemented!` 宏。填入实现时，我们会更详细地解释这个签名。

<Listing number="12-13" file-name="src/lib.rs" caption="在 *src/lib.rs* 中定义 `search` 函数">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

我们在函数定义中使用 `pub` 关键字，将 `search` 标记为库 crate 公共 API 的一部分。现在，我们有了一个既能从二进制 crate 使用、又能进行测试的库 crate！

现在需要把 _src/lib.rs_ 中定义的代码引入 _src/main.rs_ 的二进制 crate 作用域并调用它，如清单 12-14 所示。

<Listing number="12-14" file-name="src/main.rs" caption="在 *src/main.rs* 中使用 `minigrep` 库 crate 的 `search` 函数">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

我们添加 `use minigrep::search` 这一行，把库 crate 中的 `search` 函数引入二进制 crate 的作用域。然后在 `run` 函数中，不再打印文件内容，而是调用 `search` 函数，并将 `config.query` 值和 `contents` 作为参数传入。接着，`run` 使用 `for` 循环打印 `search` 返回且匹配查询的每一行。现在也适合移除 `println!` 函数中用于显示查询字符串和文件路径的 `main` 调用，让程序只打印搜索结果（如果没有发生错误）。

注意，搜索函数会先把所有结果收集到要返回的向量中，然后才开始打印。这种实现搜索大文件时可能会较慢地显示结果，因为找到结果时不会立即打印；我们会在第 13 章讨论使用迭代器解决这个问题的一种可能方式。

呼！工作量确实不小，但我们已经为未来的成功做好了准备。现在处理错误容易多了，代码也更加模块化。从这里开始，几乎所有工作都会在 _src/lib.rs_ 中完成。

让我们利用新获得的模块化特性，做一件旧代码很难做到、而新代码很容易做到的事：编写一些测试！

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
