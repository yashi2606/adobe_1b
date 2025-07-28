import spacy
from collections import defaultdict

class PersonaAnalyzer:
    def __init__(self, persona, job):
        self.nlp = spacy.load("en_core_web_sm")
        self.persona = persona.lower()
        self.job = job.lower()
        
        # Define keywords for different personas
        self.keyword_weights = self._get_keyword_weights()
        
    def _get_keyword_weights(self):
        weights = defaultdict(float)
        
        # Persona-specific keywords
        if 'travel' in self.persona or 'planner' in self.persona:
            weights.update({
                'itinerary': 0.9,
                'accommodation': 0.8,
                'transport': 0.7,
                'activity': 0.8,
                'restaurant': 0.7,
                'hotel': 0.7,
                'budget': 0.6,
                'group': 0.7,
                'day': 0.6,
                'trip': 0.9,
                'plan': 0.9,
                'visit': 0.7,
                'experience': 0.6
            })
        
        # Job-specific keywords
        if 'college' in self.job and 'friends' in self.job:
            weights.update({
                'budget': 0.8,
                'fun': 0.7,
                'nightlife': 0.8,
                'adventure': 0.7,
                'group': 0.9,
                'young': 0.6,
                'student': 0.7
            })
        
        return weights
    
    def analyze(self, text):
        doc = self.nlp(text.lower())
        score = 0.0
        matched_keywords = 0
        
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
                
            if token.text in self.keyword_weights:
                score += self.keyword_weights[token.text]
                matched_keywords += 1
        
        # Normalize score
        if matched_keywords > 0:
            score = score / (matched_keywords * 0.8)  # Adjust for text length
            
        return min(score, 1.0)  # Cap at 1.0
