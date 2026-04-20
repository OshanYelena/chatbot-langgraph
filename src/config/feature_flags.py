from dataclasses import dataclass


@dataclass
class FeatureFlags:
    enable_rag: bool = True
    enable_tools: bool = True
    enable_long_term_memory: bool = True
    enable_streaming: bool = True
    enable_safety_filter: bool = True


flags = FeatureFlags()
