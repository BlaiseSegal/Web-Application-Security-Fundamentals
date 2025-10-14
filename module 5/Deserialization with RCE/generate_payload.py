import pickle
import base64

object = {"message": "test"}

benign_serialized_object = pickle.dumps(object)
benign_payload = base64.b64encode(benign_serialized_object)

print("payload de test :")
print(benign_payload.decode('utf-8'))

# payload de test : gASVFQAAAAAAAAB9lIwHbWVzc2FnZZSMBHRlc3SUcy4=





command_to_execute = "cat /etc/passwd"
dangerous_serialized_object = pickle.dumps(command_to_execute)

dangerous_payload = base64.b64encode(dangerous_serialized_object)

print("payload malveillant :")
print(dangerous_payload.decode('utf-8'))

# payload malveillant : gASVEwAAAAAAAACMD2NhdCAvZXRjL3Bhc3N3ZJQu