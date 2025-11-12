from haystack.components.generators import HuggingFaceLocalGenerator
from haystack.utils import ComponentDevice, Device

device = ComponentDevice.from_single(Device.gpu(0))

device = ComponentDevice.from_str("cuda:1")

generator = HuggingFaceLocalGenerator(model="google/flan-t5-small", device=device)
