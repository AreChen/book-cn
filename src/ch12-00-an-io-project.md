# I/O 项目：构建命令行程序

本章将回顾你目前学到的许多技能，并探索标准库中的一些其他功能。我们将构建一个与文件及命令行输入输出交互的命令行工具，用来练习你已经掌握的 Rust 概念。

Rust 速度快、安全、能够输出单个二进制文件，并且支持跨平台，因此非常适合用来创建命令行工具。在本项目中，我们将实现经典命令行搜索工具 `grep` 的一个版本（**g**lobally search a **r**egular **e**xpression and **p**rint，即全局搜索正则表达式并打印）。在最简单的用法中，`grep` 会在指定文件中搜索指定字符串。为此，`grep` 接受文件路径和字符串作为参数，然后读取文件，找到其中包含该字符串的行并打印出来。

在这个过程中，我们还会展示如何让命令行工具使用许多其他命令行工具所使用的终端功能。我们会读取环境变量的值，让用户能够配置工具的行为。我们还会把错误消息打印到标准错误控制台流（`stderr`），而不是标准输出（`stdout`），这样用户就可以把成功输出重定向到文件，同时仍在屏幕上看到错误消息。

Rust 社区成员 Andrew Gallant 已经创建了一个功能完整且速度很快的 `grep` 版本，名为 `ripgrep`。相比之下，我们的版本会相当简单，但本章会为你理解 `ripgrep` 这样的真实项目提供一些必要的背景知识。

我们的 `grep` 项目会综合运用你目前学到的多个概念：

- 组织代码（[第 7 章][ch7]<!-- ignore -->）
- 使用向量和字符串（[第 8 章][ch8]<!-- ignore -->）
- 处理错误（[第 9 章][ch9]<!-- ignore -->）
- 在适当的地方使用 trait 和生命周期（[第 10 章][ch10]<!-- ignore -->）
- 编写测试（[第 11 章][ch11]<!-- ignore -->）

我们还会简要介绍闭包、迭代器和 trait 对象；[第 13 章][ch13]<!-- ignore -->和[第 18 章][ch18]<!-- ignore -->会详细讲解它们。

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
