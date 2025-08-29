from enum import Enum 

class feedingMethod(str, Enum):
	breastfeeding = "breastfeeding"
	bottle = "bottle"
	food = "food"