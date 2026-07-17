## 使用环境变量

我们将通过添加一项额外特性改进这个 `minigrep` 二进制项目：用户可通过环境变量打开的不区分大小写的检索选项。我们本可以构造这一特性为命令行选项，并要求用户每次希望应用时输入他，但通过构造其为环境变量，我们允许用户设置一次环境变量，而让该终端会话中的所有检索都不区分大小写。

<!-- Old headings. Do not remove or links may break. -->

<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### 为不区分大小写的检索编写失败测试

我们首先添加一个新的 `search_case_insensitive` 函数到 `minigrep` 库，将在环境变量有值时调用。我们将继续遵循 TDD 流程，因此第一步仍然是编写失败的测试。我们将为新的 `search_case_insensitive` 函数添加一个新的测试，并将原有测试从 `one_result` 重命名为 `case_sensitive`，以区分两个测试的差异，如下清单 12-20 中所示。

<Listing number="12-20" file-name="src/lib.rs" caption="为我们即将添加的不区分大小写的函数，添加新的失败测试">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

请注意，我们也编辑了原先测试的 `contents`。我们添加了个有着文本 `"Duct tape."` 的新行。当我们以区分大小写的方式检索时，使用大写 *D* 不应与查询字串 `"duct"` 匹配。以这种方式修改原来的测试，有助于确保我们不会意外破坏我们已经实现的区分大小写的检索功能。这个测试现在应该通过，并且在我们开发不区分大小写的检索时，也应会继续通过。

针对 *不区分* 大小写的检索的新测试使用 `"rUsT"` 作为查询字符串。在我们将要添加的 `search_case_insensitive` 函数中，查询字符串 `"rUsT"` 应匹配包含有着大写字母 R 的 `"Rust:"` 的行，并会匹配行 `"Trust me."`。即使两行有着与查询字符串不同的大小写。这是我们的失败测试，他将编译失败，因为我们尚未定义 `search_case_insensitive` 函数。请随意添加一个始终返回空矢量值的骨架实现，类似于我们在 [清单 12-16] 中对 `search` 函数所做的方式，以看到测试会编译并会失败。

### 实现 `search_case_insensitive` 函数

如下清单 12-21 中所示，`search_case_insensitive` 函数将几乎与 `search` 函数一样。唯一区别就是，我们将把 `query` 与每个 `line` 都小写，以便无论输入参数的大小写如何，当我们检查该行是否包含查询字符串时，他们都将是同一种大小写。

<Listing number="12-21" file-name="src/lib.rs" caption="定义 `search_case_insensitive` 函数为在比较查询字符串和行之前将他们小写">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

首先，我们将 `query` 字符串小写并将其存储在名字相同的新的变量中，从而遮蔽原先的 `query`。在查询字串上调用 `to_lowercase` 是必要的，这样无论用户查询的是 `"rust"`、`"RUST"`、`"Rust"` 还是 `"rUsT"`，我们都将把查询字符串当作 `"rust"` 处理，而对大小写不敏感。虽然 `to_lowercase` 可以处理基本的 Unicode 字符，但他不会 100% 准确。若我们在编写真正的应用时，我们会希望在这里做更多的处理，但由于这一小节是关于环境变量，而非 Unicode，因此暂且到此为止。

请注意，现在 `query` 是个 `String` 而非字符串切片，因为调用 `to_lowercase` 会创建新数据而不是引用既有收据。例如假设查询字符串是 `"rUsT"`：该字符串切片不包含可供我们使用的小写字母 `u` 或 `t`，因此我们必须分配一个包含 `String` 的新 `"rust"`。当我们现在作为参数传递  `query` 给 `contains` 时，我们需要添加一个 & 运算符，因为 `contains` 的签名被定义为取一个字符串切片。

接下来，我们对每个 `to_lowercase` 调用 `line`，以小写所有字符。现在我们转换了 `line` 和 `query` 为小写，无论查询字符串为何种大小写，我们都将找到匹配项。

我们来看看这一实现是否会通过测试：

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

太好了！测试通过了。现在，我们来在 `search_case_insensitive` 函数中调用新的 `run` 函数。首先，我们将添加一个配置项到 `Config` 结构体，以在区分大小写与不区分大小写的检索之间切换。添加这个字段将导致编译器报错，因为我们尚未在任何地方初始化这个字段：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

我们添加了个保存布尔值的 `ignore_case` 字段。接下来，我们需要 `run` 函数来检查 `ignore_case` 字段的值，并使用该值来决定调用 `search` 函数还是 `search_case_insensitive` 函数，如下清单 12-22 中所示。这段代码仍然还不会编译。

<Listing number="12-22" file-name="src/main.rs" caption="依据 `search` 中的值调用 `search_case_insensitive` 或 `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

最后，我们需要检查环境变量。用于处理环境变量的函数位于便准库中的 `env` 模组中，其已在作用域中，位于 src/main.rs 的顶部。我们将使用 `var` 模组中的 `env` 函数，来检查是否已经为名为 `IGNORE_CASE` 的环境变量设置了任何值，如下清单 12-23 中所示。

<Listing number="12-23" file-name="src/main.rs" caption="检查名为 `IGNORE_CASE` 的环境变量中的是否有任何值">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

在这里，我们创建一个新变量 `ignore_case`。为了获取他的值，我们调用 `env::var` 函数并传递给他 `IGNORE_CASE` 环境变量的名字。当该环境变量被设置了任何值时，`env::var` 函数会返回一个 `Result` 值，其将是包含该环境变量的值的 `Ok` 变种。当该环境变量未被设置时，他将返回 `Err` 变种。

我们使用 `is_ok` 上的 `Result` 方法，来检查环境变量是否设置，这意味着程序应执行不区分大小写的检索。当 `IGNORE_CASE` 环境变量未设置为任何内容时，`is_ok` 将返回 `false`，进而程序将执行区分大小写的检索。我们不关心该环境变量的 *值*，只关心他是已设置或未设置，因此我们检查 `is_ok`，而不是使用 `unwrap`、`expect` 或我们已经在 `Result` 上看到的任何其他方法。

我们传递 `ignore_case` 变量中的值给 `Config` 实例，以便 `run` 函数可以读取到该值，并决定是调用 `search_case_insensitive` 还是 `search`，正如我们在清单 12-22 中所实现的那样。

我们来试一试！首先，我们将在不设置环境变量，并以查询字符串 `to` 运行程序，这应匹配任何包含全部小写单词 “to” 的行：

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

看起来这仍然正常工作！现在我们来在 `IGNORE_CASE` 设置为 `1` 下，而以同样的查询字符串 `to` 运行程序：

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

当咱们使用的是 PowerShell 时，咱们将需要以单独命令分别设置环境变量和运行程序：

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

这将使 `IGNORE_CASE` 在咱们的 shell 会话的剩余时间内持续存在。该环境变量可以使用 `Remove-Item` 这个 cmdlet 取消设置。

```console
PS> Remove-Item Env:IGNORE_CASE
```

我们应得到包含可能有大写字母的 *to* 的行：

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

太棒了，我们还得到了包含 *To* 的行！我们的 `minigrep` 程序现在可以执行由环境变量控制的不区分大小写的检索。现在咱们知道怎样使用命令行参数或环境变量来管理选项集。

一些程序允许针对同一配置同时使用命令行参数 *和* 环境变量。在这些情况下，程序会决定其中一个优先。对于咱们自己的其他练习，请尝试通过命令行参数或环境变量控制区分大小写。当程序以一组区分大小写和另一组忽略大小写时，请确定是命令行参数优先，还是环境变量优先。

`std::env` 模组包含许多用于处理环境变量的更有用特性：请查看文档以了解哪些特性可用。
