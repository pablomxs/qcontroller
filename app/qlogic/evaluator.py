from app.qlogic.sensors.humidistat import classify_humidistat
from app.qlogic.sensors.thermometer import classify_thermometer
from app.qlogic.sensors._registry import SENSOR_CLASSIFIERS
import logging

logger = logging.getLogger(__name__)

def evaluate_sensors(parsed_data: dict) -> dict:
    """
    Takes the parsed data and evaluates the sensors based on the classification functions,
    which are imported from the sensors folder.
    """

    # Example of parsed_data structure:
    # {
    #     "reference": {
    #         "temperature": 70.0,
    #         "humidity": 45.0
    #     },
    #     "sensors": {
    #         "temp-1": {
    #             "type": "thermometer",
    #             "values": [72.4, 76.0, 79.1, 75.6, 71.2, 71.4, 69.2, 65.2, 62.8, 61.4, 64.0, 67.5, 69.4]
    #         },
    #         "temp-2": {
    #             "type": "thermometer",
    #             "values": [69.5, 70.1, 71.3, 71.5, 69.8]
    #         },
    #         "hum-1": {
    #             "type": "humidistat",
    #             "values": [45.2, 45.3, 45.1]
    #         },
    #         "hum-2": {
    #             "type": "humidistat",
    #             "values": []
    #         },
    #         "hum-3": {
    #             "type": "humidistat",
    #             "values": [44.4, 43.9, 44.9, 43.8, 42.1]
    #         }
    #     }
    # }


    reference = parsed_data["reference"]
    sensors = parsed_data["sensors"]

    results = {}

    for name, sensor in sensors.items():
        sensor_type = sensor["type"]
        values = sensor["values"]
        logger.info(f"Evaluating sensor {name} of type {sensor_type} with values: {values}")

        # We get the classifier function and reference key for the sensor type from the dict
        classifier_entry = SENSOR_CLASSIFIERS.get(sensor_type)

        # If we don't have a classifier for the sensor type, skip it
        if not classifier_entry:
            logger.warning(f"Unsupported sensor type: {sensor_type} for sensor {name}. Skipping.")
            continue

        # We get the data from the classifier entry we retrieved from the dict
        reference_key, classifier_func_value = classifier_entry
        # We get the reference physical property from the parsed data using the reference key
        # we retrieved from the dict
        reference_key_value = reference[reference_key]

        # We call the obtained classifier function with the values from the parsed data and the
        # reference physical property we obtained in the previous step
        # and store the result in the results dictionary under the current sensor name
        results[name] = classifier_func_value(values, reference_key_value)
        logger.info(f"Sensor {name} classified as: {results[name]}")
    
    return results
