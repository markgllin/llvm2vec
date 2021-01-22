from llvmir.function_cfg import FunctionCFG
from asm2vec.asm import Function
from asm2vec.model import Asm2Vec, Asm2VecMemento
import llvmlite.binding as llvm
import os 
import logging

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

import pprint
import pdb

import numpy as np
import tensorflow as tf

from tensorboard.plugins import projector

pp = pprint.PrettyPrinter(indent=4)
# import pdb
# pdb.set_trace()

logging.basicConfig(level=logging.DEBUG)

f = open("llvm2vec_dataset/zlib/arm/zlib-O3/libz/adler32.o.bc", "rb")
data=f.read()
f.close()

print("Parsing bitcode...")
moduleref= llvm.parse_bitcode(data)

functions = []
for raw_func in moduleref.functions:
  cfg_func = FunctionCFG(raw_func)
  
  if cfg_func.blocks:
    functions.append(Function(cfg_func.root(), cfg_func.id))

# train model 
print("Training model...")
model = Asm2Vec(d=200)
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


max_size = len(function_vectors)
print("Number of functions "+ str(max_size))
func2vec = np.zeros((max_size, function_vectors[0].size))
print(function_vectors)
print(func2vec)

if not os.path.exists('projections'):
  os.makedirs('projections')

with open("projections/metadata.tsv", 'w+') as file_metadata:
  for i, word in enumerate(function_vectors[:max_size]):
    func2vec[i] = function_vectors[i]
    file_metadata.write(str(i) + '\n')

tf.compat.v1.disable_eager_execution()
sess=tf.compat.v1.InteractiveSession()
with tf.device("/cpu:0"):
  embedding = tf.Variable(func2vec, trainable=False, name='embedding')

sess.run(tf.compat.v1.global_variables_initializer())
saver = tf.compat.v1.train.Saver()
writer = tf.compat.v1.summary.FileWriter('projections', sess.graph)
config = projector.ProjectorConfig()
embed = config.embeddings.add()
embed.tensor_name = 'embedding'
embed.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(writer, config)
saver.save(sess, 'projections/model.ckpt', global_step=max_size)

# print("Generating TSNE plot...")
# tsne = TSNE(n_components=3, random_state=0)
# function_vectors_2d = tsne.fit_transform(function_vectors)
# print(function_vectors_2d)

# df_subset = {}
# df_subset['tsne-2d-one'] = function_vectors_2d[:,0]
# df_subset['tsne-2d-two'] = function_vectors_2d[:,1]
# print(df_subset)
# plt.figure(figsize=(16,10))
# sns.scatterplot(
#     x="tsne-2d-one", y="tsne-2d-two",
#     # hue="y",
#     palette=sns.color_palette("hls", 10),
#     data=df_subset,
#     legend="full",
#     alpha=0.3
# )
# plt.savefig('zlib-arm-retdec-03.png')


