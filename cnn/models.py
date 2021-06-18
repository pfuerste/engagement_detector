from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Reshape, Conv2D, BatchNormalization, Activation, Dropout, MaxPool2D, GlobalAveragePooling2D
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.metrics as metrics
from tensorflow.keras import Model
import tensorflow as tf
import keras


def get_model(input_shape=(32, 32, 3)):
    """Returns a compiled model.

    Args:
        input_shape (tuple, optional): input shape of single images. Defaults to (32, 32, 3).

    Returns:
        tf.keras.models.Sequential: compiled model
    """
    model = Sequential()

    model.add(Conv2D(
        filters=192,
        kernel_size=(3, 3),
        padding="same",
        input_shape=input_shape,
    ))
    model.add(BatchNormalization())
    model.add(Activation("relu"))
    model.add(Conv2D(
        filters=192,
        kernel_size=(1, 1),
        padding="same",
    ))
    model.add(Activation("relu"))

    model.add(Conv2D(
        filters=192,
        kernel_size=(3, 3),
        padding="same",
        strides=2,
    ))
    model.add(BatchNormalization())
    model.add(Activation("relu"))
    model.add(Dropout(0.5))

    model.add(Conv2D(
        filters=96,
        kernel_size=(3, 3),
        padding="same",
    ))
    model.add(BatchNormalization())
    model.add(Activation("relu"))
    model.add(Conv2D(
        filters=96,
        kernel_size=(1, 1),
    ))
    model.add(Activation("relu"))
    model.add(Conv2D(
        filters=96,
        kernel_size=(1, 1),
    ))
    model.add(Activation("relu"))

    model.add(MaxPool2D(
              pool_size=3,
              strides=2
              ))
    model.add(Dropout(0.5))

    model.add(Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    ))
    model.add(Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    ))
    model.add(Conv2D(
        filters=32,
        kernel_size=(3, 3),
    ))

    model.add(Conv2D(
        filters=4,
        kernel_size=(1, 1),
    ))
    model.add(GlobalAveragePooling2D())

    model.add(Dense(
        units=4,
        activation="softmax"))
    optimizer = optimizers.Adam()

    model.compile(optimizer=optimizer,
                  loss=losses.MeanSquaredError(),
                  metrics=[metrics.MeanSquaredError()])
    loss = losses.SparseCategoricalCrossentropy()
    #loss = losses.MeanSquaredError()
    model.compile(optimizer=optimizer,
                  loss=loss, metrics=[metrics.sparse_categorical_crossentropy])
    print(model.summary())
    return model


def get_func_model(input_shape=(32, 32, 3)):
    """Returns a compiled model.

    Args:
        input_shape (tuple, optional): input shape of single images. Defaults to (32, 32, 3).

    Returns:
        tf.keras.models.Sequential: compiled model
    """
    from tensorflow.python.framework.ops import disable_eager_execution
    disable_eager_execution()
    # tf.compat.v1.experimental.output_all_intermediates(True)

    inp = tf.keras.Input(shape=input_shape)
    x = Conv2D(filters=192,
               kernel_size=(3, 3),
               padding="same",
               input_shape=input_shape,
               )(inp)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=192,
               kernel_size=(1, 1),
               padding="same",
               )(x)
    x = Activation("relu")(x)

    x = Conv2D(
        filters=192,
        kernel_size=(3, 3),
        padding="same",
        strides=2,
    )(x)
    x = (BatchNormalization())(x)
    x = (Activation("relu"))(x)
    x = (Dropout(0.5))(x)

    x = Conv2D(
        filters=96,
        kernel_size=(3, 3),
        padding="same",
    )(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Conv2D(
        filters=96,
        kernel_size=(1, 1),
    )(x)
    x = Activation("relu")(x)
    x = Conv2D(
        filters=96,
        kernel_size=(1, 1),
    )(x)
    x = Activation("relu")(x)

    x = MaxPool2D(
        pool_size=3,
        strides=2
    )(x)
    x = Dropout(0.5)(x)

    # Boredom Branch
    b0 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(x)
    b1 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(b0)
    b2 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
    )(b1)
    b3 = Conv2D(
        filters=4,
        kernel_size=(1, 1),
    )(b2)
    b4 = GlobalAveragePooling2D()(b3)
    b5 = Dense(
        units=4,
        activation="softmax",
        name="Boredom")(b4)

    # Engagement Branch
    e0 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(x)
    e1 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(e0)
    e2 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
    )(e1)
    e3 = Conv2D(
        filters=4,
        kernel_size=(1, 1),
    )(e2)
    e4 = GlobalAveragePooling2D()(e3)
    e5 = Dense(
        units=4,
        activation="softmax",
        name="Engagement")(e4)

    # Confusion Branch
    c0 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(x)
    c1 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(c0)
    c2 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
    )(c1)
    c3 = Conv2D(
        filters=4,
        kernel_size=(1, 1),
    )(c2)
    c4 = GlobalAveragePooling2D()(c3)
    c5 = Dense(
        units=4,
        activation="softmax",
        name="Confusion")(c4)

    # Frustration Branch
    f0 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(x)
    f1 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding="same",
    )(f0)
    f2 = Conv2D(
        filters=32,
        kernel_size=(3, 3),
    )(f1)
    f3 = Conv2D(
        filters=4,
        kernel_size=(1, 1),
    )(f2)
    f4 = GlobalAveragePooling2D()(f3)
    f5 = Dense(
        units=4,
        activation="softmax",
        name="Frustration")(f4)

    optimizer = optimizers.Adam()
    model = Model(inputs=inp, outputs=[b5, e5, c5, f5])

    # loss = losses.SparseCategoricalCrossentropy()
    model.compile(optimizer=optimizer,
                  loss={"Boredom": 'sparse_categorical_crossentropy',
                        "Engagement": 'sparse_categorical_crossentropy',
                        #"Engagement2": 'sparse_categorical_crossentropy',

                        "Frustration": 'sparse_categorical_crossentropy',
                        "Confusion": 'sparse_categorical_crossentropy'},
                  metrics=['sparse_categorical_crossentropy', 'accuracy'])
    print(model.summary())
    return model


if __name__ == "__main__":
    # get_model()
    get_func_model()
