import tensorflow as tf


class Net(tf.keras.Model):
    def __init__(self):
        super(Net, self).__init__()
        self.a1 = tf.keras.layers.Conv2D(filters=16,
                                         kernel_size=3,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.a2 = tf.keras.layers.Conv2D(filters=16,
                                         kernel_size=3,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.a_out = tf.keras.layers.Conv2D(filters=32,
                                            kernel_size=3,
                                            padding='same',
                                            strides=2,
                                            activation='relu',
                                            data_format='channels_last')

        self.b1 = tf.keras.layers.Conv2D(filters=32,
                                         kernel_size=3,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.b2 = tf.keras.layers.Conv2D(filters=32,
                                         kernel_size=3,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.b_out = tf.keras.layers.Conv2D(filters=64,
                                            kernel_size=3,
                                            padding='same',
                                            strides=2,
                                            activation='relu',
                                            data_format='channels_last')

        self.c1 = tf.keras.layers.Conv2D(filters=64,
                                         kernel_size=2,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.c2 = tf.keras.layers.Conv2D(filters=64,
                                         kernel_size=2,
                                         padding='same',
                                         activation='relu',
                                         data_format='channels_last')
        self.c_out = tf.keras.layers.Conv2D(filters=128,
                                            kernel_size=2,
                                            padding='same',
                                            strides=2,
                                            activation='relu',
                                            data_format='channels_last')

        self.d = tf.keras.layers.Conv2D(filters=128,
                                        kernel_size=1,
                                        padding='same',
                                        activation='relu',
                                        data_format='channels_last')

        self.drop = tf.keras.layers.Dropout(0.2)

        self.flatten = tf.keras.layers.Flatten()
        self.out = tf.keras.layers.Dense(1, activation='tanh')

    def call(self, inp):
        x = self.a1(inp)
        x = self.a2(x)
        x = self.a_out(x)

        x = self.b1(x)
        x = self.b2(x)
        x = self.b_out(x)

        x = self.c1(x)
        x = self.c2(x)
        x = self.c_out(x)

        x = self.d(x)

        x = self.drop(x)
        x = self.flatten(x)
        return self.out(x)
