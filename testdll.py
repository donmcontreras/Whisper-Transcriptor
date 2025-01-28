import torch
print(torch.cuda.is_available())  # Esto debe devolver True si tienes CUDA disponible
print(torch.cuda.current_device())  # Esto te dirá qué GPU está activa
print(torch.cuda.get_device_name(0))  # Para obtener el nombre de la GPU 2
