## 引用与借用

清单 4-5 中的元组代码的问题在于，我们必须将 `String` 返回给调用函数，这样在调用
之后仍然可以使用这个 `String`；这是因为在 `calculate_length` 调用中，`String` 被
移动到了 `calculate_length` 中。作为替代，我们可以提供 `String` 值的引用。
引用就像指针，因为它是一个可以跟随的地址，我们可以通过它访问存储在该地址的数据；
该数据由其他变量拥有。与指针不同，引用保证在其生命周期内始终指向特定类型的有效值。

下面是定义和使用 `calculate_length` 函数的方法：它以对象的引用作为参数，而不是获取
值的所有权：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:all}}
```

</Listing>

首先，注意变量声明和函数返回值中的所有元组代码都消失了。其次，注意我们将 `&s1`
传入 `calculate_length`，并且在其定义中使用 `&String` 而不是 `String`。这些与号
表示引用，允许你引用某个值而不取得其所有权。图 4-6 描绘了这个概念。

<img alt="三张表：s 的表只包含一个指向 s1 的表的指针。s1 的表包含 s1 的栈数据，并指向堆上的字符串数据。" src="img/trpl04-06.svg" class="center" />

<span class="caption">图 4-6：`&String` 示意图：`s` 指向 `String` `s1`</span>

> 注意：使用 `&` 进行引用的相反操作是_解引用_，由解引用运算符 `*` 完成。我们将在
> 第 8 章看到解引用运算符的一些用法，并在第 15 章详细讨论解引用。

让我们更仔细地看看这里的函数调用：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-07-reference/src/main.rs:here}}
```

`&s1` 语法让我们创建一个_指向_ `s1` 值的引用，但不拥有它。因为引用不拥有它所
指向的值，所以当引用停止使用时，该值不会被丢弃。

同样，函数签名使用 `&` 表示参数 `s` 的类型是引用。让我们添加一些解释性注释：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-08-reference-with-annotations/src/main.rs:here}}
```

变量 `s` 有效的作用域与任何函数参数的作用域相同，但引用所指向的值不会在 `s`
停止使用时被丢弃，因为 `s` 不拥有它。当函数使用引用作为参数而非实际值时，我们不
必为了归还所有权而返回值，因为我们从未拥有过所有权。

创建引用的行为称为_借用_。就像现实生活中一样，如果某人拥有某件东西，你可以从他
那里借来。使用完后必须归还；你并不拥有它。

那么，如果我们试图修改正在借用的东西，会发生什么？试试清单 4-6 中的代码。先提
示一下：它行不通！

<Listing number="4-6" file-name="src/main.rs" caption="尝试修改借用的值">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-06/src/main.rs}}
```

</Listing>

错误如下：

```console
{{#include ../listings/ch04-understanding-ownership/listing-04-06/output.txt}}
```

正如变量默认不可变一样，引用也默认不可变。我们不能修改引用所指向的东西。

### 可变引用

只需做一些小改动，改用_可变引用_，就可以修复清单 4-6 中的代码，使我们能够修改
借用的值：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-09-fixes-listing-04-06/src/main.rs}}
```

</Listing>

首先，我们将 `s` 改为 `mut`。然后，使用 `&mut s` 创建可变引用并调用 `change` 函数，
同时更新函数签名，使其接受 `some_string: &mut String` 这样的可变引用。这样就非常
清楚地表明，`change` 函数会修改它借用的值。

可变引用有一条重要限制：如果你有一个值的可变引用，就不能再拥有该值的其他引用。
下面这段试图为 `s` 创建两个可变引用的代码会失败：

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/src/main.rs:here}}
```

</Listing>

错误如下：

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-10-multiple-mut-not-allowed/output.txt}}
```

这条错误信息说明，代码无效是因为我们不能在同一时间多次将 `s` 借用为可变引用。
第一个可变借用位于 `r1` 中，必须一直持续到它在 `println!` 中被使用；但在创建这个
可变引用与使用它之间，我们又试图在 `r2` 中创建一个借用与 `r1` 相同数据的可变引用。

禁止同时存在同一数据的多个可变引用，可以在非常受控的方式下进行修改。新接触 Rust
的人常常会为此感到困难，因为大多数语言都允许你随时修改数据。这条限制的好处是，
Rust 可以在编译时阻止数据竞争。_数据竞争_类似于竞态条件，会在以下三种行为同时发
生时出现：

- 两个或更多指针同时访问同一数据。
- 至少有一个指针用于写入数据。
- 没有使用任何机制来同步对数据的访问。

数据竞争会导致未定义行为，在运行时追踪时可能很难诊断和修复；Rust 通过拒绝编译含
有数据竞争的代码来避免这个问题！

和往常一样，我们可以使用花括号创建新的作用域，从而允许存在多个可变引用，只是它们
不能_同时_存在：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-11-muts-in-separate-scopes/src/main.rs:here}}
```

Rust 对组合可变引用与不可变引用也施加了类似的规则。下面这段代码会产生错误：

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/src/main.rs:here}}
```

错误如下：

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-12-immutable-and-mutable-not-allowed/output.txt}}
```

呼！当我们拥有同一个值的不可变引用时，也不能拥有可变引用。

使用不可变引用的人不会预期值突然在眼前发生改变！不过，多个不可变引用是
允许的，因为只读取数据的人无法影响其他人对数据的读取。

注意，引用的作用域从引入引用的地方开始，一直持续到最后一次使用该引用。例如，下面
的代码可以编译，因为不可变引用最后一次使用是在引入可变引用之前的 `println!` 中：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-13-reference-scope-ends/src/main.rs:here}}
```

不可变引用 `r1` 和 `r2` 的作用域在它们最后一次使用的 `println!` 之后结束，而这发
生在创建可变引用 `r3` 之前。这些作用域没有重叠，因此代码是允许的：编译器可以判断
出，在作用域结束前的某个位置已经不再使用该引用。

即使借用错误有时令人沮丧，也要记住，这是 Rust 编译器在早期（编译时而不是运行时）
指出潜在错误，并准确告诉你问题所在。这样，你就不必追查数据为何没有保持预期的状态。

### 悬空引用

在使用指针的语言中，很容易错误地创建一个_悬空指针_——即指向某个内存位置的指针——
例如释放内存，却保留指向该内存的指针，而该位置可能已经交给了其他人。相比之下，
在 Rust 中，编译器保证引用永远不会悬空：如果你拥有某些数据的引用，编译器会确保
该数据不会在引用本身失效之前离开作用域。

让我们尝试创建一个悬空引用，看看 Rust 如何通过编译时错误阻止它：

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/src/main.rs}}
```

</Listing>

错误如下：

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-14-dangling-reference/output.txt}}
```

这条错误信息提到了我们尚未介绍的特性：生命周期。我们将在第 10 章详细讨论生命周
期。不过，忽略有关生命周期的部分后，错误信息确实包含了说明这段代码为何有问题的
关键：

```text
this function's return type contains a borrowed value, but there is no value
for it to be borrowed from
```

让我们更仔细地看看 `dangle` 代码的每个阶段究竟发生了什么：

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-15-dangling-reference-annotated/src/main.rs:here}}
```

</Listing>

因为 `s` 在 `dangle` 内部创建，所以 `dangle` 的代码执行完毕时，`s` 就会被释放。
但我们试图返回一个指向它的引用。这意味着该引用会指向无效的 `String`。这当然不行！
Rust 不会允许我们这样做。

这里的解决方案是直接返回 `String`：

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-16-no-dangle/src/main.rs:here}}
```

这样做不会有任何问题。所有权被移出，并且没有数据被释放。

### 引用的规则

我们来回顾一下我们讨论过的关于引用的内容：

- 在任何给定时间，你可以_要么_拥有一个可变引用，_要么_拥有任意数量的不可变引用。
- 引用必须始终有效。

接下来，我们将看看另一种不同的引用：切片。
