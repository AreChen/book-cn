## 泛型数据类型

我们使用泛型为函数签名或结构体等项目创建定义，然后就可以将它们与许多不同的
具体数据类型一起使用。先来看看如何使用泛型定义函数、结构体、枚举和方法。然
后，我们会讨论泛型如何影响代码性能。

### 在函数定义中

定义使用泛型的函数时，应当把泛型放在函数签名中通常指定参数和返回值数据类型
的位置。这样可以让代码更加灵活，为函数调用方提供更多功能，同时避免代码重复。

继续讨论 `largest` 函数。清单 10-4 展示了两个都查找切片中最大值的函数。之后
我们会将它们合并为一个使用泛型的函数。

<Listing number="10-4" file-name="src/main.rs" caption="仅名称和签名中的类型不同的两个函数">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

`largest_i32` 函数就是我们在清单 10-3 中提取的函数，用于查找切片中的最大
`i32`。`largest_char` 函数查找切片中的最大 `char`。这两个函数的函数体代码相同，
因此我们可以在一个函数中引入泛型类型参数来消除重复。

要在新的单一函数中参数化类型，需要像给函数的值参数命名一样，为类型参数命名。
类型参数名可以使用任意标识符。不过我们将使用 `T`，因为按照惯例，Rust 中的类
型参数名很短，通常只有一个字母，并且遵循 UpperCamelCase 类型命名约定。`T` 是
_type_ 的缩写，是大多数 Rust 程序员的默认选择。

在函数体中使用参数时，必须在签名中声明参数名，让编译器知道该名称的含义。同样，
在函数签名中使用类型参数名时，也必须在使用前声明类型参数名。要定义泛型
`largest` 函数，可以像下面这样，将类型名声明放在尖括号 `<>` 中，位于函数名
和参数列表之间：

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

我们可以将这个定义读作：“函数 `largest` 对某种类型 `T` 是泛型的。”这个函数有
一个名为 `list` 的参数，它是 `T` 类型值的切片。`largest` 函数会返回指向同一
`T` 类型值的引用。

清单 10-5 展示了在签名中使用泛型数据类型的合并版 `largest` 函数定义。清单还
展示了如何使用 `i32` 值切片或 `char` 值切片调用该函数。注意，这段代码目前还
无法编译。

<Listing number="10-5" file-name="src/main.rs" caption="使用泛型类型参数的 `largest` 函数；这段代码目前还无法编译">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

现在编译这段代码，会得到以下错误：

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

帮助文本提到了 `std::cmp::PartialOrd`，它是一个 trait；下一节将讨论 trait。现在
只需知道，这个错误表示 `largest` 的函数体无法适用于 `T` 可能代表的所有类型。
因为函数体中想要比较 `T` 类型的值，所以只能使用值可以排序的类型。为了支持比
较，标准库提供了 `std::cmp::PartialOrd` trait，可以在类型上实现它（有关这个
trait 的更多信息，请参阅附录 C）。要修复清单 10-5，可以按照帮助文本的建议，
将 `T` 的有效类型限制为实现了 `PartialOrd` 的类型。这样清单就能编译了，因为
标准库为 `PartialOrd` 和 `i32` 都实现了 `char`。

### 在结构体定义中

我们也可以使用 `<>` 语法定义结构体，让一个或多个字段使用泛型类型参数。清单
10-6 定义了一个 `Point<T>` 结构体，用来保存任意类型的 `x` 和 `y` 坐标值。

<Listing number="10-6" file-name="src/main.rs" caption="保存 `Point<T>` 类型 `x` 和 `y` 值的 `T` 结构体">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

在结构体定义中使用泛型的语法与函数定义中的语法类似。首先，在结构体名称之后
紧接着的尖括号中声明类型参数名。然后，在结构体定义中原本要指定具体数据类型
的位置使用泛型类型。

注意，因为定义 `Point<T>` 时只使用了一个泛型类型，这个定义表示 `Point<T>` 对
某种类型 `T` 是泛型的，并且无论 T 是什么类型，字段 `x` 和 `y` 都是_同一种_
类型。如果像清单 10-7 那样创建包含不同类型值的 `Point<T>` 实例，代码就无法
编译。

<Listing number="10-7" file-name="src/main.rs" caption="字段 `x` 和 `y` 必须是同一类型，因为它们使用相同的泛型数据类型 `T`。">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

在这个示例中，将整数值 `5` 赋给 `x` 时，我们让编译器知道这个实例的泛型类型
`T` 将是整数，即 `Point<T>`。随后指定 `4.0` 作为 `y` 的值；由于我们将其定义为与
`x` 具有相同类型，就会得到如下类型不匹配错误：

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

要定义一个 `Point` 结构体，让 `x` 和 `y` 都是泛型但可以具有不同类型，可以使用
多个泛型类型参数。例如在清单 10-8 中，我们将 `Point` 定义为对类型 `T` 和 `U`
泛型，其中 `x` 是 `T` 类型，`y` 是 `U` 类型。

<Listing number="10-8" file-name="src/main.rs" caption="对两种类型泛型的 `Point<T, U>`，使 `x` 和 `y` 可以是不同类型的值">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

现在展示的所有 `Point` 实例都合法了！定义中可以使用任意数量的泛型类型参数，
但使用超过几个参数会让代码难以阅读。如果发现代码需要大量泛型类型，可能说明
应该将代码重构为更小的部分。

### 在枚举定义中

和结构体一样，我们可以定义枚举，让其变体保存泛型数据类型。再看看标准库提供
的、我们在第 6 章使用过的 `Option<T>` 枚举：

```rust
enum Option<T> {
    Some(T),
    None,
}
```

现在这个定义应该更容易理解了。可以看到，`Option<T>` 枚举对类型 `T` 是泛型的，
有两个变体：`Some` 保存一个 `T` 类型的值，`None` 不保存任何值。通过使用
`Option<T>` 枚举，我们可以表达“可选值”这一抽象概念；由于 `Option<T>` 是泛型
的，无论可选值是什么类型，都可以使用这个抽象。

枚举也可以使用多个泛型类型。我们在第 9 章使用的 `Result` 枚举就是一个例子：

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`Result` 枚举对两种类型 `T` 和 `E` 是泛型的，并有两个变体：`Ok` 保存 `T` 类型
的值，`Err` 保存 `E` 类型的值。这个定义让我们可以在任何可能成功（返回某种
`Result` 类型的值）或失败（返回某种 `T` 类型的错误）的操作中方便地使用 `E` 枚
举。事实上，清单 9-3 中打开文件时就使用了它：文件成功打开时，`T` 被填充为
`std::fs::File` 类型；打开文件出现问题时，`E` 被填充为 `std::io::Error` 类型。

当你发现代码中有多个结构体或枚举定义，它们的区别仅在于所保存值的类型时，可以
改用泛型类型来避免重复。

### 在方法定义中

我们可以像第 5 章那样为结构体和枚举实现方法，也可以在方法定义中使用泛型类型。
清单 10-9 展示了为清单 10-6 中定义的 `Point<T>` 结构体实现名为 `x` 的方法。

<Listing number="10-9" file-name="src/main.rs" caption="在 `x` 结构体上实现名为 `Point<T>` 的方法，返回 `x` 类型 `T` 字段的引用">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

这里，我们在 `x` 上定义了名为 `Point<T>` 的方法，它返回字段 `x` 中数据的引用。

注意，我们必须紧接在 `T` 后声明 `impl`，这样才能用 `T` 指定正在为 `Point<T>`
类型实现方法。在 `T` 后将 `impl` 声明为泛型类型后，Rust 就能识别 `Point` 尖括
号中的类型是泛型类型，而不是具体类型。这个泛型参数可以使用不同于结构体定义
中泛型参数的名称，但使用相同名称是惯例。如果在声明了泛型类型的 `impl` 中编写
方法，那么无论泛型类型最终替换成什么具体类型，该方法都会定义在该类型的所有
实例上。

在为类型定义方法时，也可以指定泛型类型的约束。例如，可以只为 `Point<f32>` 实
例实现方法，而不是为任意泛型类型的 `Point<T>` 实例实现。在清单 10-10 中，我
们使用具体类型 `f32`，这意味着不需要在 `impl` 后声明任何类型。

<Listing number="10-10" file-name="src/main.rs" caption="只适用于泛型类型参数 `impl` 为特定具体类型的结构体的 `T` 块">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

这段代码意味着 `Point<f32>` 类型会拥有 `distance_from_origin` 方法；`Point<T>` 不是
`T` 类型的其他 `f32` 实例不会定义这个方法。该方法测量点与坐标为 (0.0,
0.0) 的点之间的距离，并使用只有浮点类型才支持的数学运算。

结构体定义中的泛型类型参数不一定与该结构体方法签名中使用的泛型类型参数相同。
为了让示例更清晰，清单 10-11 为 `X1` 结构体使用泛型类型 `Y1` 和 `Point`，为
`X2` 方法签名使用 `Y2` 和 `mixup`。该方法创建一个新的 `Point` 实例，其中 `x`
值来自 `self` `Point`（类型为 `X1`），`y` 值来自传入的 `Point`（类型为 `Y2`）。

<Listing number="10-11" file-name="src/main.rs" caption="使用不同于结构体定义的泛型类型的方法">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

在 `main` 中，我们定义了一个 `Point`：类型为 `i32` 的 `x` 字段值为 `5`，
类型为 `f64` 的 `y` 字段值为 `10.4`。变量 `p2` 是一个 `Point` 结构体：它的
`x` 是字符串切片（值为 `"Hello"`），而 `char` 类型的 `y` 值为 `c`。调用 `mixup`，
以 `p1` 为对象、`p2` 为参数，会得到 `p3`；它会有 `i32` 类型的 `x`，因为 `x` 来自 `p1`；
`p3` 会有 `char` 类型的 `y`，因为 `y` 来自 `p2`。`println!` 宏调用会打印
`p3.x = 5, p3.y = c`。

这个示例旨在演示一种情况：一些泛型参数在 `impl` 中声明，另一些在方法定义中
声明。这里，泛型参数 `X1` 和 `Y1` 在 `impl` 后声明，因为它们属于结构体定义。
泛型参数 `X2` 和 `Y2` 在 `fn mixup` 后声明，因为它们只与该方法相关。

### 使用泛型的代码的性能

你可能会想，使用泛型类型参数是否会带来运行时成本。好消息是，使用泛型类型不
会让程序比使用具体类型时运行得更慢。

Rust 通过在编译时对使用泛型的代码进行单态化来实现这一点。_单态化_ 是将编译时
使用的具体类型填入泛型代码、把它转换为具体代码的过程。在这个过程中，编译器
执行的步骤与我们创建清单 10-5 中泛型函数时相反：编译器查找所有调用泛型代码的
位置，并为调用泛型代码时使用的具体类型生成代码。

使用标准库的泛型 `Option<T>` 枚举，看看它是如何工作的：

```rust
let integer = Some(5);
let float = Some(5.0);
```

Rust 编译这段代码时，会执行单态化。在这个过程中，编译器读取 `Option<T>` 实例
中使用的值，并识别出两种 `Option<T>`：一种是 `i32`，另一种是 `f64`。于是，它
将 `Option<T>` 的泛型定义展开为分别针对 `i32` 和 `f64` 的两个定义，用具体定义
替换泛型定义。

代码的单态化版本类似下面这样（这里只为说明方便，编译器使用的名称与这里不同）：

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

泛型 `Option<T>` 被编译器创建的具体定义替换。由于 Rust 会将泛型代码编译为每
个实例都指定类型的代码，使用泛型不会产生运行时成本。代码运行时，其行为与我
们手动复制每个定义完全相同。单态化过程让 Rust 的泛型在运行时非常高效。
