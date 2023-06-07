#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper for iwyu-tool.py"""
import sys
from typing import List

from hooks.utils import StaticAnalyzerCmd


class IWYUtoolCmd(StaticAnalyzerCmd):
    """Class for the iwyu-tool.py command."""

    command = "python3 iwyu_tool.py"
    lookbehind = "python3 iwyu_tool.py "

    def __init__(self, args: List[str]):
        super().__init__(self.command, self.lookbehind, args)
        self.check_installed()
        self.parse_args(args)

    def run(self):
        """Run iwyu-tool.py. Error if diff is incorrect. "Correct" """

        for filename in self.files:
            self.run_command([filename] + self.args)
            is_correct = b"has correct #includes/fwd-decls" in self.stderr
            if is_correct:
                self.returncode = 0
                self.stdout = b""
                self.stderr = b""
            else:
                sys.stderr.buffer.write(self.stdout + self.stderr)
                sys.exit(self.returncode)


def main(argv: List[str] = sys.argv):
    cmd = IWYUtoolCmd(argv)
    cmd.run()


if __name__ == "__main__":
    main()
