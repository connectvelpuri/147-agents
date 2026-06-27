
"""
Account Intelligence Engine - RAG Pipeline
Lightweight TF-IDF + cosine similarity RAG over intel data
No external dependencies beyond Python stdlib
"""
import json, re, math
from collections import Counter
from pathlib import Path

class IntelRAG:
    """Retrieval-Augmented Generation over account intelligence"""
    
    def __init__(self, db_path=None):
        self.documents = []
        self.doc_sources = []
        self.idf = {}
        self.built = False
    
    def load_from_database(self, db_module):
        """Load all account data into searchable document store"""
        accounts = db_module.query_all_accounts()
        for acct in accounts:
            aid = acct["id"]
            # Build document from account data
            doc = f"{acct['company']} ({acct['sector']}) - {acct['sap_erp']}"
            contacts = db_module.query_contacts(aid)
            pains = db_module.query_pain_points(aid)
            signals = db_module.query_signals(aid)
            
            if contacts:
                doc += " Leadership: " + "; ".join([f"{c['name']} ({c['role']})" for c in contacts])
            if pains:
                doc += " Pain Points: " + "; ".join([p["pain"] for p in pains])
            if signals:
                doc += " Signals: " + "; ".join([s["signal_text"] for s in signals])
            
            self.documents.append(doc)
            self.doc_sources.append(acct["company"])
        
        self._build_index()
        return len(self.documents)
    
    def add_document(self, text, source):
        self.documents.append(text)
        self.doc_sources.append(source)
    
    def _tokenize(self, text):
        return re.findall(r'\w+', text.lower())
    
    def _build_index(self):
        """Build TF-IDF index"""
        n = len(self.documents)
        if n == 0:
            return
        all_terms = set()
        for doc in self.documents:
            all_terms.update(self._tokenize(doc))
        
        for term in all_terms:
            df = sum(1 for doc in self.documents if term in self._tokenize(doc))
            self.idf[term] = math.log((n + 1) / (df + 1)) + 1
        
        self.built = True
    
    def search(self, query, top_k=3):
        """Search documents by TF-IDF cosine similarity"""
        if not self.built:
            return []
        query_tokens = self._tokenize(query)
        query_tf = Counter(query_tokens)
        query_norm = math.sqrt(sum(v*v for v in query_tf.values()))
        
        scores = []
        for i, doc in enumerate(self.documents):
            doc_tokens = self._tokenize(doc)
            doc_tf = Counter(doc_tokens)
            doc_norm = math.sqrt(sum(v*v for v in doc_tf.values()))
            
            dot_product = 0
            for term, qtf in query_tf.items():
                if term in doc_tf:
                    dot_product += qtf * doc_tf[term] * self.idf.get(term, 1)
            
            denominator = query_norm * doc_norm
            similarity = dot_product / denominator if denominator > 0 else 0
            scores.append((similarity, self.doc_sources[i], doc[:300]))
        
        scores.sort(reverse=True)
        return [{"source": s[1], "similarity": round(s[0], 3), "snippet": s[2]} for s in scores[:top_k] if s[0] > 0]

if __name__ == "__main__":
    print("RAG module ready")
