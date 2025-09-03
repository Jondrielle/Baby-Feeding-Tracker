import pytest
from backend.schemas import FeedEntry,FeedEntryID
from pydantic import ValidationError
from datetime import datetime,timedelta,timezone

def test_valid_feed_entry():
    # valid feed entry 
    feed = FeedEntry(method="food",amount_oz=5,amount_ml=0)
    assert feed.method == "food"
    assert isinstance(feed.time, datetime)
    assert feed.amount_oz == 5
    assert feed.amount_ml == 0

def test_oz_and_ml_cant_both_be_more_than_zero():
    # oz and ml cant both be more than 0
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="breastfeeding",amount_oz=8,amount_ml=30,notes="Test note")
    
    # Check that the exception message contains the expected error
    assert "Either amount_oz or amount_ml must be set, not both" in str(exc_info.value)

def test_oz_and_ml_cant_both_be_zero():
    # oz and ml cant both be 0
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="bottle",amount_oz=0,amount_ml=0)

    # Check that the exception message contains the expected error 
    assert "Either amount_oz or amount_ml must be set" in str(exc_info.value)

def test_oz_and_ml_must_be_in_its_range():
    # oz range must be in the range of 
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="bottle",amount_oz=39,amount_ml=0)

    # Check that the exception message contains the expected error 
    assert "Amount_oz cannot be more than 32 ounces for a day" in str(exc_info.value)

    # ml range must be in the range of 
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="breastfeeding", amount_oz=0, amount_ml=4900)

    # Check that the exception message contains the expected error 
    assert "Amount_ml cannot be more than 950 ml for a day" in str(exc_info.value)

def test_nonnegative_oz_or_ml_values():
    # oz cant be less than 0
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="food",amount_oz=-100,amount_ml=0)

    # Check that the exception message contains the expected error 
    assert "Amount_oz cannot be negative" in str(exc_info.value)

    # ml cant be less than 0
    with pytest.raises(ValidationError) as exc_info:
        feed = FeedEntry(method="bottle",amount_oz=0,amount_ml=-20)

    # Check that the exception message contains the expected error 
    assert "Amount_ml cannot be negative" in str(exc_info.value)

    # Test both negative values for amount_ml and amount_oz
    with pytest.raises(ValidationError) as exc_info:
        FeedEntry(method="food", amount_oz=-5, amount_ml=-20)

    # Check that the exception message contains the expected error
    assert "Amount_oz cannot be negative" in str(exc_info.value) or "Amount_ml cannot be negative" in str(exc_info.value)

def test_sanitize_notes():
    # notes can not be any html text
    feed = FeedEntry(method= "food", amount_oz= 0, amount_ml= 1, notes= "<script></script")
    assert feed.notes == "&lt;/script"


    # Test case with correct plain text 
    feed2 = FeedEntry(method="food", amount_oz=0, amount_ml=1, notes="Feed went well")
    assert feed2.notes == "Feed went well"  

    # If notes are None, it should stay None
    # Test case with correct plain text 
    feed3 = FeedEntry(method="food", amount_oz=0, amount_ml=1, notes=None)
    assert feed3.notes == "" 

def test_time_not_in_future():
    future_time = datetime.now(timezone.utc) + timedelta(hours=1)
    try:
        feed = FeedEntry(method="breastfeeding",time=future_time,amount_oz=20,amount_ml=0,notes="Feed was took a minute")
        assert False, "Expected ValidationError but none was raised"
    except ValidationError as e:
        # Check if the correct error message is in the exception
        assert "Time cannot be in the future" in str(e)

def test_feed_entry_id_is_valid():
    feedID = FeedEntryID(id= 21)
    assert feedID.id == 21