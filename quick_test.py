import sys
sys.path.insert(0, "features/chatbot")
from retriever import retrieve
print("Testing retrieval...")
for q in ["dharma", "duty", "Krishna"]:
    r = retrieve(q, top_k=1)
    print(f"Query '{q}': {len(r)} results")
