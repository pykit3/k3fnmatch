#!/usr/bin/env python
# coding: utf-8

import re
import unittest

import k3fnmatch


class TestTranslate(unittest.TestCase):
    """Test translate() function with various patterns"""

    def test_simple_star(self):
        """Test single * wildcard"""
        cases = [
            ("*.txt", "file.txt", True),
            ("*.txt", "dir/file.txt", False),
            ("*.txt", "file.md", False),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match, f"Pattern {pattern} vs {path}")

    def test_double_star(self):
        """Test ** for multi-segment matching"""
        cases = [
            ("**/*.md", "foo/bar/doc.md", True),
            ("**/*.md", "foo/doc.md", True),
            ("**/*.md", "a/b/c/d.md", True),
            ("**/*.md", "no-match.txt", False),
            # ** requires at least one /, so "doc.md" without prefix doesn't match
            ("**/*.md", "doc.md", False),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match)

    def test_question_mark(self):
        """Test ? for single character"""
        cases = [
            ("file?.txt", "file1.txt", True),
            ("file?.txt", "fileA.txt", True),
            ("file?.txt", "file.txt", False),
            ("file?.txt", "file12.txt", False),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match)

    def test_character_class(self):
        """Test [...] character classes"""
        cases = [
            ("file[123].txt", "file1.txt", True),
            ("file[123].txt", "file4.txt", False),
            ("file[a-z].txt", "filex.txt", True),
            ("file[!0-9].txt", "filea.txt", True),
            ("file[!0-9].txt", "file5.txt", False),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match)

    def test_grouping_capture(self):
        """Test that regex produces capture groups"""
        pattern = "**/*.md"
        regex = k3fnmatch.translate(pattern)
        m = re.match(regex, "foo/bar/doc.md")
        self.assertIsNotNone(m)
        groups = m.groups()
        # Pattern **/*.md produces 5 groups: ('', multi-segment, '/', single-segment, '.md')
        self.assertEqual(len(groups), 5)
        # Verify key captured segments
        self.assertEqual(groups[0], "")  # Empty prefix before **
        self.assertEqual(groups[1], "foo/bar")  # Multi-segment match
        self.assertEqual(groups[2], "/")  # Separator
        self.assertEqual(groups[3], "doc")  # Filename
        self.assertEqual(groups[4], ".md")  # Extension

    def test_escaped_chars(self):
        """Test escaping special characters"""
        cases = [
            ("file.txt", "file.txt", True),
            ("file.txt", "filetxt", False),
            # [1] is a character class matching '1'
            ("file[1].txt", "file1.txt", True),
            ("file[1].txt", "file[1].txt", False),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match)

    def test_consecutive_stars(self):
        """Test that *** compresses to **"""
        regex1 = k3fnmatch.translate("**/*.txt")
        regex2 = k3fnmatch.translate("***/*.txt")
        regex3 = k3fnmatch.translate("****/*.txt")
        self.assertEqual(regex1, regex2)
        self.assertEqual(regex1, regex3)

    def test_regex_format(self):
        """Test exact regex output format from original test suite"""
        # Test simple * pattern
        self.assertEqual(
            r"(?s:(foo/)((?:[^/\\]|\\/|\\\\)*?)(\.md))\Z",
            k3fnmatch.translate(r"foo/*.md"),
        )

        # Test ** pattern
        self.assertEqual(
            r"(?s:(foo/)(.*?)(/)((?:[^/\\]|\\/|\\\\)*?)(\.md))\Z",
            k3fnmatch.translate(r"foo/**/*.md"),
        )

        # Test ** with fixed middle segment
        self.assertEqual(
            r"(?s:(foo/)(.*?)(/d/)((?:[^/\\]|\\/|\\\\)*?)(\.md))\Z",
            k3fnmatch.translate(r"foo/**/d/*.md"),
        )


class TestFnmap(unittest.TestCase):
    """Test fnmap() path transformation"""

    def test_basic_transformation(self):
        """Test simple path transformation"""
        cases = [
            ("foo/x/y.md", "**/*.md", "**/*-cn.md", "foo/x/y-cn.md"),
            ("a/b.txt", "*/*.txt", "*/*.log", "a/b.log"),
            ("file.md", "*.md", "*-backup.md", "file-backup.md"),
        ]
        for src, src_pat, dst_pat, expected in cases:
            result = k3fnmatch.fnmap(src, src_pat, dst_pat)
            self.assertEqual(result, expected, f"{src} + {src_pat} → {dst_pat}")

    def test_multiple_wildcards(self):
        """Test multiple wildcards in pattern"""
        result = k3fnmatch.fnmap("docs/guide/intro.md", "*/*/*.md", "*/*/*.html")
        self.assertEqual(result, "docs/guide/intro.html")

    def test_star_with_single_char(self):
        """Test * matching single character"""
        # Use * for both src and dst patterns
        result = k3fnmatch.fnmap("file1.txt", "file*.txt", "file*-new.txt")
        self.assertEqual(result, "file1-new.txt")

    def test_mixed_wildcards(self):
        """Test mixing ** and * wildcards"""
        result = k3fnmatch.fnmap("src/foo/bar/test.py", "src/**/*.py", "dist/**/*.js")
        self.assertEqual(result, "dist/foo/bar/test.js")

    def test_no_wildcards(self):
        """Test pattern without wildcards"""
        result = k3fnmatch.fnmap("file.txt", "file.txt", "newfile.txt")
        self.assertEqual(result, "newfile.txt")

    def test_original_md2zhihu_cases(self):
        """Test cases from original md2zhihu test suite"""
        src = r"foo/x/y/z/d/bar.md"

        # Replace prefix: foo -> bar
        self.assertEqual(
            r"bar/x/y/z/d/bar.cn.md",
            k3fnmatch.fnmap(src, r"foo/**/*.md", r"bar/**/*.cn.md"),
        )

        # Match with fixed middle segment /d/
        self.assertEqual(
            r"bar/x/y/z/d/bar.cn.md",
            k3fnmatch.fnmap(src, r"foo/**/d/*.md", r"bar/**/d/*.cn.md"),
        )

        # Insert new segment /f/ in destination
        self.assertEqual(
            r"bar/x/y/z/d/f/bar.cn.md",
            k3fnmatch.fnmap(src, r"foo/**/*.md", r"bar/**/f/*.cn.md"),
        )


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def test_empty_pattern(self):
        """Test empty pattern"""
        regex = k3fnmatch.translate("")
        self.assertTrue(re.match(regex, ""))
        self.assertFalse(re.match(regex, "anything"))

    def test_pattern_with_backslash(self):
        """Test patterns with escaped backslashes"""
        pattern = "*"
        regex = k3fnmatch.translate(pattern)
        # Should match paths with escaped slashes
        self.assertTrue(re.match(regex, "file"))

    def test_star_at_boundaries(self):
        """Test * at start/end of pattern"""
        cases = [
            ("*", "anything", True),
            ("*.txt", "file.txt", True),
            ("prefix*", "prefixsuffix", True),
        ]
        for pattern, path, should_match in cases:
            regex = k3fnmatch.translate(pattern)
            matches = re.match(regex, path) is not None
            self.assertEqual(matches, should_match)


if __name__ == "__main__":
    unittest.main()
