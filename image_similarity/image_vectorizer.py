import glob
import struct
import os
import numpy as np
import tensorflow as tf
from image_similarity.vectorizers import VGG16Vectorizer, MobileNetVectorizer, ResNetVectorizer, InceptionNetVectorizer


class ImageVectorizer(object):

    def __init__(self, model="VGG16"):

        self.model_type = model

        if model == "VGG16":
            self.vectorizer = VGG16Vectorizer()
        elif model == "MobileNet":
            self.vectorizer = MobileNetVectorizer()
        elif model == "ResNet":
            self.vectorizer = ResNetVectorizer()
        elif model == "InceptionNet":
            self.vectorizer = InceptionNetVectorizer()
        else:
            raise ValueError("model {} not recognized".format(model))

    def generate_vectors_cache_from_images(self, images_path, output_name, image_extension="jpeg", output_dir=None):

        dataset, image_paths = self._load_images_bulk(images_path=images_path, image_extension=image_extension)

        if output_dir:
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)
            output_path = os.path.join(output_dir,output_name)
        else:
            output_path = output_name
        self._write_vectors_to_file(dataset, image_paths, path=output_path)

    def test_generate_vectors(self, images_path, image_extension="jpeg"):

        dataset, image_paths = self._load_images_bulk(images_path=images_path, image_extension=image_extension)
        for i, batch in enumerate(dataset):

            if i == 0:
                fvecs = self.vectorizer.vectorize(batch)
            else:
                break

        return fvecs

    def _preprocess(self, img_path):

        img = tf.io.read_file(img_path)
        img = tf.image.decode_jpeg(img, channels=self.vectorizer.input_shape[2])
        img = tf.image.resize(img, self.vectorizer.input_shape[:2])
        img = self.vectorizer.preprocess(img)

        return img

    def _load_images_bulk(self, images_path, image_extension="jpeg", batch_size=100):

        image_paths = glob.glob("{}/*.{}".format(images_path, image_extension), recursive=True)
        dataset = tf.data.Dataset.from_tensor_slices(image_paths)
        ds = dataset.map(lambda x: self._preprocess(x), num_parallel_calls=-1)
        dataset = ds.batch(batch_size).prefetch(-1)

        return dataset, image_paths

    def _write_vectors_to_file(self, dataset, fnames, path="image_vectors_cache"):

        with open("{}.bin".format(path), "wb") as f:
            for i, batch in enumerate(dataset):
                # Report progress
                print("Batch #{}".format(i))
                fvecs = self.vectorizer.vectorize(batch)
                fvecs = np.divide(fvecs.T, np.linalg.norm(fvecs, axis=-1)).T
                fmt = f'{np.prod(fvecs.shape)}f'
                f.write(struct.pack(fmt, *(fvecs.flatten())))

        with open("{}.fnames.txt".format(path), "w") as metadata_file:
            metadata_file.write("\n".join(fnames))
