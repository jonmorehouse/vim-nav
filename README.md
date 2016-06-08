# Vim-Nav

Smarter, horizontal navigation in vim.


[![asciicast](https://asciinema.org/a/7ewafmt0dx3ruwjphpwew1c8g.png)](https://asciinema.org/a/7ewafmt0dx3ruwjphpwew1c8g?autoplay=1)

`vim-nav` is a simple plugin that hijacks `b` and `e` for smarter navigation between characters. **vim-nav** allows you to navigate through snake case, camel case and normal word breaks. Break characters are also configurable for custom navigation.

`vim-nav` works by replacing the `b` and `e` mappings in normal mode.

## Installation

`vim-nav` should work with your vim plugin dependency manager. The recommended way to install `vim-nav` is using the [vundle]() plugin manager.

Simply add this to your `vundle` config:

```vim
Plugin 'jonmorehouse/vim-nav'
```

And then run `:PluginInstall` from within a `vim` session to install.


## FAQ

> Why use python? 

Well, it's just easier!

> Hasn't this been done before?

Yeah, probably; I haven't found anything that fits my needs just yet so this simple plugin 

> What is next?

Future iterations of `vim-nav` _could_ support vertical navigation. Right now, it just focuses on horizontal nav though.
