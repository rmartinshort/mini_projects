
import numpy as np
import tensorflow as tf
import pandas as pd
import nmslib
import os

from image_similarity.image_vectorizer import ImageVectorizer


class ImageMatcher(object):

    def __init__(self, vectorizer=None, matcher=None, matching_names=None):

        self.vectorizer = vectorizer
        self.matching_list = matching_names
        self.matcher = matcher

    @classmethod
    def build_matcher_and_vectorizer(cls, images_location, model_type="ResNet", output_name="vectors", output_dir=None):

        vectorizer = ImageVectorizer(model=model_type)

        vectorizer.generate_vectors_cache_from_images(
            images_path=images_location,
            output_name="{}_{}_v0.0.1".format(output_name, model_type.lower()),
            image_extension="jpeg",
            output_dir=output_dir
        )

        if output_dir:

            names_path = os.path.join(output_dir, "{}_{}_v0.0.1.fnames.txt".format(output_name, model_type.lower()))
            vecs_path = os.path.join(output_dir, "{}_{}_v0.0.1.bin".format(output_name, model_type.lower()))

        else:
            names_path = "{}_{}_v0.0.1.fnames.txt".format(output_name, model_type.lower())
            vecs_path = "{}_{}_v0.0.1.bin".format(output_name, model_type.lower())

        my_matcher = cls(vectorizer=vectorizer)
        my_matcher.matching_list = my_matcher._get_files_list(names_path)
        my_matcher.matcher = my_matcher._generate_matcher_from_vecs(vecs_path)

        return my_matcher

    @classmethod
    def build_matcher_from_vectorizer_files(cls, vectorizer, vecs_path, names_path):

        my_matcher = cls(vectorizer=vectorizer)
        my_matcher.matching_list = my_matcher._get_files_list(names_path)
        my_matcher.matcher = my_matcher._generate_matcher_from_vecs(vecs_path)

        return my_matcher

    @staticmethod
    def _get_files_list(file_names_path):

        file_names = pd.read_csv(file_names_path, names=["fname"])["fname"].tolist()
        return file_names

    def _generate_matcher_from_vecs(self, vecs_file_path):

        # check if vecs file path is for the appropriate model
        dim = self.vectorizer.vectorizer.output_vector_dim
        vecs = np.fromfile(vecs_file_path, dtype="float32").reshape(-1, dim)
        nmslib_method = "hnsw"
        nmslib_space = "l2"
        matcher_params = {"M": 30, "indexThreadQty": 4, "efConstruction": 100, "post": 0}
        matcher = nmslib.init(method=nmslib_method, space=nmslib_space)
        matcher.addDataPointBatch(vecs)
        matcher.createIndex(matcher_params, print_progress=True)
        return matcher

    def suggest(self, input_path, n_return=5, block_exact_match=True):

        list_ds = tf.data.Dataset.from_tensor_slices([input_path])
        ds = list_ds.map(lambda x: self.vectorizer._preprocess(x), num_parallel_calls=-1)
        image_vec = ds.batch(1).prefetch(-1)

        vectors_batch = []
        for batch in image_vec:
            fvecs = self.vectorizer.vectorizer.vectorize(batch)
            fvecs = np.divide(fvecs.T, np.linalg.norm(fvecs, axis=-1)).T
            vectors_batch.append(fvecs)

        for vec in vectors_batch:
            ids, distances = self.matcher.knnQuery(vec, k=n_return)

        # Display results of a search
        distances_list = [None] * len(distances)
        results_list = [None] * len(ids)
        original_query_list = [None] * len(ids)
        k = 0
        for i, j in zip(ids, distances):
            distances_list[k] = j
            results_list[k] = self.matching_list[i]
            original_query_list[k] = input_path
            k += 1

        scores_df = pd.DataFrame({"query": original_query_list, "score": distances_list, "match": results_list})
        return self._augument_scores(scores_df, block_exact_match=block_exact_match)

    @staticmethod
    def _augument_scores(scores,block_exact_match=True):

        if block_exact_match:
            # A very tiny score means that the image is exactly the same as the input image
            scores = scores[scores["score"] > 1e-6]

        return scores.reset_index(drop=True)
