from lexai.core.match_engine import generate_matches


class LexAIService:
    @staticmethod
    def handle_query(query: str, location: str) -> str:
        return generate_matches(query, location)
