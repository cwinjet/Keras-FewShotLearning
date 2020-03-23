"""
All these metrics functions assume y_pred is a gram matrix computed on the batch (output of GramMatrix layer for
instance). y_true should be one-hot encoded
"""
import tensorflow as tf


def top_score_classification_accuracy(y_true, y_pred):
    """
    Use the top score of an image against all the samples from the same class to get a score per class for each image.
    """
    y_true = tf.dtypes.cast(y_true, tf.float32)
    y_pred = tf.linalg.set_diag(y_pred, tf.zeros(tf.shape(y_pred)[0]))
    return tf.reduce_sum(
        y_true * tf.linalg.matmul(tf.cast(y_pred == tf.reduce_max(y_pred, axis=1, keepdims=True), tf.float32), y_true)
    ) / tf.cast(tf.shape(y_pred)[0], tf.float32)


def same_image_score(y_pred, _):
    """
    Same image score may not be always one especially when bias is used in the head_model
    """
    return tf.reduce_mean(tf.linalg.diag_part(y_pred))


def accuracy(margin=0.0):
    """
    Compute the relative number of pairs with a score in the margin, ie. #{pairs | |y_true - y_pred| < m}
    """

    def _accuracy(y_true, y_pred):
        y_true = tf.matmul(y_true, y_true, transpose_b=True)
        return tf.reduce_mean(tf.cast(tf.abs(y_true - y_pred) < margin, tf.float32))

    return _accuracy


def min_eigenvalue(_, y_pred):
    """
    Compute the minimum eigenvalue of the y_pred tensor. If this value if non-negative (resp. positive) then the
    similarity or distance learnt is a positive semi-definite (resp. positive definite) kernel.
    See Also [Positive-definite kernel](https://en.wikipedia.org/wiki/Positive-definite_kernel)
    """
    return tf.reduce_min(tf.linalg.svd(y_pred, compute_uv=False))