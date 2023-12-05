import os
from invoke import task

from util import mytask


@mytask
def build(c):
    inc_dir = os.getenv("DASMINC", ".")
    c.run(
        f"dasm rainbow.dasm -I{inc_dir} -f3 -lrainbow.list.txt -v -orainbow.bin"
    )


@mytask
def test(c):
    raise NotImplementedError


@mytask
def clean(c):
    c.run("rm -f *.bin")
