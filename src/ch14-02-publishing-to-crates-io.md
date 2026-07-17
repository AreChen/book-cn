## 发布代码箱到 Crates.io

我们已将 [crates.io](https://crates.io/) 上的包用作过项目的依赖项，但我们也可以通过发布咱们自己的包，与其他人分享自己的代码。位于 [crates.io](https://crates.io/) 网站的代码箱登记簿，会分发咱们包的源码，因此他主要托管开源代码。

Rust 与 Cargo 都有着一些让我们发布的包，更容易被人们找到并使用的特性。接下来我们将讨论其中一些特性，然后讲解怎样发布包。

### 制作有用的文档注释

准确地为咱们的包编写文档，将帮助到其他用户了解怎样及何时来使用他们，因此投入时间编写文档是非常值得的。在第 3 章中，我们讨论过怎样使用双斜杠 `//` 来注释 Rust 代码。Rust 还有针对文档的一种特别注释，通常称为 *文档注释，documentation comment*，将生成 HTML 文档。生成的 HTML 会显示针对公开 API 项目的文档注释内容，是为有兴趣了解怎样 *使用* 咱们的代码箱，而不是对其 *实现* 感兴趣的程序员准确的。

文档注释使用三斜杠 `///` 而非双斜杠，并支持 Markdown 表示法来格式化文本。要放置文档注释于他们说明的项目正上方。下面清单 14-1 展示了名为 `add_one` 的代码箱中 `my_crate` 函数的文档注释。

<Listing number="14-1" file-name="src/lib.rs" caption="函数的文档注释">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

在这里，我们描述了 `add_one` 函数执行的操作，以标题 `Examples` 开始了一个小节，然后提供了演示怎样使用 `add_one` 函数的代码。我们可以通过运行 `cargo doc` 从这一文档注释生成 HTML 文档。这条命令运行随 Rust 一起分发的 `rustdoc` 工具，并放置生成的 HTML 文档于 target/doc 目录中。

出于便利目的，运行 `cargo doc --open` 将针对咱们的当前代码箱的文档（以及所有咱们的代码箱的依赖项的文档）构建 HTML，并在 web 浏览器中打开结果。导航到 `add_one` 函数，咱们将看到文档注释中的文本是如何渲染的，如下图 14-01 中所示：

例如，为了添加描述包含 `add_one` 函数的 `my_crate` 代码箱用途的文档，我们就要添加以 //! 开头的文档注释，至 src/lib.rs 文件的开头，如下清单 14-2 中所示：

文件：`add_one`

#### 常用小节

请注意，以 `# Examples` 开头的最后一行之后没有任何代码。由于我们以 //! 而不是 /// 开始注释，因此我们是在给包含这种注释的程序项目，而非紧接着这种注释之后的程序项目编写文档。在这一情形下，该项目是 src/lib.rs 文件，是代码箱根。这些注释描述了整个代码箱。
- **Panics**：这里描述文档中函数可能 panic 的场景。不希望程序 panic 的调用者，应确保不会在这些场景下调用该函数。
- **错误**：如果函数返回 `Result`，说明可能发生的错误类型，以及可能导致这些错误返回的条件，会帮助调用者编写代码来以不同方式处理错误。
- **安全性**：如果调用函数需要 `unsafe`（我们将在第 20 章讨论不安全性），应说明函数为何不安全，并覆盖函数期望调用者维护的不变量。

大多数文档注释不需要包含所有这些小节，但这是一份很好的检查清单，可以提醒你用户希望了解代码的哪些方面。
#### 作为测试的文档注释

在文档注释中添加示例代码块，可以帮助展示如何使用库，而且还有额外好处：运行 `cargo test` 会把文档中的代码示例作为测试运行！没有什么比带有示例的文档更好，但也没有什么比因代码在编写文档后发生变化而无法运行的示例更糟。如果我们再次运行 `cargo test`，针对清单 14-1 中 `add_one` 函数的文档，会在测试结果中看到类似下面的部分：
```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

现在，如果修改函数或示例，使示例中的 `assert_eq!` 触发 panic，然后再次运行 `cargo test`，就会看到文档测试能够发现示例与代码彼此不同步！
<a id="commenting-contained-items"></a>

#### 包含的程序项目注释

请注意，以 `//!` 开头的最后一行之后没有任何代码。由于我们以 `my_crate` 而不是 `add_one` 开始注释，因此我们是在给包含这种注释的程序项目，而非紧接着这种注释之后的程序项目编写文档。在这一情形下，该项目是 `//!` 文件，是代码箱根。这些注释描述了整个代码箱。

<Listing number="14-2" file-name="src/lib.rs" caption="`my_crate` 代码箱作为一个整体的文档">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

请注意，以 `//!` 开头的最后一行之后没有任何代码。由于我们以 `//!` 而不是 `///` 开始注释，因此我们是在为包含该注释的项目编写文档，而不是为该注释之后的项目编写文档。在这里，这个项目是作为箱根的 _src/lib.rs_ 文件。这些注释描述整个箱。

运行 `cargo doc --open` 时，这些注释会显示在 `my_crate` 文档首页的公开项目列表上方，如图 14-2 所示。
项目内的文档注释对于描述代码箱及模组尤其有用。请使用他们说明容器的总体用途，以帮助咱们的用户理解代码箱的组织结构。
![渲染出的 cargo_features_demo 代码箱文档]

**图 14-02**：`my_crate` 渲染后的文档, 包括作为整体描述该代码箱的注释

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

### 导出便捷的公开 API

在第 7 章中，咱们介绍了怎样使用 `pub` 关键字构造项目为公开，以及怎样以 `use` 关键字带入项目到作用域。然而，在开发代码箱时对咱们有意义的组织结构（模组树），对于咱们的用户可能并不方便。咱们可能打算组织咱们的结构为包含多个级别的层次结构，但后来打算使用某个咱们定义在层次结构深处的类型的人，可能在找出该类型是否存在时遇到麻烦。他们可能还会因为不得不输入 `use
my_crate::some_module::another_module::UsefulType;`，而不是输入 `use
my_crate::UsefulType;` 而感到恼火。

好消息是，当组织结构 *不* 便于其他人在另一库中使用时，咱们不必调整咱们的内部组织结构：相反，咱们可以通过使用 `pub use` 重新导出程序项目，以构造一种不同于咱们的私有组织结构的公开组织结构。所谓 *重新导出*，会取位于一处的某个公开程序项目，并构造其为在另一处公开，就像他被定义在另一处一样。

例如，假设我们出于建模美术概念目的，构造了一个名为 `art` 的库。这个库内有两个模组：包含两个名为 `kinds` 与 `PrimaryColor` 枚举的 `SecondaryColor` 模组，和包含名为 `utils` 函数的 `mix` 模组，如下清单 14-3 中所示：

<Listing number="14-3" file-name="src/lib.rs" caption="`art` 库，有着组织在 `kinds` 与 `utils` 两个模组中的程序项目">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

下图 14-03 展示了由 `cargo doc` 生成的这个代码箱的文档的首页的样子：

**图 14-3**：`art` 库的文档的首页，列出了 `kinds` 与 `utils` 两个模组

请注意，`art` 与 SecondaryColor 两个类型并未在首页上列出，mix 函数也如此。我们必须点击 `kinds` 与 `utils` 才能看到他们。

请注意，`PrimaryColor` 和 `SecondaryColor` 类型没有列在首页上，`mix` 函数也没有。我们必须点击 `kinds` 和 `utils` 才能看到它们。

依赖这个库的另一个箱需要使用 `use` 语句将 `art` 中的项目引入作用域，并指定当前定义的模块结构。清单 14-4 展示了一个使用 `PrimaryColor` 和 `mix` 项目的 `art` 箱。

<Listing number="14-4" file-name="src/main.rs" caption="使用 `art` 代码箱的项目的代码箱，art 代码箱的内部组织结构已导出">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

清单 14-4 中使用 `art` 箱的代码作者必须弄清楚 `PrimaryColor` 位于 `kinds` 模块，而 `mix` 位于 `utils` 模块。`art` 箱的模块结构对于开发 `art` 箱的人比对于使用它的人更有意义。内部结构并没有提供使用 `art` 箱所需的有用信息，反而会造成困惑，因为使用者必须找出应该查看的位置，并在 `use` 语句中指定模块名。
在存在许多嵌套模组的情形下，以 `art` 在顶层重新导出类型，可以对使用代码箱的人的体验造成显著差异。`pub use` 的另一个常见用途是重新导出当前代码箱中的依赖项的定义，以使该代码箱的定义，成为咱们的代码箱的公开 API 的一部分。

<Listing number="14-5" file-name="src/lib.rs" caption="添加 `pub use` 语句以重新导出程序项目">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

现在，`cargo doc` 为该箱生成的 API 文档会在首页列出并链接重新导出的项目，如图 14-4 所示，使 `PrimaryColor` 和 `SecondaryColor` 类型以及 `mix` 函数更容易找到。
<img alt="Rendered documentation for the `art` crate with the re-exports on the front page" src="img/trpl14-04.png" class="center" />
<span class="caption">图 14-4：`art` 文档首页，其中列出了重新导出的项目</span>
`art` 箱的用户仍然可以像清单 14-4 所示那样查看并使用清单 14-3 中的内部结构，也可以如清单 14-6 所示使用清单 14-5 中更方便的结构。

<Listing number="14-6" file-name="src/main.rs" caption="使用 `art` 代码箱中重新导出项目的程序">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

当存在许多嵌套模块时，在顶层使用 `pub use` 重新导出类型，可以显著改善箱用户的体验。`pub use` 的另一个常见用途，是重新导出当前箱中依赖项的定义，使该依赖项的定义成为你的箱公开 API 的一部分。

创建有用的公开 API 结构更像是一门艺术，而不是一门科学；你可以不断尝试，找出最适合用户的 API。选择 `pub use` 可以让你灵活组织箱的内部结构，并将内部结构与你向用户展示的内容解耦。可以看看已安装箱的一些代码，了解它们的内部结构是否不同于公开 API。
### 建立 Crates.io 帐号

在发布任何代码箱之前，咱们需要在 [crates.io](https://crates.io/) 上创建一个账户并获取 API 令牌。为此，请访问 [crates.io](https://crates.io/) 的主页，并通过 GitHub 帐号登录。（目前需要 GitHub 账户，但该站点今后可能会支持其他创建帐号的方式。）登录后，请访问 [https://crates.io/me/](https://crates.io/me/) 处的帐号设置，并获取咱们的 API 密钥。然后，运行 `cargo login` 命令并在出现提示时粘贴咱们的密钥，如下所示：

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

这条命令将告知 Cargo 咱们的 API 令牌，并存储在本地的 ~/.cargo/credentials 文件中。请注意，这个令牌属于机密信息：请不要与任何人分享。当咱们出于任何原因与任何人分享了时，咱们都应在 [crates.io](https://crates.io/) 上吊销他并生成一个新的令牌。

### 添加元数据到新代码箱

假设咱们有个打算发布的代码箱。在发布前，咱们将需要在该代码箱的 Cargo.toml 文件的 `[package]` 小节中添加一些元数据。

咱们的代码箱将需要一个独特的名字。在本地开发代码箱时，咱们可以给代码箱取随意命名。但是，[crates.io](https://crates.io/) 上的代码箱名字，是按照先到先得的原则分配的。一旦某个名字已被占用，其他人就不能以那个名字发布代码箱。在尝试发布代码箱之前，请县检索咱们打算使用的名字。当名字已被使用时，咱们将需要找到另一个名字，并编辑 `name` 文件中 `[package]` 小节下的 name 字段，以使用新的名字进行发布，像下面这样：

<span class="filename">文件名： Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

即使咱们选择了个独特的名字，当咱们此时运行 `cargo publish` 来发布代码箱时，仍将受到一条告警，然后一条报错：

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

这导致了一个报错，因为咱们缺少一些关键信息：描述信息及许可证是必需的，由此人们才会知道咱们的代码箱做什么，以及可以在什么条款下使用他。在 Cargo.toml 中，添加以两句话的描述信息，因为他会与咱们的代码箱一起出现在搜索结果中。对于 `license` 字段，咱们需要提供 *许可证标识符值*。[Linux 基金会的软件包数据交换] 列出了咱们可以针对该值使用的标识符。例如，要指定咱们已使用 MIT 许可证授权咱们的代码箱，请添加 `MIT` 标识符：

<span class="filename">文件名： Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

当咱们打算使用某种未出现在 SPDX 中的许可证时，咱们就需要放置该许可证的文本于文件中，在咱们的项目中包含该文件，然后使用 `license-file` 来指定该文件的名字，而不是使用 `license` 键。

关于哪种许可证适合咱们的项目方面的指南超出了这本书的范围。Rust 社区的许多人都以与 Rust 项目相同方式，使用 `MIT OR Apache-2.0` 双重许可证授权他们的项目。这种做法表明，咱们也可以指定由 `OR` 分隔的多个许可证标识符，有着针对咱们项目的多种许可证。

添加了唯一名字、版本号、描述信息及许可证后，某个已准备好发布的项目的 Cargo.toml文件可能看起来像下面这样：

<span class="filename">文件名： Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Cargo 的文档](https://doc.rust-lang.org/cargo/) 描述了其他咱们可以指定的元数据，以确保其他人可以更轻松地发现和使用咱们的代码箱。

### 发布到 Crates.io

现在咱们已经创建了账号，保存了 API 令牌，为代码箱选择了名字，并指定了所需的元数据，咱们就可以开始发布了！发布代码箱会上传特定版本到 [crates.io](https://crates.io/)，供他人使用。

请小心！因为发布是 *永久性的*。该版本永远无法被覆盖，除特殊情况外，代码也无法被删除。Crates.io 的一个主要目标是充当代码的永久存档，以便依赖于 [crates.io](https://crates.io/) 上的代码箱的所有项目的构建都将持续工作。允许版本删除将使该目标变得不可能。不过，咱们可以发布的代码箱版本数量没有限制。

再次运行 `cargo publish` 命令。现在应该成功了：

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

恭喜！咱们现在已经与 Rust 社区分享了咱们的代码，任何人都可以轻松地添加咱们的代码箱为他们项目的依赖项。

### 发布现有代码箱的新版本

当咱们对代码箱的进行了修改，而准备发布新版本时，咱们要修改在 Cargo.toml 中指定的 `version` 值并重新发布。请根据咱们所做的修改类型，使用 [语义化版本控制规则] 来确定合适的下一个版本编号。然后，运行 `cargo publish` 上传新的版本。

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>

<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### 弃用 Crates.io 上的版本

尽管咱们无法移除代码箱的较早版本，但咱们可以阻止任何今后的项目添加他们为新的依赖项。当代码箱版本出于某种原因被破坏时，这一特性非常有用。在这种情形下，Cargo 支持 *抽出* 代码箱版本。

*抽出* 版本会防止新项目依赖于该版本，同时允许所有依赖他的现有项目继续正常运行。本质上，抽出意味着所有带有 Cargo.lock 的项目都不会中断，并且任何今后生成的 Cargo.lock 文件都将不会使用抽出的版本。

要抽出代码箱的某个版本，就要在咱们先前发布的代码箱目录下，运行 `cargo yank` 并指定咱们打算抽出的版本。例如，当咱们已发布一个名为 `guessing_game` 版本 0.1.0 的代码箱，而打算抽出他时，那么我们就要在 `guessing_game` 的项目目录下运行以下命令：

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

通过添加 `--undo` 到这个命令，咱们还可以撤销抽出，而允许项目再次依赖于某个版本：

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

抽出版本 *不会* 删除任何代码。例如，他无法删除意外上传的机密信息。当发生这种情况时，咱们必须立即重置这些机密信息。

<!-- ignore -->

<!-- ignore -->

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- ignore -->

<!-- ignore -->

<!-- ignore -->

<!-- ignore
-->

<!-- ignore -->

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

<!-- ignore -->

<!-- ignore -->

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

<!-- Old headings. Do not remove or links may break. -->

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/
