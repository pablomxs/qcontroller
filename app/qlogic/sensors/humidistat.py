import logging

logger = logging.getLogger(__name__)

def classify_humidistat(values: list, reference_hum: float) -> str:
    """
    Classifies the humidistat based on the provided values and reference humidity.
    """
    # If the log file has less than one value, we consider the sensor can't be
    # evaluated and return "not enough values".
    if len(values) < 1:
        logger.warning("Not enough values to classify the humidistat")
        return "not enough values"
    
    for val in values:
        if abs(val - reference_hum) > 1:
            return "discard"
    return "keep"
