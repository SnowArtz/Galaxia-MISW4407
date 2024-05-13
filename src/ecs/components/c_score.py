class CScore:
    def __init__(self, base_score=0, state_scores=None):
        self.base_score = base_score
        self.state_score = 0
        self.state_scores = state_scores or {}
    
    @classmethod
    def update_state_score(self, new_state):
        self.state_score = self.state_scores.get(new_state, self.state_scores['default'])
