
from assembly.binary import Binary
from llvmir.llvm2vec import LLVM2Vec

f = open("llvm_binary_example/hello.bc", "rb")
data=f.read()
f.close()

llvm_binary = Binary(data)

print(llvm_binary.functions[0].generate_execution_traces())
un_id = llvm_binary.instr_vectors['un_id'].neuIn
label = llvm_binary.instr_vectors['label'].neuIn

concatted_word_vecs = LLVM2Vec.concat_vectors([un_id, label])
func_vec = llvm_binary.functions[0].vector.neuIn
print(LLVM2Vec.average_vectors([concatted_word_vecs, func_vec]))
# print(llvm_binary.functions[0].vector.neuIn)
