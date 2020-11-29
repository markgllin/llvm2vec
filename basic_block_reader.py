
from assembly.binary import Binary

# llvm.initialize()
# llvm.initialize_native_target()
# llvm.initialize_native_asmprinter()

f = open("llvm_binary_example/hello.bc", "rb")
data=f.read()
f.close()

llvm_binary = Binary(data)
