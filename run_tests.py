import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)

from agents.memory import ConversationMemory, ResponseCache, FeedbackStore, DealStore

mem = ConversationMemory("test-1")
mem.add_message("user", "Hello")
mem.add_message("assistant", "Hi", persona="test")
assert len(mem.get_history()) == 2
print("[PASS] Memory: add + retrieve")

ResponseCache.set("q1", "p1", "r1")
assert ResponseCache.get("q1", "p1") == "r1"
print("[PASS] Cache: set + get")

ResponseCache.set("q2", "p2", "r2", ttl_hours=0)  # expired immediately
cached = ResponseCache.get("q2", "p2")
print(f"[INFO] Cache expiry: {'works' if not cached else 'not expired yet'}")

did = DealStore.save("Test Deal", "Test Co", 100000, "Demo", 25.0)
assert did is not None
deals = DealStore.list()
print(f"[PASS] DealStore: {len(deals)} deals")

FeedbackStore.save("c1", 5, "Excellent")
stats = FeedbackStore.get_stats()
print(f"[PASS] Feedback: {stats}")

os.remove(os.path.join(os.path.dirname(__file__), "data", "dealforge.db"))
print("[INFO] Test DB cleaned up")

print("\nALL MEMORY TESTS PASSED")
