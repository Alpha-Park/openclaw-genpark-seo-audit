# -*- coding: utf-8 -*-
from client import OpenClawGenParkSeoAudit

seo = OpenClawGenParkSeoAudit()

sample_article = """
Autonomous AI agents are revolutionizing decentralized commerce through the Model Context Protocol.
These intelligent agents negotiate prices, verify cryptographic receipts, and manage multi-cloud infrastructure.
By using robust algorithmic game theory, agent systems achieve Nash equilibrium in spot compute auctions.
"""

# 1. Readability
read = seo.calculate_readability_metrics(sample_article)
print(f"Readability: Flesch Reading Ease={read['flesch_reading_ease']} (Grade Level: {read['flesch_kincaid_grade_level']}, {read['readability_classification']})")

# 2. Keyword Stuffing Audit
kws = ["AI agents", "Model Context Protocol", "cryptographic receipts"]
density = seo.audit_keyword_density_and_stuffing(sample_article, kws, max_safe_density_pct=3.0)
print(f"\nKeyword Audit: Penalty={density['has_keyword_stuffing_penalty']} ({density['seo_density_posture']})")
for k in density['keyword_breakdown']:
    print(f"  {k['keyword']}: {k['density_percentage']}% (Count={k['occurrences']})")

# 3. Internal Linking PageRank Depth
depth = seo.compute_internal_linking_page_rank_penalty(crawl_depth=2, internal_inlinks_count=24)
print(f"\nInternal Linking Equity: Score={depth['estimated_link_equity_score']} ({depth['indexability_status']})")
