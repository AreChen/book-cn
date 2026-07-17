## 注释

所有程序员都努力让自己的代码易于理解，但有时还需要补充说明。在这种情况下，程序员会在源代码中留下*注释*，编译器会忽略它们，但阅读源代码的人可能会觉得有用。

下面是一个简单的注释：

```rust
// hello, world
```

在 Rust 中，惯用的注释风格是用两个斜杠开始注释，注释会持续到行尾。对于跨越多行的注释，需要在每一行都写上 `//`，如下所示：

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

注释也可以放在包含代码的行末：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

不过，更常见的是下面这种格式：将注释放在要注释的代码上方的单独一行：

<span class="filename">文件名： src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust 还有另一种注释，即文档注释，我们会在第 14 章的[“将代码包发布到 Crates.io”][publishing]<!-- ignore -->一节讨论。

[publishing]: ch14-02-publishing-to-crates-io.html
