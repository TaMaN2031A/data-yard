from haystack.components.generators import HuggingFaceLocalGenerator
from haystack.utils import ComponentDevice, Device

device = ComponentDevice.from_single(Device.gpu(id=1))
# Alternatively, use a PyTorch device string
device = ComponentDevice.from_str("cuda:1")
generator = HuggingFaceLocalGenerator(model="meta-llama/Llama-2-7b-hf", device=device)