from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, BatchNormalization, Activation, Dropout, MaxPool2D, GlobalAveragePooling2D
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.metrics as metrics


def get_model():
    input_shape = (32, 32, 1)
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
                  loss=losses.BinaryCrossentropy,
                  metrics=metrics.Accuracy)
    print(model.summary())


if __name__ == "__main__":
    get_model()
