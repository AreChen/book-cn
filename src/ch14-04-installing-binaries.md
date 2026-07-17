

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## 以 `cargo install` 安装二进制代码箱

`cargo install` 命令允许咱们在本地安装和使用二进制代码箱。这并不是为了取代系统包；他的目的是为 Rust 开发者提供一种便捷的方式，来安装其他人在 [crates.io](https://crates.io/) 上共享的工具。请注意，我们只能安装有着二进制目标的包。所谓 *二进制目标*，是在代码箱有着 src/main.rs 文件或指定为二进制代码箱的另一文件时创建的可运行程序，与本身不可运行而适合于包含在其他程序中的库目标相反。通常，代码箱在 README 文件中有着关于其是否是库，还是有着二进制目标，或者二者皆具方面的信息。

以 `cargo install` 安装的所有二进制代码箱，都存储在安装根目录下的 bin 文件夹中。当咱们是使用 rustup.rs 安装的 Rust，且没有任何定制配置时，那么这个目录将是 $HOME/.cargo/bin。为了能够运行咱们使用 `$PATH` 安装的程序，请确保这个目录在咱们的 `cargo install` 中。

例如，在第 12 章中我们曾提到，有个名为 ripgrep 的 `grep` 工具的 Rust 实现 `ripgrep`，用于检索文件。要安装 `ripgrep`，我们可以运行以下命令：



```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

输出的倒数第二行显示已安装的二进制程序的位置与名字，在 `ripgrep` 的情形下为 `rg`。正如前面提到的，只要安装目录在咱们的 `$PATH` 中，随后咱们就可以运行 `rg --help`，并开始使用这个更快、更具 Rust 风格的工具来检索文件！

<!-- Old headings. Do not remove or links may break. -->

<!-- ignore -->

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->
