
---

## 3. `crowbar_nonverbal_v0_1.py` – minimal working skeleton

Here’s a **stdlib-only** CLI you can drop in and extend later:

```python
#!/usr/bin/env python3
"""
Cognitive Crowbar – Non-Verbal Edition (v0.1)

Local-only, AI-free tool for extracting simple cognitive-state proxies
from behavioural time-series (e.g. animal behaviour logs).
"""

import argparse
import csv
import json
from pathlib import Path
from collections import Counter, defaultdict


def read_events(csv_path):
    events = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                t = float(row["timestamp_sec"])
            except (KeyError, ValueError):
                continue
            agent = row.get("agent_id", "agent_0")
            behavior = row.get("behavior", "").strip() or "unknown"
            events.append({
                "t": t,
                "agent_id": agent,
                "behavior": behavior
            })
    events.sort(key=lambda e: e["t"])
    return events


def segment_events(events, window_size=5.0):
    """
    Very simple segmentation:
    - fixed windows of window_size seconds
    - per agent
    """
    episodes = []
    if not events:
        return episodes

    by_agent = defaultdict(list)
    for ev in events:
        by_agent[ev["agent_id"]].append(ev)

    for agent, agent_events in by_agent.items():
        start_t = agent_events[0]["t"]
        end_t = agent_events[-1]["t"]
        current_start = start_t

        while current_start <= end_t:
            current_end = current_start + window_size
            window_events = [
                ev for ev in agent_events
                if current_start <= ev["t"] < current_end
            ]
            if window_events:
                episodes.append({
                    "agent_id": agent,
                    "start_t": current_start,
                    "end_t": current_end,
                    "events": window_events
                })
            current_start = current_end

    return episodes


def compute_metrics(episode):
    events = episode["events"]
    behaviors = [e["behavior"] for e in events]
    duration = max(episode["end_t"] - episode["start_t"], 1e-6)

    count = len(events)
    unique_behaviors = len(set(behaviors))
    behavior_counts = Counter(behaviors)

    # crude proxies
    event_rate = count / duration
    diversity = unique_behaviors / count if count else 0.0
    # behaviour switching rate: count transitions between different behaviours
    switches = 0
    for b1, b2 in zip(behaviors, behaviors[1:]):
        if b1 != b2:
            switches += 1
    switch_rate = switches / duration

    return {
        "event_count": count,
        "unique_behaviors": unique_behaviors,
        "event_rate": event_rate,
        "diversity": diversity,
        "switch_rate": switch_rate,
        "behavior_counts": behavior_counts
    }


def classify_episode(metrics, thresholds):
    """
    Very simple heuristic:
    - high_entropy: high event_rate or high switch_rate
    - low_entropy: low event_rate and low switch_rate
    - middle: everything else
    """
    er = metrics["event_rate"]
    sr = metrics["switch_rate"]

    high_er = er >= thresholds["event_rate_high"]
    high_sr = sr >= thresholds["switch_rate_high"]
    low_er = er <= thresholds["event_rate_low"]
    low_sr = sr <= thresholds["switch_rate_low"]

    if high_er or high_sr:
        return "high_entropy"
    if low_er and low_sr:
        return "low_entropy"
    return "middle"


def cmd_segment(args):
    input_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    events = read_events(input_path)
    if not events:
        print("No valid events found in input.")
        return

    episodes = segment_events(events, window_size=args.window)
    if not episodes:
        print("No episodes produced.")
        return

    # gather metrics for all episodes to estimate rough thresholds
    metrics_list = []
    for ep in episodes:
        m = compute_metrics(ep)
        metrics_list.append(m)

    # thresholds: simple percentiles-ish via sorted list
    def get_threshold(values, frac):
        if not values:
            return 0.0
        values = sorted(values)
        idx = int(frac * (len(values) - 1))
        return values[idx]

    event_rates = [m["event_rate"] for m in metrics_list]
    switch_rates = [m["switch_rate"] for m in metrics_list]

    thresholds = {
        "event_rate_low": get_threshold(event_rates, 0.2),
        "event_rate_high": get_threshold(event_rates, 0.8),
        "switch_rate_low": get_threshold(switch_rates, 0.2),
        "switch_rate_high": get_threshold(switch_rates, 0.8),
    }

    output = []
    for ep, m in zip(episodes, metrics_list):
        cls = classify_episode(m, thresholds)
        output.append({
            "agent_id": ep["agent_id"],
            "start_t": ep["start_t"],
            "end_t": ep["end_t"],
            "metrics": {
                "event_count": m["event_count"],
                "unique_behaviors": m["unique_behaviors"],
                "event_rate": m["event_rate"],
                "diversity": m["diversity"],
                "switch_rate": m["switch_rate"],
            },
            "class": cls,
            "events": ep["events"]
        })

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(output)} episodes to {out_path}")


def cmd_summarize(args):
    episodes_path = Path(args.episodes).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not episodes_path.exists():
        print("Episodes file not found.")
        return

    episodes = json.loads(episodes_path.read_text(encoding="utf-8"))
    if not episodes:
        print("No episodes to summarise.")
        return

    class_counts = Counter(ep["class"] for ep in episodes)
    per_agent = defaultdict(lambda: Counter())

    for ep in episodes:
        per_agent[ep["agent_id"]][ep["class"]] += 1

    summary = {
        "total_episodes": len(episodes),
        "class_counts": dict(class_counts),
        "per_agent_class_counts": {
            agent: dict(cnts) for agent, cnts in per_agent.items()
        }
    }

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Saved summary to {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Cognitive Crowbar – Non-Verbal Edition (v0.1)\n"
            "Local-only, AI-free behavioural entropy profiler."
        )
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_seg = sub.add_parser("segment", help="Segment CSV events into episodes and classify them.")
    p_seg.add_argument("--input", required=True, help="Input CSV file with behaviour events.")
    p_seg.add_argument("--out", required=True, help="Output JSON file for episodes.")
    p_seg.add_argument("--window", type=float, default=5.0,
                       help="Episode window size in seconds (default: 5.0).")
    p_seg.set_defaults(func=cmd_segment)

    p_sum = sub.add_parser("summarize", help="Summarise episode classes.")
    p_sum.add_argument("--episodes", required=True, help="Input episodes JSON file.")
    p_sum.add_argument("--out", required=True, help="Output JSON summary file.")
    p_sum.set_defaults(func=cmd_summarize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
