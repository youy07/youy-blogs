import os
import csv
import sys
import time
import argparse

KLINE_MAP = {
    1: 8,
    5: 0,
    15: 1,
    60: 3,
}

SERVERS = [
    ("180.153.18.170", 7709),
    ("180.153.18.171", 7709),
    ("202.108.253.130", 7709),
    ("119.147.212.81", 7709),
    ("101.227.73.20", 7709),
    ("115.238.56.198", 7709),
    ("218.75.126.9", 7709),
]

TRADING_MINUTES_PER_DAY = 240
HEADERS = ["datetime", "open", "close", "high", "low", "vol", "amount"]


def connect():
    from pytdx.hq import TdxHq_API
    for ip, port in SERVERS:
        api = TdxHq_API()
        try:
            if api.connect(ip, port, time_out=5):
                return api
        except Exception:
            pass
    raise ConnectionError("connect failed")


def fetch_bars(api, category, total_needed):
    all_data = []
    start = 0
    while len(all_data) < total_needed:
        count = min(800, total_needed - len(all_data))
        data = api.get_index_bars(category, 1, "880009", start, count)
        if not data:
            break
        all_data.extend(data)
        if len(data) < count:
            break
        start += count
        time.sleep(0.1)
    return all_data


def format_dt(row):
    return f"{row['year']:04d}-{row['month']:02d}-{row['day']:02d} {row['hour']:02d}:{row['minute']:02d}"


def main():
    parser = argparse.ArgumentParser(description="880009 Kline")
    parser.add_argument("--ktype", type=int, default=15, choices=[1, 3, 5, 15, 60],
                        help="Kline type in minutes")
    parser.add_argument("--dnum", type=int, default=7,
                        help="history days")
    args = parser.parse_args()

    if args.ktype not in KLINE_MAP:
        print(f"error: {args.ktype}min kline not supported by tdx")
        sys.exit(1)

    category = KLINE_MAP[args.ktype]
    total_needed = args.dnum * TRADING_MINUTES_PER_DAY // args.ktype
    out_file = f"880009_{args.ktype}min.csv"

    existing_rows = []
    seen = set()
    if os.path.exists(out_file):
        with open(out_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows.append(row)
                seen.add(row["datetime"])

    api = connect()
    try:
        rows = fetch_bars(api, category, total_needed)
    finally:
        try:
            api.disconnect()
        except Exception:
            pass

    if not rows:
        print("no data")
        return

    new_rows = []
    for r in rows:
        dt_str = format_dt(r)
        if dt_str not in seen:
            new_rows.append({
                "datetime": dt_str,
                "open": r["open"],
                "close": r["close"],
                "high": r["high"],
                "low": r["low"],
                "vol": int(r["vol"]),
                "amount": int(r["amount"]),
            })
            seen.add(dt_str)

    if not new_rows:
        print("no new data")
        return

    all_rows = existing_rows + new_rows
    all_rows.sort(key=lambda x: x["datetime"])

    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"880009_{args.ktype}min.csv: {len(new_rows)} new rows, total {len(all_rows)} rows")


if __name__ == "__main__":
    main()
