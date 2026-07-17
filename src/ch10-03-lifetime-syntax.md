<a id="preventing-dangling-references-with-lifetimes"></a>

## 以生命周期验证引用

生命周期属于另一种我们已在使用的泛型。与确保类型有着我们所期望的行为不同，生命周期确保引用在咱们需要他们的整个期间内都有效。

我们在第 4 章中的 [引用与借用] 小节中未曾讨论的一个细节是，Rust 中的每个引用都有一个生命周期，即该引用有效的作用域。大多数时候，生命周期都是隐式的和推导出的，就像大多数时候类型是推导出的一样。只有当存在多种可能的类型时，我们才需要注解类型。以类似方式，当引用的生命周期可以数种方式关联时，我们必须注解生命周期。Rust 要求我们使用泛型声明周期参数注解关系，以确保运行时使用的实际引用将肯定有效。

注解生命周期甚至都不是绝大多数其他编程语言所有的概念，因此这会让人感到陌生。尽管我们在这一章中不会介绍生命周期的全部，但咱们将讨论咱们可能会遇到生命周期语法的常见方式，以便咱们可以适应这个概念。

### 悬空引用

生命周期的主要目的是防止悬空引用，dangling references，若允许他们存在，将导致程序引用与其预期不同的数据。请考虑下面清单 10-16 中的程序，他有一个外层作用域和一个内层作用域。

<Listing number="10-16" caption="尝试使用其值已超出作用域的引用">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> **注意**：清单 10-16、10-17 及 10-23 中的示例均在没有赋予变量初始值下声明了变量，因此变量名字存在于外层作用域中。乍一看，这似乎与 Rust 没有空值相冲突。然而，当我们在赋值前尝试使用变量，我们将得到一个编译器时错误，这表示 Rust 确实不允许空值。

外层作用域声明了个名为 `r` 的变量，没有初始值，内层作用域声明了个名为 `x` 的变量，有着初始值 `5`。在内层作用域内，咱们尝试将 `r` 的值设置为到 `x` 的引用。然后，内层作用域结束，我们尝试打印 `r` 中的值。这段代码将不编译，因为在我们尝试使用 `r` 所引用的值前，他已超出了作用域。下面是错误消息：

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

错误消息指出，变量 `x` “does not live long enough. （未存活足够长时间）” 原因是 `x` 将在第 7 行处内层作用域结束时超出作用域。但 `r` 对于外层作用域仍有效；由于其作用域更大，我们说他 “存活时间更长”。若 Rust 允许这段代码工作，`r` 将引用 `x` 超出作用域时解除分配的内存，而尝试对 `r` 执行的任何操作都将不会正确地工作。那么，Rust 是怎样判断这段代码无效的呢？他使用借用检查器。

> **译注**：Rust 使作用域成为可定量计算、可参数化。
### 借用检查器

Rust 编译器有个 *借用检查器，borrow checker*，会比较作用域以确定所有借用是否有效。下面清单 10-17 显示了与清单 10-16 相同的代码，但带有展示变量生命周期的注解。

<Listing number="10-17" caption="`r` 与 `x` 的生命周期注解，分别命名为 `'a` 和 `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

在这里，咱们以 `r` 注解了 `'a` 的声明周期，以 `x` 注解了 `'b` 的生命周期。正如咱们所见，相比外层的 `'b` 声明周期块，内层的 `'a` 块小得多。在编译时，Rust 会比较这两个生命周期的大小，发现 `r` 有着 `'a` 的生命周期，但他引用了有着 `'b` 生命周期的内存。这个程序被拒绝，因为 `'b` 短于 `'a`：引用主体存活时间短于引用。

下面清单 10-18 修复了该代码，使其没有悬空引用进而其会在没有任何错误下编译。

<Listing number="10-18" caption="有效引用，因为数据有着比引用更长的生命周期">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

这里，`x` 有着生命周期 `'b`，在这一情形下大于 `'a`。这意味着 `r` 可以应用 `x`，因为 Rust 知道当 `r` 有效时，`x` 中的引用将始终有效。

现在咱们知道引用的生命周期在何处以及 Rust 怎样分析生命周期以确保引用将始终有效，下面我们来探讨函数参数与返回值中的泛型生命周期。

### 函数中的泛型生命周期

我们将编写一个函数，返回两个字符串切片中较长的那个。这个函数将取两个字符串切片，并返回单个字符串切片。在我们实现 `longest` 函数后，下面清单 10-19 中的代码应打印 `The longest string is abcd`。

<Listing number="10-19" file-name="src/main.rs" caption="调用 `main` 函数来找出两个字符串切片中较长的那个的 `longest` 函数">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

当咱们尝试实现如下面清单 10-20 中所示的 `longest` 函数时，其将不编译。

我们来看看生命周期注解怎样通过传入有着不同具体生命周期的引用限制 `longest` 函数。下面清单 10-22 是个直观的示例。

<Listing number="10-20" file-name="src/main.rs" caption="一种 `longest` 函数的实现，返回两个字符串切片中较长的那个，但尚不会编译">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

在这个示例中，string1 在外层作用域结束之前有效，string2 在内层作用域结束之前有效，而 result 引用在内层作用域结束之前有效的内容。运行这段代码，咱们将看到借用检查器批准；他将编译并打印 最长字符串为 长字符串就是长。

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

帮助文本揭示，返回类型需要其上的泛型生命周期，因为 Rust 无法区分返回的引用指向 `x` 还是 `y`。实际上，我们也不知道，因为这个函数主体中的`if` 代码块返回一个到参数 `x` 的引用，而 `else` 代码块返回一个到 `y` 的引用！
当咱们定义这个函数时，我们不知道将传入这个函数的具体值，因此我们不知道`if` 情况将执行，还是 `else` 情况将执行。我们也不知道将传入的引用的具体生命周期，因此我们无法像我们在 [清单 10-17]) 与 [清单 10-18]) 中那样，查看作用域来确定我们返回的引用将是否始终有效。借用检查器也无法确定这点，因为他不知道 `x` 与 `y` 的生命周期如何与返回值的生命周期关联。为了修复这个错误，我们将添加定义引用之间关系的泛型生命周期参数，以便借用检查器可以执行其分析。
### 生命周期注解语法

生命周期注解不会改变任何引用的存活时间。相反，他们在不影响生命周期下，描述了多个引用的生命周期相互之间的关系。正如在签名指定了泛型参数后函数可以接受任何类型一样，函数可以通过指定泛型生命周期参数接受带有任何生命周期的引用。
生命周期注解有着些许不同寻常的语法：生命周期参数的名字必须以撇号（单引号，`'`）开头，通常都是小写，并且像泛型一样非常短。大多数人使用名字 `'a` 作为第一个生命周期注解。我们将生命周期注解放在引用的 `&` 之后，使用空格将这种注解与引用的类型分开。
下面是一些示例 -- 到没有生命周期参数的 `i32` 的引用、到有着名为 `i32` 的生命周期参数的 `'a` 的引用，以及到同样有着生命周期 `i32` 的 `'a` 的可变引用。
```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

<a id="lifetime-annotations-in-function-signatures"></a>

在从函数返回引用时，返回类型的生命周期参数需要与参数之一的生命周期参数一致。当返回的引用 *未* 指向参数之一时，其必定会指向这个函数内部创建的某个值。但是，这将是个悬空引用，因为该值将在函数结束处超出作用域。请考虑下面这个将不编译的 `longest` 函数的尝试实现：

### 函数签名方面

在这里，尽管咱们已对返回类型指定了生命周期参数 'a，这一实现仍将无法编译，因为返回值的生命周期与参数的生命周期完全无关。下面是我们得到的错误消息：

我们希望签名表达以下约束：返回的引用将在两个参数都有效期间有效。这就是参数的生命周期与返回值的之间的关系。咱们将命名生命周期为 `'a`，然后添加他到每个引用，如下清单 10-21 中所示。

<Listing number="10-21" file-name="src/main.rs" caption="`longest` 函数的定义，指定签名中的所有引用都必须有着同一生命周期 `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

当我们与清单 10-19 的 `main` 函数一起使用这段代码时，他应编译并产生我们想要的结果。
函数签名现在告诉 Rust，针对某一生命周期 `'a`，该函数取两个参数，他们都是字符串切片，存活时间至少与生命周期 `'a` 一样长。这个函数签名还告诉 Rust，从该函数返回的字符串切片将存活至少与生命周期 `'a` 一样长。实际上，这意味着由 `longest` 函数返回的引用的生命周期，与由函数参数引用的值的生命周期中较小的相同。这些关系是我们希望 Rust 在分析这段代码时要使用的。
请记住，当我们在这个函数签名中指定生命周期参数时，我们没有改变任何传入值或返回值的生命周期。相反，我们是在指定借用检查器应该拒绝任何未遵守这些约束的值。请注意，`longest` 函数不需要确切地知道 `x` 与 `y` 将存活多长时间，只要有某一作用域可替代 `'a` 即将满足这一签名。
让我们应用第一条规则：每个参数都会得到自己的生命周期。这次我们有两个参数而不是一个，因此我们有两个生命周期：

咱们可以看到，第二条规则不适用，因为有多个输入生命周期。第三条规则也不适用，因为 longest 是个函数而非方法，因此两个参数都不是 self。在逐一检查所有三条规则后，我们仍未计算出返回类型的生命周期。这就是为什么我们在尝试编译清单 10-20 中的代码时遇到报错：编译器逐一检查了生命周期省略规则，但仍无法计算出该签名中引用的所有生命周期。

当咱们传递具体引用给 `longest` 时，替换 `'a` 的具体生命周期的即为 `x` 的作用域与 `y` 的作用域重叠的部分。换句话说，泛型生命周期 `'a` 将获得与 `x` 与 `y` 的生命周期中较小者相等的具体生命周期。因为我们已通过同一生命周期参数 `'a` 注解了返回的引用，所以返回的引用也将在 `x` 与 `y` 的生命周期中较小者的长度内有效。
我们来看看生命周期注解怎样通过传入有着不同具体生命周期的引用限制 `longest` 函数。下面清单 10-22 是个直观的示例。

<Listing number="10-22" file-name="src/main.rs" caption="以到具有不同具体生命周期的 `longest` 类型值的一些引用，使用 `String` 函数">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

在这个示例中，`string1` 在外层作用域结束之前有效，`string2` 在内层作用域结束之前有效，而 `result` 引用在内层作用域结束之前有效的内容。运行这段代码，咱们将看到借用检查器批准；他将编译并打印 `The longest string
is long string is long`。
接下来，我们来尝试一个实例，展示 `result` 中的引用的生命周期必须是两个参数中较小的生命周期。我们将把 `result` 变量的声明移出内层作用域，而把对 `result` 变量的赋值留在有着 `string2` 变量的作用域内。然后，我们将把使用 `println!` 的 `result` 语句移出内层作用域，在内层作用域结束之后。下面清单 10-23 中的代码将不编译。

<Listing number="10-23" file-name="src/main.rs" caption="在 `result` 已超出作用域后尝试使用 `string2`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

当我们尝试编译这段代码时，我们会得到下面这个报错：
```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

<a id="thinking-in-terms-of-lifetimes"></a>

这一报错表明，要让 `result` 对 `println!` 语句有效，`string2` 将需要在外层作用域结束前有效。Rust 之所以知道这点，是因为我们使用同一生命周期参数 `'a` 注解了该函数的参数和返回值。
作为人类，我们可以查看这段代码，发现 `string1` 长于 `string2`，因此 `result` 将包含到 `string1` 的引用。因为 `string1` 尚未超出作用域，所以到 `string1` 的引用对于 `println!` 语句仍将有效。但是，编译器无法看出看出这一情形下该引用是有效的。我们已经告诉 Rust，由 `longest` 函数返回的引用的生命周期与传入的引用的生命周期中较小的那个相同。因此，借用检查器未放行清单 10-23 中的代码，因为可能有无效引用。
请尝试设计更多实验，让传入 `longest` 函数的引用的值和生命周期，以及返回的引用的使用方式上各不相同。在咱们编译前，要就咱们的试验是否会通过借用检查器提出假设；然后，检查一下咱们是否正确！
### 关于关系

我们需要以何种方式指定生命周期参数，取决于咱们的函数正在做什么。例如，当我们修改 `longest` 函数的实现为始终返回第一个参数，而非最长的字符串切片，那么我们将不需要在参数 `y` 上指定生命周期。以下代码将编译：

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

咱们已对参数 `'a` 与返回类型指定了生命周期参数 `x`，而未对参数 `y` 指定，因为 `y` 的生命周期与 `x` 或返回值的生命周期没有任何关系。
在从函数返回引用时，返回类型的生命周期参数需要与参数之一的生命周期参数一致。当返回的引用 *未* 指向参数之一时，其必定会指向这个函数内部创建的某个值。但是，这将是个悬空引用，因为该值将在函数结束处超出作用域。请考虑下面这个将不编译的 `longest` 函数的尝试实现：

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

在这里，尽管咱们已对返回类型指定了生命周期参数 `'a`，这一实现仍将无法编译，因为返回值的生命周期与参数的生命周期完全无关。下面是我们得到的错误消息：
```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

<a id="lifetime-annotations-in-struct-definitions"></a>

问题在于 `result` 会在 `longest` 函数结束处超出作用域而被清理掉。我们还试图从该函数返回到 `result` 的引用。咱们无法指定任何能改变悬空引用的生命周期参数，而 Rust 将不会让我们创建悬空引用。在这种情况下，最佳的修复方案将是返回一个自有的数据类型而非引用（译注：这样看来引用是没有所有权的），以便调用函数随后负责清理该值。
最终，生命周期语法是关于连接函数的不同参数与返回值的生命周期。一旦他们联系起来，Rust 就有足够信息来实现内存安全的操作，并禁止会创建悬空指针或以其他方式违反内存安全的操作。
### 结构体定义方面

到目前为止，我们已定义的结构体都存储的是自有类型。我们可以定义结构体为存储引用，但在这种情况下，我们就需要在结构体定义中的每个引用上添加生命周期注解。下面清单 10-24 有个名为 `ImportantExcerpt` 的结构体，存储了一个字符串切片。

<Listing number="10-24" file-name="src/main.rs" caption="存储引用的结构体，需要生命周期注解">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

这个结构体有单个字段，保存着一个字符串切片，而这是个引用。与泛型数据类型一样，我们在结构体名字后的尖括号内声明泛型生命周期参数的名字，以便我们可以在结构体定义的主体中使用生命周期参数。这个注解意味着 `part` 的实例不能存活超过其在 `ImportantExcerpt` 字段中保存的引用。
这里的 `part` 函数创建了一个 `main` 结构体的实例，保存着到变量 `ImportantExcerpt` 拥有的 `String` 的第一个句子的引用。`novel` 中的数据在 `novel` 实例创建之前就存在。此外，在这个 `ImportantExcerpt` 超出作用域之前，`novel` 不会超出作用域，因此这个 `ImportantExcerpt` 实例中的引用是有效的。
### 生命周期的省略

咱们已经了解到，每个引用都有生命周期，并且咱们需要为用到引用的函数与结构体指定生命周期参数。然而，我们在 [清单 4-9]) 中曾有函数，下面再次于清单 10-25 中给出，在不带生命周期注解下也编译了。

<Listing number="10-25" file-name="src/lib.rs" caption="咱们在清单 4-9 中定义的一个函数，即使参数与返回值均为引用，也在不带生命周期注解下编译了">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

这个函数在不带生命周期注解下就会编译的原因，是历史性的：在 Rust 的早期版本（`ImportantExcerpt`）中，这段代码不会被编译，因为每个引用都需要显式的生命周期。那时，该函数签名将被写成下面这样：
```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

在编写大量 Rust 代码后，Rust 团队发现 Rust 程序员们在某些特定情形下一次又一次地输入同样的生命周期注解。这些情况是可以预测的，并遵循了少数几种确定性模式。开发者们编成了这些模式到编译器的代码中，以便借用检查器可以推断这些情形下的生命周期而不再需要显式注解。
Rust 的这段历史是相关的，因为更多的确定性模式可能出现并被添加到编译器。今后，所需的生命周期注解可能将更少。
编程到 Rust 引用分析中的模式称为 *生命周期省略规则，lifetime elision rules*。这些不是要 Rust 程序员遵循的规则；他们是编译器将考虑的一套特殊情形，当咱们的代码符合这些情形时，咱们就无需显式地编写生命周期。
省略规则不提供完全的推断。当 Rust 应用这些规则后，引用所具有的生命周期仍然存在歧义时，编译器将不会猜测其余引用变量应如何。编译器不会猜测，而是将给咱们一个报错，咱们可以通过添加生命周期注解来解决该报错。
函数或方法参数的生命周期称为 *输入生命周期，input lifetimes*，返回值的生命周期称为 *输出生命周期，output lifetimes*。
当没有显式的注解时，编译器使用三条规则来计算引用的生命周期。第一条规则适用于输入生命周期，第二及第三条规则均适用于输出生命周期。当编译器到达这三条规则的结束处并且仍然存在无法计算出生命周期的引用时，则编译器将以一个报错停止。这三条规则适用于 `fn` 定义以及 `impl` 代码块。
第一条规则是编译器会给每个是引用的参数指派一个生命周期参数。换句话说，带有一个参数的函数会获得一个生命周期参数：`fn foo<'a>(x: &'a i32)`；带有两个参数的函数会得到两个单独的生命周期参数：`fn foo<'a, 'b>(x: &'a i32,
y: &'b i32)`；以此类推。
第二条规则是，当只有一个输入生命周期参数时，则该生命周期会被指派给所有输出生命周期参数：`fn foo<'a>(x: &'a i32)
-> &'a i32`。
第三条规则是，当存在多个输入生命周期参数，但因为这是个方法而其中之一是 `&self` 或 `&mut self` 时，则 `self` 的生命周期会被指派给所有输出生命周期参数。这条规则使方法更易于读写，因为所需的符号更少。
我们来充当编译器。我们将应用这些规则来计算 [清单 10-25]) 中 `first_word` 函数签名中引用的生命周期。该函数签名以不带与引用关联的任何生命周期开始：
```rust,ignore
fn first_word(s: &str) -> &str {
```

然后，编译器应用第一条规则，其规定每个参数都有自己的生命周期。我们将与往常一样将其称为 `'a`，因此现在该函数签名是这样的：
```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

由于只有一个输入生命周期，因此第二条规则适用。第二条规则规定，一个输入参数的生命周期会被指派给输出生命周期，因此该函数签名现在为下面这样：
```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

现在这个函数签名中的所有引用都有了生命周期，编译器可以继续分析，而无需程序员注解这个函数签名中的生命周期。
我们来看另一个示例，这次使用 `longest` 函数，当我们在 [清单 10-20]) 中开始编写他时还没有生命周期参数：
```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

让我们应用第一条规则：每个参数都会得到自己的生命周期。这次我们有两个参数而不是一个，因此我们有两个生命周期：
```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

<a id="lifetime-annotations-in-method-definitions"></a>

咱们可以看到，第二条规则不适用，因为有多个输入生命周期。第三条规则也不适用，因为 `longest` 是个函数而非方法，因此两个参数都不是 `self`。在逐一检查所有三条规则后，我们仍未计算出返回类型的生命周期。这就是为什么我们在尝试编译清单 10-20 中的代码时遇到报错：编译器逐一检查了生命周期省略规则，但仍无法计算出该签名中引用的所有生命周期。
因为第三条规则实际上只适用于方法签名，所以接下来我们将在这一背景下探讨生命周期，以了解为何第三条规则意味着我们不必经常在方法签名中注解生命周期。
### 方法定义方面

当我们在带有生命周期的结构体上实现方法时，我们会用到与 [清单 10-11]) 中展示的泛型类型参数的相同语法。我们于何处声明及使用生命周期参数，取决于他们是否与结构体字段，或方法参数及返回值相关。
结构体字段的生命周期名字始终需要声明于 `impl` 关键字之后，然后在结构体名字后使用，因为这些生命周期属于是结构体类型的一部分。
在 `impl` 代码块内的方法签名中，引用可能与结构体字段中的引用的生命周期绑定，也可能是独立的。此外，生命周期省略规则通常使方法签名中无需生命周期注解。我们来看一些使用我们在 [清单 10-24]) 中定义的名为 `ImportantExcerpt` 的结构体的示例。
首先，咱们将使用一个名为 `level` 的方法，其唯一参数是到 `self` 的引用，且返回值为 `i32`，不是到任何内容的引用：
```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

在 `impl` 之后的生命周期参数声明及其在类型名字之后的使用是必需的，但由于第一条省略规则，我们无需注解到 `self` 的引用的生命周期。
下面是个第三条生命周期省略规则适用的示例：
```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

由于有两个输入生命周期，Rust 会应用第一条生命周期省略规则，并同时赋予 `&self` 与 `announcement` 各自的生命周期。然后，因为参数之一是 `&self`，所以返回类型得到 `&self` 的生命周期，而所有生命周期都已计算在内。
### 静态生命周期

我们需要讨论的一种特殊生命周期是 `'static`，他表示受其影响的引用 *可以* 在程序整个持续时间内存活。所有的字符串字面值都有着 `'static` 的生命周期，咱们可以如下注解这种生命周期：
```rust
let s: &'static str = "I have a static lifetime.";
```

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

这个字符串的文本直接存储在该程序的二进制数据中，而程序的二进制数据是始终可用的。因此，所有字符串字面值的生命周期都是 `'static`。
咱们可能会在错误消息中看到要使用 `'static` 生命周期的建议。但在为引用指定 `'static` 生命周期之前，要考虑该引用是否确实会存活于程序的整个生命周期，以及咱们是否想要他如此。大多数时候，建议 `'static` 生命周期的错误消息，都是由于尝试创建悬空引用，或可用生命周期不匹配导致的。在这种情况下，解决方法是修复这些问题，而不是指定 `'static` 生命周期。
## 泛型类型参数、特质边界与生命周期三位一体

咱们来简要地看一下，在一个函数中同时指定泛型类型参数、特质边界与生命周期的语法！
```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

这是 [清单 10-21]) 中的 `longest` 函数，返回两个字符串切片中较长的那个。但现在他有个名为 `ann` 的泛型类型 `T` 的额外参数，可以由任何实现 `Display` 子句所指定的 `where` 特质的类型填入。这个额外参数将使用 `{}` 打印出来，这就是为何 `Display` 特质边界是必要的。由于生命周期属于泛型类型，所以生命周期参数 `'a` 与泛型类型参数 `T` 的声明位于函数名字之后尖括号内的同一列表中。
## 本章小结

我们在这一章中介绍了很多内容！现在咱们已经了解了泛型类型参数、特质与特质边界，以及泛型生命周期参数，咱们已准备好编写没有重复且适用于许多不同情况的代码。泛型类型参数允许咱们应用代码于不同类型。特质与特质边界确保即使类型是泛型，他们仍将有着代码所需的行为。我们学习了如何使用生命周期注解来确保这种灵活的代码不会有任何悬空引用。所有这些分析都发生在编译时，这不会影响运行时性能！
不管咱们信不信，关于我们在本章讨论的主题，还有很多内容要学习：第 18 章会讨论特质对象，trait objects，这是使用特质的另一种方式。还有一些更复杂的场景下涉及生命周期注解；对于这些，咱们应该阅读 [Rust 指南])。但接下来，咱们将学习怎样编写 Rust 中的测试，以便确保咱们的代码以其应有的方式工作。
<!-- ignore -->

<!-- Old headings. Do not remove or links may break. -->

<!-- ignore -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

<!-- Old headings. Do not remove or links may break. -->

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
