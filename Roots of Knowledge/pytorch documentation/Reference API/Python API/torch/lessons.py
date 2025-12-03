import torch
from pandas.tests.io.test_sql import drop_table

x = torch.tensor([1, 2, 3])
print(torch.is_tensor(x))

print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.complex64)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.complex128)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.int32)))
print(torch.is_complex(torch.tensor([1, 2, 3], dtype=torch.float16)))


"""
1. البداية — «User Guide» (أساسيات + مفاهيم)

ابدأ من هنا لو أنت بتتعلم PyTorch لأول مرة أو عايز ترضِّي صورة شاملة:

Pytorch Overview — نظرة عامة على PyTorch، فلسفته، إمكانياته. 
docs.pytorch.org
+1

Get Started — الخطوات الأساسية لتثبيت PyTorch، إعداد الجهاز (CPU / GPU)، أول كود بسيط. 
docs.pytorch.org
+1

Learn the Basics — مفاهيم أساسية: Tensors، العمليات الأساسية، autograd إن لزم، كيفية بناء برنامج بسيط. 
docs.pytorch.org
+1

PyTorch Main Components — أهم مكوّنات PyTorch (مثل tensor operations, nn, optim, modules …). 
docs.pytorch.org
+1

الهدف من المرحلة دي: تفهم “إيه PyTorch” و “إزاي تشتغل بيه” من غير غوص مفاجئ في التفاصيل.

2. شوف Tutorials — تطبيقات + أمثلة عملية

بعد ما تكون فهمت الأساسيات بشكل نظري من User Guide، انزل على قسم Tutorials. هناك هتلاقي: 
docs.pytorch.org
+1

tutorials للمبتدئين (getting started, loading data, building simple nets…) 
docs.pytorch.org
+1

مشاريع تطبيقية: تدريب شبكة، تصنيف صور/نصوص، استخدام DataLoader, تدريب عملي …

“Recipes” و “Examples” جاهزة: كود قصير عملي لحاجات شائعة (data loading, augmentation, training loop …). 
docs.pytorch.org
+1

الهدف: تحوّل الفهم النظري إلى كود عملي — لما تشوف مثال شغال وتعبّيه بإيدك تفهم PyTorch أحسن.

3. تعمّق في API — «Reference API»

بعد ما تكون اشتغلت شوية بTutorials وفهمت البروسيجر العام، الوقت تقرأ Reference API عشان تعرف الدوال / الكلاسات المتاحة بالتفصيل. 
docs.pytorch.org
+1

ابدأ بـ torch.Tensor, العمليات على التنسورات، التابع .grad, .backward() … 
docs.pytorch.org

بعده torch.nn, torch.optim, torch.nn.functional — موديولات بناء الشبكات، الطبقات، loss, activation … 
docs.pytorch.org

كمان لو هتستخدم GPU / AMP / autograd / distributed / وغيرها — شوف الأقسام الخاصة. 
docs.pytorch.org

الهدف: تعرف “كل أداة” في مكتبة PyTorch، بمواصفاتها ووسائل استخدامها.

4. مواضيع متقدمة / ملاحظات للمطورين (Advanced / Developer Notes)

لما تكون مرتاح بالأساسيات + API + شغلت شوية مشاريع — خش على:

Developer Notes — تفاصيل تصميم PyTorch، best‑practices، كيف تتعامل مع الأداء، memory, precision … 
docs.pytorch.org
+1

مواضيع متقدمة لو انت ناوي: custom autograd, distributed training, mixed‑precision, TorchScript، إلخ. 
docs.pytorch.org
+2
docs.pytorch.wiki
+2

الهدف: تفهم PyTorch “من جوه”، مش بس استخدام مكتبة، عشان ممكن تبني حاجات أكثر تعقيدًا أو تساهم في مشاريع كبيرة.

🔄 مثال “مسار سريع” — لو هتبدأ من الصفر

افتح User Guide → Get Started → Learn the Basics → Main Components

بعدها شغّل Tutorials — خليك تجرب Minimum working examples

ارجع لـ API Reference و افتح كل جزء مستخدم في Tutorials (تنسورات، nn, optim, autograd)

بمجرد ما تتعود، شوف Developer Notes / Advanced Topics

مع كل خطوة: طبّق كود عملي — مش بس قراءة
"""