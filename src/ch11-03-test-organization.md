## 测试组织

正如本章开头所述，测试是一门复杂的学科，不同的人会使用不同的术语和组织方式。Rust 社区将测试分为两大类：单元测试和集成测试。_单元测试_规模较小、目标更集中，每次在隔离环境中测试一个模块，并且可以测试私有接口。_集成测试_完全位于库外部，以其他外部代码使用库的相同方式使用你的代码，只使用公共接口，并且每个测试可能会涉及多个模块。

编写这两类测试对于确保库的各个部分分别以及协同执行预期操作非常重要。

### 单元测试

单元测试的目的是将每个代码单元与其余代码隔离开来进行测试，从而快速定位哪些代码按预期工作、哪些没有。你会把单元测试放在 _src_ 目录中、与被测试代码所在的文件里。通常的做法是在每个文件中创建一个名为 `tests` 的模块，用来包含测试函数，并用 `cfg(test)` 标注该模块。

#### `tests` 模块与 `#[cfg(test)]`

`#[cfg(test)]` 标注附加在 `tests` 模块上，告诉 Rust 仅在运行 `cargo test` 时编译并运行测试代码，而不是在运行 `cargo
build` 时编译和运行。这在你只想构建库时可以节省编译时间，也能节省最终编译产物的空间，因为其中不包含测试。你会看到，由于集成测试位于不同的目录中，它们不需要 `#[cfg(test)]` 标注。不过，由于单元测试与代码位于同一文件中，你需要使用 `#[cfg(test)]` 指定不应将它们包含在编译结果中。

回想一下，当我们在本章第一节生成新的 `adder` 项目时，Cargo 为我们生成了下面这段代码：

<span class="filename">文件名： src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

在自动生成的 `tests` 模块上，属性 `cfg` 代表_配置_，它告诉 Rust，只有在给定某个配置选项时，后续项目才应被包含。在这里，配置选项是 `test`，Rust 在编译和运行测试时会提供它。通过使用 `cfg` 属性，Cargo 只会在我们主动用 `cargo test` 运行测试时编译测试代码。除了用 `#[test]` 标注的函数外，这还包括该模块中可能存在的任何辅助函数。

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### 私有函数测试

测试社区一直在争论是否应该直接测试私有函数，而其他语言让测试私有函数变得困难甚至不可能。无论你坚持哪种测试理念，Rust 的隐私规则确实允许测试私有函数。请看清单 11-12 中包含私有函数 `internal_adder` 的代码。

<Listing number="11-12" file-name="src/lib.rs" caption="Testing a private function">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

请注意，`internal_adder` 函数没有标记为 `pub`。测试只是 Rust 代码，而 `tests` 模块也只是另一个模块。正如我们在[“引用模块树中项目的路径”][paths]<!-- ignore -->中讨论的那样，子模块中的项目可以使用其祖先模块中的项目。在这个测试中，我们将属于 `tests` 模块父模块的所有项目通过 `use super::*` 引入作用域，然后测试就可以调用 `internal_adder`。如果你认为不应该测试私有函数，Rust 也没有任何机制强迫你这样做。

### 集成测试

在 Rust 中，集成测试完全位于库外部。它们以其他代码使用库的相同方式使用你的库，这意味着只能调用属于库公共 API 的函数。集成测试的目的是检验库的多个部分能否正确协同工作。单独运行正常的代码单元在集成后可能出现问题，因此覆盖集成代码的测试同样重要。要创建集成测试，首先需要一个 _tests_ 目录。

#### _tests_ 目录

我们在项目目录顶层、与 _src_ 并列的位置创建 _tests_ 目录。Cargo 知道要在这个目录中查找集成测试文件。随后可以根据需要创建任意多个测试文件，Cargo 会将每个文件编译为一个独立的 crate（代码包）。

我们来创建一个集成测试。保留清单 11-12 的代码在 _src/lib.rs_ 文件中，创建一个 _tests_ 目录，并新建名为 _tests/integration_test.rs_ 的文件。目录结构应如下所示：

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

将清单 11-13 中的代码输入 _tests/integration_test.rs_ 文件。

<Listing number="11-13" file-name="tests/integration_test.rs" caption="An integration test of a function in the `adder` crate">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

_tests_ 目录中的每个文件都是一个独立的 crate，因此我们需要将库引入每个测试 crate 的作用域。为此，我们在代码顶部添加 `use
adder::add_two;`，而单元测试不需要这样做。

我们不需要在 _tests/integration_test.rs_ 中的任何代码上添加 `#[cfg(test)]`。Cargo 会特殊处理 _tests_ 目录，只有在运行 `cargo test` 时才会编译该目录中的文件。现在运行 `cargo test`：

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

输出的三个部分包括单元测试、集成测试和文档测试。注意，如果某个部分中的任何测试失败，后面的部分就不会运行。例如，如果单元测试失败，就不会有集成测试和文档测试的输出，因为只有在所有单元测试都通过时，才会运行这些测试。

单元测试的第一部分与我们之前看到的一样：每个单元测试占一行（其中一个名为 `internal`，是我们在清单 11-12 中添加的），然后是一行单元测试摘要。

集成测试部分以 `Running
tests/integration_test.rs` 这一行开头。接下来，该集成测试中的每个测试函数各占一行，并且在 `Doc-tests adder` 部分开始之前还有一行集成测试结果摘要。

每个集成测试文件都有自己的部分，因此如果我们在 _tests_ 目录中添加更多文件，就会有更多集成测试部分。

我们仍然可以将测试函数的名称指定为 `cargo test` 的参数，以运行某个特定的集成测试函数。要运行某个特定集成测试文件中的全部测试，请使用 `--test` 参数，该参数属于 `cargo test`，后面跟上文件名：

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

这条命令只运行 _tests/integration_test.rs_ 文件中的测试。

#### 集成测试中的子模块

随着集成测试增多，你可能希望在 _tests_ 目录中创建更多文件来帮助组织它们；例如，可以按照被测试的功能对测试函数分组。如前所述，_tests_ 目录中的每个文件都会作为一个独立的 crate 编译，这有助于创建独立作用域，更贴近最终用户使用你的 crate 的方式。不过，这也意味着 _tests_ 目录中的文件与 _src_ 中的文件行为不同，正如你在第 7 章学习如何将代码拆分到模块和文件中时所了解的那样。

_tests_ 目录中文件的这种不同之处，在你有一组要供多个集成测试文件使用的辅助函数，并尝试按照第 7 章[“将模块拆分到不同文件”][separating-modules-into-files]<!-- ignore -->一节中的步骤将它们提取到公共模块时，最为明显。例如，如果创建 _tests/common.rs_ 并在其中放置一个名为 `setup` 的函数，就可以在 `setup` 中添加一些代码，供多个测试文件中的多个测试函数调用：

<span class="filename">文件名： tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

当我们再次运行测试时，会在测试输出中看到 _common.rs_ 文件对应的新部分，即使该文件不包含任何测试函数，我们也没有从任何地方调用 `setup` 函数：

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

让 `common` 出现在测试结果中并显示 `running 0 tests` 并不是我们想要的结果。我们只是想与其他集成测试文件共享一些代码。为了避免 `common` 出现在测试输出中，我们将创建 _tests/common/mod.rs_，而不是 _tests/common.rs_。现在项目目录如下所示：

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

这是 Rust 也能理解的旧命名约定，我们在第 7 章[“备用文件路径”][alt-paths]<!-- ignore -->一节提到过。采用这种方式命名文件会告诉 Rust，不要将 `common` 模块视为集成测试文件。当我们将 `setup` 函数的代码移到 _tests/common/mod.rs_ 并删除 _tests/common.rs_ 文件后，测试输出中就不会再出现这一部分。_tests_ 目录子目录中的文件不会被编译为独立的 crate，也不会在测试输出中拥有单独的部分。

创建 _tests/common/mod.rs_ 后，我们可以在任何集成测试文件中将它作为模块使用。下面展示了 `setup` 函数在 _tests/integration_test.rs_ 的 `it_adds_two` 测试中的调用示例：

<span class="filename">文件名： tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

请注意，`mod common;` 声明与我们在清单 7-21 中演示的模块声明相同。然后，在测试函数中，我们可以调用 `common::setup()` 函数。

#### 二进制代码包的集成测试

如果我们的项目是一个只包含 _src/main.rs_ 文件、没有 _src/lib.rs_ 文件的二进制 crate，就不能在 _tests_ 目录中创建集成测试，也不能通过 `use` 语句将 _src/main.rs_ 中定义的函数引入作用域。只有库 crate 会公开其他 crate 可以使用的函数；二进制 crate 的用途是独立运行。

这也是提供二进制文件的 Rust 项目通常采用简单的 _src/main.rs_ 文件的原因之一：该文件会调用位于 _src/lib.rs_ 文件中的逻辑。采用这种结构后，集成测试_可以_通过 `use` 测试库 crate，从而使用重要功能。如果重要功能正常工作，_src/main.rs_ 文件中的少量代码也会正常工作，因此这部分代码不需要测试。

## 总结

Rust 的测试功能提供了一种指定代码应如何运行的方式，确保即使你进行修改，代码仍会按预期工作。单元测试分别测试库的不同部分，也可以测试私有实现细节。集成测试检查库的多个部分是否正确协同工作，并使用库的公共 API，以外部代码使用库的相同方式测试代码。尽管 Rust 的类型系统和所有权规则有助于防止某些类型的 bug，测试对于减少与代码预期行为有关的逻辑 bug 仍然很重要。

让我们结合本章和前面章节学到的知识，开始做一个项目吧！

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
