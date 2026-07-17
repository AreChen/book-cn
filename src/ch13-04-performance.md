<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## 循环与迭代器下的性能问题

要确定是使用循环还是迭代器，咱们需要知道哪种实现更快：带有显式 `search` 循环的 `for` 函数版本，还带有迭代器的版本。

我们通过加载 Arthur Conan Doyle 爵士所著的《福尔摩斯历险记》的全部内容到一个 `String` 中，然后在内容中查找单词 *the*，运行了一个基准测试。下面是该基准测试对使用 `search` 循环的 `for` 版本，和使用迭代器的版本的结果：

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

两种实现有着相似的性能！我们不会在这里解释基准测试的代码，因为重点不是证明两个版本等价，而是大致了解这两种实现在性能方面的比较情况。

出于更全面的测试，咱们应该使用不同大小的各种文本作为 `contents`、不同长度的不同单词作为 `query`，以及所有类别的变量来检查。重点是：迭代器虽然属于高级抽象，仍会被编译成与咱们自己编写的低级（地层）代码大致相同的代码。迭代器属于 Rust 的 *零成本抽象* 之一，这意味着使用这一抽象不会带来额外的运行时开销。这类似于 C++ 最初设计者和实现者 Bjarne Stroustrup 在其 2012 年 ETAPS 的主题演讲 [《C++ 基础》] 中，对 “零开销” 的定义：

> 一般来说，C++ 的实现遵循“零开销”原则：不使用的东西，就不需要付出开销。更进一步：咱们真正用到的东西，咱们无法更好地手工编写代码，the zero-overhead principle: What you don't use, you don't pay for. And further: What you do use, you couldn't hand code any better。

> **注意**：
>
> - zero-cost abstraction, 零成本抽象

## 本章小结

作为另一个示例，以下代码取自某个音频解码器。该解码算法使用线性预测数学运算，根据前几个采样值的线性函数来估计未来值。这段代码使用迭代器链，对作用域中的三个变量执行一些数学计算：

- 一个数据的 `cargo` 切片
- 一个包含 12 个 coefficients 的数组
- 以及 qlp_shift 中偏移数据的数量
