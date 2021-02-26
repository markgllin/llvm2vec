import click
import numpy as np
import tensorflow as tf
import os 
from tensorboard.plugins import projector

from llvmir.ir_reader import IRReader
from asm2vec.model import Asm2Vec, Asm2VecMemento

DIM = 200

def cosine_similarity(v1, v2):
    return (v1 @ v2 / (v1.norm() * v2.norm())).item()


@click.command()
@click.option('-f1', '--file1', 'f1', help='target bin 1', required=True)
@click.option('-f2', '--file2', 'f2', help='target bin 2', required=True)
@click.option('-m', '--model', 'mpath', help='model path', required=True)
def cli(f1, f2, mpath):
  print('HELLO')
  print(mpath)
  memento = Asm2VecMemento()
  memento.load_from_disk(mpath)
  model = Asm2Vec(d=200)
  model.set_memento(memento)

  irreader = IRReader()
  print(f1)
  f1 = irreader.parse_bc_file(f1, "f1")
  f2 = irreader.parse_bc_file(f2, "f2")

  print("Generating f1 vectors...")
  f1_vectors = {}
  for function,value in f1.items():
    f1_vectors[function + "_source"]={'vector': model.to_vec(value['asm_function']), 'filename':value['filename'], 'role': 'f1'}

  print("Generating f2 vectors...")
  f2_vectors = {}
  for function,value in f2.items():
    f2_vectors[function + "_query"]={'vector': model.to_vec(value['asm_function']), 'filename':value['filename'], 'role': 'f2'}

  for qfunc, value in f2.items():
    target_vec = value['vector']
    print('=================================\n')
    print(qfunc + '\n')
    sims = {}
    for sfunc, value in f1.items():
      source_vec = value['vector']
      sim = cosine_similarity(source_vec, target_vec)
      sims[sfunc] = sim
    
    sims = dict(sorted(sims.items(), key=lambda item: item[1], reverse=True))
    for key, value in sims.items():
      print("\t" + key + ":" + str(value) + '\n')

  function_vectors = {**f1_vectors, **f2_vectors}
  max_size = len(function_vectors)
  print("Number of functions "+ str(max_size))
  func2vec = np.zeros((max_size, DIM*2))

  if not os.path.exists('compare_projections'):
    os.makedirs('compare_projections')

  with open("compare_projections/metadata.tsv", 'w+') as file_metadata:
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
  writer = tf.compat.v1.summary.FileWriter('compare_projections', sess.graph)
  config = projector.ProjectorConfig()
  embed = config.embeddings.add()
  embed.tensor_name = 'embedding'
  embed.metadata_path = 'metadata.tsv'
  projector.visualize_embeddings(writer, config)
  saver.save(sess, 'compare_projections/model.ckpt', global_step=max_size)