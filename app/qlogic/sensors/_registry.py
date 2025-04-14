from app.qlogic.sensors.thermometer import classify_thermometer
from app.qlogic.sensors.humidistat import classify_humidistat

# This dictionary maps the supported sensor types to their respective classification functions.
# The key is the sensor type (thermometer, humidistat, etc.), and the value is a tuple containing the
# reference physical property (temperature, humidity, etc.) and the classification function.
# Classification functions are stored in separate files in the /qlogic/sensors folder for organization purposes.
#
# If we need to add a new sensor type, we can simply add a new entry to this dictionary,
# along with the corresponding classification function (rules) in the sensors folder.

SENSOR_CLASSIFIERS = {
    "thermometer": ("temperature", classify_thermometer),
    "humidistat": ("humidity", classify_humidistat)
}
