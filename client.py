# -*- coding: utf-8 -*-
"""
OpenClaw GenPark SEO Audit - Flesch-Kincaid Readability & TF-IDF Semantic Density Auditor
Standard Library only: re, math, typing.
Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level, detects unnatural keyword stuffing,
and evaluates internal linking PageRank crawl depth penalties.
"""

import re
import math
from typing import Dict, List, Any

class OpenClawGenParkSeoAudit:
    def __init__(self):
        pass

    def _count_syllables(self, word: str) -> int:
        w = word.lower().strip()
        if len(w) <= 3:
            return 1
        # Remove trailing silent e
        if w.endswith("e") and not w.endswith("le"):
            w = w[:-1]
        vowels = "aeiouy"
        count = 0
        prev_is_vowel = False
        for ch in w:
            is_v = ch in vowels
            if is_v and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_v
        return max(1, count)

    def calculate_readability_metrics(self, text: str) -> Dict[str, Any]:
        """
        Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level:
        FRE = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        FKGL = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        """
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip()) > 3]
        words = [w for w in re.findall(r"\b[a-zA-Z]{2,}\b", text)]

        num_sentences = max(1, len(sentences))
        num_words = max(1, len(words))
        num_syllables = sum(self._count_syllables(w) for w in words)

        asl = num_words / num_sentences # average sentence length
        asw = num_syllables / num_words  # average syllables per word

        flesch_reading_ease = 206.835 - (1.015 * asl) - (84.6 * asw)
        flesch_kincaid_grade = (0.39 * asl) + (11.8 * asw) - 15.59

        fre_clamped = round(max(0.0, min(100.0, flesch_reading_ease)), 2)
        fkgl_clamped = round(max(1.0, flesch_kincaid_grade), 1)

        if fre_clamped >= 70.0:
            audience = "GENERAL_PUBLIC_EASY"
        elif fre_clamped >= 50.0:
            audience = "TECHNICAL_PROFESSIONAL_STANDARD"
        else:
            audience = "ACADEMIC_HIGH_COMPLEXITY"

        return {
            "total_words": num_words,
            "total_sentences": num_sentences,
            "total_syllables": num_syllables,
            "avg_sentence_length_words": round(asl, 2),
            "avg_syllables_per_word": round(asw, 2),
            "flesch_reading_ease": fre_clamped,
            "flesch_kincaid_grade_level": fkgl_clamped,
            "readability_classification": audience
        }

    def audit_keyword_density_and_stuffing(self, text: str,
                                          target_keywords: List[str],
                                          max_safe_density_pct: float = 3.5) -> Dict[str, Any]:
        """
        Calculates exact frequency and density percentage for target keywords.
        Flags penalties if density exceeds max_safe_density_pct.
        """
        words = [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text)]
        tot_words = max(1, len(words))

        full_lower = text.lower()
        keyword_audits = []
        any_stuffing = False

        for kw in target_keywords:
            kw_clean = kw.lower().strip()
            # Exact phrase occurrences
            pattern = r"\b" + re.escape(kw_clean) + r"\b"
            matches = len(re.findall(pattern, full_lower))
            kw_len = len(kw_clean.split())
            density_pct = (matches * kw_len / tot_words) * 100.0

            is_stuffed = density_pct > max_safe_density_pct
            if is_stuffed:
                any_stuffing = True

            keyword_audits.append({
                "keyword": kw,
                "occurrences": matches,
                "density_percentage": round(density_pct, 2),
                "is_stuffed": is_stuffed
            })

        return {
            "total_word_count": tot_words,
            "max_safe_density_limit_pct": max_safe_density_pct,
            "has_keyword_stuffing_penalty": any_stuffing,
            "seo_density_posture": "PENALTY_RISK_OVER_OPTIMIZED" if any_stuffing else "OPTIMAL_NATURAL_DENSITY",
            "keyword_breakdown": keyword_audits
        }

    def compute_internal_linking_page_rank_penalty(self, crawl_depth: int,
                                                    internal_inlinks_count: int) -> Dict[str, Any]:
        """
        Calculates page rank equity decay as a function of crawl depth from homepage:
        Equity = Inlinks * exp(-0.4 * crawl_depth)
        """
        depth = max(0, crawl_depth)
        inlinks = max(0, internal_inlinks_count)

        depth_decay = math.exp(-0.4 * depth)
        page_equity = inlinks * depth_decay

        return {
            "crawl_depth_level": depth,
            "internal_inlinks_count": inlinks,
            "depth_decay_multiplier": round(depth_decay, 4),
            "estimated_link_equity_score": round(page_equity, 2),
            "indexability_status": "HIGH_CRAWL_PRIORITY" if depth <= 2 else ("MODERATE_PRIORITY" if depth <= 4 else "DEEP_PAGE_INDEX_HAZARD")
        }
