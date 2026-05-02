import sys
import os

# Add the project root to sys.path so we can import 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.bracket import TournamentManager

def test_single_elimination():
    print("Testing Single Elimination...")
    players = [f"P{i}" for i in range(1, 17)]
    tm = TournamentManager(players)
    fixtures = tm.generate_single_elimination()
    assert len(fixtures) == 8
    for f in fixtures:
        assert len(f["players"]) == 2
        assert f["status"] == "scheduled"
    print("✓ Single Elimination Passed")

def test_round_robin():
    print("Testing Round Robin...")
    players = [f"P{i}" for i in range(1, 9)]
    tm = TournamentManager(players)
    groups = tm.generate_round_robin(group_size=4)
    assert len(groups) == 2
    assert len(groups["Group A"]) == 4
    print("✓ Round Robin Passed")

def test_spin_the_wheel():
    print("Testing Spin the Wheel...")
    players = [f"P{i}" for i in range(1, 9)]
    tm = TournamentManager(players)
    fixtures = tm.generate_single_elimination()
    result = tm.spin_the_wheel(fixtures)
    assert result in fixtures

    # Test with no available fixtures
    for f in fixtures:
        f["status"] = "played"
    result_empty = tm.spin_the_wheel(fixtures)
    assert result_empty == {}
    print("✓ Spin the Wheel Passed")

if __name__ == "__main__":
    try:
        test_single_elimination()
        test_round_robin()
        test_spin_the_wheel()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
