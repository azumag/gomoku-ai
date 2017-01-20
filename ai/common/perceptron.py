import tensorflow as tf
import util as u

class Perceptron:
    data_path = '/home/azumagakito/gomoku-ai/ai/tmp/'
    layer = 3
    weights = []
    neurons = []
    biases  = []
    y_ = None
    util = None
    sess = None

    def __init__(self, layer):
        self.util = u.Util()
        self.sess = tf.Session()
        self.layer = layer

    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def train(self, file_name, batch):
        train_data  = self.util.load_data(self.data_path+'h-'+file_name)
        train_label = self.util.load_data(self.data_path+'a-'+file_name)
        train_step = self.layer_set()

        self.util.print_start()
        print "--- start train ---"
        # for avoiding problem: huge number of input
        for i in range(len(train_data)):
            batch_range = i+batch
            print 'batch: ' + str(i) + ' - ' + str(batch_range)
            batch_data  = train_data[i: batch_range]
            batch_label = train_label[i: batch_range]
            self.sess.run(train_step, feed_dict={x: batch_data, y_: batch_label})
        print "--- end train ---"
        self.util.print_end()

    def test(self, file_name):
        test_data  = self.util.load_data(data_path+'h-'+file_name)
        test_label = self.util.load_data(data_path+'a-'+file_name)

        correct_prediction = tf.equal(tf.argmax(self.neurons[-1],1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print(self.sess.run(accuracy, feed_dict={x: test_data, y_: test_label}))

    def layer_set(self):
        x = tf.placeholder(tf.float32, [None, 81])

        self.weights = [ self.weight_variable(tf.zeros([81, 81])) for i in range(self.layer)]
        self.biases  = [ self.bias_variable(tf.zeros([81, 81])) for i in range(self.layer)]
        self.neurons = [ tf.nn.relu(tf.matmul(x, weights[0])+b[0]) ]
        for i in range(1, self.layer-1):
            self.neurons.append(
                tf.nn.relu(
                    tf.matmul(
                        self.neurons[i-1], self.weights[i])+self.biases[i] ) )
        self.neurons.append(
            tf.nn.softmax(
                tf.matmul(self.neurons[-1], self.weights[-1]) + self.biases[-1]))

        self.y_ = tf.placeholder(tf.float32, [None, 81])

        cross_entropy = -tf.reduce_sum(self.y_*tf.log(self.neurons[-1]))
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

        init = tf.global_variables_initializer()
        sess.run(init)

        return train_step
