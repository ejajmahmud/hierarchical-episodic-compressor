"""Unit tests for hierarchical-episodic-compressor."""
import unittest
from hierarchical_episodic_compressor.compressor import HierarchicalEpisodicCompressor


class TestHierarchicalEpisodicCompressor(unittest.TestCase):
    def test_add_turns_and_micro_chunking(self):
        c = HierarchicalEpisodicCompressor(micro_chunk_size=3)
        c.add_turn("user", "Hello")
        c.add_turn("assistant", "Hi", action="greet")
        self.assertEqual(len(c.micro_summaries), 0)
        c.add_turn("user", "Run query")
        self.assertEqual(len(c.micro_summaries), 1)

    def test_macro_milestone_crystallization(self):
        c = HierarchicalEpisodicCompressor(micro_chunk_size=2)
        for i in range(6):
            c.add_turn("user", f"Turn {i}", action=f"act_{i}")
        self.assertGreaterEqual(len(c.macro_milestones), 1)

    def test_compressed_context_structure(self):
        c = HierarchicalEpisodicCompressor(micro_chunk_size=3)
        for i in range(5):
            c.add_turn("user", f"Content {i}")
        ctx = c.get_compressed_context()
        self.assertEqual(ctx["total_raw_turns"], 5)
        self.assertIn("active_turns", ctx)
