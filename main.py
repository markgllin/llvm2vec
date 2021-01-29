import os 
import logging
import numpy as np
import tensorflow as tf
from tensorboard.plugins import projector

from llvmir.ir_reader import IRReader
from asm2vec.model import Asm2Vec, Asm2VecMemento

logging.basicConfig(level=logging.DEBUG)

file = "llvm2vec_dataset/zlib/arm/zlib-O3/libz/adler32.o.bc"

irreader = IRReader()
functions = irreader.parse_bc_file(file)

# train model 
print("Training model...")
model = Asm2Vec(d=200)
train_repo = model.make_function_repo(functions)
model.train(train_repo)

function_vectors = []
print("Generating function vectors...")
for function in functions:
  function_vectors.append(model.to_vec(function))


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


# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
# import seaborn as sns
# 
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


