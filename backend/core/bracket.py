import random
from typing import List, Dict, Any, Optional

class TournamentManager:
    def __init__(self, players: List[str]):
        """
        Initializes the tournament manager with a list of player names or IDs.
        """
        self.players = players
        self.num_players = len(players)

    def generate_single_elimination(self) -> List[Dict[str, Any]]:
        """
        Generates the first round fixtures for a single elimination bracket.
        Automatically handles 8, 16, 32 players (and others by adding BYEs).
        """
        shuffled = list(self.players)
        random.shuffle(shuffled)

        # Calculate next power of 2 for bracket size if needed,
        # but prompt specifies 8, 16, 32.
        fixtures = []
        for i in range(0, len(shuffled), 2):
            p1 = shuffled[i]
            p2 = shuffled[i+1] if i+1 < len(shuffled) else "BYE"
            fixtures.append({
                "id": i // 2,
                "players": [p1, p2],
                "status": "scheduled",
                "winner": None
            })
        return fixtures

    def generate_round_robin(self, group_size: int = 4) -> Dict[str, List[str]]:
        """
        Divides players into groups for Round Robin play.
        Default group size is 4.
        """
        shuffled = list(self.players)
        random.shuffle(shuffled)

        groups = {}
        for i in range(0, len(shuffled), group_size):
            group_label = f"Group {chr(65 + i//group_size)}"
            groups[group_label] = shuffled[i:i+group_size]
        return groups

    def spin_the_wheel(self, fixtures: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Result generator that selects a slot from available bracket fixtures.
        Designed to be modular for easy attachment to a physics-based frontend.
        """
        if not fixtures:
            return {}

        # Filter for fixtures that are yet to be played
        available_slots = [f for f in fixtures if f.get("status") == "scheduled"]

        if not available_slots:
            # If nothing is scheduled, maybe look for already active ones?
            # For now, stick to scheduled.
            return {}

        # Weighted selection could be added here if needed,
        # but for now, it's a random selection (the "spin" result).
        selected = random.choice(available_slots)
        return selected

    def update_fixture_winner(self, fixtures: List[Dict[str, Any]], fixture_id: int, winner: str) -> List[Dict[str, Any]]:
        """
        Updates the winner of a fixture and marks it as 'played'.
        """
        for f in fixtures:
            if f["id"] == fixture_id:
                f["winner"] = winner
                f["status"] = "played"
                break
        return fixtures

if __name__ == "__main__":
    # Quick sanity check
    players = [f"Player {i}" for i in range(1, 9)]
    tm = TournamentManager(players)

    print("--- Single Elimination Bracket ---")
    se_fixtures = tm.generate_single_elimination()
    for f in se_fixtures:
        print(f)

    print("\n--- Round Robin Groups ---")
    rr_groups = tm.generate_round_robin()
    print(rr_groups)

    print("\n--- Spin the Wheel Result ---")
    print(tm.spin_the_wheel(se_fixtures))
