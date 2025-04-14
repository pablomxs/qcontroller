from app.qlogic.sensors._registry import SENSOR_CLASSIFIERS
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Getting the current supported sensors from the registry
SUPPORTED_SENSOR_TYPES = SENSOR_CLASSIFIERS.keys()


# Function to check if a given string is a timestamp
def is_timestamp(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M")
        return True
    except ValueError:
        return False
    

def parse_log(content: str) -> dict:
    """
    Parses the log content and returns a dictionary with the information.
    """
    logger.info("Parsing log content...")
    lines = content.strip().splitlines()

    # Check if the log file is empty
    if not lines:
        logger.error("Log file is empty")
        raise ValueError("Log file is empty")

    parsed_data = {
        "reference": {},
        "sensors": {}
    }
    current_sensor = None

    try:
        for i, line in enumerate(lines):
            line_parts = line.strip().split()

            # We get the first line with the reference values
            if i == 0 and line_parts[0] == "reference":
                parsed_data["reference"] = {
                    "temperature": float(line_parts[1]),
                    "humidity": float(line_parts[2])
                }
                logger.info(f"Reference values found: {parsed_data['reference']}")
                continue
            
            # We get lines with sensor type and name
            if len(line_parts) == 2 and line_parts[0] in SUPPORTED_SENSOR_TYPES:
                sensor_type = line_parts[0]
                sensor_name = line_parts[1]
                current_sensor = sensor_name
                parsed_data["sensors"][sensor_name] = {
                    "type": sensor_type,
                    "values": []
                }
                logger.info(f"Sensor data found: {line_parts}")
            
            # We get lines with timestamp and value
            elif len(line_parts) == 2 and current_sensor and is_timestamp(line_parts[0]):
                try:
                    value = float(line_parts[1])
                    parsed_data["sensors"][current_sensor]["values"].append(value)
                    logger.info(f"Found value for sensor {current_sensor}: {value}")
                except ValueError:
                    # If conversion to float fails, we log a warning and skip the value
                    logger.warning(f"Invalid value for {current_sensor}: {line_parts[1]}")
                    continue
            
            # At this point, we have a line with two parts but first part is not a timestamp
            # so we assume it's an invalid line or an unknown sensor type
            elif len(line_parts) == 2 and not is_timestamp(line_parts[0]):
                logger.warning(f"Unknown sensor type or invalid line: {' '.join(line_parts)}")
                current_sensor = None

    except Exception as e:
        logger.error(f"Unexpected error while parsing log: {str(e)}")
        raise ValueError("Invalid log format")
    
    # We throw an error if the reference data is missing as we can't proceed without it
    if not {"temperature", "humidity"}.issubset(parsed_data["reference"]):
        logger.error(f"Reference data is missing")
        raise ValueError("Reference data is missing")

    return parsed_data
