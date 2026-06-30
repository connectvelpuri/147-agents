
import sys, os
sys.path.insert(0, r"C:\Users\Lenovo\saleshouse")
from agents.account_intel.engine import AccountIntelEngine

engine = AccountIntelEngine()
md = engine.to_markdown("CEVA Logistics", "Logistics")
print(f"Report generated: {len(md)} chars, {md.count(chr(10))} lines")
print(md[:400])
print("...")
print("OK - Account Intelligence Engine works!")
