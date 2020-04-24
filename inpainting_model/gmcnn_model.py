from tensorflow.keras.applications.vgg19 import VGG19
import tensorflow as tf
from tensorflow.keras import layers
from config import *
from functools import partial


def vgg19_pretrained_model():
    model = VGG19()
    print(model.summary())


class GMCNN(tf.keras.Model):
    def __init__(self):
        super(GMCNN, self).__init__()

    def call(self, inputs, training=True):
        # Branch 1
        conv7 = partial(layers.Conv2D, kernel_size=7, activation=tf.nn.elu, padding='SAME')
        x = conv7(filters=cnum, strides=1)(inputs)
        x = conv7(filters=2 * cnum, strides=2)(x)
        x = conv7(filters=2 * cnum, strides=1)(x)
        x = conv7(filters=4 * cnum, strides=2)(x)
        x = conv7(filters=4 * cnum, strides=1)(x)
        x = conv7(filters=4 * cnum, strides=1)(x)
        x = conv7(filters=4 * cnum, strides=1, dilation_rate=2)(x)
        x = conv7(filters=4 * cnum, strides=1, dilation_rate=4)(x)
        x = conv7(filters=4 * cnum, strides=1, dilation_rate=8)(x)
        x = conv7(filters=4 * cnum, strides=1, dilation_rate=16)(x)
        x = conv7(filters=4 * cnum, strides=1)(x)
        x = conv7(filters=4 * cnum, strides=1)(x)
        x_b1 = tf.image.resize(x, (image_height, image_width))  # By default it's bilinear interpolation

        # Branch 2
        conv5 = partial(layers.Conv2D, kernel_size=5, activation=tf.nn.elu, padding='SAME')
        x = conv5(filters=cnum, strides=1)(inputs)
        x = conv5(filters=2 * cnum, strides=2)(x)
        x = conv5(filters=2 * cnum, strides=1)(x)
        x = conv5(filters=4 * cnum, strides=2)(x)
        x = conv5(filters=4 * cnum, strides=1)(x)
        x = conv5(filters=4 * cnum, strides=1)(x)
        x = conv5(filters=4 * cnum, strides=1, dilation_rate=2)(x)
        x = conv5(filters=4 * cnum, strides=1, dilation_rate=4)(x)
        x = conv5(filters=4 * cnum, strides=1, dilation_rate=8)(x)
        x = conv5(filters=4 * cnum, strides=1, dilation_rate=16)(x)
        x = conv5(filters=4 * cnum, strides=1)(x)
        x = conv5(filters=2 * cnum, strides=1)(x)
        x = conv5(filters=2 * cnum, strides=1)(x)
        x_b2 = tf.image.resize(x, (image_height, image_width))  # By default it's bilinear interpolation

        # Branch 3
        conv3 = partial(layers.Conv2D, kernel_size=3, activation=tf.nn.elu, padding='SAME')
        x = conv3(filters=cnum, strides=1)(inputs)
        x = conv3(filters=2 * cnum, strides=2)(x)
        x = conv3(filters=2 * cnum, strides=1)(x)
        x = conv3(filters=4 * cnum, strides=2)(x)
        x = conv3(filters=4 * cnum, strides=1)(x)
        x = conv3(filters=4 * cnum, strides=1)(x)
        x = conv3(filters=4 * cnum, strides=1, dilation_rate=2)(x)
        x = conv3(filters=4 * cnum, strides=1, dilation_rate=4)(x)
        x = conv3(filters=4 * cnum, strides=1, dilation_rate=8)(x)
        x = conv3(filters=4 * cnum, strides=1, dilation_rate=16)(x)
        x = conv3(filters=4 * cnum, strides=1)(x)
        x = conv3(filters=2 * cnum, strides=1)(x)
        x = conv3(filters=2 * cnum, strides=1)(x)
        x_b3 = tf.image.resize(x, (image_height, image_width), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

        x_merge = tf.concat([x_b1, x_b2, x_b3], axis=3)
        x = conv3(filters=cnum // 2, strides=1)(x_merge)
        x = layers.Conv2D(inputs=x, kernel_size=3, filters=3, strides=1, activation=None, padding='SAME')(x)
        x = tf.clip_by_value(x, -1., 1.)
        return x


if __name__ == "__main__":
    gmcnn_model = GMCNN()
    gmcnn_model(inputs=)
