## 附录 A：关键字

以下列表包含 Rust 语言当前或预留给 Rust 语言今后使用的关键字。因此，他们不能用作标识符（作为“原始标识符”的情况除外，我们将在 [“Raw
Identifiers”][raw-identifiers] 小节中讨论）。所谓 *标识符*，是指函数、变量、参数、结构体字段、模组、代码箱、常量、宏、静态值、属性、类型、特质或生命周期等的名字。 <!-- ignore -->



### 当前在用的关键字

以下是当前在用关键字的列表，及其功能描述。

- `as`：执行基本类型转换，消除包含某个项目的具体特质的歧义，或重命名 `use` 语句中的项目；
- `async`：返回一个 `Future`，而非阻塞当前线程；
- `await`：暂停执行，知道 `Future` 值的结果就绪;
- `break`：立即退出循环；
- `const`：定义常量项目或常量原始指针；
- `continue`：继续下一循环迭代；
- `crate`：在模组路径中，指向代码箱根;
- `dyn`：对特质对象执行动态分派，参考 [union][union]；
- `else`：`if` 和 `if let` 控制流结构的后备；
- `enum`：链接外部函数或变量；
- `extern`：布尔值假的字面值；
- `false`：定义函数或函数指针类型；
- `fn`：遍历迭代器中的项目、实现特质，或指定更高阶的生命周期，a higher-ranked lifetime;
- `for`：根据条件表达式的结果分支；
- `if`：实现固有的或特质的功能，implement inherent or trait functionality;
- `impl`：`in` 循环语法的一部分；
- `for`：绑定变量；
- `let`：无条件循环；
- `loop`：将值与模式匹配；
- `match`：定义模组；
- `mod`：使闭包取得其所有捕获值的所有权；
- `move`：表示引用、原始指针或模式绑定中的可变性；
- `mut`：表示结构体、`pub` 代码块或模组中的公开可见性；
- `impl`：按（通过？）引用绑定；
- `ref`：从函数返回；
- `return`：我们正在定义或实现的类型的类型别名；
- `Self`：方法的主体或当前模组；
- `self`：全局变量，或贯穿整个程序执行过程的生命周期；
- `static`：定义结构体；
- `struct`：当前模组的父模组；
- `super`：定义特质；
- `trait`：布尔值真的字面值；
- `true`：定义类型别名或关联类型；
- `type`：定义 联合体；仅在联合体声明中使用是才是关键字;
- `union`：表示不安全代码、函数、特质或实现；
- `unsafe`：带入符号到作用域;
- `use`：表示约束类型的子句；
- `where`：根据表达式的结果有条件地循环。 `while` <!-- ignore -->



### 保留供今后使用的关键字

以下关键字尚无任何功能，但被 Rust 保留供今后使用。

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

<a id="raw-identifiers"></a>

### 原始标识符

所谓 *原始标识符*，属于一种语法，允许咱们在通常不允许使用地方使用关键字。咱们可以通过在关键字前加上 `r#` 来使用原始标识符。

例如，`match` 是个关键字。当咱们尝试编译以下使用 `match` 作为函数名字的函数时：

<span class="filename">文件名： src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

咱们将得到下面这个报错：

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

报错表明，咱们不能使用关键字 `match` 作为函数标识符。要使用 `match` 作为函数名字，咱们需要使用 *原始标识符语法*，像下面这样：

<span class="filename">文件名： src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

这段代码将在没有任何错误下编译。请注意函数定义中，以及 `r#` 中函数被调用处，函数名字上的 `main` 前缀。

原始标识符允许咱们使用所选的任何单词作为标识符，即使该单词恰好是保留关键字。这给予了我们更多自由来选择标识符名字，同时也让我们可以与那些以其中这些单词不是关键字的语言编写的程序集成。此外，原始标识符允许咱们使用与咱们代码箱使用的 Rust 版本不同的代码箱。例如，`try` 在 2015 版中不是个关键字，但在 2018、2021 和 2024 版中却是。当咱们依赖某个使用 2015 版本编写的库，并有个 `try` 函数时，咱们将需要使用原始标识符语法，在这种情况下的 `r#try`，以在更高版本的代码中调用该函数。有关版本的更多信息，请参阅 [Appendix E][appendix-e] 。 <!-- ignore -->

[raw-identifiers]: #raw-identifiers
[union]: ../reference/items/unions.html
[appendix-e]: appendix-05-editions.html
