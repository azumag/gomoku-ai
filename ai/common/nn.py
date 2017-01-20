class NN:
    data_path = '/home/azumagakito/gomoku-ai/ai/tmp/'
    batch = 1000
    test_ratio = 0.1
    util = None

    def __init__(self):
        util = Util()

    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def train(file_name):
        train_data  = util.load_data(data_path+'h-'+file_name)
        train_label = util.load_data(data_path+'a-'+file_name)

    def layer_set:
        x = tf.placeholder(tf.float32, [None, 81])
        # 重み
W = tf.Variable(tf.zeros([81, 81]))
W2 = tf.Variable(tf.zeros([81, 81]))
W3 = tf.Variable(tf.zeros([81, 81]))
# バイアス
b = tf.Variable(tf.zeros([81]))
b2 = tf.Variable(tf.zeros([81]))
b3 = tf.Variable(tf.zeros([81]))

# ソフトマックス回帰を実行
# yは入力x of 確率の分布
# matmul関数で行列xとWの掛け算を行った後、bを加算する。
# yは[1, 81]の行列
y = tf.nn.relu(tf.matmul(x, W) + b)
y2 = tf.nn.relu(tf.matmul(y, W2) + b2)
y3 = tf.nn.softmax(tf.matmul(y2, W3) + b3)

# 交差エントロピー
# y_は正解データのラベル
y_ = tf.placeholder(tf.float32, [None, 81])
cross_entropy = -tf.reduce_sum(y_*tf.log(y3))

# 勾配法を用い交差エントロピーが最小となるようyを最適化する
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# 用意した変数Veriableの初期化を実行する
init = tf.global_variables_initializer()

# Sessionを開始する
# runすることで初めて実行開始される（run(init)しないとinitが実行されない）

sess = tf.Session()
sess.run(init)

# train_stepを実行する
# feed_dictでplaceholderに値を入力することができる
print "--- 訓練開始 ---"
for i in range(len(hst_data)):
    print 'batch: ' + str(i)
    train_data  = hst_data[i: i+1*batch]
    train_label = ans_data[i: i+1*batch]
    sess.run(train_step, feed_dict={x: train_data, y_: train_label})
print "--- 訓練終了 ---"

# 正しいかの予測
