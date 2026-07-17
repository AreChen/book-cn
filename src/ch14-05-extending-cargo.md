## 使用自定义命令扩展 Cargo

Cargo 的设计允许你通过新增子命令来扩展它，而无需修改 Cargo 本身。如果 `$PATH`
中的二进制文件名为 `cargo-something`，就可以运行 `cargo something`，把它当作
Cargo 子命令使用。运行 `cargo --list` 时也会列出这类自定义命令。可以使用
`cargo install` 安装扩展，然后像运行 Cargo 内置工具一样运行它们，这是 Cargo
设计带来的非常便利的好处！

## 小结

与 Cargo 和 [crates.io](https://crates.io/)<!-- ignore --> 共享代码，是 Rust
生态系统能够服务许多不同任务的原因之一。Rust 的标准库小巧而稳定，但 crate
很容易分享、使用和改进，其演进节奏也可以不同于语言本身。不要吝于在
[crates.io](https://crates.io/)<!-- ignore
--> 上分享对你有用的代码；它很可能
也会对其他人有用！
