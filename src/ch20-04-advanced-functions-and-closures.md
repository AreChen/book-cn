## 高级函数和闭包

这一小节探讨与函数和闭包相关的一些高级特性，包括函数指针以及返回闭包。

### 函数指针

我们已经讨论了怎样传递闭包给函数；咱们也可以传递常规函数给函数！当咱们打算传递某个已定义好的函数，而不是定义新的闭包时，这种技巧非常有用。函数会强制转换为 `fn` 类型（`Fn` 小写），而不会与 `fn` 的闭包特质混淆。fn 类型被称为 *函数指针，function pointer*。通过函数指针传递函数将允许咱们把函数作为其他函数的参数使用。

指定参数为函数指针的语法与闭包的语法类似，如下清单 20-28 中所示，其中我们定义了个名为 `add_one` 的函数，会将其参数加 1。函数 `do_twice` 取两个参数：一个指向任何取 `i32` 的参数并返回 `i32` 值的函数的函数指针，以及一个 `i32` 值。`do_twice` 函数调用函数 `f` 两次，向其传递 `arg` 值，然后将两次函数调用的结果相加。`main` 函数以参数 `do_twice` 与 `add_one` 调用 `5`。

<Listing number="20-28" file-name="src/main.rs" caption="Using the `fn` type to accept a function pointer as an argument">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

这段代码打印 `The answer is: 12`。我们指定 `f` 中的参数 `do_twice` 是个 `fn`，取 `i32` 类型的参数并返回一个 `i32`。然后我们可以在 `f` 的函数体中调用 `do_twice`。在 `main` 中，我们可以作为第一个参数传递函数名 `add_one` 给 `do_twice`。

与闭包不同，`fn` 是一种类型而非特质，因此我们可以直接指定 `fn` 为参数类型，而不是以 `Fn` 的特质之一作为特质边界，声明一个泛型类型参数。

函数指针实现了所有三个闭包特质（`Fn`、`FnMut` 和 `FnOnce`），这意味着咱们始终可以作为参数，传递函数指针给期望闭包的函数。最好使用泛型类型和闭包特质之一编写函数，以便咱们的函数既可以接受函数，也可以接受闭包。

也就是说，咱们只希望接受 `fn` 而不接受闭包的一种示例，是与不支持闭包的外部代码交互时：C 函数可以接受函数作为参数，但 C 不支持闭包。

作为咱们既可以使用内联定义的闭包，也可以使用命名函数的示例，我们来看看标准库中 `map` 特质提供的 `Iterator` 方法的用法。要使用 `map` 方法将一个数字矢量转换为字符串矢量，我们可以使用闭包，如下清单 20-29 中所示。

<Listing number="20-29" caption="Using a closure with the `map` method to convert numbers to strings">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

或者，我们可以将一个函数作为 `map` 的参数代替闭包。下面清单 20-30 展示了这种做法的样子。

<Listing number="20-30" caption="Using the `String::to_string` function with the `map` method to convert numbers to strings">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

请注意，由于存在名为 `to_string` 的可用函数，因此我们必须使用在 [“Advanced Traits”][advanced-traits] 小节中提到的完全限定语法。 <!-- ignore -->

在这里， 我们使用的是定义在 `to_string` 特质中的 `ToString` 函数，标准库已针对任何实现 `Display` 特质的类型实现了这一特质。

回顾第 6 章中 [“Enum Values”][enum-values] 小节，我们定义的每个枚举变种的名字，也会成为一个初始化函数。我们可以将这些初始化函数作为实现闭包特质的函数指针使用，这意味着我们指定初始化函数为取闭包的方法的参数，如下清单 20-31 中所示。 <!-- ignore -->

<Listing number="20-31" caption="Using an enum initializer with the `map` method to create a `Status` instance from numbers">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

在这里，我们通过使用 `Status::Value` 的初始化函数，使用对其调用 `u32` 的范围中的每个 `map` 值创建 `Status::Value` 的实例。有些人希望这种风格，有些人则更倾向于使用闭包。两种方式会编译为同样的代码，因此请使用咱们觉得更清晰的风格。

### 返回闭包

闭包由特质表示，这意味着咱们不能直接返回闭包。在大多数咱们可能希望返回特质的情形下，咱们可以转而使用实现该特质的具体类型作为函数的返回值。然而，对于闭包咱们通常不能这样做，因为他们没有可返回的具体类型；例如，当闭包捕获了其作用域中的任何值时，咱们就不允许使用函数指针 `fn` 作为返回类型。

相反，咱们将通常使用我们在第 10 章学过的 `impl Trait` 语法。咱们可以使用 `Fn`、`FnOnce` 和 `FnMut`，返回任何函数类型。例如，以下清单 20-32 中的代码将正常编译。

<Listing number="20-32" caption="Returning a closure from a function using the `impl Trait` syntax">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

然而，正如我们在第 13 章中 [“Inferring and Annotating Closure
Types”][closure-types] 小节中指出的，每个闭包本身也属于其自己的独特类型。当咱们需要处理多个有着相同签名，却有着不同实现的函数时，就将需要为他们使用特质对象。试想一下，当咱们编写像是下面清单 20-33 中所示的代码时，会发生什么。 <!-- ignore -->

<Listing file-name="src/main.rs" number="20-33" caption="Creating a `Vec<T>` of closures defined by functions that return `impl Fn` types">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

这里我们有两个函数：`returns_closure` 和 `returns_initialized_closure`，他们都返回 `impl Fn(i32) -> i32`。请注意，尽管他们实现了同一类型，但返回的闭包却不同。当我们尝试编译这段代码时，Rust 会让我们知道这行不通：

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

这一报错消息告诉我们，每当我们返回 `impl Trait` 时，Rust 都会创建一个唯一的 *不透明类型，opaque type*，其中我们无法窥见 Rust 为我们构建的具体细节，也无法推测出 Rust 将生成何种类型供我们自行编写。因此，尽管这两个函数返回了实现相同特质（`Fn(i32) -> i32`） 的闭包，但 Rust 为每个闭包生成的不透明类型却是不同的。（这类似于我们在第 17 章中 [“The `Pin` Type and the `Unpin` Trait”][future-types] 中看到的，即使不同异步代码块有着同一输出类型，Rust 也会为他们生成不同的具体类型。）我们已经多次看到这种问题的解决方案：我们可以使用特质对象，如下清单 20-34 中所示。 <!-- ignore -->

<Listing number="20-34" caption="Creating a `Vec<T>` of closures defined by functions that return `Box<dyn Fn>` so that they have the same type">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

这段代码可以正常编译。有关特质对象的更多信息，请参阅第 18 章中 [“Using Trait Objects To Abstract over Shared
Behavior”][trait-objects] 小节。 <!-- ignore -->

接下来，我们来看看宏！

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
