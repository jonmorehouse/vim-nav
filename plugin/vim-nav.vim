" TODO add back after debugging finished
if exists("g:vim_nav_loaded") || &cp
  finish
endif
let g:vim_nav_loaded = 1

""" vim nav requres python support. This should be fairly standard amongst
""" most vim installations.
if !has("python3")
  echo "vim-nav requires python3 support"
  finish
endif

python3 <<EOF
from os import path as p
import sys
import vim

lib_path = p.abspath(p.join(vim.eval("expand('<sfile>:p:h')"), "../lib"))
sys.path.insert(0, lib_path)

import nav
EOF

" map b in normal mode to nav.backwards()
"nmap b :python3 nav.backwards()<CR>
"nmap b @dd

:nnoremap b :<C-U>exe ":python3 nav.backwards(count=".v:count1.")"<CR>
:nnoremap e :<C-U>exe ":python3 nav.forwards(count=".v:count1.")"<CR>
