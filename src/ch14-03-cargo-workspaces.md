## Cargo 工作区

在第 12 章中，我们构建了一个包含二进制代码箱和库代码箱的包。随着项目的发展，你可能会发现库代码箱不断变大，并希望将包进一步拆分为多个库代码箱。Cargo 提供了名为 _工作区_ 的功能，可以帮助管理协同开发的多个相关包。

### 创建工作区

_工作区_ 是一组共享同一个 _Cargo.lock_ 文件和输出目录的包。让我们创建一个使用工作区的项目——我们会使用简单的代码，以便专注于工作区的结构。组织工作区有多种方式，所以这里只展示一种常见的方式。我们将创建一个包含一个二进制代码箱和两个库代码箱的工作区。提供主要功能的二进制代码箱将依赖这两个库代码箱。一个库代码箱将提供 `add_one` 函数，另一个库代码箱将提供 `add_two` 函数。这三个代码箱将属于同一工作区。我们先创建一个新的工作区目录：

```console
$ mkdir add
$ cd add
```

接下来，在 _add_ 目录中，我们创建用于配置整个工作区的 _Cargo.toml_ 文件。这个文件不会有 `[package]` 部分。相反，它会以 `[workspace]` 部分开头，从而允许我们向工作区添加成员。我们还通过将 `resolver` 的值设置为 `"3"`，特意让工作区使用 Cargo 解析器算法的最新版本：

<span class="filename">文件名： Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

接下来，我们将创建 `adder` 二进制代码箱，方法是在 _add_ 目录中运行 `cargo new`：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

在工作区内运行 `cargo new` 也会自动将新创建的包添加到工作区 _Cargo.toml_ 中 `members` 键所在的 `[workspace]` 定义中，如下所示：

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

此时，我们可以通过运行 `cargo build` 来构建工作区。_add_ 目录中的文件应如下所示：

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

工作区顶层只有一个 _target_ 目录，编译产物会放置其中；`adder` 包没有自己的 _target_ 目录。即使我们从 _adder_ 目录中运行 `cargo build`，编译产物仍会进入 _add/target_，而不是 _add/adder/target_。Cargo 之所以这样组织工作区中的 _target_ 目录，是因为工作区中的代码箱预期会相互依赖。如果每个代码箱都有自己的 _target_ 目录，那么为了将产物放入自己的 _target_ 目录，每个代码箱都必须重新编译工作区中的其他每个代码箱。共享一个 _target_ 目录可以避免不必要的重新构建。

### 在工作区中创建第二个包

接下来，让我们在工作区中创建另一个成员包，并将其命名为 `add_one`。生成一个名为 `add_one` 的新库代码箱：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

顶层的 _Cargo.toml_ 现在会在 `members` 列表中包含 _add_one_ 路径：

<span class="filename">文件名： Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

你的 _add_ 目录现在应该包含以下目录和文件：

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

在 _add_one/src/lib.rs_ 文件中，让我们添加一个 `add_one` 函数：

<span class="filename">文件名： add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

现在，我们可以让包含二进制代码箱的 `adder` 包依赖包含库的 `add_one` 包。首先，需要在 _adder/Cargo.toml_ 中为 `add_one` 添加路径依赖。

<span class="filename">文件名： adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo 不会假设工作区中的代码箱会相互依赖，因此我们需要明确说明依赖关系。

接下来，让我们使用 `add_one` 函数（来自 `add_one` 代码箱），并在 `adder` 代码箱中调用它。打开 _adder/src/main.rs_ 文件，将 `main` 函数改为调用 `add_one` 函数，如清单 14-7 所示。

<Listing number="14-7" file-name="adder/src/main.rs" caption="Using the `add_one` library crate from the `adder` crate">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

让我们在顶层 _add_ 目录中运行 `cargo build` 来构建工作区！

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

要从 _add_ 目录运行二进制代码箱，我们可以使用 `-p` 参数和包名，并配合 `cargo run`，来指定要运行的工作区包：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

这会运行 _adder/src/main.rs_ 中的代码，该代码依赖 `add_one` 代码箱。

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### 依赖外部包

请注意，工作区顶层只有一个 _Cargo.lock_ 文件，而不是每个代码箱目录中各有一个 _Cargo.lock_。这可以确保所有代码箱对所有依赖使用相同版本。如果我们将 `rand` 包添加到 _adder/Cargo.toml_ 和 _add_one/Cargo.toml_ 文件中，Cargo 会将二者解析为同一个 `rand` 版本，并将其记录在这一个 _Cargo.lock_ 中。让工作区中的所有代码箱使用相同的依赖意味着它们始终彼此兼容。让我们将 `rand` 代码箱添加到 _add_one/Cargo.toml_ 文件的 `[dependencies]` 部分，以便可以使用 `rand` 代码箱，并在 `add_one` 代码箱中使用它：

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">文件名： add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

现在，我们可以将 `use rand;` 添加到 _add_one/src/lib.rs_ 文件中；然后，在 _add_ 目录中运行 `cargo build` 构建整个工作区，就会引入并编译 `rand` 代码箱。由于我们没有使用引入作用域的 `rand`，因此会收到一条警告：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

顶层 _Cargo.lock_ 现在包含有关 `add_one` 依赖 `rand` 的信息。不过，尽管工作区中的某处使用了 `rand`，除非也将 `rand` 添加到其他代码箱的 _Cargo.toml_ 文件中，否则我们无法在工作区的其他代码箱中使用它。例如，如果我们将 `use rand;` 添加到 _adder/src/main.rs_ 文件中供 `adder` 包使用，就会得到一个错误：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

要修复这一问题，请编辑 `adder` 包的 _Cargo.toml_ 文件，并表明 `rand` 也是它的依赖项。构建 `adder` 包会将 `rand` 添加到 _Cargo.lock_ 中 `adder` 的依赖项列表，但不会再下载 `rand` 的副本。Cargo 会确保工作区中每个使用 `rand` 包的包中的每个代码箱都使用相同版本，只要它们指定了兼容版本的 `rand`，这样既节省空间，也确保工作区中的代码箱彼此兼容。

如果工作区中的代码箱指定了同一依赖的不兼容版本，Cargo 会解析出每个版本，但仍会尽量解析出尽可能少的版本。

### 向工作区添加测试

作为另一项改进，让我们为 `add_one::add_one` 函数在 `add_one` 代码箱中添加测试：

<span class="filename">文件名： add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

现在，在顶层 _add_ 目录中运行 `cargo test`。在像这样组织的工作区中运行 `cargo test`，会运行工作区中所有代码箱的测试：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

输出的第一部分显示 `it_works` 测试在 `add_one` 代码箱中已通过。下一部分显示在 `adder` 代码箱中找到零个测试，最后一部分显示在 `add_one` 代码箱中找到零个文档测试。

我们还可以从顶层目录运行工作区中某个代码箱的测试，方法是使用 `-p` 标志并指定要测试的代码箱名称：

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

此输出表明，`cargo test` 只运行了 `add_one` 代码箱的测试，没有运行 `adder` 代码箱的测试。

如果将工作区中的代码箱发布到
[crates.io](https://crates.io/)<!-- ignore -->，工作区中的每个代码箱都需要单独发布。与 `cargo test` 一样，我们可以使用 `-p` 标志并指定要发布的代码箱名称，来发布工作区中的特定代码箱。

作为额外练习，向此工作区添加一个 `add_two` 代码箱，方式类似于 `add_one` 代码箱！

随着项目的发展，请考虑使用工作区：它能让你使用更小、更易于理解的组件，而不是一大团代码。此外，如果代码箱经常同时发生变化，将它们保留在工作区中可以让代码箱之间更容易协调。
