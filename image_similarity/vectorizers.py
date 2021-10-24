import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as preprocess_for_mobilenet
from tensorflow.keras.applications.resnet_v2 import preprocess_input as preprocess_for_resnet
from tensorflow.keras.applications.vgg16 import preprocess_input as preprocess_for_vgg16
from tensorflow.keras.models import Model


class VGG16Vectorizer(object):

    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.output_vector_dim = 4096
        base_model = tf. \
            keras. \
            applications. \
            vgg16. \
            VGG16(include_top=True, weights="imagenet")
        base_model.trainable = False
        self.model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

    def preprocess(self, input_dataset):
        return preprocess_for_vgg16(input_dataset)

    def vectorize(self, input_dataset):
        return self.model.predict(input_dataset)


class ResNetVectorizer(object):

    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.output_vector_dim = 2048
        base_model = tf. \
            keras. \
            applications. \
            ResNet50V2(include_top=True, weights="imagenet")
        base_model.trainable = False
        self.model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

    def preprocess(self, input_dataset):
        return preprocess_for_resnet(input_dataset)

    def vectorize(self, input_dataset):
        return self.model.predict(input_dataset)


class InceptionNetVectorizer(object):

    def __init__(self):
        self.input_shape = (299, 299, 3)
        self.output_vector_dim = 2048
        base_model = tf. \
            keras. \
            applications. \
            InceptionV3(include_top=True, weights="imagenet", classifier_activation=None)
        base_model.trainable = False
        self.model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

    def preprocess(self, input_dataset):
        return preprocess_for_resnet(input_dataset)

    def vectorize(self, input_dataset):
        return self.model.predict(input_dataset)


class MobileNetVectorizer(object):

    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.output_vector_dim = 1028
        base_model = tf. \
            keras. \
            applications. \
            MobileNetV2(input_shape=self.input_shape, include_top=False, weights="imagenet")

        base_model.trainable = False
        self.model = Model(inputs=base_model.input, outputs=layers.GlobalAveragePooling2D()(base_model.output))

    def preprocess(self, input_dataset):
        return preprocess_for_mobilenet(input_dataset)

    def vectorize(self, input_dataset):
        return self.model.predict(input_dataset)
