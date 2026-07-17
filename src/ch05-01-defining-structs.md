## 定义与实例化结构体

结构体与[“元组类型”][tuples]<!--
ignore -->一节中讨论的元组类似，因为两者都保存多个相关值。与元组一样，结构体的各个部分可以是不同类型。不同于元组，结构体会为每一部分数据命名，因此值的含义很清楚。添加这些名称意味着结构体比元组更灵活：你不必依赖数据的顺序来指定或访问实例的值。

要定义结构体，我们输入关键字 `struct` 并为整个结构体命名。结构体的名称应描述分组在一起的数据各部分的意义。然后，在花括号内，我们定义这些数据部分的名称和类型，并将它们称为_字段_。例如，示例 5-1 展示了一个存储用户账户信息的结构体。

<Listing number="5-1" file-name="src/main.rs" caption="`User` 结构体定义">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

定义结构体后，要使用它，我们通过为每个字段指定具体值来创建该结构体的_实例_。我们通过写出结构体名称创建实例，然后添加包含_`key:
value`_ 对的花括号，其中键是字段名称，值是我们要存储在这些字段中的数据。我们不必按照在结构体中声明字段的相同顺序指定字段。换句话说，结构体定义像是该类型的通用模板，而实例用具体数据填充该模板，以创建该类型的值。例如，我们可以声明一个特定用户，如示例 5-2 所示。

<Listing number="5-2" file-name="src/main.rs" caption="创建 `User` 结构体的实例">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

要从结构体中获取某个特定值，我们使用点表示法。例如，要访问该用户的电子邮件地址，我们使用 `user1.email`。如果实例是可变的，我们可以使用点表示法并为某个特定字段赋值来改变值。示例 5-3 展示了如何更改一个可变实例中的 `email` 字段值，该实例属于 `User` 类型。

<Listing number="5-3" file-name="src/main.rs" caption="修改 `email` 字段的值（位于可变的 `User` 实例中）">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

请注意，整个实例必须是可变的；Rust 不允许我们只将某些字段标记为可变。与任何表达式一样，我们可以将结构体的新实例构造为函数体中的最后一个表达式，从而隐式返回这个新实例。

示例 5-4 展示了 `build_user` 函数，它接收给定的电子邮件和用户名并返回一个 `User` 实例。`active` 字段的值为 `true`，`sign_in_count` 的值为 `1`。

<Listing number="5-4" file-name="src/main.rs" caption="接收电子邮件和用户名的 `build_user` 函数，并返回一个 `User` 实例">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

让函数参数与结构体字段使用相同的名称是合理的，但不得不重复 `email` 和 `username` 字段名称及变量名有些乏味。如果结构体有更多字段，重复每个名称会更加令人厌烦。幸运的是，有一种方便的简写！

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### 使用字段初始化简写

由于示例 5-4 中的参数名称与结构体字段名称完全相同，我们可以使用_字段初始化简写_语法重写 `build_user`，使其行为完全相同，同时避免重复 `username` 和 `email`，如示例 5-5 所示。

<Listing number="5-5" file-name="src/main.rs" caption="使用字段初始化简写的 `build_user` 函数：`username` 和 `email` 参数与结构体字段同名">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

这里，我们正在创建 `User` 结构体的新实例，它有一个名为 `email` 的字段。我们希望将 `email` 字段的值设置为 `email` 参数（位于 `build_user` 函数中）的值。由于 `email` 字段和 `email` 参数同名，我们只需写下 `email`，而不是 `email: email`。

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### 使用结构体更新语法创建实例

创建一个包含同类型另一个实例的大部分值、但更改其中一些值的新实例通常很有用。你可以使用结构体更新语法完成这件事。

首先，在示例 5-6 中，我们展示如何以常规方式（不使用更新语法）创建一个新的 `User` 实例，并将其放在 `user2` 中。我们为 `email` 设置新值，但其余值使用示例 5-2 中创建的 `user1` 的相同值。

<Listing number="5-6" file-name="src/main.rs" caption="使用 `User` 中来自 `user1` 的除一个值外的所有值创建新实例">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

使用结构体更新语法，我们可以用更少的代码实现相同效果，如示例 5-7 所示。语法 `..` 指定未显式设置的其余字段应与给定实例中对应字段具有相同的值。

<Listing number="5-7" file-name="src/main.rs" caption="设置 `email` 新值的 `User` 实例，同时使用 `user1` 中的其余值">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

示例 5-7 中的代码还会在 `user2` 中创建一个实例，它的 `email` 值不同，但 `username`、`active` 和 `sign_in_count` 字段的值与 `user1` 相同。`..user1` 必须放在最后，以指定其余字段应从 `user1` 中对应的字段获取值；但无论结构体定义中字段的顺序如何，我们都可以按任意顺序为任意数量的字段指定值。

请注意，结构体更新语法像赋值一样使用 `=`；这是因为它会移动数据，正如我们在[“变量和数据交互：移动”][move]<!-- ignore -->一节中看到的那样。在这个示例中，我们不能再使用 `user1`；这是因为在创建 `user2` 后，`String` 已从 `username` 字段中的 `user1` 移动到 `user2`。如果我们给 `user2` 提供新的 `String` 值用于 `email` 和 `username` 字段，从而只使用 `active` 和 `sign_in_count` 这两个来自 `user1` 的值，那么 `user1` 在创建 `user2` 后仍然有效。`active` 和 `sign_in_count` 的类型都实现了 `Copy` 特质，因此[“仅存储在栈上的数据：Copy”][copy]<!-- ignore -->一节中讨论的行为会适用。在这个示例中，我们仍然可以使用 `user1.email`，因为它的值没有从 `user1` 中移出。

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### 使用元组结构体创建不同类型

Rust 还支持类似元组的结构体，称为_元组结构体_。元组结构体具有结构体名称带来的额外含义，但其字段没有关联的名称；相反，它们只有字段的类型。当你想给整个元组命名，使元组与其他元组成为不同类型，或者在普通结构体中命名每个字段会过于冗长或重复时，元组结构体就很有用。

要定义元组结构体，请以 `struct` 关键字和结构体名称开头，后面跟着元组中的类型。例如，这里我们定义并使用两个名为 `Color` 和 `Point` 的元组结构体：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

请注意，`black` 和 `origin` 值的类型不同，因为它们是不同元组结构体的实例。你定义的每个结构体都是自己的类型，即使结构体中的字段可能具有相同的类型。例如，接收 `Color` 类型参数的函数不能将 `Point` 作为参数，即使这两种类型都由三个 `i32` 值组成。此外，元组结构体的实例与元组类似：你可以将它们解构为各个部分，并使用 `.` 后跟索引来访问单个值。与元组不同，解构元组结构体时需要写出结构体类型。例如，我们可以写 `let Point(x, y, z) = origin;`，将 `origin` 点中的值解构为名为 `x`、`y` 和 `z` 的变量。

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### 定义类单元结构体

你还可以定义没有任何字段的结构体！这类结构体称为_类单元结构体_，因为它们的行为类似于 `()`，即我们在[“元组类型”][tuples]<!-- ignore -->一节中提到的单元类型。类单元结构体在你需要为某个类型实现特质、但不想在类型本身存储任何数据时很有用。我们将在第 10 章讨论特质。下面是声明并实例化一个名为 `AlwaysEqual` 的类单元结构体的示例：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

要定义 `AlwaysEqual`，我们使用 `struct` 关键字、想要的名称，然后写一个分号。不需要花括号或圆括号！接着，我们可以用类似的方式获得 `AlwaysEqual` 的一个实例，并将其放入 `subject` 变量中：使用定义的名称，不需要任何花括号或圆括号。想象一下，我们稍后会为这种类型实现某种行为，使 `AlwaysEqual` 的每个实例始终等于任何其他类型的每个实例，也许是为了在测试中获得一个已知结果。实现这种行为不需要任何数据！你将在第 10 章看到如何定义特质并在任何类型上实现特质，包括类单元结构体。

> ### 结构体数据的所有权
>
> 在示例 5-1 的 `User` 结构体定义中，我们使用了拥有所有权的 `String` 类型，而不是 `&str` 字符串切片类型。这是有意的，因为我们希望该结构体的每个实例都拥有自己的全部数据，并且这些数据在整个结构体有效期间都保持有效。
>
> 结构体也可以存储由其他对象拥有的数据的引用，但这需要使用_生命周期_，这是我们将在第 10 章讨论的 Rust 特性。生命周期确保结构体所引用的数据在结构体有效期间一直有效。假设你尝试在结构体中存储引用，却没有指定生命周期，就像下面 *src/main.rs* 中这样；这不会起作用：
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> 编译器会抱怨它需要生命周期说明符：
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> 在第 10 章中，我们会讨论如何修复这些错误，以便可以在结构体中存储引用；但现在，我们会使用 `String` 这样的拥有所有权的类型，而不是 `&str` 这样的引用，来修复这类错误。

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
