import os
from invoke import task
from pathlib import Path

from util import mytask

ext_bin = ".bin"
ext_list = ".list-txt"
ext_macro = ".macro"


@mytask
def build(c):
    print(f"\n> Build...\n{'-' * 20}")
    inc_dir = os.getenv("DASMINC", ".")
    dasm = os.getenv("DASM_BIN", "dasm")
    dasm_files = list(Path(c['work_dir']).glob('*.dasm'))

    for f in dasm_files:
        c.run(
            f"{dasm} {f.parts[-1]} -I{inc_dir} -f3 -l{f.stem}{ext_list} -v2 -o{f.stem}{ext_bin}"
        )


@mytask
def test(c):
    print(f"\n> Test...\n{'-' * 20}")
    gopher = os.getenv("GOPHER_BIN", "gopher2600")
    bin_files = list(Path(c['work_dir']).glob(f'*{ext_bin}'))

    for f in bin_files:
        print(f"> Testing '{f}'")
        c.run(f"{gopher} disasm {f.parts[-1]}")


@mytask
def clean(c):
    print(f"\n> Clean...\n{'-' * 20}")
    c.run(f"rm -f *{ext_bin}")
    c.run(f"rm -f *{ext_list}")


@mytask
def test_gui(c):
    print(f"\n> Test GUI...\n{'-' * 20}")
    gopher = os.getenv("GOPHER_BIN", "gopher2600")
    bin_files = list(Path(c['work_dir']).glob(f'*{ext_bin}'))

    for f in bin_files:
        macro_file = f"{f.stem}{ext_macro}"
        if Path(f"{f.parents[0]}/{macro_file}").exists():
            print(f"> Testing '{f}' with macro '{macro_file}'")
            c.run(f"{gopher} run -macro {macro_file} {f.parts[-1]}")
        else:
            print(f"> No macro for '{f}', skipping...")
