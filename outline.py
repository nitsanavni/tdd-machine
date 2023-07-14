import argparse
import os
import re


class Outline:
    def __init__(self, root_nodes=["."], max_lines=10):
        self.root_nodes = root_nodes
        self.outline = []
        self.scores = {
            "class": 3,
            "def": 2,
            "__init__": 1,
            "__main__": 1,
            "if": 1,
            "else": 1,
            "elif": 1,
            "for": 1,
            "with": 1,
            "return": 1,
        }
        lines_per_root_node = max_lines // len(root_nodes)
        self.max_lines = (
            lines_per_root_node if (lines_per_root_node != 0) else max_lines
        )

    def traverse(self, node=None):
        if not node:
            node = self.root_node
        if isinstance(node, list):
            # If node is a list (occurs when multiple root directories passed in)
            # apply traverse function to each directory in the list
            for n in node:
                self.traverse(n)
        else:
            if os.path.isdir(node):
                for dirpath, dirnames, files in os.walk(node):
                    # Remove hidden files and directories
                    files = [f for f in files if not f[0] == "."]
                    dirnames[:] = [d for d in dirnames if not d[0] == "."]

                    for name in files:
                        if not self.is_binary(f"{dirpath}/{name}"):
                            self.parse_file(os.path.join(dirpath, name))
            elif os.path.isfile(node):
                self.parse_file(node)
            else:
                print(f"Path '{node}' does not exist.")

    def is_binary(self, filename):
        """
        Return true if the file is binary.
        """
        try:
            with open(filename, "rb") as file:
                for num in range(49152):
                    byte = file.read(1)
                    if byte == b"":
                        break
                    if byte > b"\x7f":
                        return True
        except (IOError, OSError):
            pass
        return False

    def parse_file(self, filename):
        with open(filename, "rb") as file:
            # Add the file path to the outline with a high score
            # assuming file paths have a score of 100
            position = len(self.outline)
            self.outline.append((filename, 100, position, ""))
            line_number = 0  # Initialize line_number
            # print(f"{filename}:")
            for line in file:
                line_number += 1  # Increment line_number
                line = line.decode("utf8", "ignore").strip("\n")
                position = len(self.outline)
                # print(f"{line}:{self.score_line(line)}")
                self.outline.append(
                    (line, self.score_line(line), position, line_number)
                )

    def score_line(self, line):
        score = 0
        for keyword, value in self.scores.items():
            if re.search(r"\b" + keyword + r"\b", line):
                score += value
        return score

    def summarize(self):
        for root_node in self.root_nodes:
            self.outline = []
            self.root_node = root_node
            self.traverse()

            self.outline.sort(key=lambda x: -x[1])
            summary = self.outline[: self.max_lines]
            summary.sort(key=lambda x: x[2])

            for line, score, position, line_number in summary:
                print(f"{line_number}:{line}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate codebase summary with Outline."
    )

    parser.add_argument(
        "-r",
        "--root",
        nargs="+",
        default=["."],
        help="The root directories to summarize. Default is the current directory.",
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=10,
        help="The maximum number of output lines. Default is 10.",
    )

    args = parser.parse_args()

    outline = Outline(root_nodes=args.root, max_lines=args.lines)
    outline.summarize()
