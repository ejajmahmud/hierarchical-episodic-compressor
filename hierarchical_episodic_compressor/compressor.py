"""Core Hierarchical Episodic Compressor implementation."""
from typing import List, Dict, Optional, Any


class EpisodicFrame:
    def __init__(self, frame_id: int, role: str, content: str, action: Optional[str] = None):
        self.frame_id = frame_id
        self.role = role
        self.content = content
        self.action = action


class HierarchicalEpisodicCompressor:
    def __init__(self, micro_chunk_size: int = 3, max_macro_milestones: int = 5):
        self.micro_chunk_size = micro_chunk_size
        self.max_macro_milestones = max_macro_milestones
        self.raw_frames: List[EpisodicFrame] = []
        self.micro_summaries: List[str] = []
        self.macro_milestones: List[str] = []

    def add_turn(self, role: str, content: str, action: Optional[str] = None) -> int:
        frame_id = len(self.raw_frames) + 1
        frame = EpisodicFrame(frame_id, role, content, action)
        self.raw_frames.append(frame)

        if len(self.raw_frames) % self.micro_chunk_size == 0:
            self._compress_micro()
        return frame_id

    def _compress_micro(self):
        recent = self.raw_frames[-self.micro_chunk_size:]
        actions = [f.action for f in recent if f.action]
        roles = [f.role for f in recent]
        summary = f"Steps {recent[0].frame_id}-{recent[-1].frame_id}: Roles({','.join(set(roles))}) -> Actions: {','.join(actions) if actions else 'Discussion'}"
        self.micro_summaries.append(summary)

        if len(self.micro_summaries) >= 3:
            self._crystallize_macro()

    def _crystallize_macro(self):
        bundled = "; ".join(self.micro_summaries[-3:])
        macro = f"Phase {len(self.macro_milestones)+1} [Frames {len(self.raw_frames)-8}-{len(self.raw_frames)}]: {bundled}"
        self.macro_milestones.append(macro)
        if len(self.macro_milestones) > self.max_macro_milestones:
            self.macro_milestones.pop(0)

    def get_compressed_context(self) -> Dict[str, Any]:
        uncompressed_recent = self.raw_frames[-(self.micro_chunk_size - 1):] if (len(self.raw_frames) % self.micro_chunk_size != 0) else []
        return {
            "macro_milestones": list(self.macro_milestones),
            "micro_summaries": self.micro_summaries[-2:],
            "active_turns": [{"role": f.role, "content": f.content} for f in uncompressed_recent],
            "total_raw_turns": len(self.raw_frames)
        }
