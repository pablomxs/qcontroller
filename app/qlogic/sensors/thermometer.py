from statistics import mean, stdev
import logging

logger = logging.getLogger(__name__)


def classify_thermometer(values: list, reference_temp: float) -> str:
    """
    Classifies the thermometer based on the provided values and reference temperature.
    """
    # If the log file has less than two values, stddev returns a StatisticsError. In that case,
    # we consider the sensor can't be evaluated and return "not enough values".
    # Ref.: https://www.w3schools.com/python/ref_stat_stdev.asp
    if len(values) < 2:
        logger.warning("Not enough values to classify the thermometer")
        return "not enough values"
    
    avg = mean(values)
    std = stdev(values)
    diff = abs(avg - reference_temp)

    if diff <= 0.5 and std < 3:
        return "ultra precise"
    elif diff <= 0.5 and std < 5:
        return "very precise"
    else:
        return "precise"
    