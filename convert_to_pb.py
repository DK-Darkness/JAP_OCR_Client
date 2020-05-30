from tensorflow.python.tools import freeze_graph
import tensorflow as tf
def freeze_graph(input_checkpoint, output_graph):
    '''
    :param input_checkpoint:
    :param output_graph: PB模型保存路径
    '''
    # 输出节点名称
    output_node_names = "fc8/fc8" 
    
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)
    graph = tf.get_default_graph()
    input_graph_def = graph.as_graph_def()
    with tf.Session() as sess:
        saver.restore(sess, input_checkpoint)
        
        # fix batch norm nodes
        # 解决value error问题
        for node in input_graph_def.node:
          if node.op == 'RefSwitch':
            node.op = 'Switch'
            for index in range(len(node.input)):
              if 'moving_' in node.input[index]:
                node.input[index] = node.input[index] + '/read'
          elif node.op == 'AssignSub':
            node.op = 'Sub'
            if 'use_locking' in node.attr: del node.attr['use_locking']

        output_graph_def = tf.graph_util.convert_variables_to_constants(  
            sess=sess,
            input_graph_def=input_graph_def,# 等于:sess.graph_def
            output_node_names=output_node_names.split(","))
            
        with tf.gfile.GFile(output_graph, "wb") as f:
            f.write(output_graph_def.SerializeToString()) 
        print("%d ops in the final graph." % len(output_graph_def.node)) 

if __name__ == '__main__':
	input_checkpoint = 'model/model.ckpt-9999'
	output_graph = 'freeze_model.pb'
	freeze_graph(input_checkpoint, output_graph)

