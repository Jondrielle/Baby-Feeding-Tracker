from backend.models import FeedingDBModel
from backend.enums import feedingMethod
from datetime import datetime 

def test_feeding_model_defaults():
	feedingEntry = FeedingDBModel(method = feedingMethod.bottle)

	assert feedingEntry.method == feedingMethod.bottle
	assert feedingEntry.time is None or isinstance(feedingEntry.time, datetime)
	assert feedingEntry.amount_oz is None
	assert feedingEntry.amount_ml is None
	assert feedingEntry.notes is None

def test_feeding_method_enum():
	feedingEntry = FeedingDBModel(method = feedingMethod.food)
	assert feedingEntry.method == feedingMethod.food

