" TODO add back after debugging finished
if exists("g:vim_nav_loaded") || &cp
  finish
endif
let g:vim_nav_loaded = 1

""" vim nav requres python support. This should be fairly standard amongst
""" most vim installations.
if !has("python")
  echo "vim-nav requires python support"
  finish
endif

python <<EOF
from os import path as p
import sys
import vim

lib_path = p.abspath(p.join(vim.eval("expand('<sfile>:p:h')"), "../lib"))
sys.path.insert(0, lib_path)

import nav
EOF

" map b in normal mode to nav.backwards()
"nmap b :python nav.backwards()<CR>
"nmap b @dd

:nnoremap b :<C-U>exe ":python nav.backwards(count=".v:count1.")"<CR>
:nnoremap e :<C-U>exe ":python nav.forwards(count=".v:count1.")"<CR>
