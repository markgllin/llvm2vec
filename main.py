import os 
import logging
import numpy as np
import tensorflow as tf
from tensorboard.plugins import projector

from llvmir.ir_reader import IRReader
from asm2vec.model import Asm2Vec, Asm2VecMemento

logging.basicConfig(level=logging.DEBUG)

DIM = 200

irreader = IRReader()
source_functions_O1 = irreader.process_directory("llvm2vec_dataset/zlib/llvmir/zlib-O1/libz/")
source_functions_O2 = irreader.process_directory("llvm2vec_dataset/zlib/llvmir/zlib-O2/libz/")
source_functions_O3 = irreader.process_directory("llvm2vec_dataset/zlib/llvmir/zlib-O3/libz/")
query_functions_O1 = irreader.process_directory("llvm2vec_dataset/zlib/arm/zlib-O1/libz/")
query_functions_O2 = irreader.process_directory("llvm2vec_dataset/zlib/arm/zlib-O2/libz/")
query_functions_O3 = irreader.process_directory("llvm2vec_dataset/zlib/arm/zlib-O3/libz/")

# train model 
print("Training model...")
model = Asm2Vec(d=DIM)
train_repo = model.make_function_repo(source_functions_O1 + source_functions_O2 + source_functions_O3)
model.train(train_repo)

source_function_vectors = {}
print("Generating source function vectors...")
for function in source_functions_O1:
  source_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O1_" + function._filename, 'role': 'source'}
for function in source_functions_O2:
  source_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O2_" + function._filename, 'role': 'source'}
for function in source_functions_O3:
  source_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O3_" + function._filename, 'role': 'source'}

query_function_vectors = {}
print("Generating query function vectors...")
for function in query_functions_O1:
  query_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O1_" + function._filename, 'role': 'query'}
for function in query_functions_O2:
  query_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O2_" + function._filename, 'role': 'query'}
for function in query_functions_O3:
  query_function_vectors[function._name]={'vector': model.to_vec(function), 'filename':"O3_" + function._filename, 'role': 'query'}

f = open('cosine_sims.txt', 'w')
# cosine similarity:
# 1 = exactly the same
# -1 = exactly opposite
# 0 = orthoganal
for qfunc, value in query_function_vectors.items():
  target_vec = value['vector']
  f.write('=================================\n')
  f.write(qfunc + '\n')
  sims = {}
  for sfunc, value in source_function_vectors.items():
    source_vec = value['vector']
    sim = model.cosine_similarity(source_vec, target_vec)
    sims[sfunc] = sim
  
  sims = dict(sorted(sims.items(), key=lambda item: item[1], reverse=True))
  for key, value in sims.items():
    f.write("\t" + key + ":" + str(value) + '\n')

f.close()

function_vectors = {**source_function_vectors, **query_function_vectors}
max_size = len(function_vectors)
print("Number of functions "+ str(max_size))
func2vec = np.zeros((max_size, DIM*2))

if not os.path.exists('projections'):
  os.makedirs('projections')

with open("projections/metadata.tsv", 'w+') as file_metadata:
  file_metadata.write('Function\tFilename\trole\n')
  for i, (key, metadata) in enumerate(function_vectors.items()):
    func2vec[i] = metadata['vector']
    file_metadata.write( key + '\t' + metadata['filename'] + '\t' + metadata['role'] + '\n')

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