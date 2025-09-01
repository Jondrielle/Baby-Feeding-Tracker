import pytest
from backend.schemas import FeedEntry
from pydantic import ValidationError

# Using pytest's parametrize decorator for multiple inputs
@pytest.mark.parametrize("feedData, expected", [
    # valid feed entry 
    ({"id": 2, "method": "food", "amount_oz": 5, "amount_ml": 0}, True),
    # oz and ml cant both be more than 0
    ({"id": 1, "method": "breastfeeding", "amount_oz": 8, "amount_ml": 240, "notes": "Test note"}, False),
    # oz and ml cant both be 0
    ({"id": 5, "method": "food", "amount_oz": 0, "amount_ml": 0}, False),
    # oz or ml cant be less than 0
    ({"id": 5, "method": "food", "amount_oz": -100, "amount_ml": 0}, False),
    # oz range must be in the range of 
    ({"id": 5, "method": "bottle", "amount_oz": 39, "amount_ml": 0}, False),
    # ml range must be in the range of 
    ({"id": 5, "method": "breastfeeding", "amount_oz": 0, "amount_ml": 4990}, False),
])
def test_oz_or_ml(feedData, expected):
    try:
        feed_Entry = FeedEntry(**feedData)
        assert expected == True
    except ValidationError:
        assert expected == False

def test_sanitize_notes():
    # notes can not be any html text
    feed = FeedEntry(id= 12, method= "food", amount_oz= 0, amount_ml= 1, notes= "<script></script")
    assert feed.notes == "&lt;/script"


    # Test case with correct plain text 
    feed2 = FeedEntry(id=12, method="food", amount_oz=0, amount_ml=1, notes="Feed went well")
    assert feed2.notes == "Feed went well"  

    # If notes are None, it should stay None
    # Test case with correct plain text 
    feed3 = FeedEntry(id=12, method="food", amount_oz=0, amount_ml=1, notes=None)
    assert feed3.notes == ""  