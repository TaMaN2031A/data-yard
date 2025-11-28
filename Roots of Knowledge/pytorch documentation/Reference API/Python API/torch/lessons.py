import torch
from pandas.tests.io.test_sql import drop_table

x = torch.tensor([1, 2, 3])
print(torch.is_tensor(x))

print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.complex64)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.complex128)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.int32)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.float16)))
