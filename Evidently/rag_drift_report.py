"""
RAG Drift Monitoring for DetoxifyAI
Tracks distribution changes in toxicity detection queries over time
"""

import pandas as pd
import numpy as np
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset  # , TextOverviewPreset
from pathlib import Path
from datetime import datetime


class RAGDriftMonitor:
    """Monitor query distribution drift for RAG pipeline"""

    def __init__(self, reference_data_path=None):
        self.reference_queries = self._load_reference_data(reference_data_path)

    def _load_reference_data(self, path):
        """Load baseline queries from initial deployment"""
        # These would ideally come from your eval dataset or initial logs
        # For now, using representative toxic query patterns
        return [
            "You're an idiot and nobody likes you",
            "This is complete garbage, worst thing ever",
            "I hate everything about this stupid idea",
            "What a moron, can't believe people listen to you",
            "Absolutely terrible, you should be ashamed",
            "Dumbest thing I've ever heard in my life",
            "You're so stupid it's unbelievable",
            "This sucks more than anything I've seen",
            "Complete waste of time, total trash",
            "Pathetic loser with no brain at all",
            "Go away, nobody wants your stupid opinion",
            "Shut up, you don't know anything",
            "Worst comment ever made by anyone",
            "Idiotic statement from an idiot person",
            "Absolutely moronic take on everything",
        ]

    def extract_features(self, queries):
        """Extract query features for drift detection"""
        features = []

        # Profanity keywords
        profanity_words = [
            "idiot",
            "stupid",
            "hate",
            "moron",
            "dumb",
            "garbage",
            "trash",
            "loser",
            "pathetic",
        ]

        for query in queries:
            query_lower = query.lower()
            features.append(
                {
                    "query": query,
                    "length": len(query),
                    "word_count": len(query.split()),
                    "has_profanity": any(
                        word in query_lower for word in profanity_words
                    ),
                    "profanity_count": sum(
                        1 for word in profanity_words if word in query_lower
                    ),
                    "avg_word_length": np.mean([len(word) for word in query.split()]),
                    "has_caps": any(c.isupper() for c in query),
                    "exclamation_count": query.count("!"),
                }
            )

        return pd.DataFrame(features)

    def generate_report(self, current_queries, output_path="monitoring/reports"):
        """Generate Evidently drift report"""

        # Prepare data
        reference_df = self.extract_features(self.reference_queries)
        current_df = self.extract_features(current_queries)

        print(f"📊 Reference queries: {len(reference_df)}")
        print(f"📊 Current queries: {len(current_df)}")

        # Define column mapping
        column_mapping = ColumnMapping(
            text_features=["query"],
            numerical_features=[
                "length",
                "word_count",
                "profanity_count",
                "avg_word_length",
                "exclamation_count",
            ],
        )

        # Create report
        report = Report(
            metrics=[
                DataDriftPreset(),
            ]
        )

        report.run(
            reference_data=reference_df,
            current_data=current_df,
            column_mapping=column_mapping,
        )

        # Save report
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"rag_drift_report_{timestamp}.html"
        report.save_html(str(report_path))

        # Also save as latest
        latest_path = output_dir / "rag_drift_report_latest.html"
        report.save_html(str(latest_path))

        print("✅ Report saved:")
        print(f"   - {report_path}")
        print(f"   - {latest_path}")

        return report_path


def simulate_current_queries():
    """Simulate current production queries (in real scenario, load from logs)"""
    # Simulate slight drift - queries are less aggressive
    return [
        "You're wrong about this completely",
        "Bad take on the subject matter",
        "Disagree strongly with your position",
        "Not a smart way to approach this",
        "Terrible idea that won't work out",
        "This doesn't make any sense to me",
        "Absolutely disagree with your point",
        "Wrong answer to the question asked",
        "Incorrect information being shared here",
        "Mistaken belief about how this works",
        "Flawed reasoning in your argument today",
        "Poor understanding of the actual issue",
        "Weak argument that lacks evidence now",
        "Questionable logic in your statement",
        "Dubious claim without proper support",
    ]


if __name__ == "__main__":
    print("🔍 DetoxifyAI - RAG Drift Monitoring")
    print("=" * 50)

    # Initialize monitor
    monitor = RAGDriftMonitor()

    # Simulate current queries (in production, load from FastAPI logs)
    current_queries = simulate_current_queries()

    # Generate report
    report_path = monitor.generate_report(current_queries)

    print("\n📈 Open report in browser:")
    print(f"   file://{report_path.absolute()}")
