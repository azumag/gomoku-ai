import tensorflow as tf
import util as u

class Perceptron:
    layer = 0
    weights = []
    neurons = []
    biases  = []
    n_input = 0
    n_output = 0
    x  = None
    y_ = None
    util = None
    sess = None
    train_step = None

    # now input = output is required... TODO; FIXME;
    def __init__(self, layer, n_input, n_output):
        self.util = u.Util()
        self.sess = tf.Session()
        self.layer = layer
        self.n_input = n_input
        self.n_output = n_output
        self.train_step = self.layer_set()

    def train(self, train_file, label_file, batch):
        train_data  = self.util.load_data(train_file)
        train_label = self.util.load_data(label_file)

        self.util.print_start()
        print "--- start train ---"
        # for avoiding problem: huge number of input
        for i in range(len(train_data)):
            batch_range = i+batch
            print 'batch: ' + str(i) + ' - ' + str(batch_range)
            batch_data  = train_data[i: batch_range]
            batch_label = train_label[i: batch_range]
            self.sess.run(self.train_step, feed_dict={self.x: batch_data, self.y_: batch_label})
        print "--- end train ---"
        self.util.print_end()

    def test(self, data_file, label_file):
        test_data  = self.util.load_data(data_file)
        test_label = self.util.load_data(label_file)

        correct_prediction = tf.equal(tf.argmax(self.neurons[-1],1), tf.argmax(self.y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        return (self.sess.run(accuracy, feed_dict={self.x: test_data, self.y_: test_label}))

    def execute(self, input_d):
        return (self.sess.run(tf.argmax(self.neurons[-1], 1), feed_dict={self.x: input_d}))[0]

    def save(self, save_file):
        saver = tf.train.Saver()
        saver.save(sess, save_file)

    def load(self, save_file):
        saver = tf.train.Saver()
        saver.restore(sess, save_file)

    def layer_set(self):
        self.x = tf.placeholder(tf.float32, [None, self.n_input])

        self.weights = [ tf.Variable(tf.zeros([n_input, n_input])) for i in range(self.layer)]
        self.biases  = [ tf.Variable(tf.zeros([n_input])) for i in range(self.layer)]
        self.neurons = [ tf.nn.relu(tf.matmul(self.x, self.weights[0])+self.biases[0]) ]

        for i in range(1, self.layer-1):
            self.neurons.append(
                tf.nn.relu(
                    tf.matmul(
                        self.neurons[i-1], self.weights[i])+self.biases[i] ) )
        self.neurons.append(
            tf.nn.softmax(
                tf.matmul(self.neurons[-1], self.weights[-1]) + self.biases[-1]))

        self.y_ = tf.placeholder(tf.float32, [None, n_output])

        cross_entropy = -tf.reduce_sum(self.y_*tf.log(self.neurons[-1]))
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

        init = tf.initialize_all_variables()
        self.sess.run(init)

        return train_step
