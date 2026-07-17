## 实现一种面向对象的设计模式

[*状态模式，the state pattern*]，属于一种面向对象的设计模式。这种模式的关键在于，我们定义某个值可能在内部具有的一套状态。这些状态由一组 *状态对象，state objects* 表示，而值的行为会根据其状态而变化。我们即将进行一个博客帖子结构体的示例，其有着一个保存其状态的字段，该字段将为 “草稿”、“审阅” 或 “已发布” 三个状态集中的一个状态对象。

状态对象共用功能：当然，在 Rust 中，我们使用结构体与特质，而非对象与继承。每个状态对象都负责自己的行为，并管理何时应转换为另一种状态。保存状态对象的值，对状态的不同行为，或何时进行状态转换一无所知。

使用状态模式的优势在于，当程序的业务需求发生变化时，我们无需修改保存状态的值的代码，或用到该值的代码。我们只需更新某个状态对象内部的代码即可更改其规则，或者添加更多状态对象。

首先，我们将以更传统的面向对象方式实现状态模式，然后，我们将使用一种在 Rust 中更自然的方式。我们来深入研究如何使用状态模式，逐步实现博客帖子的工作流。

最终的功能将看起来像下面这样：

1. 博客帖子作为空白的草稿开始；
2. 草稿完成后，对帖子的审阅是必需的；
3. 帖子被批准后，其得以发布；
4. 只有已发布的博客帖子才会返回用以打印的内容，从而未获批准的帖子不会意外发布。

对帖子尝试的任何其他修改均应无效。例如，当我们在请求审核之前尝试批准博客帖子草稿时，该帖子应保持为未发布的草稿。

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### 尝试传统的面向对象风格

为了解决同一个问题，代码的结构方式有无数种，每种都有不同的权衡取舍。这一节的实现更多的是传统的面向对象风格，虽然在 Rust 中可以这样编写，但并未利用 Rust 的某些优势。稍后，我们将演示一种不同的解决方案，他虽然仍采用面向对象的设计模式，但其结构方式对于有面向对象编程经验的开发者而言，可能显得不太熟悉。我们将比较这两种方案，以体验到与其他语言的代码相比，以不同方式设计 Rust 代码的权衡取舍。

下面清单 18-11 以代码形式展示了这一工作流程：这是我们将在名为 `blog` 的库代码箱中实现的 API 的一个使用示例。这还不会编译，因为我们尚未实现 `blog` 代码箱。

<Listing number="18-11" file-name="src/main.rs" caption="演示我们希望 `blog` 代码箱具备的预期行为的代码">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

我们希望允许用户使用 `Post::new`，创建新的博客帖子草稿。我们打算允许添加文本到博客帖子。当我们尝试在审批之前立即获取帖子的内容时，我们不应得到任何文本，因为该帖子仍然是草稿。出于演示目的，我们在代码中添加了 `assert_eq!`。针对这点的理想单元测试是，断言帖子草稿会从 `content` 方法返回空字符串，但我们不会为这个示例编写测试。

接下来，我们希望启用对帖子的一次审阅请求，并且我们希望在等待审阅期间，`content` 返回空字符串。当帖子获得批准后，他应得以发布，这意味着当 `content` 被调用时，该帖子的正文将被返回。

请注意，我们与该代码箱中交互的唯一类型是 `Post` 类型。这个类型将使用状态模式，并保存一个值，该值将是三个状态对象之一，表示帖子可能出于的不同状态 -- 草稿、等待审阅或已发布。从一种状态到另一状态的更改，将在 `Post` 类型内部得以内部地管理。状态的变化，是响应于库用户对 `Post` 实例调用的方法而发生的，但用户不必直接管理状态变更。此外，用户也不会在状态方面犯错，比如在审阅前发布帖子。

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### 定义 `Post` 并创建新实例

我们来开始库的实现！我们知道我们需要一个公开的 `Post` 结构体保存一些内容，因此我们将从该结构体的定义，及用于创建 `new` 实例的关联公开 `Post` 函数开始，如下清单 18-12 中所示。我们还将构造一个私有的 `State` 特质，将定义某个 `Post` 的所有状态对象必须具备的行为。

然后，`Post` 类型将在名为 `Box<dyn State>` 的私有字段的 `Option<T>` 值内，保存 `state` 的特质对象，以保存状态对象。稍后咱们就会明白为何 `Option<T>` 是必要的。

<Listing number="18-12" file-name="src/lib.rs" caption="`Post` 结构体的定义，和创建新 `new` 实例的 `Post` 函数、`State` 特质，以及 `Draft` 结构体">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

其中 `State` 特质定义了不同帖子状态共用的行为。状态对象分别是 `Draft`、`PendingReview` 和 `Published`，他们都将实现 `State` 特质。目前，这一特质没有任何方法，且我们以仅定义 `Draft` 状态开始，因为这是我们的帖子开始的状态。

当我们创建新的 `Post` 实例时，我们设置其 `state` 字段为包含一个 `Some` 值的 `Box` 值。这个 `Box` 值指向一个 `Draft` 结构体的新实例。这确保了每当我们创建一个 `Post` 的新实例时，他都将以草稿形式开始。由于 `state` 的 `Post` 字段是私有的，因此没有办法创建处于任何其他状态的 `Post`！在 `Post::new` 函数中，我们设置 `content` 字段为一个新的、空 `String`。

#### 存储帖子内容的文本

我们在清单 18-11 中看到，我们希望能够调用一个名为 `add_text` 的方法，并传递给他一个 `&str`，然后添加为博客帖子的文本内容。我们会作为方法实现这点，而不是暴露 `content` 字段为 `pub`，以便稍后我们可以实现一个方法，其将控制 `content` 字段的数据被读取的方式。`add_text` 方法相当简单，因此我们来添加下面清单 18-13 中的实现到 `impl
Post` 代码块。

<Listing number="18-13" file-name="src/lib.rs" caption="实现 `add_text` 方法，以添加文本到帖子的 `content` 字段">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

`add_text` 方法取到 `self` 的可变引用，因为我们正在修改我们正对其调用 `Post` 的 `add_text` 实例。然后，我们对 `push_str` 字段中的 `String` 值调用 `content` 并传递 `text` 参数，以添加到已保存的 `content`。这一行为不依赖于帖子所处的状态，因此他不是状态模式的一部分。`add_text` 方法完全不与 `state` 字段交互，但他是我们希望支持的行为的一部分。

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### 确保草稿帖子的内容为空

即使我们调用了 `add_text` 并添加了一些内容到帖子，我们仍然希望 `content` 方法返回一个空的字符串切片，因为帖子仍处于草稿状态，正如清单 18-11 中的第一个 `assert_eq!` 所示。目前，我们来以将满足这一要求的最简单方式实现 `content` 方法：始终返回一个空字符串切片。一旦稍后实现修改帖子的状态以便其可被发布的能力后，我们将修改这个方法。到目前为止，贴子只能处于草稿状态，因此帖子内容应始终为空。下面清单 18-14 展示了这一占位符实现, a placehoder implementation。

<Listing number="18-14" file-name="src/lib.rs" caption="为 `content` 上 `Post` 方法添加占位符实现，其始终返回一个空字符串切片">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

通过这个添加的 `content` 方法，清单 18-11 中直到第一个 `assert_eq!` 的所有代码都会按预期运行。

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>

<a id="requesting-a-review-changes-the-posts-state"></a>

#### 请求审阅，改变帖子的状态

接下来，我们需要添加请求对帖子审阅的功能，这应该将其状态从 `Draft` 更改为 `PendingReview`。下面清单 18-15 展示了这一代码。

<Listing number="18-15" file-name="src/lib.rs" caption="实现 `request_review` 与 `Post` 特质上的 `State` 方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

我们给予 `Post` 一个名为 `request_review` 的公开方法，其将取一个到 `self` 的可变引用。然后，我们对 `request_review` 的当前状态调用内部的 `Post` 方法，而这第二个 `request_review` 方法会消费当前状态并返回一个新状态。

我们添加 `request_review` 方法到 `State` 特质；所有实现这个特质的类型，现在都将需要实现 `request_review` 方法。请注意，我们没有使用 `self`、`&self` 或 `&mut self` 作为这个方法的第一个参数，而是使用 `self: Box<Self>`。这种语法意味着，这个方法仅在对包含这种类型的 `Box` 调用时才有效。这种语法会取得 `Box<Self>` 的所有权，从而使旧状态失效，以便 `Post` 的状态值可以转换为新状态。

为了消费旧的状态，`request_review` 方法需要取得状态值的所有权。这就是 `Option` 的 `state` 字段中 `Post` 发挥作用的地方：我们调用 `take` 方法（译注：标准库 `Some` 上的），来从 `state` 字段取出 `None` 值，并在其位置留下一个 `state`，因为 Rust 不允许我们在结构体中有着未填充的（无效或空字段) 字段。这让我们可以从 `Post` 中迁出 `state` 值，而不是借用他。然后，我们将设置帖子的 state 值为这一操作的结果。

为了获的 `state` 值的所有权，我们需要暂时设置 `None` 为 `self.state = self.state.request_review();`，而不是以 `state` 这样的代码直接设置他。这确保了在我们将 Post 转换为新的状态后，`Post` 无法再使用旧的 `state` 值。

`request_review` 上的 `Draft` 方法返回一个新的、装箱后的新 `PendingReview` 结构体实例，表示帖子等待审阅时的状态。`PendingReview` 结构体也实现了 `request_review` 方法，但不执行任何转换。相反，他会返回自身，因为当我们对已处于 `PendingReview` 状态的帖子请求审阅时，他应保持处于 `PendingReview` 状态。

`request_review` 方法将类似于 `Post` 方法：他将设置 `state` 为当前状态规定的，再状态为 “批准” 时应具有的值，如下清单 18-16 中所示。

现在我们需要更新 `content` 上的 `Post` 方法。我们希望 `Post` 返回的值取决于 `PendingReview` 的当前状态，因此我们即将让 `Draft` 委托给定义在其 `PendingReview` 上的 `assert_eq!` 方法，如下清单 18-17 中所示。

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>

<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### 添加 `approve` 以修改 `content` 的行为

其他重复包括 `approve` 上 `request_review` 和 approve 两个方法的相似实现。这两个方法都对 Post 的 `state` 字段使用了 Option::take，并在 state 为 Some 时，他们委派给同一个方法的封装值的实现，并设置 state 的新值为该方法的结果。若我们在 Post 上有大量遵循这种模式的方法时，我们可能会考虑定义一个宏，defining a macro，来消除这种重复（请参阅第 20 章中的 [关于宏] 小节）。

<Listing number="18-16" file-name="src/lib.rs" caption="实现 `approve` 与 `Post` 特质上的 `State` 方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

但我们还必须对 `approve` 进行一些小的更改。`State` 和 `State` 两个方法都会返回新的实例，而不是修改在其上调用他们的结构体，因此我们需要添加更多 `Published` 的遮蔽赋值，来保存返回的实例。我们还不能有那些关于草稿和等待审阅帖子的内容为空字符串的断言，也不需要这些断言：我们无法再编译尝试使用处于这些状态的帖子的内容的代码。main 中更新后的代码显示于下面清单 18-21 中。

与 `request_review` 上 `PendingReview` 的工作方式类似，当我们对 `approve` 调用 `Draft` 方法时，他将不会产生效果，因为 `approve` 将返回 `self`。在我们对 `approve` 调用 `PendingReview` 时，他返回一个新的、装箱后的 `Published` 结构体实例。`Published` 结构体实现了 `State` 特质，而对于 `request_review` 及 `approve` 这两个方法，他都会返回自身，因为在这些情形下，帖子都应保持处于 `Published` 状态。
现在我们需要更新 `content` 上的 `Post` 方法。我们希望 `content` 返回的值取决于 `Post` 的当前状态，因此我们即将让 `Post` 委托给定义在其 `content` 上的 `state` 方法，如下清单 18-17 中所示。

<Listing number="18-17" file-name="src/lib.rs" caption="更新 `content` 上的 `Post` 方法为，委托给 `content` 上的 `State` 方法">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

由于目标是要保留所有这些规则在实现 `State` 的结构体内，因此我们对 `content` 中的值调用 `state` 方法，并作为参数传递帖子实例（即 `self`）。然后，我们对 `content` 值使用 `state` 方法返回的值。
我们调用 `as_ref` 方法（它属于 `Option`），因为我们想要引用 `Option` 内部的值，
而不是取得该值的所有权。由于 `state` 是一个 `Option<Box<dyn State>>`，调用
`as_ref` 后会返回 `Option<&Box<dyn
State>>`。如果不调用 `as_ref`，就会报错，因为我们无法将 `state` 从函数参数中
借用的 `&self` 中移出。
此时，当我们调用 `unwrap` 上的 `Post` 方法时，解引用强制转换，deref coercion，将对 `state` 和 `Some` 生效，从而最终对实现 `None` 特质的类型调用 content 方法。这意味着我们需要添加 content 到 State 特质定义，这就是我们放置根据我们拥有的状态，返回何种内容的逻辑之处，如下清单 18-18 中所示。 [“When You Have More Information Than the
Compiler”][more-info-than-rustc] <!-- ignore -->
我们添加了一个 `content` 方法的默认实现，会返回一个空字符串切片。这意味着我们无需对 `&Box<dyn State>` 与 `&` 两个结构体实现 `Box` 方法。`content` 结构体则将重写 `State` 方法，并返回 `content` 中的值。虽然这样做很方便，但让 `State` 上的 content 方法决定 Post 的内容，模糊了 State 与 Post 职责之间的界线。

<Listing number="18-18" file-name="src/lib.rs" caption="添加 `content` 方法到 `State` 特质">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

请注意，正如我们在第 10 章中讨论的那样，我们需要对这个方法的生命周期注解。我们取的是到某个 `content` 值的引用作为参数，并返回的是到该 `content` 一部分的引用，因此返回的引用的生命周期便与该 `Draft` 参数的生命周期相关。 `PendingReview` `Published` `content` `post.content` `content` `State` `Post` `State` `Post`
我们就完成了——现在清单 18-11 中的全部代码都可以正常工作了！正如第 10 章所述，我们取得到某个 `post` 的引用作为参数，并返回到该 `post` 一部分的引用，因此返回引用的生命周期与 `post` 参数的生命周期相关。我们已经按照博客帖子工作流程的规则实现了状态模式。与规则相关的逻辑存在于状态对象中，而不是分散在 `Post` 的各处。
> **为什么不使用枚举**？
>
> 咱们可能已经在想，为什么我们没有使用枚举，将不同的帖子可能状态作为变种。这当然是一种可行的办法；请尝试并比较最终结果，看看咱们要选哪种方案！使用枚举的一个缺点是，凡是会检查枚举的值的地方，都需有一个 `match` 表达式，或类似的表达式来处理所有可能的变种。这可能比这种特质对象的方法更加重复。
<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### 评估状态模式

我们已经展示了，Rust 能够实现面向对象的状态模式，封装博客帖子在每种状态下应具备的不同类别的行为。`Post` 上的方法对这些不同行为一无所知。由于我们组织代码的方式，我们只须查看一个地方，即可了解已发布帖子的不同行为方式：即 `State` 结构体上对 `Published` 特质的实现。
若我们要创建一种不使用状态模式的替代实现，我们可能转而使用 `match` 表达式来处理 `Post` 的方法，甚至在 `main` 代码中检查博客帖子状态并改变行为。这意味着为了理解处于已发布状态的帖子的所有影响，我们将必须在多个地方查看。
在状态模式下，`Post` 的方法以及我们使用 `Post` 的地方都不需要 `match` 表达式，而要添加新的状态，我们将只需要添加一个新结构体，并在一处对一个结构体实现特质方法即可。
使用状态模式的实现易于扩展以添加更多功能。要了解维护使用状态模式的代码的简单性，请尝试以下这些建议：
- 添加一个 `reject` 方法，将帖子状态从 `PendingReview` 改回 `Draft`；
- 需要两次调用 `approve`，然后状态才可以更改为 `Published`；
- 仅当博客帖子处于 `Draft` 状态时，才允许用户添加文本内容。提示：让状态对象负责内容可能的变更，但不负责修改 `Post`。
状态模式的一个缺点则是，由于状态本身实现了状态之间的转换，因此某些状态会相互耦合。当我们在 `PendingReview` 和 `Published` 之间添加另一状态，比如 `Scheduled` 时，我们将不得不修改 `PendingReview` 中的代码为转而过渡到 `Scheduled`。若 `PendingReview` 在新状态的添加下无需修改，那么工作量会减少，但这意味着要转换到另一种设计模式。
另一个缺点是我们重复了一些逻辑。为了消除部分重复，我们可能会为 `request_review` 特质上，返回 `approve` 的 `State` 和 `self` 两个方法构造默认实现；但这行不通：当作为特质对象使用 `State` 时，该特质不知道具体的 `self` 究竟是什么，因此在编译时返回类型是未知的。（这属于早先提到的 dyn 兼容性规则 之一。）
其他重复包括 `request_review` 上 `approve` 和 `Post` 两个方法的相似实现。这两个方法都对 `Option::take` 的 `state` 字段使用了 `Post`，并在 `state` 为 `Some` 时，他们委派给同一个方法的封装值的实现，并设置 `state` 的新值为该方法的结果。若我们在 `Post` 上有大量遵循这种模式的方法时，我们可能会考虑定义一个宏，defining a macro，来消除这种重复（请参阅第 20 章中的 [“Macros”][macros] 小节）。 <!-- ignore -->
通过完全按照面向对象的定义实现状态模式，我们没有利用我们原本可以利用的 Rust 的优势。我们来看看可以对 `blog` 代码箱进行哪些修改，可以使无效状态以及无效的状态转换，成为编译时的报错。
### 编码状态和行为为类型

我们将展示怎样重新构思状态模式，以获得一套不同的权衡取舍。与其完全地封装状态及状态过渡，从而使外部代码对他们一无所知，我们将编码状态为不同的类型。于是乎，Rust 的类型检查系统就将通过发出编译器报错，阻止在仅允许已发布的帖子之处使用草稿帖子的尝试。
我们来考虑 清单 18-11 中 `main` 函数的第一部分：

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

我们仍然实现了使用 `Post::new` 创建处于草稿状态的帖子，以及添加文本到帖子内容的能力。但与在草稿帖子上提供一个返回空字符串的 `content` 方法不同，我们让 `content` 根本没有 `Post` 方法。这样，当我们尝试获取草稿帖子的内容时，我们将得到一个编译器报错，告诉我们该方法不存在。因此，我们不可能在生产中意外地显示草稿帖子内容，因为相关代码甚至不会编译。下面清单 18-19 展示了 `DraftPost` 结构体的定义和一个 DraftPost 结构体，以及各自的方法。

<Listing number="18-19" file-name="src/lib.rs" caption="A `Post` with a `content` method and a `DraftPost` without a `content` method">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

`Post` 与 `DraftPost` 这两个结构体都包含一个私有 `content` 字段，存储博客帖子文本。两个结构体不再包含 `state` 字段，因为我们正在迁移对状态的编码到结构体的类型。`Post` 结构体将表示已发布的帖子，并且他有个返回 `content` 的 `content` 方法。
我们仍然有个 `Post::new` 函数，但他不再返回 `Post` 的实例，而是返回 `DraftPost` 的实例。由于 `content` 是私有的，并且没有任何返回 `Post` 值的函数，因此现在无法创建 `Post` 的实例。
`DraftPost` 结构体有个 `add_text` 方法，因此我们可以像以前一样添加文本到 `content`，但请注意，`DraftPost` 没有定义 `content` 方法！因此，现在程序确保了所有帖子都以草稿帖子开始，而草稿帖子没有让他们的内容可用于显示。任何试图绕过这些约束的尝试都将导致编译器报错。
<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

那么，我们怎样得到已发布的帖子呢？我们希望强制执行草稿帖子必须被审阅和批准后，才能发布的规则。处于等待审阅状态的帖子仍不应显示任何内容。我们来通过 `PendingReviewPost` `request_review` `DraftPost` `PendingReviewPost` `approve` `PendingReviewPost` `Post`

<Listing number="18-20" file-name="src/lib.rs" caption="通过对 `PendingReviewPost` 调用 `request_review`，一个 `DraftPost` 得以创建，以及一个转换 `approve` 为已发布的 `PendingReviewPost` 的 `Post` 方法">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

- 添加另一结构体 `request_review`、
- 在 `approve` 上定义一个返回 `self` 实例的 `DraftPost` 方法，
- 并在 `PendingReviewPost` 上定义返回 `PendingReviewPost` 的 `Post` 方法， `DraftPost` `request_review` `PendingReviewPost` `content` `DraftPost` `Post` `content` `approve` `PendingReviewPost` `PendingReviewPost` `request_review` `DraftPost`
来实现这些约束，如下清单 18-20 中所示。 `main` `request_review` `approve` `let post =` `main`

<Listing number="18-21" file-name="src/main.rs" caption="对 `main` 的修改，以使用博客帖子工作流的新实现">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

我们需要对 `main` 进行修改以重新指派 `post`，意味着这种实现已不再严格遵循面向对象的状态模式：状态之间的转换不再完全封装在 `Post` 的实现内。不过，我们的收获是，由于类型系统和编译时发生的类型检查，无效状态现在是不可能的！这确保了一些错误，比如未发布的帖子的内容的显示等，在投入生产之前就会被发现。

请在清单 18-21 之后的 `blog` 代码箱的基础上，尝试这一小节开头建议的任务，看看咱们对这一版本代码的设计有何看法。请注意，某些任务可能已在这一设计中完成。

我们已经看到，尽管 Rust 能够实现面向对象的设计模式，但在 Rust 中其他模式，比如编码状态为类型系统等也是可用的。这些模式有着不同的权衡取舍。尽管咱们可能对面向对象的模式非常熟悉，但重新构思问题以利用 Rust 的特性，会带来诸多好处，比如在编译时防止 bug 等。由于面向对象语言不具备所有权这样的一些特性，因此面向对象模式并不总是 Rust 中的最佳解决方案。

## 本章小节

无论咱们在读完这一章后，是否认为 Rust 属于面向对象语言，咱们现在都知道，可以在 Rust 中使用特质对象获得一些面向对象的特性。动态分派可以在损失部分运行时性能下，给予咱们一定的灵活性。我们可以利用这种灵活性来实现面向对象的模式，从而提高代码的可维护性。Rust 还具备面向对象语言所没有的其他特性，比如所有权等。面向对象模式并不总是利用 Rust 优势的最佳方式，但他是一种可用选项。

接下来，我们将看看模式，这是 Rust 另一项赋予代码灵活性的特性。虽然我们在全书中已对其进行了简要介绍，但还没有了解他们的全部能力。我们来开始吧！

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
