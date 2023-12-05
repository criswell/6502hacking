import os
from invoke import task
from pathlib import Path

from util import mytask

ext_bin = ".bin"
ext_list = ".list-txt"


@mytask
def build(c):
    inc_dir = os.getenv("DASMINC", ".")
    dasm_files = list(Path(c['work_dir']).glob('*.dasm'))

    for f in dasm_files:
        c.run(
            f"dasm {f.parts[-1]} -I{inc_dir} -f3 -l{f.stem}{ext_list} -v2 -o{f.stem}{ext_bin}"
        )


@mytask
def test(c):
    raise NotImplementedError


@mytask
def clean(c):
    c.run(f"rm -f *{ext_bin}")
    c.run(f"rm -f *{ext_list}")
