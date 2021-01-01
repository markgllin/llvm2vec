from llvmir.function_cfg import FunctionCFG
from asm2vec.asm import Function
from asm2vec.model import Asm2Vec, Asm2VecMemento
import llvmlite.binding as llvm
import logging

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

import pprint
import pdb

pp = pprint.PrettyPrinter(indent=4)
# import pdb
# pdb.set_trace()

logging.basicConfig(level=logging.DEBUG)

f = open("llvm_binary_example/busybox-O0.bc", "rb")
data=f.read()
f.close()

moduleref= llvm.parse_bitcode(data)

functions = []
for raw_func in moduleref.functions:
  cfg_func = FunctionCFG(raw_func)
  
  if cfg_func.blocks:
    functions.append(Function(cfg_func.root(), cfg_func.id))

# train model 
print("Training model...")
model = Asm2Vec(d=3)
train_repo = model.make_function_repo(functions)
model.train(train_repo)

# and save memento to disk
print("Saving memento to disk...")
serialized = model.memento().save_to_disk()
# model.save_function_repo_to_disk()

# load memento from disk and recreate model with memento
memento = Asm2VecMemento()
memento.load_from_disk()
model2 = Asm2Vec(d=200)
model2.set_memento(memento)
# fuc_repo = model2.load_function_repo_from_disk()


function_vectors = []
print("Generating function vectors...")
for function in functions:
  function_vectors.append(model2.to_vec(function))

# func1 = function_vectors[0]
# func2 = function_vectors[1]
# distance = model2.cosine_distance(func1, func2)
# similarity = model2.cosine_similarity(func1, func2)
# print(distance)
# print(similarity)
# exit()


print("Generating TSNE plot...")
tsne = TSNE(n_components=3, random_state=0)
function_vectors_2d = tsne.fit_transform(function_vectors)
print(function_vectors_2d)
# pdb.set_trace()
df_subset = {}
df_subset['tsne-2d-one'] = function_vectors_2d[:,0]
df_subset['tsne-2d-two'] = function_vectors_2d[:,1]
print(df_subset)
plt.figure(figsize=(16,10))
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    # hue="y",
    palette=sns.color_palette("hls", 10),
    data=df_subset,
    legend="full",
    alpha=0.3
)
plt.savefig('foo2.png')


